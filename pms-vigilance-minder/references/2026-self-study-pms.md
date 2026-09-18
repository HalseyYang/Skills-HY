# 2026 团队自学：医疗器械 PMS / 警戒（Vigilance）最新动态

> 学习日期：2026-08-16｜方法：联网检索（FDA / 欧盟委员会 / NMPA 等官网及权威合规解读）
> 用途：附着到 pms-vigilance-minder 技能，补充 2025–2026 PMS/警戒最新要点。
> 原则：关键术语保留英文；每条变化附官方信源 URL；**拿不准标注「待核实」**；日期/时限以官方最新发布为准。

---

## 一、EU MDR Art 83–92 PMS 体系（PMS Plan / PSUR / PMCF）

### 1.1 PMS Plan 与 PMCF（Art 83–85 / Annex III / Annex XIV）
- PMS 系统是**每款器械**必须建立的、与风险等级相称的、内置于 QMS 的持续过程（Art 83）；其输出须回流至至少 7 个 QMS 环节：风险管理文件、CER、标签/IFU、CAPA、SSCP（III 类/植入）、设计制造信息、可用性改进（Art 83(3)）。
- PMCF 是 PMS 的临床证据子集，须有书面 PMCF Plan（MDCG 2020-7 模板），结果回流 CER 与风险文件。MedTech Europe 2025 立场文件呼吁对低风险、长期安全使用器械采取**风险分级、务实**的 PMCF 要求（待核实是否影响 MDCG 修订）。
- 信源：Reg (EU) 2017/745 Art 83–85；MDCG 2020-7；https://health.ec.europa.eu/medical-devices/mdcg-guiding-documents_en

### 1.2 PSUR（Art 86，MDCG 2022-21）
- **适用与频次**：Class I → PMS Report（PMSR，Art 85，必要时更新，留存备查供 CA 索取）；Class IIa → PSUR 至少每 2 年；Class IIb（非植入） → PSUR 至少每年；Class IIb（植入）+ Class III → PSUR 至少每年。
- **提交路径（关键澄清）**：
  - Class III 与植入式器械 PSUR 依 Art 86(2) **通过 Art 92 电子系统（即 EUDAMED 警戒与 PMS 模块）提交 NB**，NB 评估后供主管当局调阅。
  - Class IIa 与非植入式 IIb 依 Art 86(3) **留在技术文件中，供 NB 调阅、CA 索取**，无主动提交义务。
  - ⚠️ 在 EUDAMED 警戒模块正式强制前（见第三节），III 类/植入 PSUR 暂按 NB 既有通道（安全传输/邮箱）提交，模板遵循 MDCG 2022-21。
- **NB 实操时限（非法规硬性）**：BSI 等公告机构公开口径——PSUR 数据收集期结束后 **90 天内**未提交将触发提醒，再给 **30 天**窗口，逾期可暂停乃至撤销证书。属 NB 运营实践，非法律条款，建议在 SOP 中设置内部提前量。
- **2025-12 EU 简化提案（待核实）**：欧盟委员会 2025-12-16 提出简化 MDR/IVDR 提案，拟调整 PSUR 频次等要求；**尚未生效**，最终以官方立法结果为准。
- 信源：MDCG 2022-21；https://health.ec.europa.eu/medical-devices/mdcg-guiding-documents_en ；BSI/NB 公开实务说明（经 meddeviceguide.com 等合规解读汇总）

---

## 二、EU MDR 警戒报告时间线（Art 87 / 88 / 89 / 90）

### 2.1 严重事件（Serious Incident，Art 87）报告时限（自「获知日」起算）
| 情形 | 时限 |
|------|------|
| 一般严重事件 | **15 天**（日历日） |
| 导致死亡或不可预期健康严重恶化 | **10 天** |
| 构成严重公共卫生威胁 | **2 天** |
- 可先提交不完整报告以满足时限，再补正。同一事件在多成员国发生 → 一份 MIR 报至「最先获知」的协调主管当局（Coordinating CA，Art 89(4)）。
- 信源：https://eumdr.com/vigilance/ ；Reg (EU) 2017/745 Art 87(3)–(5)

### 2.2 FSCA（Field Safety Corrective Action，Art 87/89）
- 一旦**获知需采取 FSCA**（含第三国发起、且原因同样适用于欧盟在售同器械者），**立即、无延迟**通知主管当局与 NB；FSN 发给用户。
- 业界通行内部 SLA 取 **24 小时内** 通知 NB/当局（法规原文为「立即/无延迟」，24h 为常见实操口径，具体以 NB/CA 要求为准，标注「待核实精确数值」）。
- 信源：https://eumdr.com/vigilance/ ；MDCG 2024-2（警戒指南）

### 2.3 趋势报告（Trend Report，Art 88）——最易被忽视
- 触发：非严重事件或**预期不良副作用**的频率/严重度出现**统计学显著上升**，可能显著影响受益-风险评估。
- **无统一日历时限**：制造商在 PMS Plan 中**预先定义基线、统计方法与「显著上升」判定标准**（如 2σ 越界、基线率翻倍、CUSUM 超阈），一旦越阈即「无延迟」报告。
- 强调：趋势报告与严重事件报告（Art 87）是**并行机制**；即使单个事件未达严重，只要整体偏离基线即须报。多用控制图（c/u 图）、CUSUM、卡方/Fisher、贝叶斯信号检测。
- 信源：https://zechmeister-solutions.com/en/blog/mdr-articles-87-92-vigilance-framework ；MDCG 2024-1（Device-Specific Vigilance Guidance, DSVG）：https://health.ec.europa.eu/document/download/dbd0d748-d646-4274-afaa-399952809389_en?filename=mdcg_2024-1_en.pdf

### 2.4 调查与系统级分析（Art 89/90）
- Art 89：须**无延迟调查**、按 ISO 14971 风险评估、决定是否 FSCA、与主管当局（及相关 NB）**主动合作**（属法定义务）、更新技术文件/CER/风险文件。
- Art 90：从个案上升到系统级模式分析（signal detection）。
- 表单版本（2026 更新）：MIR v7.3.1（2026-05 更新）、FSCA v2.11、FSN Rev1、Trend Report v12/11 等。术语对齐 MedDRA / SNOMED CT / IMDRF 编码。
- 信源：https://eumdr.com/step-10/ ；MDCG 2023-3 rev.2（警戒术语 Q&A）

---

## 三、EUDAMED 警戒模块与强制时间线（重要澄清）

- **Commission Decision (EU) 2025/2371**（2025-11-27 刊载 OJEU）确认首批 **4 个模块**功能完备，自 **2026-05-28** 起强制使用：① 经济运营商注册(Actor) ② UDI/器械注册(UDI/DEV) ③ 公告机构与证书(NB/CRF) ④ 市场监管(MSU)。
- **警戒与 PMS 模块（Vigilance & PMS, VGL）不在首批**：当前路线图预计 **2026 Q4** 发布功能完备公告，**约 2027 Q2** 起强制（尚待官方审计与公告确认，标注「待核实」）。临床调查模块(CI/PS)另行排期。
- ⚠️ **对技能 Step 7 的修正提示**：本技能正文 Step 7 称「EUDAMED 警戒模块 2026-05-28 强制」系不准确——2026-05-28 强制的是前 4 模块；警戒模块强制约在 2027 Q2。过渡期内 III 类/植入 PSUR 与严重事件仍走 NB/国家 portal 通道。但**即使警戒模块未强制，若某器械成为严重不良事件或 FSCA 对象，须立即在 EUDAMED 注册并上报**（无豁免）。
- UDI/器械注册缓冲：2026-05-28 前已首次投放市场的遗留器械，最迟 **2026-11-27**（或 2026-11-28，以官方为准，待核实）前完成 UDI/DEV 注册。
- 信源：https://health.ec.europa.eu/medical-devices-eudamed/overview_en ；Commission Decision (EU) 2025/2371（EUR-Lex）；路线图经 medenvoyglobal.com / abroadlink.com / seleon.com 等汇总

---

## 四、FDA PMS / 警戒（21 CFR 803 / 806，召回 I/II/III，Section 522）

### 4.1 MDR 报告（21 CFR Part 803）
- 报告范围：器械可能导致或促成**死亡/严重伤害**，或**故障**若再发可能导致死亡/严重伤害。
- 时限：**30 个日历日**（自「获知」起算，获知即任一员工知悉，非管理层确认）；若需**立即采取行动防止重大公共卫生不合理风险**或 FDA 要求加急，则为 **5 个工作日**。
- 信源：https://www.ecfr.gov/current/title21/part803 ；https://www.fda.gov/medical-devices/postmarket-requirements-devices/medical-device-reporting-mdr

### 4.2 纠正/撤除（Recall，21 CFR 806 / 7）
- 制造商发起纠正或撤除以降低健康风险时，须在 **10 个工作日内**向 FDA 提交报告（21 CFR 806.10）；若已就同一事件提交 MDR，则通常无需另交 806 报告（21 CFR 806.10(f)）。
- **召回分类**：Class I（合理使用致严重不良健康后果或死亡，概率高）；Class II（可逆或暂时性不良后果，或严重后果概率低）；Class III（不太可能造成不良健康后果）。多数为**自愿**召回，但 FDA 依 FD&C Act §518(e) 可强制召回。
- 有效性核查（Effectiveness Check）5 级 A–E（Class I 通常 A/B 级，即 100% 或 >10% 受送达方确认）。
- 信源：https://www.fda.gov/medical-devices/postmarket-requirements-devices/medical-device-recalls ；21 CFR Part 806/810

### 4.3 Section 522 上市后研究（既有要求）
- FD&C Act §522 授权 FDA 对部分 Class II 器械命令开展**上市后监测研究（Postmarket Surveillance Studies）**，以评估上市后死亡、严重伤害或 malfunction 等罕见结局。属既有长期要求，2025–2026 无重大时限变动（标注「既有要求」）。
- 信源：https://www.fda.gov/medical-devices/postmarket-requirements-devices/postmarket-surveillance-studies

### 4.4 数据与信号源
- MAUDE 数据库（不良事件/召回，公开）、Recalls 数据库、MedWatch、openFDA API。建议 I 类召回每日监控、II/III 类每周（经 medflux.live 等汇总）。

---

## 五、中国 NMPA 不良事件监测与再评价（2025–2026）

- **新版《医疗器械生产质量管理规范》（2025 年第 107 号公告）**：2026-11-01 施行。第 123 条要求建立**不良事件监测制度**并及时报告、调查、分析、评价、必要时采取风险控制；第 124 条数据分析程序（形成质量风险评价报告）；第 125 条 CAPA；第 126 条**召回管理制度**；第 127 条产品信息告知程序。
- **《医疗器械监督管理条例》**：第 61–65 条确立国家不良事件监测制度、注册人/备案人监测体系义务、再评价触发（科学认知改变/监测表明可能存在缺陷等）、风险信号处置。
- **风险信号处置（地方实践，如福建 闽药监规〔2025〕3号）**：死亡 1 例及以上、群体事件、短期同产品多例聚集、持续/周期性异常增长趋势等均列为风险信号，须调查评估处置。
- 信源：https://www.gov.cn/gongbao/2026/issue_12506/202601/content_7055196.html ；NMPA 条例 https://www.nmpa.gov.cn/

---

## 六、AI/SaMD 持续性能监测（PCCP 后市场义务 + EU AI Act）

### 6.1 FDA PCCP 与 TPLC
- **PCCP 最终指南**（2024-12 发布，2025-08 更新）允许在原始申报中预定义 AI 模型变更计划（含变更描述、变更协议、影响评估三要素），经 FDA 授权后按计划更新**无需逐次重新申报**。
- ⚠️ **PCCP 不减轻反而加重 PMS 义务**：每次 PCCP 下实施的变更须文档化、版本受控、按验收标准做**部署后性能监测**，若发现安全/有效性问题须报告。
- **AI-DSF TPLC 生命周期管理草案指南（2025-01）**：要求描述上市后性能监测计划（追踪指标、数据来源、报告时间表），明确监测性能退化、数据漂移、分布偏移；2025-09 公开征求意见，评论截止 2025-12-01（后续采纳状态待核实）。
- **漂移检测**：数据漂移（输入分布变化，PSI > 0.25 通常视为显著）、概念漂移（特征-标签关系变化）等；偏差(bias)检测跨年龄/性别/族群亚组。
- 信源：https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence ；TPLC 草案经 chinamedglobal.com / quantiva.co 等汇总

### 6.2 EU AI Act（Reg 2024/1689）+ Digital Omnibus（Reg 2026/1744）
- 医疗器械内嵌 AI 属**高风险**（Annex I 嵌入受监管产品）。**Digital Omnibus Reg (EU) 2026/1744（2026-07-27 生效）**将高风险义务推迟：独立 Annex III 系统 → 2027-12-02；**嵌入受监管产品（含医疗器械）→ 2028-08-02**；但**第 50 条透明度义务自 2026-08-02 适用**。
- 制造商须数据治理、人类监督、技术文档、**上市后 AI 监测**（性能/漂移/偏差/鲁棒性）。与 MDR PMS 整合，不重复建系统。
- 信源：EUR-Lex Reg (EU) 2026/1744；AI Act 解读经 enz.ai / legalithm.com 等汇总

---

## 七、全球 PMS 差异速览（信号检测 / 数据互通）

- **EU**：集中式 EUDAMED（警戒模块 2027 Q2 预计强制）+ MDCG 模板；趋势报告为 Art 88 强制并行机制。
- **US**：MAUDE/Recalls/openFDA 公开数据；MDR 30 日/5 日；召回 I/II/III；Section 522 研究。
- **China**：NMPA 不良事件监测技术机构网络 + 注册人监测体系 + 再评价 + 风险信号处置；新 GMP 2026-11-01 强化。
- **Japan PMDA / Korea MFDS / Brazil ANVISA / Health Canada / TGA**：详见团队共享 `end2end-registration-workflow/references/2026-regulatory-updates.md`（如日本 IDATEN 简化 SaMD 再训练、韩国 DMPA 数字医疗器械 GMP 含 AI 管控、巴西 SIUD UDI 数据库等）。
- **跨国协调难点**：同一事件各国 reportability 判定不同（如未达 FDA MDR 阈值的事件可能达 EU 严重事件阈值，反之亦然）；EUDAMED 警戒模块强制前多国仍需分别经国家 portal 提交，AR 承担本地化/翻译义务。

---

## 八、对本技能的实践建议（仅提示，不改核心逻辑）
1. **修正 Step 7 时间线表述**：EUDAMED 首批 4 模块 2026-05-28 强制，警戒模块约 2027 Q2；过渡期走 NB/国家 portal，但 FSCA/严重事件需即时在 EUDAMED 注册。
2. **补充 Art 88 趋势报告**：在 PMS Plan 模板中强制要求预定义基线 + 统计方法 + 阈值（控制图/CUSUM）。
3. **细化 PSUR 提交路径**：区分 Art 86(2)（III 类/植入，经 EUDAMED 提交 NB）与 Art 86(3)（IIa/非植入 IIb，留存备查供调阅）。
4. **强化 AI 后市场监测**：PCCP 变更须版本受控 + 部署后漂移/偏差监测，衔接 CAPA。
5. **中国新 GMP 衔接**：2026-11-01 起将不良事件监测、数据分析、召回、信息告知纳入 QMS 程序。
