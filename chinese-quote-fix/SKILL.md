---
name: chinese-quote-fix
description: >
  Fix Chinese quotation marks that use ASCII ' and " (U+0022/U+0027) inside
  Python source code, which conflict with Python string delimiters and cause
  SyntaxError. Uses tokenize-based precise detection to convert only
  CJK-adjacent interior quotes to Unicode curly quotes
  (U+2018/U+2019/U+201C/U+201D), leaving Python delimiters untouched. Trigger
  when: Python .py file has SyntaxError caused by Chinese quotes in strings, or
  when generating Chinese-heavy Python scripts that need quote sanitization. DO
  NOT use regex-based or state-machine guessing — always use
  scripts/fix_quotes.py.
agent_created: true
disable: true
---

# Chinese Quote Fix

## Overview

When Chinese text is embedded in Python strings, ASCII `'` and `"` used as Chinese quotation marks
conflict with Python string delimiters. This skill provides a one-pass, tokenize-based fix that
precisely identifies string literal boundaries and converts only interior CJK-adjacent quotes to
Unicode curly quotes — no guessing, no iteration.

## Why Tokenize, Not Regex

**Wrong approach (causes infinite loops):**
- State machines confused by `FONT_CN = '微软雅黑'` → converts Python delimiter to curly quote
- Iterative fix scripts that fix one line, recompile, fix next → breaks things it already fixed
- Regex that can't distinguish `"inside string"` from `"string boundary"`

**Right approach:**
`tokenize` module returns exact `(line, col)` spans of every string literal. Only quotes
*inside* those spans that are CJK-adjacent get converted. String delimiters are never touched.

## When to Use

- Python `.py` file with `SyntaxError` caused by Chinese quotes
- Before running any Chinese-heavy Python script for the first time
- After writing Python code that embeds Chinese text with quotation marks
- If you suspect a file was previously "fixed" with regex/state-machine (check for leftover `\u2018`/`\u201c` outside strings)

## Fix Workflow

### Step 1: Run the fix script

```bash
python scripts/fix_quotes.py <file.py>
```

This does a single pass:
1. Tokenizes the file to get all string literal boundaries
2. Scans each string's interior for CJK-adjacent ASCII quotes
3. Converts them to paired Unicode curly quotes
4. Verifies the file compiles after fix

### Step 2: If compilation still fails

If `fix_quotes.py` reports "WARNING: file still has compilation errors", the remaining errors
are likely NOT Chinese quote issues. Possible causes:
- Actual Python syntax errors (missing commas, unmatched brackets)
- Non-ASCII characters outside string literals
- Previously corrupted lines from bad regex fixes (e.g., `""text` with extra quotes)

For these cases, read the error line, check for leftover `\u201c`/`\u2018` outside strings, and fix
manually. Do NOT write another iterative fix script — that's what caused this skill to be created.

### Step 3: Dry-run for inspection

```bash
python scripts/fix_quotes.py <file.py> --dry-run
```

Reports the number of string literals found without modifying anything.

## Anti-Patterns (DO NOT DO)

- ❌ Write `auto_fix.py` that iterates compile→fix→compile→fix
- ❌ Use regex with CJK character class to find-and-replace in the whole file
- ❌ State machines that track whether you're "inside" or "outside" a string
- ❌ Convert all `'` to `\u2018` / `"` to `\u201c` indiscriminately (Python delimiters get nuked)

Only use `scripts/fix_quotes.py`. If it can't fix something, examine the line manually.
