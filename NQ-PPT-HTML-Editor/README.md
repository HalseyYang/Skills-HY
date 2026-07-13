# NQ-PPT-HTML-Editor

> Give any AI-generated HTML (especially viewport-based PPT decks) a **visual editable version** — open in browser, tweak by hand, export a clean copy. Built as an AI coding skill: a toolbox plus the model's judgment, not a fixed program.

English | [简体中文](README.zh-CN.md)

## The problem it solves

When an AI generates an HTML file — a slide deck, a landing page, a doc — the user often wants to fine-tune it: nudge a title up, shrink a card, fix a font weight. But the only way to do that is go back to the AI, describe the change, iterate. That's slow for tiny tweaks.

**NQ-PPT-HTML-Editor** turns that HTML into a *self-editable* file: double-click, edit visually in the browser (select / drag / panel), click Export, get a clean version back. No code, no AI round-trip for every comma.

## Why not just use an existing HTML editor?

Most visual HTML editors die on the kinds of HTML that AI tools actually produce:

- **Viewport-unit PPT decks** (`100vw × 100vh`, `font-size: 7.5vw`) — these resolve against the browser viewport. Stuff them into an iframe whose size follows content, and the height collapses to zero. (This is exactly what killed `htmlcanvas-editor` on our decks.)
- **WebGL / GLSL backgrounds** — shader source contains naked `<` (e.g. `for(float i=1.0;i<4.0;i++)`). Store the original HTML in a `<template>` and the parser mangles it. Store it in `<script type="text/plain">` and `</script>` inside the source closes the tag early.
- **Inline scripts everywhere** — `<script type="module">`, animation libs, nav logic. Naive serialization breaks them.

This project's solutions are hard-won:

| Problem | Solution |
|---|---|
| `vw`/`vh` collapse in editor iframe | Fixed-size 16:9 iframe (adaptive) gives viewport units a stable reference |
| GLSL `<` / multiple `</script>` break storage | Original HTML stored as **base64** — zero HTML-meaningful characters |
| Editor code leaks into export | Export serializes a fresh iframe snapshot, strips editor traces |
| Ctrl+E enter/exit nesting & write-back corruption | **No toggle** — open-as-editor + explicit Export button |
| iframe swallows mouse/keyboard events | Shortcuts bound on both outer doc and iframe contentWindow |

## How it works

```
┌──────────────────────────────────────────────────────────┐
│  xxx-editable.html (self-contained, double-click to run) │
│                                                          │
│  <div data-source="base64原始HTML">   ← 原始内容        │
│  <script> serializer.js              ← 保存/清理逻辑     │
│  <script> editor.js                  ← 编辑器主逻辑      │
│  <style>  editor.css                 ← 面板/工具栏视觉   │
│  <script> autoEnter()                ← 打开即进入编辑    │
│                                                          │
│  ┌─────────────────────────┐  ┌──────────────┐          │
│  │ iframe (16:9 PPT 画布)   │  │ 属性面板      │          │
│  │ 单击选中 · 双击改字       │  │ 字号/颜色/宽高 │          │
│  │ 拖动移动                 │  │ 滑动条/上下键  │          │
│  └─────────────────────────┘  └──────────────┘          │
│  [导出纯净版]  [全屏预览]                                 │
└──────────────────────────────────────────────────────────┘
```

## Quick start

### As an AI skill (intended use)

This is designed as a **Claude Code / ZCode / Cursor skill**. Drop the folder into your skill directory, then ask your AI:

> "把 `deck.html` 弄成可编辑的" / "make `deck.html` editable"

The AI reads your HTML, analyzes it, and runs:

```bash
node build-editable.js deck.html deck-editable.html mydeck
```

You then open `deck-editable.html` in Chrome/Edge and edit visually.

### Standalone (without an AI)

```bash
git clone https://github.com/<you>/NQ-PPT-HTML-Editor.git
cd NQ-PPT-HTML-Editor
node build-editable.js path/to/your.html your-editable.html yourfile
# open your-editable.html in Chrome/Edge
```

## What the user can do in the editor

| 操作 | 方式 |
|------|------|
| 改文字 | 双击元素（不全选，方向键移光标改单字） |
| 字号 / 字重 / 颜色 / 行高 / 字间距 | 面板数字框 + 滑动条 + 上下键（Shift 大幅） |
| 改位置 | 拖元素本体 / 面板"位置"数字 |
| 改宽高 | 面板"尺寸"数字 + 滑动条 |
| 复制 / 删除 / 调换组件 | 面板按钮 |
| 翻页（PPT） | 工具栏 ◀ ▶ |
| 导出纯净版 | 点按钮 / Ctrl+S |
| 全屏预览 | 点按钮，ESC / 关闭按钮退出 |
| 撤销 | Ctrl+Z |

## Project layout

```
NQ-PPT-HTML-Editor/
├── SKILL.md                ← AI trigger description + workflow (the skill's brain)
├── build-editable.js       ← Builder: original HTML + assets → editable version
├── assets/
│   ├── editor.js           ← Editor logic (autoEnter / export / preview / editing)
│   ├── editor.css          ← Panel / toolbar styling
│   └── serializer.js       ← Save/clean logic (state-machine id injection + validation)
├── tests/
│   ├── test-serializer.js  ← Node tests for serializer (36 assertions, run after any change)
│   └── fixtures/           ← Sample HTML files (PPT + webpage)
└── evals/
    └── evals.json          ← AI triggering eval cases
```

## Testing

The serializer (save logic) is the most bug-prone part. It has a Node test suite — run it after any change to `assets/serializer.js`:

```bash
node tests/test-serializer.js
# Expect: 🎉 全部通过 (通过 36/36)
```

Covers: id injection (skips script/style), style patch, text patch, remove, duplicate, multi-element mixed patches, round-trip byte-identity, validation, real PPT sample.

## Design philosophy: toolbox + judgment

This is deliberately **not a fixed program**. It's a toolbox (`build-editable.js` + `assets/`) plus the AI's judgment:

- A `vw`/`vh` PPT deck → the AI picks the 16:9 canvas strategy
- A `px` flow webpage → the AI picks the scrollable canvas
- A file with WebGL shaders → the AI knows base64 storage protects them
- Grid/flex layouts → the AI warns that drag-move may reflow neighbors

A fixed editor can't adapt to HTML forms it didn't anticipate. An AI with this toolbox can.

## Limitations

- **Drag-move uses margin** — works in flow layouts; in grid/flex, neighbors may reflow. Undo if unwanted.
- **No handle-drag resize** — sizing is panel-only (handle-drag had coordinate bugs across the iframe boundary).
- **Export re-serializes** — exported HTML is the browser's re-serialization; hand-written indentation may normalize (content/behavior preserved).
- **No live file sync** — you edit the editable version, then Export to get the clean result. No in-place overwrite of the original (deliberate, avoids corruption).
- **Chromium recommended** — the editor works everywhere; download/export is most reliable in Chrome/Edge.

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgments

The incremental-patch save idea was inspired by [`htmlcanvas-editor`](https://www.npmjs.com/package/htmlcanvas-editor) (whose `<template>`-based storage and viewport-following iframe approach we learned not to copy). The state-machine id injection here is our rewrite to survive GLSL and multiple `</script>` tags.
