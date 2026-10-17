---
name: pms-vigilance-minder
description: Post-Market Surveillance (PMS) and Vigilance system designer for
  medical devices. Generates PMS Plan, PSUR (Annex III audit-grade structure),
  vigilance reporting timelines (EU
  MDR Article 87, FDA 21 CFR 803 with 5/10/30-day decision tree, China NMPA, Japan PMDA), global incident
  reporting workflows, FSCA/FSN templates, CAPA triggering logic, and
  cybersecurity post-market vulnerability management (FDA Section 524B + EU MDR
  Annex I §17.4 IT 安全——§17.2 为软件生命周期，勿混). Also covers EU AI Act
  2024/1689 post-market monitoring for high-risk AI medical devices（Digital
  Omnibus (EU) 2026/1744 修订时间线：嵌入器械高风险义务 2028-08-02、第 50 条透明度
  2026-08-02 已适用）, EUDAMED vigilance module rollout（遗留器械 2026-11-28 截止）, and
  AAMI SW96/TIR97 referenced cyber risk practices. Built to the audit-grade
  deliverable standard（提交前验收门，目标零整改）。
agent_created: true
author: 北京奥斯曼认证咨询
version: 1.2.1
display_name: "上市后监管与警戒系统规划器"
display_name_en: "PMS & Vigilance Minder"
description_zh: "设计 PMS 计划、PSUR、多国警戒报告时间线、FSCA/FSN 模板、CAPA 触发逻辑与网络安全漏洞管理，覆盖 EU AI Act 上市后监控"
description_en: "Design PMS plans, PSURs, multi-market vigilance timelines, FSCA/FSN templates, CAPA triggers and cyber vulnerability management, including EU AI Act post-market monitoring."
---

# 上市后监管与警戒系统规划器（PMS & Vigilance Minder）v1.2

> 🆕 **v1.2.1 升级**（2026-10-16 官方核实修正）：**NMPA 报告时限全线勘误**（gov.cn / NMPA / SAMR 三源核实）——原表"严重事件 15 个工作日 / 死亡 24h 内"无法规依据，现按总局令第 1 号第二十五条改为**死亡 7 日内、严重伤害/可能严重伤害/可能死亡 20 日内**；群体事件 12h 电话 + 24h 个例系统报告；境外事件 30 日；评价结果死亡 30 日/严重伤害 45 日；FSCA 对应《医疗器械召回管理办法》**一级 1 日/二级 3 日/三级 7 日**通知到位 + 立即报事件报告表 + 5 个工作日交评估报告。同步修正流程图与 `references/vigilance-timeline-matrix.md`。
>
> 🆕 **v1.2 升级**（2026-10-16 审核级专项）：① PSUR 升级为 **Annex III 全结构（A–G 七节）**审核级指南——含暴露量分母、reportability 判定记录、趋势图、CAPA 有效性验证、收益-风险结论等 NB 审核视角要点；② 新增 FDA MDR 报告决策树（5/10/30 天三档判定 + 起算点规则）；③ 内置提交前验收门（与全技能族 audit-grade-deliverable-standards 对齐），目标 **PSUR/警戒记录零整改**。
>
> 🆕 **v1.1 升级**（2026-10-16）：① 补充版本元数据（与线上发布对齐，v1.0.0→v1.1.0）；② 修订网络安全条款引用：EU MDR Annex I **§17.4 = IT 安全**（§17.2 为软件生命周期，业界常误标）；③ EU AI Act 严重事故报告改为**三档时限（2/10/15 天）**并同步 Digital Omnibus (EU) 2026/1744 延期口径；④ 增补 EUDAMED 遗留器械 2026-11-28 截止与 VPMS 模块状态；⑤ 补齐 references/ 三个配套文件（此前清单列名但文件缺失）。

## 目的

帮助医疗器械制造商在**产品上市后**建立完善的**上市后监管（PMS）系统**和**警戒（Vigilance）系统**，确保符合：
- **欧盟 MDR (EU) 2017/745 Article 83-87**（PMS + PSUR + Vigilance + EUDAMED）
- **美国 FDA 21 CFR Part 803**（MDR + 5-day Correction Reporting）
- **中国 NMPA《医疗器械不良事件监测和再评价管理办法》**（总局令第 1 号，2019-01-01 施行）
- **日本 PMDA JFMDA** + **英国 MHRA MORE** + **加拿大 HC MPR** + **澳大利亚 TGA IRIS** + **巴西 ANVISA**

**核心能力**：
1. **PMS Plan 框架**（数据源 + 频次 + 责任人 + 触发 CAPA 条件）
2. **PSUR 模板**（Class IIa 起每年更新）
3. **Vigilance 报告时间线**（EU 10/15 天、FDA 10/30 天、China 7/15 天）
4. **FSCA + FSN 模板与流程**
5. **CAPA 8 触发源监控**（与 ISO 13485 §8.3 整合）
6. **🆕 EU EUDAMED 强制报告**（2026-05-28 起）
7. **🆕 网络安全上市后管理**（Vulnerability Management Plan + CVD）
8. **🆕 EU AI Act 上市后监控**（高风险 AI 系统持续监控义务）

## 使用方式

### 步骤 1：确认产品基线

需要收集以下信息：
- 产品名称 + 分类（Class I/IIa/IIb/III，参见 med-device-classifier skill）
- **已上市市场**（哪些国家已上市） + **新进入市场**（待进入国家）
- 现有 QMS 体系状态（是否已建立 ISO 13485）
- 现有投诉/反馈/事件收集渠道
- 是否含 AI/ML/网络连接（触发额外监控义务）

### 步骤 2：生成 PMS Plan 框架

#### 2.1 PMS 数据源设计

医疗器械上市后数据来源**至少 8 类**：

| # | 数据源 | 收集方式 | 频次 |
|---|--------|---------|------|
| 1 | **投诉**（Complaints） | CRM 系统 + 客户邮件 + 客户电话 | 实时 |
| 2 | **不良事件**（Adverse Events） | 客户/医院直接报告 + 主管当局反馈 | 实时 |
| 3 | **召回/FSCA** | 内部质量系统 + 主管当局公告 | 事件驱动 |
| 4 | **文献监测** | PubMed、Embase、行业期刊、NMPA 不良事件通讯 | 月度 |
| 5 | **用户反馈** | 用户调查 + 现场拜访 | 季度 |
| 6 | **临床登记**（Registry） | 患者登记系统 | 持续 |
| 7 | **社交媒体监测** | 行业论坛、患者社区、新闻 | 季度 |
| 8 | **🆕 上市后临床随访（PMCF）** | EU MDR 强制的上市后数据收集 | 持续 |

#### 2.2 评估指标与触发 CAPA 的条件

**建议监控的 12 项指标**：
- 投诉率（每月/每 1000 件）
- 不良事件率（每月/每 1000 件）
- 严重事件比例
- 召回率
- FSCA 次数
- 用户反馈 NPS 分数
- **🆕 网络安全漏洞数（按 CVSS 等级）**
- **🆕 AI 算法性能衰减（AUC 下降、敏感度下降）**
- **🆕 数据漂移指数（PSI/KL 散度）**
- 上市后不良事件趋势（同比、环比）
- 上市后投诉趋势
- 监管公告/法规更新

**CAPA 触发条件**：
- 投诉率/不良事件率超出历史基线 1.5σ
- 严重事件重复出现（≥2 起同类）
- 主管当局/法院提出关切
- **🆕 Critical 漏洞未在 30 天内修复**
- **🆕 AI 算法 AUC 下降 ≥ 0.05**

#### 2.3 责任人矩阵

| 角色 | 责任 |
|------|------|
| **PRRC（Person Responsible for Regulatory Compliance）** | EU 法规 + EUDAMED 上报 |
| **Complaint Handler** | 投诉接收 + 分类 |
| **Vigilance Officer** | 警戒事件评估 + 报告 |
| **Quality Manager** | CAPA 启动 + 跟进 |
| **Clinical/Medical Affairs** | 临床事件评估 |
| **🆕 Cybersecurity Officer** | 网络安全事件响应 + CVD |
| **🆕 AI/ML Performance Monitor** | 算法性能监控 |
| **Post-market Surveillance Lead** | PMS 总体协调 |

#### 2.4 输出 PMS Plan 模板

PMS Plan 必须包含的 9 部分：
1. **目的与范围**（Purpose & Scope）
2. **职责分工**（Responsibilities）
3. **数据收集方法**（Data Collection Methods）
4. **数据分析与评估**（Data Analysis & Evaluation）
5. **指标与触发**（Metrics & Triggers）
6. **CAPA 衔接**（CAPA Interface）
7. **报告与文档**（Reporting & Documentation）
8. **🆕 网络安全与 AI 监控**（Cyber & AI Monitoring）
9. **审核与更新**（Review & Update，至少每年一次）

### 步骤 3：生成 PSUR 模板（Class IIa+ 必须）

#### 3.1 PSUR vs PMSR 适用范围

| 器械 | 文件 | 频次 | 提交 |
|------|------|------|------|
| **Class I** | PMSR (PMS Report) | 必要时 | 留存备查 |
| **Class IIa** | PSUR | 至少每 2 年 | 通知 NB |
| **Class IIb（非植入/非生命维持）** | PSUR | 至少每年 | 提交 NB |
| **Class IIb（植入/生命维持）** | PSUR | 至少每年 | 提交 NB |
| **Class III** | PSUR | 至少每年 | 提交 NB |
| **🆕 EU AI Act 高风险 AI** | 上市后监控报告 | 持续 + 重大事件 | 公告机构 + 市场监督 |

#### 3.2 PSUR 标准结构（Annex III A–G 七节，审核级）

**完整撰写指南（含每节必备内容与 NB 高频问题）见 `references/psur-annex3-audit-structure.md`**。结构速览：

| 节 | 内容 | NB 审核视角 |
|----|------|-----------|
| **A** | 器械与报告期标识（名称/型号/BUDI-DI/分类/NB 证书号 + EUDAMED 一致性核对） | 与 EUDAMED 不一致 = 退回 |
| **B** | 销售量与暴露人群估算（**分母**） | 没有分母的绝对数无意义 |
| **C** | 严重事件与投诉摘要（按类型×严重度分布 + 每起的 reportability 判定记录） | 「没报」的事件也要有判定理由 |
| **D** | 趋势分析与信号检测（投诉率/事件率历史趋势 + 阈值比对） | 只放总数不放趋势 = 退回 |
| **E** | CAPA 与 FSCA 摘要（CAPA 有效性验证 + FSN 回复率） | CAPA 未验证有效性 = 体系缺陷 |
| **F** | 临床数据与 PMCF 更新 | PMCF 须挂回 CER 缺口 |
| **G** | 结论与改进措施（收益-风险结论显式 + PRRC/管理层签字） | 结论含糊 = 退回 |

**⚠️ Class I 没有 PSUR**——按 Article 85 编制 PMSR，留存备查、不主动提交。

### 步骤 4：Vigilance 报告时间线与决策树

#### 4.1 各国报告时间线对照表

**FDA 三档报告（5/10/30 天）判定决策树见 `references/fda-mdr-decision-tree.md`**——含 reportable 判定流程、报告内容必备清单与 483 高频错误。

| 事件类型 | EU MDR (Article 87) | FDA 21 CFR 803 | NMPA（总局令第1号） | PMDA | HC | TGA |
|---------|---------------------|----------------|------------------|------|-----|-----|
| **严重事件（非死亡）** | 15 天 | 30 天（30-day） | **20 日**（严重伤害/可能严重伤害/可能死亡） | 15 天 | 30 天 | 30 天 |
| **死亡** | 10 天 | 10 天（10-day） | **7 日** | 10 天 | 10 天 | 10 天 |
| **群体不良事件** | 10 天（EUDAMED）| 10 天 | **12h 电话报告 + 24h 系统按个例报告** | 10 天 | 10 天 | 10 天 |
| **FSCA / 召回通知** | **24h** 通知 NB/当局 | 5 个工作日 | **分级：一级 1 日 / 二级 3 日 / 三级 7 日**通知到位；立即报召回事件报告表 + **5 个工作日**交调查评估报告和召回计划 | 24h | 24h | 24h |
| **FSN 致用户** | 24h 内分发 | 5 个工作日 | 随召回分级通知同步执行 | 24h | 24h | 24h |
| **Trend Report** | 显著增加即报 | CFR 803.53 | 显著增加即报 | 显著增加 | 趋势 | 趋势 |
| **PSUR** | IIa 2 年、IIb/III 1 年 | 年度（部分） | 年度 | 年度 | 年度 | 年度 |
| **🆕 漏洞披露（CVD）** | 90 天 | 90 天 | 暂无明文 | 90 天 | 90 天 | 90 天 |

**⚠️ NMPA 口径依据**（《医疗器械不良事件监测和再评价管理办法》，总局令第 1 号，2019-01-01 施行，非"2022 修订"）：持有人发现可疑不良事件**应立即调查原因**，导致死亡 **7 日内**报告，导致严重伤害、可能导致严重伤害或死亡 **20 日内**报告（第二十五条）；群体事件 **12 小时内**电话报告 + 每起 **24 小时内**按个例报告（第三十一条）；境外发生的死亡/可能死亡事件 **30 日内**报告（第二十七条）；死亡事件 **30 日内**、严重伤害事件 **45 日内**向省级监测机构报告评价结果（办法个例报告章节口径）。召回时限另按《医疗器械召回管理办法》（2017-05-01 施行）第十五/十六条执行。

**⚠️ 起算点：事件首次获知时间**（不是事件发生时间；任何员工获知即启动计时）

#### 4.2 严重事件判定流程图

```
不良事件收到
    │
    ▼
是否：死亡？ ─── 是 ─→ 10 天内报告（EU） / 7 日内报告（NMPA）
    │
    ▼ 否
是否：严重伤害（住院/延长住院/永久/显著伤残）？
    │
    ▼ 是
是否：可预期？（在 IFU/标签中已充分告知）
    │
    ▼ 否（不可预期）
10 天内报告（EU） / 20 日内报告（NMPA）
    │
    ▼ 是（可预期）
记录在 PSUR 中 + 监控趋势
    │
    ▼
是否：事件重复发生？（同型号/同问题 ≥2 次）
    │
    ▼ 是
触发 Trend Report + 风险文件更新
```

### 步骤 5：FSCA + FSN 模板

#### 5.1 FSCA 决策树

```
潜在风险
    │
    ▼
是否：可能影响多个用户/多台器械？
    │
    ▼ 是
是否：可能需要用户采取行动（召回/修改/告警/使用限制）？
    │
    ▼ 是
启动 FSCA 流程
    │
    ├─→ 24h 内通知 NB/当局（EU）
    ├─→ 召回分级通知到位（NMPA：一级 1 日 / 二级 3 日 / 三级 7 日；立即报召回事件报告表，5 个工作日交调查评估报告和召回计划——《医疗器械召回管理办法》第十五/十六条）
    ├─→ 5 工作日内通知 FDA
    ├─→ 同步发布 FSN 给受影响用户
    └─→ 跟踪回复率（目标 >95%）
```

#### 5.2 FSN（Field Safety Notice）核心要素
1. **致用户开头**（称呼 + 紧急程度）
2. **器械信息**（型号/序列号/LOT 范围）
3. **问题描述**（什么问题、风险等级、影响）
4. **用户应采取的行动**（具体步骤）
5. **本 FSN 是否影响使用**（继续使用/立即停止/有限使用）
6. **联系方式**（24h 电话 + 邮箱）
7. **签字**（PRRC + QA Director）

### 步骤 6：CAPA 8 触发源监控（与 ISO 13485 §8.3 整合）

```
触发源 1: 投诉
触发源 2: 不合格品
触发源 3: 内审不符合项
触发源 4: 外审不符合项
触发源 5: 管理评审输出
触发源 6: 数据分析异常（投诉率/不良事件率偏离基线）
触发源 7: PMS/PSUR 趋势分析
触发源 8: 文献/法规更新/同行事件（信号检测）
```

**新增触发源 9-10（2024-2026）**：
```
触发源 9:  网络安全漏洞（CVSS ≥ 7.0 即触发评估）
触发源 10: AI 算法性能下降（任一指标下降 ≥ 5%）
```

### 步骤 7：🆕 EU EUDAMED 强制报告（2026-05-28 起）

#### 7.1 EUDAMED 警戒模块功能
- 制造商注册（SRN）
- 器械注册（UDI-DI + UDI-PI）
- 公告机构证书（NB 上传）
- 市场监督（主管当局上传）
- **🆕 警戒事件提交**（严重事件、FSCA、Trend Report）
- **🆕 安全相关字段报告**（Field Safety Notice）

#### 7.2 EUDAMED 报告时间线
- 严重事件：**事件获知起 15 天内**（与 EU MDR 一致）
- FSCA 计划：**24h 内**通知主管当局（与 EU MDR 一致）
- 完整警戒报告：与 EU MDR 第 87 条一致
- **遗留器械 UDI/器械注册补录截止 2026-11-28**（自 2026-05-28 起 6 个月宽限）——未注册器械不得合法投放，PMS 数据链断档
- **警戒与上市后监督（VPMS）模块**：📅 开发中（可能 2027 强制）；就绪前警戒报告按 MDR Article 87 时限向主管当局提交

#### 7.3 EUDAMED 注册步骤
1. 经济运营商在 EUDAMED 注册 → 获取 SRN
2. 制造商注册器械（UDI-DI）
3. NB 上传证书
4. PRRC 提交警戒事件
5. 主管当局审核 + 反馈

### 步骤 8：🆕 网络安全上市后管理（Vulnerability Management Plan）

#### 8.1 漏洞响应 SLA

| CVSS 等级 | 风险等级 | 响应时间 | 修复时间 |
|----------|---------|---------|---------|
| **9.0-10.0 Critical** | 🔴 立即响应 | 24h 内评估 | **30 天内** |
| **7.0-8.9 High** | 🟠 紧迫 | 7 天内评估 | **60 天内** |
| **4.0-6.9 Medium** | 🟡 重要 | 30 天内评估 | 90 天内 |
| **0.1-3.9 Low** | 🟢 监控 | 60 天内评估 | 180 天内 |

#### 8.2 漏洞响应流程

```
NVD/CISA/内部测试发现漏洞
    │
    ▼
1. Triage（24h 内）：评分（CVSS）+ 评估适用范围
    │
    ▼
2. 影响评估（7 天内）：哪些型号/版本受影响？风险等级？
    │
    ▼
3. 修复开发：补丁/更新/配置变更
    │
    ▼
4. 内部测试 + 验证
    │
    ▼
5. 安全更新发布（按 SLA 截止）
    │
    ▼
6. 客户通知 + 部署协助
    │
    ▼
7. CVD 公开披露（90 天内）
    │
    ▼
8. 关闭漏洞 + CAPA 记录
```

#### 8.3 CVD（Coordinated Vulnerability Disclosure）模板
- 漏洞描述（不暴露具体攻击代码）
- 受影响产品和版本
- CVSS 评分
- 缓解措施
- 致谢（白帽/研究人员）
- 时间线
- 联系方式

### 步骤 9：🆕 EU AI Act 上市后监控（高风险 AI 医疗系统）

#### 9.1 适用条件
- **Class IIa 及以上** 含有 AI/ML 算法的医疗器械
- 在 EU AI Act 框架下多归"高风险 AI"（Annex I Section A——医疗器械未被移出）
- 与 MDR PMS 整合（不重复建系统）

> ⏳ **Digital Omnibus (EU) 2026/1744（2026-07-27 生效）**：嵌入器械的高风险义务适用日推迟至 **2028-08-02**（原 2027-08-02），Annex III 独立系统 2027-12-02；第 50 条透明度义务已自 **2026-08-02** 适用（未延期）。上市后监控义务内容不变——多出的一年用于建设监控体系，不是放松理由。

#### 9.2 持续监控义务
- 算法性能监控（与 PCCP 衔接）
- 数据漂移检测
- 偏差（Bias）检测
- 鲁棒性监控
- 关键 KPI：敏感度、特异度、AUC、Calibration、Demographic Parity

#### 9.3 重大事件报告（AI Act Article 73 三档时限）

| 情形 | 时限 |
|------|------|
| 导致死亡或健康严重损害 | **2 天内** |
| 基本权利受到广泛侵害 | **10 天内** |
| 其他严重事故 | **15 天内** |

- 与 MDR 警戒报告同步提交（同一 NB + 市场监督机构）
- 涉及生命安全或基本权利的事件，不可因 Digital Omnibus 延期而推迟报告体系准备

#### 9.4 持续学习（Continuous Learning）管理
- 再训练触发器定义（性能下降阈值）
- 影子部署（Shadow Mode）
- A/B 测试
- 重新评估（Re-certification）触发条件

## 输出标准

- PMS Plan 引用 MDR Article 84 + 85 + MDCG 2020-7
- **PSUR 按 Annex III A–G 七节结构撰写**（含暴露量分母与 reportability 判定记录）
- 报告时间线以**自然日**为标准（与法规保持一致）
- 模板覆盖 EU/FDA/NMPA/PMDA/HC/TGA 至少 6 个主要市场
- 警戒事件决策树清晰可执行
- CAPA 触发源至少 10 个（含新增 9/10）
- 网络安全 SLA 量化（CVSS + 响应时间）
- AI 算法监控指标量化
- **🆕 交付前跑 PSUR 12 问 + 验收门评分 ≥90 且零致命项**
- 输出语言与用户需求一致

## 约束

- 不替代 PRRC（Person Responsible for Regulatory Compliance）法定职责
- 严重事件是否构成"严重"最终以监管机构判定为准
- 警戒时间起算以"事件首次获知时间"为准，不是事件发生时间
- 网络安全事件涉及机密信息时，须与法务/律师协调披露内容
- 不替代临床/医学专家对医学事件的判断
- AI 算法阈值由制造商确定，但需有科学依据并在 PCCP 中说明
- **🆕 AI Act 截止日引用 Digital Omnibus 修订后口径（嵌入器械 2028-08-02；第 50 条 2026-08-02 已适用），旧 2027-08-02 与 2026-08-02（嵌入器械）口径已失效**
- **🆕 NMPA 不良事件报告时限以《医疗器械不良事件监测和再评价管理办法》最新版为准（本表时限需在客户项目中按现行法规复核后使用）**

## 参考资料

- `references/vigilance-timeline-matrix.md`：各市场警戒报告时间线对照表
- `references/psur-annex3-audit-structure.md`：**PSUR Annex III A–G 七节审核级撰写指南**（NB 高频问题 + PSUR 12 问）
- `references/fda-mdr-decision-tree.md`：**FDA MDR 报告决策树**（5/10/30 天判定 + 内容必备 + 483 高频错误）
- `references/eudamed-registration-guide.md`：EUDAMED 注册步骤详解
- `references/vulnerability-management-playbook.md`：网络安全漏洞响应 Playbook
- `references/audit-grade-deliverable-standards.md`：审核级交付标准总纲（成熟度四级/五性/验收门评分卡/致命项）
- 基于《合规之战：全球医疗器械监管进化史》第十五章（PMS 专题）
