---
name: pms-vigilance-minder
description: "Post-Market Surveillance (PMS) and Vigilance system designer for medical devices. Generates PMS Plan, PSUR, vigilance reporting timelines (EU MDR Article 87, FDA 21 CFR 803, China NMPA, Japan PMDA), global incident reporting workflows, FSCA/FSN templates, CAPA triggering logic, and cybersecurity post-market vulnerability management (FDA Section 524B + EU MDR Annex I §17.2). Also covers EU AI Act 2024/1689 post-market monitoring for high-risk AI medical devices."
agent_created: true
author: 北京奥斯曼认证咨询
version: 1.0.0
display_name: "上市后监管与警戒系统规划器"
display_name_en: "Post-Market Surveillance & Vigilance Planner"
description_zh: "生成 PMS 计划、PSUR、警戒报告时限（MDR Art.87 / FDA 803 / NMPA / PMDA）、FSCA/FSN 模板与 CAPA 触发逻辑"
description_en: "Generates PMS plans, PSUR, vigilance reporting timelines (EU MDR Art.87, FDA 21 CFR 803, NMPA, PMDA), FSCA/FSN templates and CAPA triggering logic."
---

# 上市后监管与警戒系统规划器（PMS & Vigilance Minder）

## 目的

帮助医疗器械制造商在**产品上市后**建立完善的**上市后监管（PMS）系统**和**警戒（Vigilance）系统**，确保符合：
- **欧盟 MDR (EU) 2017/745 Article 83-87**（PMS + PSUR + Vigilance + EUDAMED）
- **美国 FDA 21 CFR Part 803**（MDR + 5-day Correction Reporting）
- **中国 NMPA《医疗器械不良事件监测和再评价管理办法》**（2022 修订）
- **日本 PMDA JFMDA** + **英国 MHRA MORE** + **加拿大 HC MPR** + **澳大利亚 TGA IRIS** + **巴西 ANVISA**

**核心能力**：
1. **PMS Plan 框架**（数据源 + 频次 + 责任人 + 触发 CAPA 条件）
2. **PSUR 模板**（Class IIa 起每年更新）
3. **Vigilance 报告时间线**（EU 10/15 天、FDA 10/30 天、China 7/15 天）
4. **FSCA + FSN 模板与流程**
5. **CAPA 8 触发源监控**（与 ISO 13485 §8.3 整合）
6. **🆕 EU EUDAMED 强制报告**（首批 4 模块 2026-05-28 起；⚠️ **警戒模块约 2027 Q2 才强制**，详见步骤 7 口径校正）
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

#### 3.2 PSUR 标准结构（7 部分）

1. **产品信息**（Device Info）
2. **PSUR 时间段**（Reporting Period）
3. **销售量与暴露人群**（Sales Volume & Population Exposure）
4. **不良事件与投诉摘要**（Adverse Events & Complaints Summary）
5. **CAPA 与 FSCA 摘要**（CAPA & FSCA Summary）
6. **临床数据更新**（Clinical Data Update，包括 PMCF 进度）
7. **🆕 网络安全事件**（Cyber Incidents）
8. **🆕 AI 算法性能更新**（AI Algorithm Performance Update）
9. **结论与改进建议**（Conclusions & Recommendations）

### 步骤 4：Vigilance 报告时间线与决策树

#### 4.1 各国报告时间线对照表

| 事件类型 | EU MDR (Article 87) | FDA 21 CFR 803 | NMPA（2022 修订） | PMDA | HC | TGA |
|---------|---------------------|----------------|------------------|------|-----|-----|
| **严重事件** | 15 天 | 30 天（30-day） | 15 个工作日 | 15 天 | 30 天 | 30 天 |
| **死亡/严重伤害** | 10 天 | 10 天（10-day） | **立即**（24h 内） | 10 天 | 10 天 | 10 天 |
| **公共卫生威胁** | 10 天（EUDAMED）| 10 天 | 立刻 | 10 天 | 10 天 | 10 天 |
| **FSCA 计划** | **24h** 通知 NB/当局 | 5 个工作日 | 24h 内通知 | 24h | 24h | 24h |
| **FSN 致用户** | 24h 内分发 | 5 个工作日 | 24h | 24h | 24h | 24h |
| **Trend Report** | 显著增加即报 | CFR 803.53 | 显著增加即报 | 显著增加 | 趋势 | 趋势 |
| **PSUR** | IIa 2 年、IIb/III 1 年 | 年度（部分） | 年度 | 年度 | 年度 | 年度 |
| **🆕 漏洞披露（CVD）** | 90 天 | 90 天 | 暂无明文 | 90 天 | 90 天 | 90 天 |

**⚠️ 起算点：事件首次获知时间**（不是事件发生时间）

#### 4.2 严重事件判定流程图

```
不良事件收到
    │
    ▼
是否：死亡？ ─── 是 ─→ 10 天内报告（EU） / 立即报告（NMPA）
    │
    ▼ 否
是否：严重伤害（住院/延长住院/永久/显著伤残）？
    │
    ▼ 是
是否：可预期？（在 IFU/标签中已充分告知）
    │
    ▼ 否（不可预期）
10 天内报告（EU） / 15 个工作日（NMPA）
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
    ├─→ 24h 内通知 NB/当局（EU + NMPA）
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

### 步骤 7：🆕 EU EUDAMED 强制报告（首批 4 模块 2026-05-28 起；⚠️ 警戒模块约 2027 Q2 才强制）

> ⚠️ **口径校正（2026-08-29 复审落实）**：2026-05-28 强制的是**首批 4 模块**（Actor / UDI-DEV / NB&证书 / 市场监管）。**7.1 所列警戒事件提交与 FSCA 字段不在首批强制范围**，预计约 2027 Q2 才强制（依 Commission Decision (EU) 2025/2371）。
> 过渡期内：III 类/植入的 PSUR 与严重事件**仍走 NB / 国家 portal 通道**。
> **但无豁免的情形**：若某器械成为严重不良事件或 FSCA 对象，**须立即在 EUDAMED 注册并上报**——不受警戒模块是否强制影响。

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
- 在 EU AI Act 框架下多归"高风险 AI"（Annex III）
- 与 MDR PMS 整合（不重复建系统）

#### 9.2 持续监控义务
- 算法性能监控（与 PCCP 衔接）
- 数据漂移检测
- 偏差（Bias）检测
- 鲁棒性监控
- 关键 KPI：敏感度、特异度、AUC、Calibration、Demographic Parity

#### 9.3 重大事件报告
- **15 天内**报告严重事故
- 涉及生命安全或基本权利的事件
- 与 MDR 警戒报告同步

#### 9.4 持续学习（Continuous Learning）管理
- 再训练触发器定义（性能下降阈值）
- 影子部署（Shadow Mode）
- A/B 测试
- 重新评估（Re-certification）触发条件

## 输出标准

- PMS Plan 引用 MDR Article 84 + 85 + MDCG 2020-7
- 报告时间线以**自然日**为标准（与法规保持一致）
- 模板覆盖 EU/FDA/NMPA/PMDA/HC/TGA 至少 6 个主要市场
- 警戒事件决策树清晰可执行
- CAPA 触发源至少 10 个（含新增 9/10）
- 网络安全 SLA 量化（CVSS + 响应时间）
- AI 算法监控指标量化
- 输出语言与用户需求一致

## 约束

- 不替代 PRRC（Person Responsible for Regulatory Compliance）法定职责
- 严重事件是否构成"严重"最终以监管机构判定为准
- 警戒时间起算以"事件首次获知时间"为准，不是事件发生时间
- 网络安全事件涉及机密信息时，须与法务/律师协调披露内容
- 不替代临床/医学专家对医学事件的判断
- AI 算法阈值由制造商确定，但需有科学依据并在 PCCP 中说明

## 参考资料

- `references/vigilance-timeline-matrix.md`：各市场警戒报告时间线对照表
- `references/eudamed-registration-guide.md`：EUDAMED 注册步骤详解
- `references/vulnerability-management-playbook.md`：网络安全漏洞响应 Playbook
- 基于《合规之战：全球医疗器械监管进化史》第十五章（PMS 专题）

## 2026 团队自学更新（2026-08-16）

> 来源：联网检索 FDA / 欧盟委员会 / NMPA 官网及权威合规解读，详见 `references/2026-self-study-pms.md`。仅增不减，核心逻辑不变。

1. **EUDAMED 强制时间线修正**：2026-05-28 强制的是首批 4 模块（Actor、UDI/DEV、NB&证书、市场监管）；**警戒与 PMS 模块预计 2027 Q2 才强制**（Commission Decision (EU) 2025/2371）。Step 7 所述「警戒模块 2026-05-28 强制」不准确——过渡期走 NB/国家 portal，但 FSCA/严重事件须即时在 EUDAMED 注册。详见 reference 文件第三节。
2. **EU 趋势报告（Art 88）须预定义阈值**：PMS Plan 中必须预先设定基线、统计方法（控制图/CUSUM）与「统计学显著上升」判定标准，越阈即无延迟报告；与 Art 87 严重事件报告并行。详见 reference 文件第二节。
3. **PSUR 提交路径区分**：III 类/植入式依 Art 86(2) 经 EUDAMED 提交 NB；IIa 与非植入 IIb 依 Art 86(3) 留存技术文件供调阅（无主动提交义务）。NB 实操常设 90 天+30 天宽限，否则可暂停证书。详见 reference 文件第一节。
4. **FDA MDR/召回时限**：MDR 死亡/严重伤害/可报告故障 **30 日历日**，加急 **5 工作日**；纠正/撤除报告 **10 工作日**（21 CFR 806）；召回分 I/II/III 类。详见 reference 文件第四节。
5. **AI/SaMD 后市场监测加重**：PCCP 授权不减轻 PMS——每次变更须版本受控 + 部署后漂移/偏差监测并衔接 CAPA；EU AI Act（Digital Omnibus）医疗器械嵌入义务延至 2028-08-02，透明度义务 2026-08-02 起。详见 reference 文件第六节。
6. **中国 NMPA 新 GMP（2026-11-01 施行）**：第 123–127 条将不良事件监测、数据分析、召回、信息告知纳入 QMS 强制程序，与 PMS 体系衔接。详见 reference 文件第五节。
