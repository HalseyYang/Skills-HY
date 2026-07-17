---
name: NQ-PPT-HTML-Editor
description: >
  给已生成的静态 HTML（尤其 PPT 幻灯片，也含落地页/文档/原型）生成一个"可视化编辑版"——
  让用户在浏览器里直接可视化微调：选中元素改文字、改字号字重颜色行高字间距、拖动移动位置、
  面板数字+滑动条改元素宽高、复制/删除/上下调换组件，编辑完点"导出"生成纯净版（不含编辑器代码）， 还能"全屏预览"看效果。支持 vw/vh 自适应
  PPT 和普通 px 网页，编辑不破坏原文件的脚本/样式/自适应。 只要用户想让一个已生成的
  HTML「可以自己改」「可视化编辑」「不碰代码就能调字号/位置/大小」， 就应该用本 Skill。典型触发语：「让这个 HTML/PPT
  可以编辑」「加个编辑模式」「我想自己微调」 「改一下这个 PPT 的标题字号/位置」「把这块色块改窄一点」「生成可编辑版」「make this
  editable」 「editable html」「visual editor for html」。用户用 PPT skill / 前端 skill
  生成了文件后想自己微调、 或拿到别人给的静态 HTML 想改内容时，都应触发。不要 undertrigger。不适用于：代码编辑器、 CMS
  后台、生成全新的 HTML（那是别的 skill 的活）、修改 JSON/CSV 等非 HTML 文件。
disable: true
---

# NQ-PPT-HTML-Editor

Generate a **visual-editable version** of any static HTML file. The user opens the generated file in a
browser and gets a full visual editor immediately (no hotkeys to enter): select elements, edit text, drag
to move, tweak font/size/weight/color via panel + slider + arrow keys, duplicate/delete/reorder components,
then click **Export** to download a clean version (no editor code), or **Preview** to see it fullscreen.

This is a **toolbox + your judgment** skill — not a fixed program. You analyze each HTML and decide how to
handle it (PPT vs webpage, vw/vh vs px, which elements are editable, special scripts to preserve). The
toolbox (`build-editable.js` + `assets/`) provides tested components; you apply them with situational judgment.

## How it works

```
用户给你一个 HTML（任何形式）
  ↓
你分析它的特点（布局类型 / 单位 / 特殊脚本 / 可编辑元素）
  ↓
你用 build-editable.js 生成 xxx-editable.html：
  - 原始内容用 base64 编码存储（100% 可靠，不受 GLSL/script/特殊字符影响）
  - 内嵌编辑器代码（editor.js / editor.css / serializer.js）
  - 页面加载后 autoEnter()，打开即编辑
  - 工具栏有【导出纯净版】【全屏预览】按钮
  ↓
用户双击 xxx-editable.html：
  - 直接进编辑模式（不用 Ctrl+E）
  - 编辑（面板 / 上下键 / 滑动条 / 拖动）
  - 点【导出】→ 下载纯净版（xxx-export.html，无编辑器代码，拿去演示/部署）
  - 点【全屏预览】→ 遮罩全屏看效果，点按钮或 ESC 回编辑
```

## Toolbox layout

```
NQ-PPT-HTML-Editor/                    （skill 根目录）
├── SKILL.md                        ← 本文件（触发说明 + 工作流）
├── build-editable.js               ← 构建脚本：原始HTML + 编辑器资源 → 可编辑版
├── assets/
│   ├── editor.js                   ← 编辑器主逻辑（autoEnter / 导出 / 预览 / 编辑能力）
│   ├── editor.css                  ← 面板 / 工具栏视觉
│   └── serializer.js               ← 保存清理逻辑（状态机打标 + 清理 + 校验，已测 36/36）
└── tests/
    ├── test-serializer.js          ← serializer 的 Node 测试（纯函数，可独立验证）
    └── fixtures/
        ├── ppt-sample.html         ← PPT 测试样本（vw/vh 全屏布局）
        └── webpage-sample.html     ← 普通网页测试样本（px 流式）
```

## Workflow

### 1. Read and analyze the target HTML

Understand the structure — your judgment decides how the editor handles it:

- **PPT deck** (has `#deck` / `.slide` / `vw`-`vh` units) → editor uses a 16:9 adaptive canvas with page nav
- **Regular webpage** (px/rem, vertical scroll) → editor uses a scrollable canvas
- Note any `<script>`/`<style>`/WebGL shaders — the editor never touches them, but you should know they're there
- base64 storage means GLSL with naked `<`, multiple `</script>`, any special chars are all safe

### 2. Generate the editable version with build-editable.js

```bash
node <skill-path>/build-editable.js <原始HTML路径> <输出路径> <文件名标识>
# 例: node build-editable.js deck.html deck-editable.html mydeck
```

The script reads the original HTML + the three `assets/` files, base64-encodes the original, and emits a
self-contained `xxx-editable.html`. Tell the user to open it in **Chrome or Edge** (File System Access /
download needs Chromium; the editor itself works everywhere).

### 3. Tell the user how to use it

> 已生成可编辑版 `xxx-editable.html`。用 Chrome 或 Edge 双击打开：
> - 打开就是编辑器，**不用按任何键**
> - **单击**选中 · **双击**改字 · **拖本体**移位置 · 右侧面板改字号/颜色/宽高（数字框+滑动条+上下键）
> - **复制 / 删除 / ↑↓ 调换** 组件（流式布局会自动重排，错了 Ctrl+Z）
> - 点【导出纯净版】或 **Ctrl+S** → 下载无编辑器代码的纯净 HTML（拿去演示/部署）
> - 点【全屏预览】→ 全屏看效果，点右上角按钮或 **ESC** 回编辑
> - **Ctrl+Z** 撤销

## Editor capabilities (what the user can do)

| 操作 | 方式 |
|------|------|
| 改文字内容 | 双击元素（不全选，可改单个字，方向键移光标） |
| 字号 / 字重 / 颜色 / 行高 / 字间距 | 面板输入 + 上下键微调（Shift 大幅） |
| 改元素位置 | 拖本体，或面板"位置"数字框 |
| 改元素宽高 | 面板"尺寸"数字框 + 滑动条 |
| 复制 / 删除组件 | 面板按钮 |
| 调换组件顺序 | 面板 ↑ / ↓ |
| 翻页（仅 PPT） | 工具栏 ◀ ▶ |
| 导出纯净版 | 点按钮 / Ctrl+S |
| 全屏预览 | 点按钮，ESC / 关闭按钮退出 |
| 撤销 | Ctrl+Z |

## Safety guarantees

1. **base64 storage** — the original HTML is base64-encoded inside the editable version, so GLSL shaders,
   multiple `</script>`, special characters can never break the editor's structure (this was a hard-won
   lesson — earlier `<template>`/`<script type=text/plain>` approaches failed on WebGL decks).
2. **Export = clean iframe snapshot** — exporting serializes the iframe (which renders only the pure PPT),
   strips editor traces (selection styles, blocker scripts, data-hc-id, frozen transitions, dynamic nav),
   so the exported file is a clean, standalone HTML with working navigation/animations.
3. **serializer validation** — before download, the serializer validates script/style tag balance and
   refuses export if structure looks corrupted.

## Limitations (be upfront)

- **Drag-move uses margin** — works on flow layouts; in grid/flex PPT layouts the element may visually
  overlap neighbors or get repositioned by the layout algorithm. Undo (Ctrl+Z) if unwanted.
- **Drag-resize via handles is removed** — sizing is done via panel number box + slider + arrow keys only.
  (Handle-drag had coordinate-mapping bugs across the iframe boundary; the panel approach is reliable.)
- **Export re-serializes** — the exported HTML is the browser's re-serialization of the iframe DOM, so
  original hand-written indentation/comments may be normalized. Content and behavior are fully preserved.
- **No live file sync** — editing happens in the editable version; you must click Export to get the clean
  result. There's no in-place overwrite of the original (deliberate — avoids corruption).
- **Browser support** — Export/preview download uses Blob/`<a download>` (works everywhere); the editor
  loads via `<script src>` so it needs the assets/ present alongside the editable file OR inlined.

## Testing

The serializer (save logic — most bug-prone) has a Node test suite. Run after any `assets/serializer.js` change:

```bash
node tests/test-serializer.js
# Expect: 🎉 全部通过 (36/36)
```

## Design notes (why these choices)

These were hard-won through debugging. Future-you (or contributors) should understand them:

- **Fixed-size iframe, not inline editing**: PPT decks use `vw`/`vh` which resolve against the browser
  viewport, not a container. A fixed 16:9 iframe (960×540 or adaptive) gives those units a stable reference
  so they don't collapse to zero — this is the exact bug that killed other editors on viewport-based decks.
- **base64 over `<template>`/`<script type=text/plain>`**: GLSL shaders contain naked `<` (e.g. `i<4.0`)
  that breaks template parsing; `</script>` inside the original breaks text/plain storage. base64 has no
  HTML-meaningful characters at all.
- **autoEnter over Ctrl+E toggle**: an earlier Ctrl+E-enter/exit design caused nested editors and
  write-back corruption (document.write broke PPT scripts). Opening-as-editor + explicit export is far
  more robust.
- **iframe event boundary**: when the editor shell covers the iframe, mouse/keyboard events inside the
  iframe don't bubble to the outer document. The editor binds shortcuts on both layers and forwards.
