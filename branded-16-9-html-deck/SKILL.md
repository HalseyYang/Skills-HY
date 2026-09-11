---
name: branded-16-9-html-deck
description: >-
  Generate a brand-compliant 16:9 (1920×1080) HTML presentation deck from any
  source content (docx / outline / raw text). Produces a single self-contained
  HTML with fixed-stage scaling, keyboard/touch/wheel navigation, reveal
  animations, embedded transparent-PNG logo, and SVG diagrams (cycle, funnel,
  swimlane, flowchart with decision diamonds, pyramid, gantt, hub-and-spoke,
  stairs). Use when the user asks to turn a document or content into a 16:9
  HTML 演示/幻灯片/演示文稿/汇报 page, or wants a branded slide deck with company
  colors and logo. (agent_created: true)
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 16:9 品牌 HTML 演示文稿生成

## 触发场景
- 用户要求把一份文档/内容做成 16:9 HTML 演示（"做个16:9的html"、"做成演示文稿/幻灯片/汇报页"）。
- 需要公司配色 + Logo + 特定字体。

## 核心流程
1. **先吃透内容**：提取 docx/文本（python `zipfile`+`xml.etree` 或 `python-docx`），列明章节结构，再动手。不要跳过内容理解直接排版。
2. **确认品牌约束**（不确定就问用户）：
   - 配色精确值、Logo 文件（用**透明横向 PNG**，不要 640×640 白底方形 JPG）
   - 字体 + 字号规范（如 主标题≈28pt / 小标题≈16pt / 正文≈14pt，微软雅黑）
   - 篇幅（精简 vs 完整覆盖）
3. **确定每页构图**：不同逻辑用不同图形，不要全篇卡片网格。
4. **用 Python 生成**：写一个 `gen_deck.py`，用 `math` 程序化计算 SVG 坐标（环形节点 `ring_pos`、漏斗逐级收窄、甘特条形区间），再组装 HTML。脚本留在项目里，改内容只需重跑。
5. **Logo 内嵌**：透明 PNG → `base64` → 注入 `.brand` 的 CSS `background-image`，**只引用一次**（不要每页 `<img>`，否则文件爆炸 + 兼容问题）。
6. **自测兼容**：核对节点不重叠、标签不溢出 viewBox、无 CSS 类名冲突。

## 品牌令牌（丽和康 iDeaLab）
- 蓝 `#05BAD8`、橙 `#FF9D00`、正文黑 `#000000`/`#1A1A1A`、辅助灰 `#5B6676`、浅蓝 `#EAF9FC`、浅橙 `#FFF5E6`
- 字体微软雅黑；主标题 28pt 加粗、小标题 16pt 加粗、正文 14pt 黑色不加粗
- Logo：透明横向 PNG（如 `WorkBuddy/2026-07-28-09-47-53/logo_large.png`，1221×639 RGBA），右上角

## 设计原则（血泪教训）
- **别偷懒用卡片网格**：流程→环形/流程图，层级→金字塔，时间→甘特/时间轴，关系→中心辐射，对比→双栏。但——
- **简单 > 复杂**：图形可以简单，绝不溢出/重叠/不兼容。长句子绝不环绕摆放，长句用列表/网格/表格。
- **干净 > 堆砌**：不要蓝印网点、渐变下划线、大量带边框白盒。纯白底 + 扁平色块 + 单一强调色 + 充足留白。
- **参考 ≠ 抄袭**：用户给参考文件是"参考"，不要照搬其版式骨架。

## 技术硬坑（务必避开）
1. **Logo 兼容**：用透明横向 PNG，CSS 背景单引用；`background-size:contain` 在 `200×42` 盒内。不要用方形白底 JPG 拉成横条。
2. **CSS 类名冲突**：同一文件内类名不可复用。标题下划线 `.rule` 与列表项 `.rule` 撞名会级联合并导致元素被挤压成乱码——不同用途用独立类名（如 `.vrule`）。
3. **SVG 径向溢出**：文字标签不要 `radius × 1.2` 往外扩，长句不要 360° 环绕；改为「中心节点 + 左右/上下固定列」或「网格/列表」。
4. **坐标用 math 算**：`(cx + r*cos(rad), cy + r*sin(rad))` 程序化，别手算。
5. **viewBox 安全边界**：统一收进 `0 0 1640 680`，顶部/底部留 ≥20px 余量；节点盒尺寸要小于相邻节点间距（避免重叠）。
6. **字体不加粗正文**：正文黑色、不加粗；仅标题加粗。

## 骨架模板
- 固定舞台：`.deck-stage` 1920×1080，`transform: translate() scale()` 自适应窗口。
- 翻页：键盘 ←→/空格/PageUp/Down + 触屏滑动 + 滚轮（带 lock 防抖）+ 底部控制条。
- 动画：`.reveal` 渐入 + 延迟类 `.d1..d6`。
- 打印：`@media print` 每页一页。
- 参考完整可运行示例：本工作区的 `gen_deck.py`（docx→丽和康 16:9 演示，21 页含 8 个 SVG）。
