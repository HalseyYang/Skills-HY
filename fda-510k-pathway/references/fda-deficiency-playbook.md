# FDA 实审退回原因库与性能测试标准映射（零 AI 请求作战手册）

> **用途**：RTA 只查行政完整性；**真正的淘汰发生在实审（Substantive Review）的 AI 请求（Additional Information Request）**。本文件把 FDA 审评员最常开火的技术缺陷整理成库，逐条给出对策——交付前对照本库自查，是「零整改拿 510(k)」的核心动作。

---

## 1. FDA 审评双阶段地图

```
提交（eSTAR）
   │
   ▼
┌─────────────────────┐
│ RTA 行政完整性审查    │ ← 约 30% 首交栽在这里（29 项清单见 SKILL.md 步骤 10）
│ 180 天 Hold 补正      │
└─────────────────────┘
   │ 通过
   ▼
┌─────────────────────┐
│ 实审 Substantive Review│ ← AI 请求多发生在此；MDUFA 时钟暂停等回复
│ （AI 请求 ↔ 回复循环）  │
└─────────────────────┘
   │
   ▼
SE 判定 / NSE（可 De Novo 申请）/ Withdraw
```

> ⚠️ 回复 AI 请求只有一次完整机会；回复后仍有问题 → **Withdraw**，用户费不退。所以**首次回复必须一次到位**。

---

## 2. 实审 Top 退回原因库（按出现频率排序，行业经验估算）

### 退回 1：性能测试不充分（bench testing 缺口）
- **典型表现（审评员原文风格）**："The submitted bench testing does not adequately demonstrate that the device performs as claimed in the Indications for Use."
- **根因**：测试项与声称规格对不上——IFU 声称了，测试没做；或测试条件不能代表最坏使用场景。
- **对策**：建立「声称规格 ↔ 测试项」覆盖矩阵（每一个 IFU 数字都对应一个测试报告数据点）；测试方案经 worst-case 论证。
- **自检问题**：把 IFU 的每个性能数字圈出来，能在测试报告里逐个找到吗？

### 退回 2：生物相容性缺口
- **典型表现**："The biological evaluation does not address [new material / new contact duration / new contact type]."
- **根因**：材料或接触方式变更后未追加 ISO 10993 终点；或豁免论证无化学表征支撑。
- **对策**：ISO 10993-1:2025（FDA 认可号 2-313）框架下按接触类型和时长选终点；新接触 → 全套重评；豁免 → TRA + 化学表征。
- **自检问题**：SE 表里每个材料变化，都有对应的生物学评价或豁免论证页码吗？

### 退回 3：软件文档层级未声明 / V&V 覆盖不足
- **典型表现**："The documentation level for the device software is not identified. Provide the rationale..."
- **根因**：未按 FDA 软件指南声明 Documentation Level（Basic/Enhanced）；或单元/集成/系统测试只交了大纲。
- **对策**：① 明确声明层级并给理由（危害严重度驱动）；② IEC 62304 架构文档 + 单元/集成/系统级**完整** V&V 报告（非大纲）；③ 软件版本与测试版本一致。
- **自检问题**：风险文件里每个软件危害，都能追溯到测试用例吗？

### 退回 4：网络安全（Section 524B）缺件
- **典型表现**："The submission lacks a Software Bill of Materials (SBOM)..." / "...a vulnerability management plan..."
- **根因**：以为「不联网」就不管——**含 USB/蓝牙/调试端口也算 cyber device**。
- **对策**：7 件套齐（威胁模型/SBOM（CycloneDX 或 SPDX）/VMP/CVD/安全风险/安全测试证据/更新管理）；SBOM 用自动化工具生成（Syft 等）。
- **自检问题**：SBOM 能覆盖最终发布版本的全部组件吗？漏洞响应 SLA 写进文档了吗？

### 退回 5：HFE 类别判定错误 / URRA 缺失
- **典型表现**："The human factors submission category determination is not adequately justified..."
- **根因**：低估 UI 变更影响；URRA 只列了危险没做关键任务判定；把 IFU 修改不当 UI 变更。
- **对策**：按 Decision Point A–D 逐条留痕（2026-08-01 起强制）；类别 2 也要 URRA 摘要；无关键任务也要交类别 1/2 文档。详见 hfe-human-factors 技能。
- **自检问题**：类别 3 的器械，总结性测试报告是 7 节完整版吗？

### 退回 6：灭菌验证不完整
- **典型表现**："The sterilization validation does not include [bioburden / EO residuals / packaging integrity]."
- **根因**：只做了 SAL 部分；包装老化只做加速没做实时。
- **对策**：ISO 11135（EO：残留 EO/ECH 达标）/ ISO 11137（辐射剂量审核）/ ISO 17665（湿热）；ISO 11607-1/-2 包装验证 + ASTM F1980 加速老化 + 实时老化启动。
- **自检问题**：无菌声称的三个支柱（灭菌验证/包装完整性/货架寿命）都齐了吗？

### 退回 7：货架寿命（shelf life）缺口
- **典型表现**："Real-time aging data is not provided."
- **根因**：只交加速老化，实时老化「在进行中」未承诺。
- **对策**：加速老化数据 + 实时老化方案与时间表（承诺数据出来后提交）。
- **自检问题**：有效期声称有测试报告还是拍脑袋？

### 退回 8：电气安全 / EMC 缺 DoC
- **典型表现**："Provide a signed Declaration of Conformity for IEC 60601-1 / 60601-1-2."
- **根因**：交了测试报告，漏了符合性声明；EMC 未覆盖全工作模式。
- **对策**：IEC 60601-1 全项 + IEC 60601-1-2（含无线共存场景）+ 制造商 DoC 签字。
- **自检问题**：有源器械的 DoC 签字了吗？EMC 测试覆盖了所有运行模式吗？

### 退回 9：标签 / IFU 声称超范围
- **典型表现**："The labeling claims performance not supported by the submitted data."
- **根因**：市场部门写的标签，技术部门没审。
- **对策**：标签声称 ↔ 测试报告 ↔ SE 表三方核对；Rx/OTC 属性标注；英文完整性（境外制造商常见坑：中文警示语残留）。
- **自检问题**：标签上每个数字/声称，都有出处吗？

### 退回 10：临床数据不足（特定风险类别）
- **典型表现**："Clinical data is needed to support [new indication / new patient population / new risk profile]."
- **根因**：差异触及了 predicate 未覆盖的临床问题。
- **对策**：预期用途/人群任何实质变化 → 提前评估是否需要 De Novo 或临床数据；境外临床 → GCP + 赫尔辛基 + 认证翻译。
- **自检问题**：这个差异，predicate 审评时遇到过吗？

### 退回 11：Predicate 选择问题
- **典型表现**："The chosen predicate is not appropriate because..." / 列举多 predicate 未指定 primary。
- **根因**：主对比器械模糊；predicate 已 withdrawn。
- **对策**：唯一 Primary Predicate + 选择理由（同 product code、近期获批、IFU 接近）；secondary predicate 只能用于技术特征补充对比。
- **自检问题**：Predicate 的 K 号在 FDA 数据库里查得到且当前有效吗？

### 退回 12：测试实验室资质 / 报告形式问题
- **典型表现**："Test reports do not include [signature / date / method reference]."
- **根因**：报告无签字、无方法引用、非英文无认证翻译。
- **对策**：ISO/IEC 17025 认可实验室（ILAC-MRA）；报告完整版（含原始数据附录）；签名日期齐全。
- **自检问题**：报告是「完整版」还是「摘要版」？NB/FDA 只认完整版。

---

## 3. 性能测试标准映射表（FDA 认可共识标准清单 #66 口径）

| 测试类别 | 适用产品 | 主标准 | 关键注意 |
|---------|---------|--------|---------|
| 生物学评价 | 接触人体器械 | ISO 10993-1:2025（认可号 2-313）+ 终点系列（-5/-10/-23 等） | 新版已获承认；引用前查认可清单 |
| 电气安全 | 有源器械 | IEC 60601-1（+ 专用 Part 2） | 基本性能定义 + 单故障 |
| 电磁兼容 | 有源/含无线 | IEC 60601-1-2 | 全工作模式 + 无线共存 |
| 软件生命周期 | 含软件器械 | IEC 62304 | 文档层级声明 + V&V 完整报告 |
| 可用性/人因 | 全部（2026-08-01 起） | IEC 62366-1 | 三层分类提交 |
| 网络安全 | cyber device（含 USB/蓝牙） | Section 524B 指南（现行版 2026-02-03） | SBOM + VMP + 30/60 天 SLA |
| 环氧乙烷灭菌 | 无菌器械 | ISO 11135 + ISO 10993-7（残留） | EO/ECH 残留达标 |
| 辐照灭菌 | 无菌器械 | ISO 11137 | 剂量审核/确认 |
| 湿热灭菌 | 无菌器械 | ISO 17665 | — |
| 无菌包装 | 无菌器械 | ISO 11607-1/-2 | 密封完整性 + 老化 |
| 加速老化 | 无菌/有效期 | ASTM F1980 | 必须同步启动实时老化 |
| 激光安全 | 激光器械 | IEC 60601-2-22 | 按产品专用 Part 2 |
| 体外诊断 | IVD | CLSI EP 系列 + 产品专用 | FDA IVD 认可标准单独查 |

> ⚠️ **标准版本纪律**：「标准出了新版」≠「FDA 已承认新版」。申报前逐个查 FDA Recognized Consensus Standards 数据库当前认可号与版本。已知：**ISO 10993-1:2025 已获承认**；ASTM F2100-26、ISO 10993-7:2026 未获承认。

---

## 4. AI 请求响应黄金法则

1. **逐条回应**：复制审评员原文 → 我们的回应 → eSTAR 附件名+页码（三列对照表）。
2. **页码级引用**：审评员不想「再找一遍」。
3. **180 天内回复**（MDUFA 时钟暂停）；行政缺失 1 天补齐，技术缺陷预留检测时间。
4. **不引入新变更**：回复时改设计/改标签 = 新审评周期。
5. **模拟预审**：提交前由未参与撰写的 RA 工程师按本库模拟一轮。

---

*依据：FD&C Act §513(i)；21 CFR 807；FDA Guidance "The 510(k) Program: Evaluating Substantial Equivalence"（2014）；FDA RTA Policy for 510(k)s；Section 524B 网络安全指南（现行版 2026-02-03）；FDA 认可共识标准清单 #66（2026-08-24）。退回原因为行业经验归纳，非 FDA 官方统计。*
