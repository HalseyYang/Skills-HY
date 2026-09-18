# 2026 团队自学笔记：FDA 人因工程 / 可用性工程（HFE/UE）最新动态

> 学习日期：2026-08-16
> 来源：FDA 官网、IEC 官网、EU 委员会文件及权威合规解读（均为 2025–2026 公开来源）
> 用途：附着到 osman-device-regulatory 的 hfe-human-factors 技能，补充其 SKILL.md 的 2026 框架
> 说明：关键术语保留英文；所有日期均来自官方/权威来源，不编造

---

## 一、2026 年 FDA 人因两大指南全景

2026 年 FDA 人因合规发生十年一遇的更新，由**两份互补指南**构成：

| 指南 | 状态 | 发布/生效日期 | 角色 |
|------|------|-------------|------|
| **Applying Human Factors and Usability Engineering to Medical Devices** | 终版（Final） | **2026-08-03** 发布（原 2016-02-03 版首次修订） | 规定 HFE/UE "怎么做"（流程与期望） |
| **Content of Human Factors Information in Medical Device Marketing Submissions** | 终版（Final） | **2026-05-29** 发布（替代 2022-12 草案）；**2026-08-01** 起对收到的申报生效 | 规定上市申报 "交什么"（三层提交分类） |

- 前者是 HFE/UE 流程的"母指南"，后者是申报资料内容的"伴侣指南"，**二者互补而非替代**。
- 信源：
  - Applying HFE 终版：https://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocuments/UCM259760
  - FDA 指南发布清单（含两项 HFE 指南的 Issue Date）：https://www.fda.gov/guidance-documents-medical-devices-and-radiation-emitting-products

---

## 二、Applying HFE 终版（2026-08-03）核心变化

> 来源：https://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocuments/UCM259760 ；EMERGO 解读 https://www.emergobyul.com/news/fda-updates-landmark-human-factors-guidance-medical-devices

1. **术语现代化对齐国际标准**
   - 扩展定义：harm（危害）、normal use（正常使用）、residual risk（残余风险）、serious harm（严重伤害）、serious injury（重伤）、use-related risk analysis（URRA，使用相关风险分析）。
   - 将旧词 "risk management measures" 统一改为 **"risk control measures（风险控制措施）"**，与 ISO 14971 术语一致。
   - 整体与 FDA **QMSR**、**ISO 13485:2016**、**ISO 14971:2019**、**IEC 62366-1** 全面对齐。

2. **删除原 Appendix A（样本人因/可用性工程报告模板）**
   - 原附录 A 的样本报告结构被删除；新版 **Section 9（Documentation）** 改为直接指引到伴侣指南《Content of Human Factors Information in Medical Device Marketing Submissions》，作为申报人因资料的主要依据。

3. **核心期望不变（划重点）**
   - 仍以识别 **critical tasks（关键任务）**、通过设计降低使用风险、开展稳健的 **human factors validation testing（人因验证测试）** 为核心。
   - 仍要求每个独立用户群体（distinct user population）至少 **15 名代表性用户**；研发/内部员工不得作为受试者（专属维修人员除外）。
   - 本次修订本质是"澄清与协调（clarification and harmonization）"，而非政策转向。

---

## 三、Content of HF Information 终版（2026-05-29 / 生效 2026-08-01）

> 来源：Gardner Law https://gardner.law/news/fda-human-factors-medical-device-marketing-submissions ；MedDeviceGuide https://meddeviceguide.com/blog/fda-human-factors-final-guidance-2026-submission-categories-decision-point-d ；Lexology https://www.lexology.com/library/detail.aspx?g=5ed11b13-5ae6-40af-aa49-3900ba8ee6fd

### 1. 三层 HF Submission Categories（风险分级框架）

指南给出**四问决策树（Decision Points A→D）**，按使用相关风险把申报分为三类：

| 类别 | 适用情形 | 最低提交要求 |
|------|---------|------------|
| **Category 1** | 已上市器械的修改，且 UI/用户/用途/使用环境/培训/**标签 labeling** 均无变更 | 高层级摘要 + 结论（说明理由即可，可引用既往 FDA 已审评的人因评估） |
| **Category 2** | 新器械无关键任务；或修改未引入/未影响现有关键任务；**或关键任务存在但能给出充分的"免验证"论证** | 情境化 HFE 摘要 + URRA + 基于证据的论证（rationale） |
| **Category 3** | 新产生或实质影响关键任务，且现有风险控制不足/不再适用 | 完整 HFE/UE 报告 + 覆盖所有关键任务的 summative validation（总结性验证）测试数据 |

### 2. ⭐ Decision Point D（终版新增，最关键变化）

- 这是相对 2022 草案**新增的决策点**：即使器械存在"新关键任务"或"受影响关键任务"，**也不自动进入 Category 3**。
- 制造商可基于以下因素给出充分论证，以 Category 2 方式提交（免做昂贵的人因验证测试）：
  - 用户界面的**安全使用历史（history of use）**
  - **界面复杂性（UI complexity）**
  - **现有风险控制措施的充分性（adequacy of existing risk controls）**
- 实务含义：FDA 想传递的是"策略性风险评估"而非"一刀切强制测试"。

### 3. eSTAR 强制内嵌 + 过渡安排

- **eSTAR v7.0**（非 IVD 与 IVD 模板）自 **2026-08-01** 起内嵌 HFE 模块：申报须声明所属 HF 类别并附支撑资料；旧版 **eSTAR v6.2 于 2026-08-03 停用**。
- **过渡宽限**：FDA 不期望在 2026-08-01 之前已收到/正在审评的申报回溯重做；但此后收到的申报必须按新框架执行。
- FDA 于 **2026-07-22** 举办虚拟 town hall 解读该指南。
- 不准确回答 eSTAR 人因问题可能导致下游问题被跳过、触发最长 180 天技术筛选搁置（technical screening hold）。
- 信源（eSTAR 更新）：https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/electronic-submission-template-resource-estar

---

## 四、IEC 62366-1 可用性工程标准（2025–2026 状态）

> 来源：IEC 官网 https://webstore.iec.ch/publication/67220 ；MedDeviceGuide https://meddeviceguide.com/blog/iec-62366-usability-engineering-guide

- **现行版本：IEC 62366-1:2015 + AMD1:2020（consolidated 合并版）**，Amendment 1 发布于 **2020-06-17**，稳定性日期（stability date）**2028**；IEC 官网合并版编号：IEC 62366-1:2015+AMD1:2020 CSV。
- 配套技术报告 **IEC TR 62366-2:2016**（仅指导性，含方法学，无强制要求）。
- 标准核心流程：Use Specification（使用规范）→ 识别 UI 安全相关特性 → 识别已知/可预见危险与相关使用场景 → **formative evaluation（形成性评估，迭代改进，无通过/不通过判定）** → **summative evaluation（总结性评估，验证性，有预定接受准则）** → 形成 **usability engineering file（可用性工程文件）**。
- 与 **ISO 14971** 紧密耦合：使用相关危险情况作为风险管理的输入；残余使用风险纳入整体残余风险评估。
- **关键差异（美欧）**：IEC 62366-1 **不规定最低受试者人数**；FDA 指南建议每独立用户群体约 **15 人**。EU MDR 亦不规定最低人数。
- 全球认可状态：
  - EU MDR(2017/745) / IVDR(2017/746)：**协调标准 EN IEC 62366-1**，符合即推定符合相关 GSPR（Annex I）。
  - 美国 FDA：**认可共识标准（recognized consensus standard）**，被 HFE 指南引用。
  - Health Canada / MDSAP：认可标准；Japan PMDA、Australia TGA（经 MDSAP）亦引用。

---

## 五、与 EU MDR 可用性要求的交叉（CE 衔接）

> 来源：Kapstone Medical https://www.kapstonemedical.com/resource-center/blog/navigating-fdas-new-human-factors-guidance-vs.-eu-mdr-usability-requirements ；Zechmeister https://zechmeister-solutions.com/en/blog/risk-management-usability-engineering-link ；ChinamedGlobal https://chinamedglobal.com/blog/medical-device-usability-iec-62366-human-factors-guide

- **结构差异**：
  - FDA = 分层、按申报触发的筛选（Category 1/2/3 + Decision Point D）；
  - EU MDR = 把可用性**统一嵌入 Annex I 通用安全与性能要求（GSPR）**，对所有风险等级器械一视同仁，由公告机构（Notified Body）作为技术文件/设计控制审核的一部分永久审核。
- **MDR Annex I 关键可用性条款**：
  - §5（一般要求）：按"固有安全设计 → 防护措施 → 安全信息"三级优先降低风险；
  - §14(1)(2)：考虑用户技术知识/经验/培训/使用环境，使使用错误风险最小化；
  - §22：标签与说明书的可用性要求。
- **协调标准路径**：通过 **EN IEC 62366-1**（含 +A1:2020）实施可用性工程，可推定符合 Annex I 可用性相关 GSPR；技术文件中须将可用性工程文件作为各条款符合性证据。
- **EU 测试哲学**：IEC 62366-1 要求对每个危险相关使用场景进行测试，或可基于严重度论证合理子集——更像"让行标志（yield）"，留给判断空间；FDA 则是明确的红/黄/绿灯分级触发。
- **共性桥梁**：use-related hazardous situation（使用相关危险情况）是连接 EN ISO 14971:2019+A11:2021 与 EN 62366-1:2015+A1:2020 的桥梁；培训/标签是控制层级最低层，不能替代"设计消除"。

---

## 六、对技能判定的补强要点（供 SKILL.md 使用）

1. 申报类别判定四问已对应到 Decision Points A–D，**Decision Point D 为 2026 终版新增**，允许"有关键任务但免验证"的论证路径——这是相对既有 SKILL.md 四步流程的重要补充。
2. eSTAR v7.0 自 2026-08-01 起把 HFE 设为申报必填字段；Category 选择错误可致技术筛选搁置。
3. "Applying HFE" 终版（2026-08-03）删除了原 Appendix A 报告模板，改引用伴侣指南——写报告应以《Content of HF Information》的推荐结构为准。
4. 美欧差异需向用户明确：FDA 有 15 人/组基准与分类触发；MDR 无最低人数但须技术文件永久留存并经 NB 审核。
5. IEC 62366-1 现行合并版为 2015+AMD1:2020，稳定性日期 2028——标准本身暂无新版，技能引用 ":2015+Amd1:2020" 仍然有效。

---

## 官方信源清单（URL）

- FDA Applying HFE 终版（2026-08-03）：https://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocuments/UCM259760
- FDA 指南发布清单（含两项 HFE 指南 Issue Date）：https://www.fda.gov/guidance-documents-medical-devices-and-radiation-emitting-products
- FDA eSTAR 资源：https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/electronic-submission-template-resource-estar
- IEC 62366-1:2015+AMD1:2020 官网：https://webstore.iec.ch/publication/67220
- EU MDR 2017/745（Annex I GSPR）：https://health.ec.europa.eu/medical-devices-regulation-mdr/overview_en
- FDA HFE 终版行业解读（EMERGO）：https://www.emergobyul.com/news/fda-updates-landmark-human-factors-guidance-medical-devices
- FDA Content of HF Information 解读（Gardner Law）：https://gardner.law/news/fda-human-factors-medical-device-marketing-submissions
- FDA/ EU MDR 交叉对比（Kapstone Medical）：https://www.kapstonemedical.com/resource-center/blog/navigating-fdas-new-human-factors-guidance-vs.-eu-mdr-usability-requirements
