# 2026 FDA 510(k) 自学补强（分类与 FDA 补完小队 · 2026-08-16）

> 本文为 `fda-510k-pathway` 技能的事实补强件，聚焦 FDA 510(k) 在 2025–2026 的最新动态、前队友因「网络安全指南日期冲突」停顿的核准结论，以及 HFE / PCCP / eSTAR / predicate 等实践更新。所有日期附官方或权威信源；无法 100% 确认的标注「待核实」。

---

## 一、FDA 网络安全指南核准（核心冲突已解决）

**前队友停顿的根因**：技能内写「FDA Final Guidance 2025-06-27（取代 2023-09 版本）」，但漏掉了 **2026-02 的 QMSR 对齐修订版**。经联网核准，该指南实为**三版迭代**：

| 版本 | 发布日期 | 关键变化 | 现行性 |
|------|---------|---------|--------|
| 第 1 版（终版） | **2023-09-27** | 取代 2014 版，首次将 Section 524B 要求变为可执行（RTA 自 2023-10-01 起） | 已被取代 |
| 第 2 版（更新） | **2025-06-27** | 含 QMSR 落地前选择性更新 | 已被取代 |
| 第 3 版（现行） | **2026-02（FDA 页标 "February 2026"；第三方解读指 2026-02-03，具体日待核实）** | 标题 *Quality System Considerations* → *Quality Management System Considerations*，将 QSR 820 引用替换为 QMSR / ISO 13485:2016 条款；**524B 网络安全实质要求不变** | **现行有效** |

**对 510(k) 的影响**：联网/含软件器械的 Section 524B 七部分（威胁建模/SBOM/VMP/CVD/安全风险管理/安全测试/更新与生命周期）要求不变，但质量体系框架已转 QMSR；提交文件中网络安全论证须体现「由 QMSR/ISO 13485 受控流程生成」。技能步骤 6 引用的「2025-06-27」应改为「现行以 **2026-02 QMSR 对齐版**为准（前身 2025-06-27、2023-09-27）」。

**信源**：
- FDA 现行指南页（注明取代 2025-06-27 版）：https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-networked-medical-devices-containing-shelf-ots-software
- 联邦公报 2023-09-27（FR Doc. 2023-20955）：https://www.federalregister.gov/documents/2023/09/27/2023-20955/cybersecurity-in-medical-devices-quality-system-considerations-and-content-of-premarket-submissions
- 逐版梳理（2026-02 QMSR 对齐说明）：https://meddeviceguide.com/blog/medical-device-cybersecurity-guide

---

## 二、HFE 终版实为两份文件（技能混淆「发布日/生效日」）

**核准**：HFE 提交要求来自**两份不同指南**，技能此前将「2026-05-29」误标为「生效日」且未提 2026-08-03 的基础方法指南更新：

| 文件 | 发布/生效 | 作用 |
|------|----------|------|
| **A. *Content of Human Factors Information in Medical Device Marketing Submissions*** | 联邦公报 **2026-05-29 发布**（91 FR 2026-10734）；**2026-08-01 起** FDA 要求在此日及之后收到的申请遵循（即生效/过渡截止） | 确立 3 类提交分级（Category 1/2/3）+ Decision Point D 自判框架 |
| **B. *Applying Human Factors and Usability Engineering to Medical Devices*** | **2026-08-03 终版**（2016 后首次修订） | 基础 HFE 方法指南；术语对齐 QMSR/ISO 14971:2019/IEC 62366-1，删除旧 Appendix A、改指引至文件 A |

- **修正要点**：技能「步骤 8」标题「2026年5月29日生效」应改为「**2026-05-29 发布、2026-08-01 起生效**」；并在参考中补入文件 B 的 2026-08-03 更新（影响 HFE/UE 报告术语与结构，Appendix A 已移除）。
- 关键不变项：≥15 名代表性用户验证、关键任务（critical tasks）识别、URRA 为核心。

**信源**：
- 文件 A（Federal Register 91 FR 2026-10734，2026-05-29 发布、2026-08-01 生效）：https://meddeviceguide.com/blog/fda-human-factors-final-guidance-2026-submission-categories-decision-point-d
- 文件 B（Applying HF and UE，2026-08-03 终版）：https://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocuments/UCM259760 ；解读 https://www.emergobyul.com/news/fda-updates-landmark-human-factors-guidance-medical-devices

---

## 三、QMSR 对 510(k) 的影响（补强，非推翻）

- QMSR 2026-02-02 生效，21 CFR 820 以引用纳入 ISO 13485:2016；**QSIT 废止，改用 Compliance Program 7382.850**（六大领域数据流追踪）。
- §820.180(c) 保密豁免取消：管理评审/内审/供应商审核记录 FDA 可查。
- ⚠️ **无过渡期**：QMSR 自 2026-02-02 **生效即执法、无宽限期**；FDA 未发布任何过渡期执法裁量文件。现有 QSR 持有者须**立即**转换（原写"现有 QSR 持有者 3 年过渡（2029-02-02 截止）"系错误，2026-08-29 更正）。ISO 13485 证书 ≠ QMSR 合规。
- **eSTAR 版本**：现行 **nIVD / IVD eSTAR 7.0**（2026-06-01 发布）；**v6.2 及更早（含 v6.1）+ PreSTAR v2.2 已于 2026-08-03 退役**。
  > 原写"2026-02 更新至 v6.1（QMSR 对齐）"——v6.1 确曾存在但**已退役**；另「eSTAR 7.0 内置 QMSR 术语字段」一说**未经 FDA 官方页证实，保持"待核实"**。
- ⚠️ **RWE 指南日期存疑**：原文称"自 2026-02-17 纳入 RWE 指南（2026-02-16 生效）"。但 FDA 官方指南列表显示《Use of Real-World Evidence to Support Regulatory Decision-Making for Medical Devices》为 **2025 年 12 月**发布。**此条引用前须核实。**

**信源**：FDA QMSR FAQ：https://www.fda.gov/medical-devices/quality-management-system-regulation-qmsr/quality-management-system-regulation-frequently-asked-questions

---

## 四、PCCP 终版实践（日期核准）

- **AI 赋能器械 PCCP 终版指南**：FDA 于 **2024-12-03/04 发布**（多家律所 Ropes & Gray / JD Supra / McDermott 确认）；FDA 指南下载页标注「August 2025」，**具体 FDA 张贴日待核实**，但内容为 2024-12 终版。
- 三大模块（Description of Modifications / Modification Protocol / Impact Assessment）维持；范围扩至**全部 AI-enabled 器械**（非仅 ML）；PCCP **仅可通过 Traditional / Abbreviated 510(k) 授权**，不可走 Special 510(k)；组合产品（device-led）可含 PCCP。
- 团队速览「标注 2025-08」疑为与 2024-08 通用 PCCP 草案混淆，**技能保留 2024-12-04 更准**。

**信源**：
- FDA 指南页：https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence
- 终版发布解读（2024-12-04）：https://production.jdsupra.com/legalnews/fda-finalizes-guidance-on-predetermined-2107972/

---

## 五、eSTAR 强制进展（核准）

- **510(k) 强制 eSTAR**：自 **2023-10-01** 起（Section 745A(b)）。
- **De Novo 强制 eSTAR**：自 **2025-10-01** 起。
- 现行模板：**nIVD eSTAR 7.0 / IVD eSTAR 7.0 / PreSTAR 3.0**（**2026-06-01 发布**）。
- ⚠️ **退役节点**：**v6.2 / PreSTAR v2.2 已于 2026-08-03 退役**，旧版本系统直接拒收。
  〔2026-08-29 复审修正：原写"现行模板 nIVD/IVD eSTAR v6.1（2026-02 更新，QMSR 对齐）；PreSTAR v2"——v6.1 与 PreSTAR v2 **均已退役**。另「eSTAR 7.0 内置 QMSR 术语字段」未经 FDA 官方页证实，保持待核实；已确认内置的是 **HF 提交类别选择字段**（HFE 指南相关）〕
- 模板来源：只从 FDA eSTAR 官方页下载，禁用第三方缓存版（缺板块会被退）。
- 提示：PMA 仍非强制 eSTAR（须 eCopy）；FDA 拟将 eSTAR 扩至 Q-Sub。

**信源**：FDA CDRH Portal：https://www.fda.gov/medical-devices/industry-medical-devices/progress-tracker-premarket-submissions ；eSTAR 指南：https://meddeviceguide.com/blog/fda-estar-electronic-submission-template-guide

---

## 六、Predicate 现代化与实质等同最新实践

- FDA 已**淘汰 1,750+ 个过时 predicate**，鼓励使用近 5 年内获批 predicate（技能步骤 3 已提「优先近 5 年」一致）。
- 实质等同论证维持 12 列对比表（含差异论证列，技能 v2.1 已补回）；差异不影响安全有效性 → SE 成立。
- predicate 查找工具维持：510(k) Database / Product Classification DB / De Novo Summary DB / AI-ML Enabled Devices List。

---

## 七、待核实清单

1. FDA 网络安全指南第 3 版具体发布日（"February 2026" vs 2026-02-03）。
2. PCCP 终版 FDA 下载页为何标 "August 2025"（与 2024-12 发布存在元数据差异，待核实）。
3. HFE 文件 A 的联邦公报原文链接与文件 B 是否已在 FDA 官网更新（本文引第三方解读，建议核对 FDA 原页）。
