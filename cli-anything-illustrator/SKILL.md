---
name: cli-anything-illustrator
description: Adobe Illustrator CLI harness reference for creating and editing
  vector graphics, layers, shapes, text, and exports. Use when the user asks to
  automate Illustrator or inspect the upstream Illustrator harness. The current
  upstream implementation is Windows COM-only and is not executable on macOS.
disable: true
---

# CLI-Anything Illustrator

Use this skill as a capability reference for the Illustrator harness shipped in:

`/Users/hanyueyang/.codex/vendor/harness-anything-mac/illustrator-harness/agent-harness`

## Current Platform Status

The upstream README describes future macOS AppleScript/JXA support, but the current code imports `win32com.client` directly. Treat the current implementation as Windows-only.

On macOS:

- Do not attempt to run the harness as if it were functional.
- Explain that the installed skill is a local reference until upstream adds a macOS backend.
- For vector design tasks, use another available tool unless the user explicitly asks to inspect or repair this harness.

## Intended Command Groups

| Group | Purpose |
| --- | --- |
| `project` | Create, open, and save Illustrator documents. |
| `layers` | Add, rename, show, hide, lock, and reorder layers. |
| `shapes` | Draw rectangles, ellipses, lines, and polygons. |
| `text` | Add and update text elements. |
| `export` | Export PNG, JPEG, SVG, PDF, or AI files. |

## Upstream Example

```bash
cli-anything-illustrator project new logo.ai -w 500 -h 500
cli-anything-illustrator text add "Brand" --x 100 --y 100 --font "Arial" --size 72
cli-anything-illustrator shapes rect --x 50 --y 50 --w 200 --h 100
cli-anything-illustrator export svg output.svg
```

## Source Audit Note

The upstream `illustrator-harness/agent-harness/setup.py` currently contains copied PowerPoint package metadata and should not be installed unchanged.
