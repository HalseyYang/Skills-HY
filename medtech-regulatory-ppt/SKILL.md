---
name: medtech-regulatory-ppt
description: |
  Generates three reusable PPT instruction templates adapted to any medical device
  regulatory topic. Given a topic (e.g., "FDA 510(k) Submission Strategy", "CE MDR
  Clinical Evaluation", "EU Breakthrough Device Designation"), outputs: 指令一 (15-page
  content structure spec), 指令二 (3-4 visual style concepts via ImageGen), 指令三
  (editable PPTX generation with python-pptx — text boxes, tables, shapes; not images).
  All slide text is fully editable. Trigger: 法规PPT指令, 生成PPT指令, PPT instruction
  template, PPT指令模板, any request to "generate PPT instructions" for a regulatory topic.
agent_created: true
---

# MedTech Regulatory PPT — Instruction Template Generator

## What This Skill Does

Given a medical device regulatory topic, generate three complete, adapted instruction
documents that the user can take to any AI tool (WorkBuddy, ChatGPT, etc.) to produce a
professional consulting-grade PPT.

**This skill outputs instructions, not the PPT itself.**

## When to Use

Trigger when the user asks to generate PPT instructions for any regulatory topic:

- "帮我生成一套 FDA 510(k) 的 PPT 指令"
- "我想做 CE MDR CER 的培训 PPT，给我指令"
- "Generate PPT instructions for EU Breakthrough Device"
- "给我一套 NMPA 注册策略的 PPT 指令模板"
- Any request with topic + PPT + 指令/instruction/template

## How It Works

1. User provides a **topic** (e.g., "FDA 510(k) 申报策略")
2. Read `references/instruction-1.md`, `references/instruction-2.md`, `references/instruction-3.md`
   for the canonical instruction templates
3. Adapt all three instruction documents to the given topic
4. Output all three adapted documents as a single Markdown file

## Adaptation Rules

### For 指令一 (Content Structure)

The canonical 15-page structure is:
1. 标题页
2. 为什么现在要关注 [Topic]
3. 这不是"绿色通道"，而是"监管支持机制"（或等价概念替换）
4. 哪些器械可能符合 [Topic 核心概念]
5. 标准一：XXX 如何判断
6. 标准二：XXX 如何证明
7. 客户初筛判断矩阵
8. 申请流程总览
9. 申请材料核心文件
10. 各监管方扮演什么角色
11. 证据策略：哪些数据可前置，哪些可后置
12. 上市后证据为何是关键
13. 对认证的实际影响：能加快什么，不能承诺什么
14. 咨询公司可提供的服务包与交付物
15. 结论：客户是否应申请的三步判断

Adapt each page's topic-specific content while keeping the structural framework.
The "六、建议PPT结构" section must list the 15 adapted page titles.

### For 指令二 (Visual Style)

Almost no topic-specific changes needed. The 4 style concepts (Professional, Modern,
Technical, Premium) and 6 page types (Cover, Agenda, Section, Framework, Decision,
Summary) are universal.

Only adapt:
- Section 4 example text to match the topic's regulatory framework terms
- Section 5 example text to match the topic's decision criteria

### For 指令三 (Editable PPTX Assembly)

Almost no topic-specific changes. The assembly process (python-pptx → editable PPTX)
is universal. Key instruction: all slide content must be editable text elements
(text boxes, tables, shapes), NOT embedded images. ImageGen may be used only for
decorative backgrounds on cover and section divider pages. Adapt only the page
count if the topic requires more/fewer slides.

## Output Format

Output all three instruction documents in a single Markdown file named
`[topic]-ppt-instructions.md`. Use clear separators:

```
# [Topic] — PPT 生成指令套装

---

## 指令一：PPT 内容结构设计
... (adapted instruction 1)

---

## 指令二：视觉风格方案设计
... (adapted instruction 2)

---

## 指令三：全页生成与 PPTX 拼装
... (adapted instruction 3)
```

## Key Principles

1. **Keep the exact same structure** as the canonical templates — section numbering, output format specifications, design rules
2. **Replace topic-specific content only** — terminology, regulatory bodies, criteria names, page titles
3. **Preserve all quality rules** — consulting language, no regulation copy-paste, client-focused messaging
4. **Do NOT fabricate regulation content** — if uncertain about specific criteria for a topic, use generic placeholders and note the gap
5. **Keep the original Chinese instruction text** — the user's audience reads Chinese instructions
