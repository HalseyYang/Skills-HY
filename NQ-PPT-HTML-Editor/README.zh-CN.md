# NQ-PPT-HTML-Editor

> 给 AI 生成的 HTML（尤其是基于视口单位的 PPT 幻灯片）生成一个**可视化编辑版**——浏览器打开就能改，改完导出纯净版。它是一个 AI coding skill：工具箱 + 大模型的判断力，不是固定程序。

[English](README.md) | 简体中文

## 解决什么问题

AI 生成 HTML 文件后——一个 PPT、一个落地页、一个文档——用户经常想自己微调：标题往上挪一点、卡片缩小、字号调粗。但唯一的办法是回到 AI，描述改动，等它改，反复迭代。为了改一个字号的来回沟通，太慢了。

**NQ-PPT-HTML-Editor** 把这个 HTML 变成一个*可自己编辑*的文件：双击打开，在浏览器里可视化编辑（选中/拖拽/面板改），点导出，拿回一个纯净版本。不用碰代码，不用为每个标点符号找 AI。

## 为什么不直接用现成的 HTML 编辑器？

大多数可视化 HTML 编辑器，在 AI 工具实际产出的那种 HTML 上会挂掉：

- **视口单位 PPT**（`100vw × 100vh`、`font-size: 7.5vw`）——这些单位是相对浏览器视口算的。把它塞进一个"尺寸跟着内容走"的 iframe，高度会塌成 0。（这正是 `htmlcanvas-editor` 在我们 PPT 上挂掉的原因。）
- **WebGL / GLSL 背景**——着色器源码里有裸的 `<`（比如 `for(float i=1.0;i<4.0;i++)`）。用 `<template>` 存原始 HTML，解析器会把 `<` 当标签起始，内容全乱。用 `<script type="text/plain">` 存，原始内容里的 `</script>` 会提前闭合标签。
- **到处都是内联脚本**——`<script type="module">`、动画库、导航逻辑。粗暴的序列化会破坏它们。

这个项目的解法都是踩坑踩出来的：

| 问题 | 解法 |
|---|---|
| `vw`/`vh` 在编辑 iframe 里塌缩 | 固定 16:9 iframe（自适应尺寸），给视口单位一个稳定参照 |
| GLSL 的 `<` / 多个 `</script>` 破坏存储 | 原始 HTML 用 **base64** 存储——零个 HTML 特殊字符 |
| 编辑器代码泄漏进导出文件 | 导出时序列化一个干净的 iframe 快照，剥离编辑器痕迹 |
| Ctrl+E 进出嵌套 + 写回损坏 | **不要切换**——打开即编辑 + 显式的导出按钮 |
| iframe 吞掉鼠标/键盘事件 | 快捷键在外层文档和 iframe 内都绑一份 |

## 工作原理

```
┌──────────────────────────────────────────────────────────┐
│  xxx-editable.html（自包含，双击即可运行）                 │
│                                                          │
│  <div data-source="base64原始HTML">   ← 原始内容        │
│  <script> serializer.js              ← 保存/清理逻辑     │
│  <script> editor.js                  ← 编辑器主逻辑      │
│  <style>  editor.css                 ← 面板/工具栏视觉   │
│  <script> autoEnter()                ← 打开即进入编辑    │
│                                                          │
│  ┌─────────────────────────┐  ┌──────────────┐          │
│  │ iframe（16:9 PPT 画布）   │  │ 属性面板      │          │
│  │ 单击选中 · 双击改字       │  │ 字号/颜色/宽高 │          │
│  │ 拖动移动                 │  │ 滑动条/上下键  │          │
│  └─────────────────────────┘  └──────────────┘          │
│  [导出纯净版]  [全屏预览]                                 │
└──────────────────────────────────────────────────────────┘
```

## 快速开始

### 作为 AI skill 使用（推荐用法）

本项目设计为 **Claude Code / ZCode / Cursor 的 skill**。把文件夹放进你的 skill 目录，然后对你的 AI 说：

> "把 `deck.html` 弄成可编辑的" / "make `deck.html` editable"

AI 会读取你的 HTML、分析它的特点，然后运行：

```bash
node build-editable.js deck.html deck-editable.html mydeck
```

接着你用 Chrome/Edge 打开 `deck-editable.html`，可视化编辑。

### 不用 AI，独立使用

```bash
git clone https://github.com/Natural-Q/NQ-PPT-HTML-Editor.git
cd NQ-PPT-HTML-Editor
node build-editable.js path/to/your.html your-editable.html yourfile
# 用 Chrome/Edge 打开 your-editable.html
```

## 编辑器里能做什么

| 操作 | 方式 |
|------|------|
| 改文字 | 双击元素（不全选，方向键移光标改单个字） |
| 字号 / 字重 / 颜色 / 行高 / 字间距 | 面板数字框 + 滑动条 + 上下键（Shift 大幅） |
| 改位置 | 拖元素本体 / 面板"位置"数字 |
| 改宽高 | 面板"尺寸"数字 + 滑动条 |
| 复制 / 删除 / 调换组件 | 面板按钮 |
| 翻页（PPT） | 工具栏 ◀ ▶ |
| 导出纯净版 | 点按钮 / Ctrl+S |
| 全屏预览 | 点按钮，ESC / 关闭按钮退出 |
| 撤销 | Ctrl+Z |

## 项目结构

```
NQ-PPT-HTML-Editor/
├── SKILL.md                ← AI 触发说明 + 工作流（skill 的大脑）
├── build-editable.js       ← 构建脚本：原始 HTML + 编辑器资源 → 可编辑版
├── assets/
│   ├── editor.js           ← 编辑器逻辑（autoEnter / 导出 / 预览 / 编辑能力）
│   ├── editor.css          ← 面板 / 工具栏样式
│   └── serializer.js       ← 保存/清理逻辑（状态机打标 + 校验）
├── tests/
│   ├── test-serializer.js  ← serializer 的 Node 测试（36 条断言，改了就跑）
│   └── fixtures/           ← 示例 HTML（PPT + 普通网页）
└── evals/
    └── evals.json          ← AI 触发评估用例
```

## 测试

serializer（保存逻辑）是最容易出 bug 的部分。它有一套 Node 测试——每次改了 `assets/serializer.js` 就跑一次：

```bash
node tests/test-serializer.js
# 预期：🎉 全部通过 (通过 36/36)
```

覆盖：打 ID（跳过 script/style）、style patch、text patch、删除、复制、多元素混合改动、round-trip 字节一致性、校验、真实 PPT 样本。

## 设计哲学：工具箱 + 判断

这是**故意的**——不是固定程序。它是一套工具箱（`build-editable.js` + `assets/`）加上 AI 的判断力：

- 一个 `vw`/`vh` PPT → AI 选择 16:9 画布策略
- 一个 `px` 流式网页 → AI 选择可滚动画布
- 一个带 WebGL 着色器的文件 → AI 知道 base64 存储能保护它
- grid/flex 布局 → AI 提醒拖动可能导致邻居重排

固定编辑器没法适应它没预见到的 HTML 形式。一个拿着这个工具箱的 AI 可以。

## 局限

- **拖动移动用 margin**——流式布局下可用；在 grid/flex 里可能让邻居重排。不满意就 Ctrl+Z。
- **没有手柄拖拽改尺寸**——尺寸只走面板（手柄拖拽在 iframe 边界上有坐标换算 bug）。
- **导出会重新序列化**——导出的 HTML 是浏览器重新序列化的结果；手写的缩进可能被规范化（内容和行为完整保留）。
- **没有实时文件同步**——你在可编辑版里改，然后点导出拿干净结果。不会原地覆盖原文件（故意的，避免损坏）。
- **推荐用 Chromium 内核**——编辑器到处都能跑；下载/导出在 Chrome/Edge 上最可靠。

## 协议

MIT——见 [LICENSE](LICENSE)。

## 致谢

增量 patch 保存的思路受 [`htmlcanvas-editor`](https://www.npmjs.com/package/htmlcanvas-editor) 启发（它的 `<template>` 存储和"iframe 尺寸跟着内容走"的做法，让我们学到了不要这么干）。这里的"状态机打 ID"是我们重写的版本，目的是扛住 GLSL 和多个 `</script>` 标签。
