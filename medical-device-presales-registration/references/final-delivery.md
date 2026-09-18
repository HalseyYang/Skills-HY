# Final Version 交付规则

## 1. 默认只交付最终版

不交付：

- 初稿；
- QA Word；
- audit checklist；
- tracked-change QA copy；
- 内部意见关闭记录；
- reviewer 工作底稿。

除非用户明确索取。

## 2. 完整售前评估的默认交付物

用户请求“评估注册路径”“测试这个产品”“全面评估”“做售前方案”等完整项目时，在 Target Market Gate 已通过并完成三轮 Regulatory Audit 后，默认交付：

### A. 对话框 Executive Summary

目标是可以直接复制到微信、钉钉或发领导/客户。

默认要求：

- 1–2 个紧凑段落；
- 通常 3–5 句话；
- 原则上控制在约 120–250 个汉字，复杂项目最多约 300 个汉字；
- 只保留：**注册路径、临床要求、最大监管风险、下一步建议**；
- 先说结论，不展开完整证据链；
- 不把 full report 的章节浓缩后全部塞进 summary；
- 避免大段法规背景、标准清单、完整 predicate 比较和冗长 disclaimer。

如果必须附官方核验依据，可在 Summary 后单独放 1–3 条最关键 reference，不破坏正文可转发性。

### B. 完整 Final DOCX

默认使用 `assets/bioray-presales-clean-template.docx` 的版式和结构生成完整策略文件。

文件至少覆盖：

- Executive Summary；
- 产品监管定位；
- 主路径及备选路径；
- classification 及依据；
- predicate / additional predicate / reference device，或 similar device / equivalence candidate；
- intended use / claims strategy；
- 关键技术差异与监管风险；
- bench / animal / clinical / software / electrical / EMC / usability / biocompatibility / sterilization / packaging 等证据规划；
- multi-model / family / worst-case strategy；
- OUS clinical data / U.S. bridging（如适用）；
- Pre-Sub / NB consultation 及建议问题；
- parallel compliance；
- Pending information；
- 主要监管风险与推荐下一步；
- 官方 references 及核实日期。

DOCX 是三轮 Regulatory Audit 后的 Final Version，不带 QA comments、tracked changes 或内部审核记录。

## 3. 何时不生成 DOCX

以下情况不自动生成文件：

- 用户明确说“只给我 summary / 微信版 / 简单说”；
- 用户明确说“先不要文件 / 只在对话框分析”；
- 用户只是询问单一局部问题，例如“是否需要临床”“这个 product code 对不对”；
- 用户明确要求其他交付格式。

## 4. 市场未确认时不交付方案

目标市场未明确且当前任务无法从上下文唯一确定时，先执行 Target Market Gate。此时不要输出完整注册策略、不要生成 DOCX，也不要自行扩展为 FDA+EU 或中美欧。

## 5. Client Presales Version

完整 Final DOCX 默认使用客户可读语言，结论明确但不夸大。内部研究方法、搜索过程、反向争论和 Audit 记录不写入客户版。报价仅在用户要求时加入。

## 6. Final DOCX 文档要求

- clean final copy；
- 无 tracked changes；
- 无 reviewer comments；
- 清理自动备注/工具元数据；
- 作者设置为 `Hanyue Yang`；
- 仅保留用户明确要求的批注；
- 使用 clean template 时只复用样式和布局，不继承模板占位事实；
- 完成 render → 逐页检查 → 修订 → 再次 render → 最终交付。

## 7. 引用与链接

监管结论在完整报告中应可追溯到官方来源。对话框 Executive Summary 可以减少链接数量，但不能用没有依据的确定性结论替代证据。

正式客户版可附精简“法规核验记录”；内部证据台账无需默认输出。

## 8. 不确定性

最终版允许存在 Pending，但必须具体。例如：

“目前可优先按 510(k) 评估；若最终 intended use 包含独立疾病筛查/诊断 claim，临床证据要求和 predicate strategy 需要重新评估。”

避免仅写“具体以 FDA 为准”而不给当前判断。
