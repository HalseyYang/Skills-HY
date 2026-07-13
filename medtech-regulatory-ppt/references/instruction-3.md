# 指令三：可编辑 PPT 生成与拼装（Canonical Template）

> **Topic-adaptive markers:**
> - `[TOPIC]` = 法规主题全称
> - `[TOPIC_SHORT]` = 简称
> - `[SLIDE_COUNT]` = 总页数（默认 15）
> - `[PHASE_1_OUTPUT]` = 指令一的输出文件名
> - `[PHASE_2_STYLE]` = 指令二选定的视觉风格方案名称

---

```
参考上面选定的视觉风格方案和 [TOPIC] PPT 结构的 MD 内容文档，使用 python-pptx
生成全部的可编辑 PPT 幻灯片，拼装为一个标准的 PPTX 演示文稿。

幻灯片内容必须为可编辑的文本元素（文本框、表格、形状等），不是图片。
文字正确、清晰、可编辑、可复制、可修改。

## 总体原则

1. 所有文字内容必须可编辑——使用文本框、表格、SmartArt 等效形状，不要将文字作为图片嵌入。
2. 版式、配色、字体风格参考指令二选定的视觉方案。
3. 每张幻灯片要有演讲者注释。
4. 封面页和章节过渡页可以使用 ImageGen 生成背景图（纯装饰），但标题文字仍需以可编辑文本框叠加。

## 执行步骤

### 步骤一：读取内容文档

读取指令一输出的 Markdown 内容文档（[PHASE_1_OUTPUT]），获取全部 [SLIDE_COUNT] 页的：
- 页面标题
- 核心观点
- 页面要点
- 建议展示形式
- 讲解提示

### 步骤二：创建可编辑 PPTX

使用 python-pptx 创建标准 PPTX 文件。每张幻灯片根据内容类型采用不同的版式：

#### 幻灯片基础设置

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

prs = Presentation()
prs.slide_width  = Inches(13.333)  # 16:9
prs.slide_height = Inches(7.5)

# 定义配色（参考选定的视觉方案）
PRIMARY    = RGBColor(0x18, 0xB8, 0xC8)  # 青蓝
SECONDARY  = RGBColor(0xF2, 0xA5, 0x1A)  # 橙黄
DARK_TEXT   = RGBColor(0x1A, 0x1A, 0x2E)  # 深灰
MED_TEXT    = RGBColor(0x63, 0x6E, 0x72)  # 中灰
LIGHT_BG    = RGBColor(0xF5, 0xF7, 0xFA)  # 浅灰背景
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
```

#### 封面页版式

- 可使用 ImageGen 生成一张纯装饰背景图铺满幻灯片
- 在背景图上叠加可编辑文本框：标题（36pt 粗体）、副标题（20pt）、公司名/日期/汇报人（14pt）
- 标题颜色使用品牌主色或白色（取决于背景深浅）

#### 内容页版式

- 顶部标题栏：高度约 1.2 英寸，品牌主色填充背景，标题文字白色 28pt 粗体
- 正文区域：左对齐文本框，14-18pt，深灰色
- 每页 3-5 个要点，用项目符号区分
- 正文区留白充分，左右边距至少 0.8 英寸

#### 表格/矩阵版式

```python
from pptx.util import Inches
table = slide.shapes.add_table(rows=4, cols=4, left=Inches(1), top=Inches(1.8),
                                width=Inches(11), height=Inches(4.5)).table
# 设置表头行样式：品牌主色背景，白色文字
# 设置数据行交替浅色背景
# 设置单元格内边距和文字对齐
```

#### 流程图版式

使用圆角矩形 shapes 和连接线（connector）构建：
```python
from pptx.enum.shapes import MSO_CONNECTOR_TYPE, MSO_SHAPE
# 使用 add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ...) 创建流程节点
# 使用 add_connector(MSO_CONNECTOR_TYPE.STRAIGHT, ...) 连接节点
# 节点填充品牌色，文字白色
```

#### 章节过渡页版式

- 可使用 ImageGen 生成的背景图
- 叠加大号章节编号（72pt，半透明品牌色）和章节标题（36pt）

### 步骤三：添加演讲者注释

每页演讲者注释应：
- 使用口语化中文书写，适合口头讲解
- 不要逐字复述幻灯片内容
- 扩展页面要点，补充案例、背景或过渡语句
- 连接前后页面的逻辑
- 每页约 80-150 字

```python
notes_slide = slide.notes_slide
notes_slide.notes_text_frame.text = speaker_note_text
```

### 步骤四：保存输出

```python
prs.save("[TOPIC_SHORT]_presentation.pptx")
```

## 各页面类型的实现参考

| 页面类型 | 实现方式 | 说明 |
|----------|----------|------|
| 封面页 | ImageGen 背景图 + 文本框叠加 | 标题/副标题可编辑 |
| 目录页 | python-pptx 文本框 + 形状 | 章节列表可编辑 |
| 章节过渡页 | ImageGen 背景图 + 文本框 | 编号和标题可编辑 |
| 内容页（要点列表） | python-pptx 文本框 | 全部文字可编辑 |
| 表格/矩阵 | python-pptx table | 全部单元格可编辑 |
| 流程图 | python-pptx shapes + connectors | 节点文字可编辑 |
| 对比表 | python-pptx table | 全部可编辑 |
| 甘特图/时间轴 | python-pptx shapes + 文本框 | 全部可编辑 |
| 三角关系图 | python-pptx shapes + 文本框 | 全部可编辑 |
| 总结行动页 | python-pptx 文本框 + 形状 | 全部可编辑 |

## 质量检查

- [ ] 全部 [SLIDE_COUNT] 页幻灯片已生成
- [ ] 所有文字内容为可编辑文本框/表格/形状（非图片嵌入）
- [ ] 视觉风格全篇一致（配色、字体、版式）
- [ ] 每页均有演讲者注释
- [ ] 内容与指令一的规划一致
- [ ] 无虚构法规结论
- [ ] 术语使用一致
- [ ] 文件可正常用 PowerPoint/WPS 打开编辑
- [ ] 输出为 .pptx 文件
```
