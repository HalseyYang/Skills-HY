---
name: slide-image-to-editable-pptx
description: Convert slide screenshots, exported slide images, scanned presentation pages, or image-only decks into editable PowerPoint PPTX files. Use when the user asks to rebuild a PPT from images, make screenshots editable, convert PNG/JPG/PDF slide pages to editable slides, recreate layouts, extract tables/text/shapes from slide images, or avoid image-only PPT output.
---

# Slide Image To Editable PPTX

Use this skill to rebuild slide screenshots or image-only slide pages as editable PowerPoint decks.

Important distinction: this skill is for editable reconstruction. Do not simply place each source image full-slide unless the user explicitly asks for image-only output.

## Workflow

1. Collect inputs.
   - Accept `.png`, `.jpg`, `.jpeg`, rendered PDF pages, or existing image-only `.pptx`.
   - Preserve source order.
   - If the source is a PDF or PPTX, render pages/slides to images first for visual inspection.

2. Inspect each slide image.
   - Identify canvas aspect ratio, background color/image, title, subtitles, body text, tables, charts, icons, screenshots, and decorative shapes.
   - For dense text or tables, use OCR if available; otherwise manually transcribe from the image and flag uncertain text.
   - Preserve hierarchy over pixel-perfect decoration.

3. Rebuild as editable objects.
   - Text becomes editable text boxes.
   - Tables become editable PowerPoint tables when practical.
   - Simple rectangles, lines, callouts, separators, and badges become editable shapes.
   - Complex photos, screenshots, logos, charts, or hard-to-vectorize illustrations may remain images.
   - Charts should be rebuilt as editable charts only when source data is visible or provided; otherwise use an image placeholder and note the limitation.

4. Generate a reconstruction plan.
   - Create a per-slide JSON layout using `references/layout-schema.md`.
   - Use normalized coordinates (`x`, `y`, `w`, `h`) from `0` to `1` so the plan is independent of pixel size.
   - Include `confidence` and `notes` for uncertain text, approximate chart values, or non-editable elements.

5. Create the PPTX.
   - Prefer `scripts/build_editable_pptx.py` for deterministic generation from JSON.
   - If using another PowerPoint library, keep the same reconstruction principles.
   - Preserve 16:9 unless the source clearly uses another aspect ratio.

6. Quality check.
   - Render or visually inspect the generated deck.
   - Compare each rebuilt slide against the source image.
   - Check text overflow, alignment, font size, table structure, missing labels, and whether important items are editable.
   - Report any objects intentionally left as images.

## Output Standards

- Deliver a `.pptx` with editable text and shapes.
- Include a short reconstruction note when fidelity is approximate.
- Do not silently invent missing text, data, citations, or labels.
- For client/regulatory/business decks, preserve meaning and hierarchy before stylizing.

## Helper Script

Build PPTX from a JSON layout file:

```bash
python3 /Users/hanyueyang/.codex/skills/slide-image-to-editable-pptx/scripts/build_editable_pptx.py layout.json output.pptx
```

See `references/layout-schema.md` for the supported JSON shape model.
