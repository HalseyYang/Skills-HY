---
name: english-listening-phonetics-annotator
description: "Annotate connected speech features (liaison, weak forms, stress,
  incomplete plosion /t̚/, assimilation, linking /r/) in English listening
  materials. This skill should be used when the user asks to mark/annotate 连读,
  弱读, 重读, 吞音, 同化 in English audio transcripts, BEC/IELTS/TOEFL listening texts,
  or any English dialogue for pronunciation study. Trigger words: 标注连读, 标记重弱读,
  连读弱读, 语音标注, phonetics annotation, connected speech."
disable: true
---

# English Listening Phonetics Annotator

## Overview

Systematically annotate English listening texts with 6 categories of connected speech features, then output a color-coded HTML document with per-line IPA transcriptions. Designed for BEC/IELTS/TOEFL listening practice.

## Critical Process Rules

### Step 0: ALWAYS Ask for Original Text First

Before doing ANY audio transcription, ask the user: "Do you have the original transcript/text (PDF, image, or pasted text)?"

- If YES: Extract text directly (pdfplumber for PDF, OCR for images, or read pasted text). Skip to Step 2.
- If NO: Only then attempt audio transcription (Google Speech Recognition API with 10s chunks + retries). Warn user that transcription may contain errors and ask them to verify.

**This single step saves 30+ minutes and avoids transcription errors.**

### Step 1: Obtain the Text

- **PDF**: Use pdfplumber to extract text: `pdfplumber.open(path)` → `page.extract_text()`
- **Image**: Use OCR (ocr-local skill or pytesseract)
- **Pasted text**: Use directly
- **Audio only (last resort)**: Convert MP3→WAV with ffmpeg (imageio_ffmpeg), then Google Speech Recognition with 10s chunks, 5 retries per chunk, 3s delay between chunks

### Step 2: Apply Phonetic Rules Engine

Load `references/phonetic_rules.md` and systematically scan each sentence for all 6 categories. Process rules in this order (later rules depend on earlier ones):

1. **Stress** — Mark content words first (establishes the skeleton)
2. **Weak forms** — Mark function words (complement to stress)
3. **Liaison** — Find consonant→vowel and vowel→vowel connections
4. **Linking /r/** — Find /ə/ or /ɔː/ endings before vowels (British English)
5. **Incomplete plosion /t̚/** — Find /t/ before consonants (NOT simple elision)
6. **Assimilation** — Find h-dropping, /j//w/ glides, /ŋ/→/ŋɡ/, consonant fusion

### Step 3: Generate IPA per Line

For each annotated line, write the full IPA transcription in a box, reflecting all connected speech features. This is the "听感" (listening feel) that students can read while listening to audio.

### Step 4: Output Color-Coded HTML

Use `assets/template.html` as the base template. The 6-color system:

| Color | Phenomenon | CSS class | Visual style |
|-------|-----------|-----------|-------------|
| Red | Stress | `.stress` | Bold + underline |
| Yellow | Weak form | `.weak` | Italic + smaller |
| Blue | Liaison | `.liaison-group` | Dotted underline |
| Purple | Incomplete plosion /t̚/ | `.unreleased` | Strikethrough |
| Green | Assimilation | `.assim` | Background highlight |
| Orange | Linking /r/ | `.linkr` | Background highlight |

Each turn includes:
- Speaker label (Woman/Man or role-based)
- Annotated text with color coding
- Note box explaining each phenomenon
- IPA box with full sentence transcription

End with: summary table + learning tips section.

## Resources

### references/
- `phonetic_rules.md` — Complete phonetic rules checklist with all weak form tables, liaison patterns, h-dropping rules, linking /r/ rules, incomplete plosion patterns, and assimilation types. Load this file before annotating.

### assets/
- `template.html` — HTML template with CSS for 6-color annotation system, IPA boxes, summary table, and learning tips. Copy and fill with annotated content.

## Key Lessons (from real usage)

1. **"does" weak form is /dəz/ (schwa), NOT /dʌz/** — Common error
2. **"the" before vowel = /ði/, before consonant = /ðə/** — Two weak forms
3. **h-dropping: after consonant → drop; after vowel → keep** — "does he" drops h, "say he" keeps h
4. **"got that" is /t̚/ (incomplete plosion), NOT full elision** — /t/ is suppressed, not gone
5. **"want to" ≠ "wanna"** — British exam recordings are formal, /t/ is light but present
6. **"anything else" → /ŋɡels/** — /ŋ/ becomes /ŋɡ/ before vowel, extra /ɡ/ sound appears
7. **Linking /r/ in British English** — /ə/ ending + vowel = insert /r/ (summer‿I → /ˈsʌməraɪ/)
8. **Numbers and place names are always fully stressed** — No weak forms in addresses/amounts
