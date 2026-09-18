---
name: medical-device-presales-registration
description: 医疗器械售前注册策略评估。目标市场明确后，用于根据产品资料判断分类、申报路径、Predicate/Reference Device、测试与临床证据、Pre-Sub/NB 咨询必要性及并行合规要求；所有法规事实当次官方核验，并在内部完成三轮 Regulatory Audit 后交付 final version。完整售前评估默认在对话框提供精简 Executive Summary，并使用内置 clean template 生成完整 Final DOCX；若用户只要 summary 或明确不要文件，则仅按其要求交付。
---

# 医疗器械注册售前策略

## 核心原则

本 Skill 的目标是直接形成可用于售前沟通和项目决策的最终注册策略。所有中间分析、QA、Audit、反证检查和修订均在内部完成。默认不向用户交付草稿、QA Word、审核清单、意见关闭表或内部工作底稿。

工作顺序固定为：

`Target Market Gate → 产品事实提取 → 关键 blocker 判断 → 官方检索 → 路径设计 → 证据策略 → 三轮 Regulatory Audit → 自动修订 → Final Consistency Check → 对话框 Executive Summary + 完整 Final DOCX`

若用户明确只要 summary、只要对话框分析或不要文件，则按用户要求缩减交付物。

不得以“需要 QA”作为终点。Audit 发现的问题必须在输出前修正；无法通过现有产品资料和公开官方证据解决的问题才保留为“待确认”或建议通过 FDA Pre-Sub / NB 咨询确认。

## 必须读取的资源

1. 项目开始时读取 [intake-triage.md](references/intake-triage.md)，先执行 Target Market Gate。
2. 研究任何法规、数据库、费用、标准、Predicate、NB 或时效性事实时读取 [source-evidence-policy.md](references/source-evidence-policy.md)。
3. FDA 项目读取 [fda-pathway-strategy.md](references/fda-pathway-strategy.md)。
4. CE MDR 项目读取 [eu-mdr-pathway-strategy.md](references/eu-mdr-pathway-strategy.md)。
5. 涉及测试、动物、临床、软件、电气、可用性或多型号证据规划时读取 [evidence-strategy.md](references/evidence-strategy.md)。
6. 每个最终项目在交付前必须读取并执行 [regulatory-audit.md](references/regulatory-audit.md)。
7. 输出前读取 [final-delivery.md](references/final-delivery.md)。
8. 只要属于完整售前评估并需要生成最终 DOCX，就读取 [commercial-brand-docx.md](references/commercial-brand-docx.md) 并使用 clean template；报价、批注或特殊品牌要求同样读取该文件。

## 1. Target Market Gate：市场不明确时先确认

目标申报市场是强制前置条件。不同市场的 device qualification、classification、pathway、clinical evidence、testing、submission unit 和 post-market/parallel compliance 均可能不同，因此禁止自行默认 FDA、EU MDR、中国或多市场。

执行规则：

- 用户明确说“申报 FDA / 美国” → 直接按 FDA 执行；
- 用户明确说“CE / EU MDR / 欧盟” → 直接按 EU MDR 执行；
- 用户明确说“中美欧 / FDA+CE / 多市场” → 按指定市场组合执行；
- 用户只说“评估这个产品”“测试一下这个产品”“看看注册路径”，且当前任务没有明确市场 → **先询问目标市场，再开始法规检索和完整分析**；
- 若当前对话中同一产品、同一任务已经明确市场，可沿用，不重复提问；
- 若用户切换到新产品，不得仅因上一项目讨论过某市场就自动沿用，除非用户明确说“同样按美国/欧盟”等。

市场未确认时只问这一个问题，避免同时抛出产品细节问卷。例如：

“这次主要评估哪个市场：FDA、EU MDR，还是中美欧/其他市场？”

## 2. 先建立事实台账

产品事实优先来自用户上传资料、说明书、规格书、标签、技术文件和用户明确说明。法规事实来自当次官方检索。两类事实不得混在一起。

内部至少区分四种状态：

- `Source-confirmed`：用户资料或用户明确说明已经确认；
- `Officially verified`：本次通过官方法规、数据库、指南或标准发布方核验；
- `Analysis`：基于前两类事实形成的法规判断；
- `Pending`：现有证据不足，仍可能改变路径或证据要求。

不得用竞品、历史项目或模型常识反向补齐用户产品的关键参数。

## 3. 市场确认后，不因次要信息不全停止工作

只有缺失信息会直接阻断分类、路径、临床要求或 submission unit 判断时才先提问。其他情况下先给出条件式完整评估，并明确哪些条件会改变结论。

默认优先追问 1 个最关键开放问题；确有多个独立 blocker 时可集中询问，但避免一次抛出长问卷。

以下信息通常可能改变路径：预期用途/适应症、目标人群、作用机制、侵入/植入属性、有源诊断或治疗属性、关键输出参数、软件是否独立诊断、无菌/重复使用、组合产品属性、型号之间的实质差异。

报价、税率、签约主体等商务信息仅在用户要求报价或正式报价内容时收集，不得作为一般注册路径评估的前置条件。

## 4. 注册策略必须一次性完整设计

FDA 或 CE 注册路径评估默认至少覆盖：

- 主路径及备选路径；
- 分类依据和可能改变分类的触发条件；
- Predicate / Reference Device 或 Similar Device / Equivalence Candidate 策略；
- 关键技术差异及监管风险；
- 测试、动物、临床、软件、电气安全、EMC、可用性、生物相容性、包装/灭菌等证据规划；
- 多型号/系列产品的申报和 worst-case 逻辑；
- 是否需要美国临床、OUS 数据是否可能接受、是否需要桥接；
- Pre-Sub / NB 咨询必要性以及建议提问；
- 并行合规义务，例如 QMSR、UDI、企业注册/列名、U.S. Agent、辐射产品、网络安全、SRN、Basic UDI-DI、EUDAMED 等；
- 当前仍需确认的信息和主要监管风险。

不要等用户逐项追问再补齐上述内容。

## 5. 所有时效性事实必须当次核验

法规版本、FDA classification/product code、510(k)/De Novo/PMA 状态、Predicate 编号、submission type、Third Party Review eligibility、FDA 用户费、QMSR 状态、EUDAMED 实施、NB scope、标准版本、FDA recognition / EU harmonisation、NB 费率等，必须使用本次任务中的官方来源核验。

历史模板和旧项目中的数字只能作为线索，不能作为最终事实。

## 6. 输出前必须执行三轮 Regulatory Audit

三轮审核均为内部质量步骤，执行后自动修订，不单独向用户输出：

1. **Evidence Audit**：检查每项关键事实是否由当前官方证据支持，是否存在过期、错引、扩大解释或遗漏反例；
2. **Regulatory Logic Audit**：从反方向重新挑战 classification、pathway、predicate/equivalence、临床要求、测试充分性和 Pre-Sub/NB 必要性；
3. **Final Consistency Audit**：检查 Executive Summary、完整报告、表格、周期、费用、风险和下一步是否完全一致，删除模板残留和未经证实的确定性措辞。

每一轮发现问题必须回到正文自动修正，再进入下一轮。严禁把同一个执行者的三轮自检表述成“独立专家审核”。只有实际调用独立 reviewer 或人工专家时才能使用“独立专家复核”这一表述。

## 7. 默认交付：短 Summary + 完整 Final DOCX

对于“评估注册路径 / 测试这个产品 / 做售前方案 / 全面评估”这类完整项目，市场确认并完成三轮 Audit 后，默认交付两部分：

1. **对话框 Executive Summary**：真正可直接发微信/领导/客户，默认 1–2 个紧凑段落，通常 3–5 句话，重点只有“注册路径、临床要求、最大监管风险、下一步建议”。禁止把完整报告压缩后仍堆在对话框中；
2. **完整 Final DOCX**：使用 `assets/bioray-presales-clean-template.docx` 的结构和视觉生成，完整展开分类、路径、predicate/reference、差异、测试、动物、临床、Pre-Sub/NB、并行合规、风险、待确认项和官方 references。DOCX 必须先完成三轮法规 Audit，再做文档 QA，只交付 clean final。

例外：

- 用户说“只给我 summary / 微信版 / 简单说” → 只交付精简 Summary，不生成文件；
- 用户说“先别出文件 / 只在对话框分析” → 不生成 DOCX；
- 用户只问一个局部问题，例如“这个需要临床吗” → 直接回答该问题，不自动生成完整报告；
- 用户明确要求其他格式 → 按用户指定格式。

## 8. Final Version 的边界

最终结论应直接、可执行，但必须与证据强度匹配。可以给出首选路径、风险高低、建议动作和有条件结论；不得承诺获批、保证免临床、保证固定周期或把公开证据不能解决的问题写成确定事实。

当关键问题仍存在真实不确定性时，Final Version 中应明确写出：

- 当前最合理判断；
- 不确定性来自哪里；
- 哪个新增信息可解决；
- 是否建议 Pre-Sub / NB 咨询；
- 如监管机构给出相反反馈，备选路径是什么。
