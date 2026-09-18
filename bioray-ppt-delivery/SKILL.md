---
name: bioray-ppt-delivery
description: >
  丽和康 Bioray 的固定 PPT 交付流程（全链路）。当用户要求做 / 生成 / 制作 / 编辑 PPT、演示文稿、
  幻灯片、课件、汇报材料、竞标材料、培训材料时使用。先做需求对齐（四个决策点），再按双轨（PPTX / 16:9 HTML）
  生成，执行覆盖率自检（LibreOffice→PDF→PNG 量化非白像素占比），最后按品牌基线交付。
  覆盖范围：丽和康全部对内/对外 PPT 交付物，不限于法规主题。
  触发词：做PPT、生成PPT、PPT流程、出片、培训课件、竞标材料、汇报材料。
agent_created: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
---

# 丽和康 Bioray PPT 交付流程

## 0. 这个 Skill 解决什么

把 Hannah 反复强调过的 PPT 交付约定固化下来，避免每次重述、避免返工。
**核心问题**：Hannah 期望"先对齐设计语言再动手"，讨厌"先做完再让她纠错"。

**固定流程**：

`需求对齐（4 个决策点） → 判断合并方案 → 生成 → 覆盖率自检 → 修正 → 交付`

**绝不跳步**。特别是第 1 步，即使看起来"显然"，也要先问。唯一例外是品牌基线（已锁定，直接用）。

---

## 1. 需求对齐 —— 必问 4 项

接到 PPT 任务后，**第一件事**用 `AskUserQuestion` 问这 4 个决策点，**不要把空白清单丢给用户自己填**。

### Q1. 输出形态（双轨，必问）

| 选项 | 说明 |
|---|---|
| PPTX | 可编辑 .pptx，走 `GordenPPTSkill`。默认交付形态 |
| HTML | 16:9 (1920×1080) 静态 HTML，走 `branded-16-9-html-deck`。像素级精确 |
| 两者都要 | 先出 HTML 再转 PPTX，或分别出 |

> Hannah 默认只要 PPTX，**不要自动附 PDF**。HTML 与 PPTX 是两套东西，不得混淆交付。

### Q2. 版式语言

- **默认：不要卡片** —— 优先表格 / 流程图 / 关系图 / 金字塔 / 环形 / 时间轴 / SmartArt
- 需确认：本次是否例外要卡片

### Q3. 信息密度 / 饱满度

- 每页内容量要求
- 薄页是否允许合并

### Q4. 讲解文本位置

| 选项 | 适用 |
|---|---|
| 进备注 | **讲课 PPT 默认** |
| 正文 | 阅读型材料 |
| 不需要 | 纯展示 |

### 可选追加（有需要才问）

- 首次术语是否要全称 + 缩写（**默认要**，首次出现给全称+缩写）
- 输出格式/尺寸是否特殊（**默认 LAYOUT_WIDE 13.3"×7.5"**）

> 若用户已直接给齐信息，跳过提问。

---

## 2. 合并方案确认（源文本页数多时）

源文本页数多时，**先给"原页 → 合并页"对照表请用户确认，不直接生成**。

### 批量节奏

- **>15 页默认 10 页一批**
- 每批生成完立即自检，低页先修再进下一批

---

## 3. 品牌基线（已锁定 · 直接用 · 不再问）

### 配色

| 用途 | 色值 |
|---|---|
| 品牌蓝（主） | `#05BAD8` |
| 品牌橙（辅） | `#FF9D00` |
| 正文黑 | `#000000` |
| 辅助灰 | `#5B6676` |
| 浅蓝背景 | `#EAF9FC` |
| 浅橙背景 | `#FFF5E6` |
| 深填充·蓝 | `#D6F0F6` |
| 深填充·橙 | `#FFE8C2` |
| 标题栏深一档蓝 | `#048FB0` |

**配色规则**：品牌蓝为主，品牌橙为辅。**绿色仅表示"是/符合条件"，红色仅表示"否/不符合条件"**。

### 字体

**微软雅黑（Microsoft YaHei）**

### 字号（2026-09-03 用户明确，优先级最高）

| 层级 | 字号 |
|---|---|
| 页面大标题 | **28pt 加粗** |
| 小标题 | **14–16pt 加粗** |
| 正文 | **12–14pt** |
| 标签/编号小字 | 不小于 **12pt** |

> 展示性元素（封面主标题、hero 金句、大编号字母）不受三档约束。

### 标题文案规范

大标题要**像标题**——短名词式。例如：
- ✅ "等同性论证的本质：证据可转移性"
- ✅ "差异对应的科学证据矩阵"
- ✅ "本讲要点总结"

**禁止**：
- ❌ "是什么？""为什么？"等问句
- ❌ "先把…再说"等祈使句
- ❌ "Take-home Messages：从X走向Y"这类带总结副标题的口号话术

### 其他版式约定

- **尺寸**：LAYOUT_WIDE（13.3" × 7.5"，16:9）
- **无副标题**：只有主标题
- **无页眉页脚**：页面只留主标题 + 内容（除非用户明确要求保留）
- **术语**：首次出现给全称 + 缩写
- **作者署名**：`Hanyue Yang`（`prs.core_properties.author`）

### Logo（⚠️ 用前必须先确认文件）

**不得擅自选 logo 文件**。候选资产：

| 路径 | 规格 | 说明 |
|---|---|---|
| `C:\Users\ThinkBook\WorkBuddy\2026-07-28-09-47-53\logo_large.png` | 1221×639 RGBA | **透明横向 PNG，推荐** |
| `C:\Users\ThinkBook\WorkBuddy\CE MDR 法规要求\logo.jpg` | — | 白底方形 JPG，HTML 内嵌不建议 |
| `C:\Users\ThinkBook\Desktop\FDA药物-器械组合产品Q-sub申报经验分享\_work\logo_bioray.png` | — | 另一版本 |

> **规则**：透明横向 PNG 优先。HTML 中 logo 用 base64 注入 CSS `background-image`，**只引用一次**（不要每页 `<img>`）。`background-size:contain` 在 `200×42` 盒内。

### 参考模板

| 路径 | 用途 |
|---|---|
| `C:\Users\ThinkBook\WorkBuddy\2026-09-07-17-09-17\clean_template.pptx` | 干净 PPTX 模板 |
| `C:\Users\ThinkBook\Desktop\FDA药物-器械组合产品Q-sub申报经验分享\_work\培训课件_丽和康模板_v4.pptx` | 培训课件版式参考 |

---

## 4. 双轨生成

### 轨 A：PPTX（默认）

**主力**：`GordenPPTSkill`
- 21 套内置中文模板，或用户自带 `.pptx` 模板
- **只替换文字，不破坏原排版/配色/字号**
- 内置出框检测 + 同级标题字号一致校验

**备选**：
- `medtech-regulatory-ppt` —— 法规主题专用（输出 15 页结构规格 + 视觉概念 + 可编辑 PPTX）
- `codex-ppt-skill` / `ppt-generator-pro` / `rw-consulting-ppt` —— 图片型 PPT
- `pptx-template-clean-rebuild` —— 修复 pptx 空白 bug

**生成要点**：
- `prs.core_properties.author = "Hanyue Yang"`
- 尺寸 LAYOUT_WIDE
- 讲解文本进备注（若 Q4 选了备注）

### 轨 B：16:9 HTML

**主力**：`branded-16-9-html-deck`
- 1920×1080 固定舞台，键盘/触摸/滚轮导航
- 内嵌透明 PNG logo（base64，单次引用）
- SVG 图：环形 / 漏斗 / 泳道 / 流程图（含判定菱形）/ 金字塔 / 甘特 / 枢纽

**后处理（可选）**：`NQ-PPT-HTML-Editor` —— 若用户想自己可视化微调

**其他 HTML 渲染器**（按风格选）：
- `guizang-ppt-skill` —— 电子杂志×电子墨水 / 瑞士国际主义，横向翻页
- `html-ppt-skill` —— HTML PPT Studio，模板驱动

### 兼容优先于复杂

- **SVG / SmartArt 优先保稳态渲染**
- 放射文字、超长环绕一律改固定列 / 网格
- "参考"≠抄袭：只借鉴结构与质量层级，不搬 CSS / 配色

---

## 5. 覆盖率自检（必做 · 不可跳）

**阈值**：

| 页面类型 | 非白像素占比下限 |
|---|---|
| 内容页 | **40%+** |
| 总结页 / 时间轴页 | **20%+** |

**链路**：`LibreOffice → PDF → PNG → 量化非白色像素占比`

**执行**：

```bash
# 1. PPTX → PDF
soffice --headless --convert-to pdf --outdir <outdir> <file.pptx>

# 2. PDF → PNG（每页）
# 用 pdftoppm 或 Python (pdf2image / PyMuPDF)

# 3. 量化非白像素
# Pillow: 统计 (r,g,b) 非接近 255 的像素占比
```

**判定**：
- 低于阈值的页**先修再交**
- 每批生成后立即自检（10 页一批）

**注意**：
- 渲染产物（PDF / PNG）**只是临时文件，不交付**
- 内部自检用的 LibreOffice 链路保留，但不要把 PDF 列入交付物

---

## 6. 交付

### 交付形态（克制）

| 用户要的 | 只给 |
|---|---|
| PPT | **只出 .pptx**（不自动出 PDF） |
| 文档 | 只出 docx（不出 pdf） |
| 表格 | 只出 xlsx（不出 csv） |

**PPTX 默认只出 PPTX**，除非用户明确索要 PDF。

### 交付前自检清单

- [ ] 品牌基线是否正确（配色 / 字体 / 字号三档）
- [ ] 标题是否短名词式（无问句 / 无祈使句 / 无口号副标题）
- [ ] 无页眉页脚、无副标题（除非用户要求）
- [ ] 术语首次出现是否全称 + 缩写
- [ ] 作者署名 `Hanyue Yang`
- [ ] 覆盖率自检是否达标（内容页 40%+ / 总结页 20%+）
- [ ] 讲解文本位置是否符合 Q4
- [ ] Logo 是否与用户确认过文件
- [ ] 交付形态是否克制（没有多给 PDF）

---

## 7. 执行纪律（避免"暂停感"）

### 类型 A：输出生成到一半断掉

- 长正文 / 长报告章节**一律落文件**，不在对话回复里硬铺开
- 用脚本分块写入或 append
- 长文档分批：第 1–N 节 → 续写 → 合并
- **交付前先自检文件完整性**（行数 / 字符数 / 章节数），断了就补，**绝不把半截内容交出去**

### 类型 B：命令前台跑到超时（2 分钟默认超时）

- 预计 >1 分钟的命令**一开始就 run_in_background**
- pip 走国内镜像源（清华/阿里）
- 长脚本加实时 `print` 进度
- 大批量文件改小批（约 20 个一批）

### 本机环境坑（已实测）

- **Bash shim 缺核心命令**：`ls` / `head` / `tail` / `sed` / `dirname` / `grep` 全部 `command not found`
- **PowerShell stdout 不回显**，`Add-Type` 被拦截
- **可靠做法**：文件遍历 / 压缩解压 / 进程调用一律用托管 Python：
  `C:\Users\ThinkBook\.workbuddy\binaries\python\versions\3.13.12\python.exe`
- 输出前 `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` 防中文乱码
- **参数复杂时写成 .py 脚本文件再执行**，不要在一行 `-c` 里塞引号（会被 bash / 沙箱二次解析搞坏）
- 反斜杠路径在 `dangerouslyDisableSandbox` 下会被提前解析 → 必须落 .py 文件

---

## 8. 快速决策表

| 用户需求 | 走哪条 |
|---|---|
| 交 .pptx 成品（培训/竞标/汇报） | 轨 A · `GordenPPTSkill` |
| 16:9 品牌 HTML（像素级精确） | 轨 B · `branded-16-9-html-deck` |
| HTML 做完想自己微调 | + `NQ-PPT-HTML-Editor` |
| 法规主题 PPT 从零搭 | 轨 A · `medtech-regulatory-ppt` |
| 分享/发布会风格网页 PPT | 轨 B · `guizang-ppt-skill` |
| 咨询级纯图展示 | 轨 A · `rw-consulting-ppt` |
| PPTX 打开空白 | `pptx-template-clean-rebuild` |
