#!/usr/bin/env python3
"""
One-pass fix for Chinese quotes conflicting with Python string delimiters.

Uses Python's tokenize module to precisely identify string literal boundaries,
then converts CJK-adjacent ASCII quotes INSIDE strings to Unicode curly quotes.

Usage:
    python fix_quotes.py <file.py> [--dry-run]

Strategy (tokenize-based, NOT regex-guessing):
1. tokenize the file → get exact (start, end) spans of every string literal
2. For each string, scan its interior for ' and " characters
3. If a quote is CJK-adjacent on either side → it's a Chinese quotation mark → convert
4. Pair them: alternate left/right within each quote type per string
5. Leave Python-delimiter quotes untouched (they're at string boundaries, not interior)
"""
import sys
import tokenize
import io
import os

# Unicode curly quotes
LEFT_SINGLE = '\u2018'
RIGHT_SINGLE = '\u2019'
LEFT_DOUBLE = '\u201c'
RIGHT_DOUBLE = '\u201d'


def is_cjk(ch: str) -> bool:
    """Check if a character is CJK, fullwidth, or CJK punctuation."""
    if not ch:
        return False
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in [
        (0x4E00, 0x9FFF),   # CJK Unified Ideographs
        (0x3000, 0x303F),   # CJK Symbols and Punctuation
        (0xFF00, 0xFFEF),   # Halfwidth and Fullwidth Forms
    ])


def is_cjk_or_punct(ch: str) -> bool:
    """CJK character or fullwidth punctuation."""
    return is_cjk(ch) or ch in '\uff0c\uff0e\uff1a\uff1b\uff01\uff1f\uff08\uff09\u3001\u3002'


def fix_string_interior(text: str) -> str:
    """
    Fix CJK-adjacent quotes INSIDE a string body.
    Only convert quotes that are NOT at position 0 (Python delimiter).
    """
    chars = list(text)
    n = len(chars)
    single_state = 0  # 0 = expect left, 1 = expect right
    double_state = 0

    for i in range(n):
        ch = chars[i]
        if ch not in ("'", '"'):
            continue
        # Check CJK adjacency
        before = chars[i - 1] if i > 0 else ''
        after = chars[i + 1] if i + 1 < n else ''
        if not (is_cjk_or_punct(before) or is_cjk_or_punct(after)):
            continue  # Not a Chinese quote

        if ch == "'":
            if single_state == 0:
                chars[i] = LEFT_SINGLE
                single_state = 1
            else:
                chars[i] = RIGHT_SINGLE
                single_state = 0
        else:  # ch == '"'
            if double_state == 0:
                chars[i] = LEFT_DOUBLE
                double_state = 1
            else:
                chars[i] = RIGHT_DOUBLE
                double_state = 0

    return ''.join(chars)


def fix_file(filepath: str) -> int:
    """Fix all CJK-adjacent quotes inside string literals. Returns number of fixes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    # Step 1: tokenize to get string literal spans
    string_spans = []
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    except tokenize.TokenError as e:
        print(f'Tokenize error: {e}', file=sys.stderr)
        return 0

    for tok in tokens:
        if tok.type == tokenize.STRING:
            # tok.start = (line, col), tok.end = (line, col)
            start_row, start_col = tok.start
            end_row, end_col = tok.end
            string_spans.append((start_row, start_col, end_row, end_col))

    if not string_spans:
        print('No string literals found.')
        return 0

    lines = source.splitlines(keepends=True)
    total_fixes = 0
    replacements = {}  # line_index → list of (col_start, col_end, replacement_slice)

    for start_row, start_col, end_row, end_end in string_spans:
        row_idx = start_row - 1  # 0-based
        # Extract the string body (excluding the surrounding quote delimiters)
        line = lines[row_idx]
        # The string slice within the line
        string_slice = line[start_col:end_end]
        if not string_slice:
            continue

        # Determine delimiter: first and last chars
        raw = string_slice
        if len(raw) < 2:
            continue

        # Find the actual quote character and delimit the interior
        # Handle: '...', "...", '''...''', """...""", f"...", r"...", b"..."
        prefix = ''
        body_start = 0
        for i, ch in enumerate(raw):
            if ch in 'fFrRbBuU':
                prefix += ch
                body_start = i + 1
            else:
                break

        quote_char = raw[body_start] if body_start < len(raw) else ''
        if quote_char not in ("'", '"'):
            continue

        # Triple-quoted?
        is_triple = raw[body_start:body_start+3] in ('"""', "'''")
        if is_triple:
            interior_start = body_start + 3
            interior_end = len(raw) - 3
        else:
            interior_start = body_start + 1
            interior_end = len(raw) - 1

        if interior_end <= interior_start:
            continue

        interior = raw[interior_start:interior_end]
        fixed_interior = fix_string_interior(interior)

        if fixed_interior != interior:
            replacement = raw[:interior_start] + fixed_interior + raw[interior_end:]
            if row_idx not in replacements:
                replacements[row_idx] = []
            # Replace the string slice within the line
            replacements[row_idx].append((start_col, end_end, replacement))
            total_fixes += 1

    # Apply replacements (right-to-left within each line to preserve positions)
    for row_idx, reps in replacements.items():
        line = lines[row_idx]
        # Sort by start_col descending so earlier replacements don't shift later ones
        reps.sort(key=lambda x: x[0], reverse=True)
        for start_col, end_col, replacement in reps:
            line = line[:start_col] + replacement + line[end_col:]
        lines[row_idx] = line

    if total_fixes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    return total_fixes


def verify_file(filepath: str) -> bool:
    """Check if the file compiles successfully."""
    import py_compile
    try:
        py_compile.compile(filepath, doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <file.py> [--dry-run]')
        sys.exit(1)

    filepath = os.path.abspath(sys.argv[1])
    dry_run = '--dry-run' in sys.argv

    if not os.path.exists(filepath):
        print(f'File not found: {filepath}')
        sys.exit(1)

    if dry_run:
        # Just tokenize and report
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        try:
            tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
            string_count = sum(1 for t in tokens if t.type == tokenize.STRING)
            print(f'Found {string_count} string literals. Dry run only - no changes made.')
            return
        except tokenize.TokenError as e:
            print(f'Tokenize error: {e}')
            sys.exit(1)

    fixes = fix_file(filepath)
    print(f'Fixed {fixes} string literal(s).')

    if verify_file(filepath):
        print('SUCCESS: file compiles without errors.')
    else:
        print('WARNING: file still has compilation errors. Manual review needed.')


if __name__ == '__main__':
    main()
