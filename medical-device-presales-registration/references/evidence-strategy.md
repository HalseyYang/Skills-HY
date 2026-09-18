# 测试、动物、临床与多型号证据策略

## 1. Evidence planning 原则

证据规划必须建立在三件事上：

1. 产品风险；
2. 与 predicate / similar device 的差异；
3. 申报 claims。

禁止先列一套固定 IEC/ISO 清单，再反向套产品。

## 2. Evidence matrix

内部建议使用：

| Regulatory question | Risk / difference | Evidence needed | Method / standard | Market | Existing evidence | Gap |
|---|---|---|---|---|---|---|

所有测试都应能回答一个明确的安全、性能或等同性问题。

## 3. 常见证据模块

按适用性评估：

- functional / bench / mechanical；
- dimensional / material / chemical characterization；
- electrical safety / EMC；
- essential performance；
- software V&V；
- cybersecurity；
- wireless coexistence / interoperability；
- biocompatibility；
- sterilization / microbial limits；
- packaging integrity / transportation / shelf life；
- cleaning / disinfection / reprocessing；
- human factors / usability；
- animal performance / healing / tissue response；
- clinical performance；
- imaging / diagnostic accuracy / measurement accuracy；
- radiation / laser / X-ray / acoustic output 等特定物理能量安全。

## 4. 标准使用规则

每个标准必须核验：

- 最新或适用版本；
- FDA recognition 状态（FDA 项目）；
- EU harmonisation / state-of-the-art 状态（CE 项目）；
- 是否真正覆盖该产品和测试目的；
- 是否存在 transition period 或 superseded version。

如无法确认标准版本，Final Version 可写测试类别和“版本需结合当前认可/协调状态及实验室能力最终确认”，不得猜编号。

## 5. 临床证据层级

区分：

- 已上市临床数据；
- retrospective / literature data；
- usability / human factors data；
- clinical performance imaging/data comparison；
- feasibility / exploratory clinical study；
- pivotal clinical investigation。

不要把“需要人体数据”直接等同于“需要大样本注册临床试验”。

## 6. 临床样本量

若用户问样本量：

- 先明确 study objective、primary endpoint、effect size / margin、variance / event rate、design、alpha、power、dropout；
- 若当前仅处于售前阶段，可给区间或 precedent-based planning range，但必须说明依据；
- 不得仅依据产品分类凭空给出固定例数。

## 7. Animal study gate

仅在 bench 无法充分模拟关键生物学/组织/生理性能，或 predicate precedent / guidance / regulator 明确表明动物证据必要时建议动物试验。

说明动物试验解决的具体 regulatory question，例如：组织反应、能量作用深度、闭合完整性、慢性植入表现，而非笼统写“建议做动物”。

## 8. Software / Cybersecurity / AI

明确：

- IEC 62304 software safety classification（如适用）以及 FDA 当前 software documentation level / content framework；
- architecture、SOUP、V&V、traceability；
- network interfaces、update、authentication、logging；
- 是否属于 cyber device；
- AI/ML 的 training/validation data、locked/adaptive behavior、bias/generalizability；
- 软件变化是否会改变 intended use 或临床性能。

每次使用当前 FDA guidance，不沿用旧版模板名称。

## 9. Human factors

当操作错误可能导致严重风险、用户群特殊、界面/自动化复杂、家庭使用或 FDA guidance/precedent 关注时，单独评估 human factors / usability validation。

不要把 formative evaluation 与 summative validation 混为一谈。

## 10. Family / worst-case testing

多型号共享 submission 时需形成型号差异矩阵，并对每个测试说明代表型号选择依据：

- 最大能量/输出；
- 最大尺寸或最小尺寸；
- 最复杂软件功能；
- 最差材料接触；
- 最严苛灭菌/包装；
- 其他与特定风险直接相关的 worst case。

不能只用“最高配置型号代表全系列”作为通用逻辑。
