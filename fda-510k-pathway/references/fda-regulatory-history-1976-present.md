# 美国医疗器械监管史（1976《医疗器械修正案》至今，2026）

> 本文件为**奥斯曼医疗器械法规专家团**于 **2026-08-16** 从 FDA 官网及官方信源（fda.gov / congress.gov / federalregister.gov / govinfo.gov）自学整理的法规史参考资料。所有信源均附真实可访问 URL；个别存疑项已标注「待核实」。
>
> **最近增量更新：2026-08-31**（周度自学自动化 automation-1786846192252，第 4 轮）。本轮为**平静周**：截至 2026-08-31，FDA 无新增器械类指南、无新规则、无 Recognition List #67、eSTAR 维持 7.0 + PreSTAR 3.0、FY2027 费率无更正。**唯一须立即行动的是倒计时项：FY2026 旧费率 $26,067 的锁定窗口仅剩至 2026-09-30，10-01 起自动跳至 $28,653（详见第 4 轮日志"倒计时"栏）。** 上轮（2026-08-24）核心是 Recognition List #66 正式 FR 公告（91 FR 54715，FR 2026-17229）承认 ISO 10993-1:2025（Rec# 2-313），并确认 ASTM F2100-26 与 ISO 10993-7:2026 仍未获 FDA 承认。逐轮变更见文末**《周度增量更新日志》**。
>
> ⚠️ **链接校验说明**：fda.gov 与 accessdata.fda.gov 对脚本化请求（curl/wget）统一返回 404，属反爬行为，**不代表链接失效**——本文件 fda.gov 链接请用浏览器访问验证。federalregister.gov / govinfo.gov / open.fda.gov 可脚本校验，本轮已实测全部返回 200。

---

## 一、基线：1938 FD&C Act 与 1962 修正案（1976 年前的监管空白）

1938 年《联邦食品、药品和化妆品法》（Federal Food, Drug, and Cosmetic Act, FD&C Act）确立了药品与部分器械的安全标准，但医疗器械长期处于监管边缘：法律仅要求器械"不掺假、不误导标识"（misbranding / adulteration），并未建立上市前审评、风险分级或质量体系要求。1962 年《Kefauver-Harris 修正案》强化的是药品有效性证据，几乎未触及器械。因此直到 1976 年，除少数特定情形（如 1938 年前后已上市的"祖父"器械、部分放射性产品受 1968 年《辐射控制法》管辖）外，绝大多数医疗器械可在无任何安全性、有效性证明的情况下直接进入美国市场——这正是 1976 年《医疗器械修正案》出台的历史背景与监管空白所在。

---

## 二、里程碑总览表

| 年份/日期 | 法案 / 法规全名 | 对 510(k) 的改变 | 对器械分类的改变 | 对质量体系 / QMS 的改变 | 对用户费的改变 | 官方信源 |
|---|---|---|---|---|---|---|
| 1976-05-28 | Medical Device Amendments of 1976（PL 94-295） | **创立 510(k) 上市前通告路径**；新器械须证明与"实质性等同"（SE）的已上市器械等同 | 建立 **Class I/II/III 三类风险分级**；设立分类专家组（panels） | 首次授权 **GMP（生产质量管理规范）** 要求 | 无用户费机制 | [congress.gov S.510](https://www.congress.gov/bill/94th-congress/Senate-Bill/510) · [govinfo 公法文本](https://www.govinfo.gov/content/pkg/STATUTE-90/pdf/STATUTE-90-Pg539.pdf) |
| 1990-11-28 | Safe Medical Devices Act of 1990（SMDA, PL 101-629） | 强化上市后监督，间接提升 510(k) 器械的可追溯与不良事件数据要求 | 授权器械追踪（device tracking）与上市后监测（postmarket surveillance） | 未直接改写 GMP，但强化记录与报告（MDR） | 无 | [govinfo 公法文本](https://www.govinfo.gov/content/pkg/STATUTE-104/pdf/STATUTE-104-Pg4511.pdf) · [Federal Register 上市后监测](https://www.federalregister.gov/d/00-21827) |
| 1997-11-21 | FDA Modernization Act（FDAMA, PL 105-115） | **创立第三方（Accredited Persons）510(k) 审评**；确立 **De Novo** 路径；引入"最小负担"（least burdensome）原则 | **设立 513(g) 分类请求条款**；多数 Class I 与部分 Class II 豁免 510(k) | 未改 GMP 主体 | 无（用户费尚未设立） | [Federal Register 第三方审评](https://www.federalregister.gov/d/01-5611) |
| 2002-10-26 | Medical Device User Fee and Modernization Act（MDUFMA, PL 107-250） | 510(k) 纳入用户费；第三方 510(k)（3P510k）正式立法化 | 未大改 | 未改 | **首次设立医疗器械用户费**（510(k)/PMA/注册年费等） | [FDA MDUFMA 页面](https://www.fda.gov/industry/medical-device-user-fee-amendments-mdufa-fees/medical-device-user-fee-and-modernization-act-2002-mdufma-pl-107-250) |
| 2007-09-27 | FDA Amendments Act（FDAAA, PL 110-85） | 重申并延长第三方审评授权；强化注册与列名电子化 | 无重大分类修改 | 授权认可机构（accredited persons）进行器械工厂检查 | 续期 MDUFA（MDUFA II） | [congress.gov H.R.3580](https://www.congress.gov/bill/110th-congress/house-bill/3580) |
| 2011-01-19 | CDRH 510(k) 工作组报告与行动计划 | 发布 25 项行动计划，提升 510(k) 一致性、透明度（含 510(k) 范式、修改指南、Assurance Case 试点） | De Novo 流程优化指南 | — | — | [FDA 510(k) 行动计划](https://www.fda.gov/about-fda/cdrh-reports/accomplishments-cdrh-plan-action-510k-and-science) · [Federal Register 510(k) 实质等同指南](https://www.federalregister.gov/articles/2014/07/28/2014-17666/the-510k-program----evaluating-substantial-equivalence-in-premarket-notifications-guidance) |
| 2012-07-09 | FDASIA（PL 112-144，含 MDUFA III） | 优化 De Novo（可在收到 NSE 决定前申请降类）；强化 Pre-Submission 流程、受理标准（RTA） | 修改 513(f)，简化自动 III 类指定评估 | — | 续期 MDUFA III（约 5.95 亿美元/五年） | [FDA FDASIA 事实说明](https://www.fda.gov/regulatory-information/food-and-drug-administration-safety-and-innovation-act-fdasia/fact-sheet-medical-device-user-fee-amendments-2012) |
| 2016-12-13 | 21st Century Cures Act（PL 114-255） | 扩大突破性器械（Breakthrough Devices）计划；简化部分 Class I/II 豁免 510(k) 的规则制定 | 高风险器械附件（accessories）审查标准；扩展 HDE 适用病种 | — | 无 | [FDA Cures Act 实施说明](https://www.fda.gov/news-events/congressional-testimony/implementing-21st-century-cures-act-2018-update-fda-and-nih-07242018) |
| 2022（FY2023–2027） | MDUFA V（PL 117-180，FDA User Fee Reauthorization Act of 2022） | 提升 510(k) 审评绩效目标（如 FY2023 中位 128 天、目标缩短至 112 天） | — | — | **续期 MDUFA V**：五年约 17.84–19 亿美元；启动 TPLC/TAP 试点 | [FDA MDUFA V 页面](https://www.fda.gov/industry/medical-device-user-fee-amendments-mdufa/medical-device-user-fee-amendments-2023-mdufa-v) · [承诺函 PDF](https://www.fda.gov/media/158308/download) |
| 2024-02-02（生效 2026-02-02） | QMSR 最终规则（21 CFR 820 纳入 ISO 13485:2016） | 与 510(k) 提交的 QMS 证据要求衔接 | — | **以引用方式将 ISO 13485:2016 纳入 21 CFR 820，取代旧 QS Reg** | — | [Federal Register 2024-01709](https://www.federalregister.gov/documents/2024/02/02/2024-01709/medical-devices-quality-system-regulation-amendments) · [FDA QMSR FAQ](https://www.fda.gov/medical-devices/quality-management-system-regulation-qmsr/quality-management-system-regulation-frequently-asked-questions) |
| 2026-02-02 | QMSR 正式生效 | eSTAR 模板同步更新以对齐 QMSR | — | QMSR 强制执行，FDA 改用 7382.850 检查程序 | — | [FDA QMSR FAQ](https://www.fda.gov/medical-devices/quality-management-system-regulation-qmsr/quality-management-system-regulation-frequently-asked-questions) |
| 2026-08-01 | HFE（人因工程）最终指南生效 + eSTAR HFE 字段启用 | eSTAR 强制包含 HFE 提交类别字段；510(k) 须按三类 HFE 框架提交 | — | HFE 活动须纳入设计控制并留存 QMS 备查 | — | [FDA HFE 指南页](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-human-factors-information-medical-device-marketing-submissions) · [Federal Register 2026-10734](https://www.federalregister.gov/d/2026-10734) |
| 2026-04-20 | 草案指南《Compliance Policy for Certain NIOSH Approved Air-Purifying Respirators》（Docket FDA-2025-D-7121，评论期至 2026-06-22） | 覆盖同条 878.4040 下的 surgical N95 / N95 FFR（**MSH**）及 880.6260，**不适用 FXX**；尚未定稿 | 未改分类 | — | — | [govinfo FR 2026-07613（91 FR 21003）](https://www.govinfo.gov/content/pkg/FR-2026-04-20/html/2026-07613.htm) |
| 2026-05-25 | FDA 部分承认 **ISO 10993-1:2025**（Recognition No. 2-313），排除 6.5.11.3 中"consumer products or"及 Clause 6.9 | 生物相容性证据可引新版；**ISO 10993-1:2018 的符合性声明可用至 2029-07-01** | — | — | — | [认可共识标准库](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm) |
| 2026-05-29 | **HFE 最终指南发布**《Content of Human Factors Information in Medical Device Marketing Submissions》（Docket FDA-2015-D-4599），**2026-08-01 生效** | 建立 HFE Category 1/2/3 与决策点 A–**D**（新增 D，可用于论证免总结性验证） | — | HFE 活动须纳入设计控制并留存 QMS 备查 | — | [Federal Register 2026-10734（91 FR 32061）](https://www.federalregister.gov/d/2026-10734) |
| 2026-06-01 | **eSTAR nIVD 7.0 / IVD 7.0 + PreSTAR 3.0 发布** | 新提交须用 7.0 并选择 HF 提交类别；PreSTAR 3.0 扩展至 Submission Issue Request、Informational Meeting、Study Risk Determination、PMA Day 100、Accessory Classification | — | — | — | [FDA eSTAR 项目页](https://www.fda.gov/medical-devices/how-study-and-market-your-device/estar-program) |
| 2026-06-05 | 最终指南《Intent To Exempt Certain Unclassified Medical Devices From Premarket Notification》 | 豁免名单**不含 FXX**，口罩仍须 510(k) | 未分类器械豁免 | — | — | [Federal Register 2026-11303](https://www.federalregister.gov/documents/2026/06/05/2026-11303/intent-to-exempt-certain-unclassified-medical-devices-from-premarket-notification-requirements) |
| 2026-07-08 | **MDUFA VI 谈判进入公开阶段**：草案承诺信 + 公开会议通告（Docket FDA-2026-N-6655；会议 2026-08-05，评论截止 2026-08-07） | 涉 Third Party Review Program、Pre-Sub、审评一致性、国际协调 | — | — | 覆盖 **FY2028–FY2032**；MDUFA V 于 2027-09-30 到期 | [Federal Register 2026-13778（91 FR 42198）](https://www.federalregister.gov/documents/2026/07/08/2026-13778/medical-device-user-fee-amendments-public-meeting-request-for-comments) |
| 2026-07-30 | **FY2027 用户费公告正式发布**（Docket FDA-2026-N-7492），适用 2026-10-01 至 2027-09-30 | 510(k) 标准费 **$28,653** / 小企业 **$7,163** | — | — | 年度注册费 **$13,785**（无小企业减免） | [Federal Register 2026-15335（91 FR 48134）](https://www.federalregister.gov/documents/2026/07/30/2026-15335/medical-device-user-fee-rates-for-fiscal-year-2027) |
| FY2026 / FY2027 | MDUFA 用户费数额 | 510(k) 标准费 $26,067（FY26）/ $28,653（FY27，FR 2026-15335 确认） | — | — | 详见第三节第 12 目数额表 | [FDA 用户费页面](https://www.fda.gov/forindustry/userfees/medicaldeviceuserfee/default.htm) · [FY2027 公告](https://www.federalregister.gov/documents/2026/07/30/2026-15335/medical-device-user-fee-rates-for-fiscal-year-2027) |

> **关于「1992 年 513(g)」的说明（重要校正）**：用户需求中提及"1992 年 513(g) 分类请求条款"。经核查，**513(g) 分类请求（Request for Information）实际由 1997 年 FDAMA（PL 105-115）设立**，并非 1992 年；1992 年并无标志性的器械专项立法。本文件将 513(g) 归入 1997 年 FDAMA 一节并据实标注。

---

## 三、各里程碑详述

### 1. 1976《医疗器械修正案》（Medical Device Amendments of 1976, PL 94-295）
- **签署日期**：1976 年 5 月 28 日（President Gerald R. Ford 签署，Public Law 94-295）。
- **核心制度创设**：
  - **三类风险分级**：Class I（一般控制，general controls）、Class II（特殊控制 + 性能标准）、Class III（上市前批准 PMA）。
  - **510(k) 路径诞生**：新器械上市前 90 天须向 FDA 提交上市前通告，证明与"实质性等同"（substantially equivalent, SE）的已上市器械等同，方可上市。
  - **PMA（Premarket Approval）**：Class III 高风险器械须通过科学审评获得上市前批准。
  - **GMP 要求**：首次授权生产质量管理规范（后演进为 QS Regulation，再演进为 2026 年 QMSR）。
  - **分类专家组（Classification Panels / Advisory Panels）**：由外部专家组成，对器械分类提出建议。
  - **Preamendment / Grandfathered 器械的定义**：**Preamendment device** 指 1976 年 5 月 28 日（修正案生效日）之前已商业流通的器械；**Postamendment device** 指该日或之后首次商业流通的器械。1976 年前已上市的器械被视为"祖父条款"（grandfathered）保护，无需立即满足 PMA，可继续销售，除非被分类入 III 类且无 SE 路径。
- **官方信源**：
  - [congress.gov S.510](https://www.congress.gov/bill/94th-congress/Senate-Bill/510)
  - [govinfo 公法全文（90 Stat. 539）](https://www.govinfo.gov/content/pkg/STATUTE-90/pdf/STATUTE-90-Pg539.pdf)
  - [FDA 器械监管史](https://www.fda.gov/about-fda/histories-product-regulation/medical-device-radiological-health-regulations-come-age)
  - [FDA PMA 页面（含 preamendment 定义）](https://www.fda.gov/pma-approvals)

### 2. 1990《安全医疗器械法》（Safe Medical Devices Act, SMDA, PL 101-629）
- **签署日期**：1990 年 11 月 28 日。
- **核心改变**：
  - 建立 **医疗器械报告（MDR）** 制度，要求制造商、进口商、用户机构（医院等）报告导致死亡/严重伤害/故障的不良事件。
  - 授权 **器械追踪（device tracking）** 与 **上市后监测（postmarket surveillance, 522 条款）**，聚焦植入式、生命支持类器械。
  - 强化 FDA 的纠正、召回与通知权限。
- **对 510(k) / 分类 / QMS / 用户费**：未直接改写 510(k) 或 GMP，也未设立用户费；但显著增强了上市后的数据基础，使 FDA 能更早发现 SE 器械的潜在风险。
- **官方信源**：
  - [govinfo 公法全文（104 Stat. 4511）](https://www.govinfo.gov/content/pkg/STATUTE-104/pdf/STATUTE-104-Pg4511.pdf)
  - [Federal Register：Postmarket Surveillance（522 条款背景）](https://www.federalregister.gov/d/00-21827)

### 3. 1997《FDA 现代化法》（FDA Modernization Act, FDAMA, PL 105-115）
- **签署日期**：1997 年 11 月 21 日。
- **核心改变（与 510(k) 高度相关）**：
  - **第三方审评（Accredited Persons / 3P510k）**：FDAMA §210 将 1996 年试点立法化，授权 FDA 认可第三方机构审评部分低-中风险 510(k) 并给出初始分类建议（最终决定仍由 FDA 作出）。
  - **De Novo 路径**：允许无合法上市 predicate、但风险较低（本应落入 III 类）的器械，经申请直接被分类为 I 类或 II 类，避免被迫走 PMA。
  - **"最小负担"原则**：对具有不同技术特征的 SE 判定，FDA 须采用最小负担方式收集证据。
  - **513(g) 分类请求条款（Request for Information）**：任何人均可向 FDA 书面请求确认某器械的分类及适用法规要求，FDA 须在收到有效请求后 60 天内书面答复。
  - **豁免扩大**：取消多数 Class I 与部分 Class II 器械的 510(k) 要求。
- **官方信源**：
  - [Federal Register：第三方审评实施指南](https://www.federalregister.gov/d/01-5611)
  - [FDA 513(g) 程序指南（2024 版）](https://www.fda.gov/media/78456/download)
  - [FDA 第三方 510(k) 审评项目](https://www.fda.gov/medical-devices/premarket-submissions/510k-third-party-review-program)

### 4. 2002《医疗器械用户费与现代法》（MDUFMA, PL 107-250）
- **签署日期**：2002 年 10 月 26 日。
- **核心改变**：
  - **首设医疗器械用户费**：对 510(k)、PMA/PDP/PMR、De Novo、各类补充申请、企业注册年费等收费，收入专用于提升审评效率。
  - **第三方 510(k)（3P510k）正式立法化**：§202 将 Accredited Persons 项目写入法条，并规定经认可第三方审评的 510(k) **免缴 FDA 用户费**。
  - 同时涉及组合产品（combination products）指定、电子标签/电子注册等现代化条款。
- **官方信源**：
  - [FDA MDUFMA 公法页面](https://www.fda.gov/industry/medical-device-user-fee-amendments-mdufa-fees/medical-device-user-fee-and-modernization-act-2002-mdufma-pl-107-250)
  - [FDA 第三方 510(k) 审评项目](https://www.fda.gov/medical-devices/premarket-submissions/510k-third-party-review-program)

### 5. 2007《FDA 修正案》（FDAAA, PL 110-85）
- **签署日期**：2007 年 9 月 27 日。
- **核心改变（器械相关）**：
  - **用户费续期（MDUFA II）**：授权 2007–2012 周期用户费。
  - **唯一器械标识（UDI）系统**：§226 要求 FDA 制定 UDI 规则，为器械全生命周期追溯奠定基础（最终规则 2013 年发布，2014 年起分批实施）。
  - **第三方检查授权延长**：认可机构可对器械工厂进行检查。
  - **儿科器械（Pediatric Medical Device Safety and Improvement Act of 2007）**：PMA/HDE 等申请须包含可获得的儿科用途信息（§302 → §515A）。
  - **Sentinel 主动监测计划**：建立基于真实世界电子数据的上市后安全信号主动识别系统（后扩展至器械）。
- **官方信源**：
  - [congress.gov H.R.3580](https://www.congress.gov/bill/110th-congress/house-bill/3580)

### 6. 2011 CDRH 510(k) 工作组与行动计划
- **背景**：2009 年 CDRH 成立 510(k) 工作组与科学利用任务组；2010 年 8 月发布初步报告，2011 年 1 月 19 日发布《510(k) and Science Report Recommendations》与 **含 25 项具体行动的"行动计划"（Plan of Action）**。
- **核心改变**：
  - 提升 510(k) 的 **一致性、可预测性、透明度**：制定 510(k) 修改指南、510(k) 范式指南、De Novo 流程指南、获益-风险考量指南。
  - 启动 **Assurance Case 试点**、建立 **Center Science Council**、强化上市后数据分析与多项指南/标准作业程序（SOP）。
  - 形成后续 FDA 2018《510(k) 项目强化报告》与 2019 起 Safety and Performance Based Pathway 的政策源头。
- **官方信源**：
  - [FDA 510(k) 行动计划与成果](https://www.fda.gov/about-fda/cdrh-reports/accomplishments-cdrh-plan-action-510k-and-science)
  - [Federal Register：510(k) 实质等同评价指南（2014，源自工作组成果）](https://www.federalregister.gov/articles/2014/07/28/2014-17666/the-510k-program----evaluating-substantial-equivalence-in-premarket-notifications-guidance)

### 7. 2012 FDASIA（含 MDUFA III）
- **签署日期**：2012 年 7 月 9 日（PL 112-144）。
- **核心改变**：
  - **用户费续期（MDUFA III）**：2012-10-01 至 2017-09-30，五年约 **5.95 亿美元**（含通胀调整）；设 510(k) 审评绩效目标（如 FY2013 起一定比例 510(k) 在 90 天内决定）。
  - **De Novo 简化**：允许企业在收到 NSE（非实质性等同）决定**之前**即申请 De Novo 降类，缩短时间。
  - **受理标准（RTA）/ Pre-Submission 结构化**：强化拒收标准、预提交互动流程，提升审评效率与可预测性。
  - 修订 513(f)，简化"自动 III 类指定评估"。
- **官方信源**：
  - [FDA FDASIA / MDUFA III 事实说明](https://www.fda.gov/regulatory-information/food-and-drug-administration-safety-and-innovation-act-fdasia/fact-sheet-medical-device-user-fee-amendments-2012)

### 8. 2016《21 世纪治愈法》（21st Century Cures Act, PL 114-255）
- **签署日期**：2016 年 12 月 13 日。
- **核心改变（器械相关）**：
  - **突破性器械计划（Breakthrough Devices Program）**：将原有的 Expedited Access Pathway 扩展为正式计划，允许 FDA 与申办方就临床试验方案达成具约束力的协议，加速危及生命/不可逆衰竭疾病的器械开发。
  - **510(k) 豁免简化**：授权 FDA 以简化规则制定程序，豁免更多 Class I/II 器械的 510(k) 要求（CDRH 据 Cures  authority 已豁免 70+ Class I 与 1000+ Class II 器械类型）。
  - **软件例外（数字健康）**：将若干低风险软件功能排除出"器械"定义，催生 FDA 数字健康创新行动计划与软件 Pre-Cert 试点。
  - **HDE 扩大**：将人道主义器械豁免适用人群从每年 ≤4,000 人扩展至 ≤8,000 人。
- **官方信源**：
  - [FDA 实施 21st Century Cures Act 说明（2018）](https://www.fda.gov/news-events/congressional-testimony/implementing-21st-century-cures-act-2018-update-fda-and-nih-07242018)

### 9. 2022 MDUFA V（FY2023–FY2027）
- **立法**：2022 年《FDA User Fee Reauthorization Act》（PL 117-180，MDUFA V），涵盖 FY2023–FY2027。
- **核心改变**：
  - 五年总收益约 **17.84 亿美元**（达标最高约 19 亿美元），较 MDUFA IV 大幅增长。
  - **510(k) 绩效目标提升**：承诺 FY2023 中位审评 128 天，并在两年内缩短至 112 天；设立共享结果目标（total elapsed time）。
  - 启动 **TPLC Advisory Program（TAP）试点**，强化器械全生命周期早期互动。
  - 承诺：草案指南须在 5 年内最终定稿或撤回；加强数字健康等能力建设。
- **官方信源**：
  - [FDA MDUFA V 页面](https://www.fda.gov/industry/medical-device-user-fee-amendments-mdufa/medical-device-user-fee-amendments-2023-mdufa-v)
  - [MDUFA V 承诺函 PDF](https://www.fda.gov/media/158308/download)
  - [Federal Register：MDUFA 公开会议通知](https://www.federalregister.gov/d/2022-07451)

### 10. 2024 QMSR 最终规则（21 CFR 820 纳入 ISO 13485:2016）
- **发布日期 / 生效日期**：联邦公报 2024-02-02 发布（**89 FR 7496，文件号 2024-01709**），**2026-02-02 生效**（发布后两年）。2024-10-15 发布更正（补充"batch or lot"定义，FR Doc. 2024-23701）。
- **核心改变**：
  - **以引用（incorporation by reference）方式将 ISO 13485:2016 纳入 21 CFR 820**，并将原"Quality System (QS) Regulation"更名为 **Quality Management System Regulation（QMSR）**。
  - 同时纳入 ISO 9000:2015 第 3 条术语；保留/新增若干 FDA 特定要求（投诉、维修记录、标签与包装控制、MDR/UDI 关联等），避免与既有 FDA 要求冲突。
  - 目的：与美国主要贸易伙伴的质量体系要求国际协调，促进全球监管一致。
- **官方信源**：
  - [Federal Register 2024-01709（QMSR 最终规则）](https://www.federalregister.gov/documents/2024/02/02/2024-01709/medical-devices-quality-system-regulation-amendments)
  - [FDA QMSR FAQ](https://www.fda.gov/medical-devices/quality-management-system-regulation-qmsr/quality-management-system-regulation-frequently-asked-questions)

### 11. 2026 年关键节点（QMSR 生效、eSTAR 强制更新、HFE 指南）
- **2026-02-02 — QMSR 正式生效**：FDA 停止沿用 QSIT 检查法，改用更新后的 **7382.850** 检查合规程序；原 **7382.845 与 7383.001 同步停用**。据 QMSR FAQ（2026-02-02 更新）：**自生效日即开始执法、无宽限期**；检查可**回溯审阅 2026-02-02 之前生成的 QMS 记录**；原 820.180(c) 对**内审与管理评审记录的免查已取消**（内审/管理评审记录现可被检查官调阅）。**未发现任何正式"过渡期执法裁量"文件**。配套：2026-04-01 FDA 举办 QMSR 风险为本检查 Town Hall（CP 7382.850 两种检查模型、六大 QMS 领域 + 四项 OAFR），幻灯与记录已公开。
  - *（原表述"eSTAR 模板于同日更新至 v6.1 以对齐 QMSR"——**待核实**：FDA eSTAR 官方页未载明 v6.1/QMSR 专用字段，亦未载明旧版退役日期，该说法疑源自二手资料。）*
- **eSTAR 电子化（强制时间线）**：510(k) 的 eSTAR **强制自 2023-10-01** 起（依 FD&C Act §745A(b) 与 2023-10 最终指南）；**De Novo 的 eSTAR 强制自 2025-10-01** 起。**当前版本：nIVD eSTAR 7.0 / IVD eSTAR 7.0 / PreSTAR 3.0（2026-06-01 发布）**，已纳入 HFE 指南内容，可在模板内选择 HF 提交类别；**注意 7.0 于 2026-06-01 即已发布，早于 HFE 指南 2026-08-01 生效日**。「eSTAR 6.2 于 2026-08-03 强制退役」**已核实**（FDA eSTAR 官方页确认 v6.2 / PreSTAR v2.2 于 2026-08-03 退役，新提交须用 7.0）；「7.0 内置 QMSR 术语字段」仍**待核实**（官方页未载，7.0 已确认内置 HFE 提交类别字段）。
- **2026-05-29 发布 / 2026-08-01 生效 — HFE（人因工程）最终指南**：《Content of Human Factors Information in Medical Device Marketing Submissions》（Docket FDA-2015-D-4599，Federal Register 2026-10734，91 FR 32061），对 510(k)、De Novo、PMA、HDE 建立**基于风险的三类 HFE 提交框架**（Category 1/2/3）与决策点 A–D（**本轮核实：新增 Decision Point D**，可用于论证免做总结性验证 summative validation）；eSTAR 7.0 内含 HF 提交类别选择。配套指南为《Applying Human Factors and Usability Engineering to Medical Devices》（FDA 页面标注 August 2026 版）。2026-07-22 FDA 举办 HFE Town Hall。**口罩类（FXX）通常落入 Category 1/2**，可用 Decision Point D 论证豁免总结性验证。
- **官方信源**：
  - [FDA QMSR FAQ](https://www.fda.gov/medical-devices/quality-management-system-regulation-qmsr/quality-management-system-regulation-frequently-asked-questions)
  - [FDA eSTAR 510(k) 电子提交指南（2023-10）](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electronic-submission-template-medical-device-510k-submissions)
  - [FDA 510(k) 项目强化更新（含 eSTAR 时间线）](https://www.fda.gov/medical-devices/510k-clearances/fda-continues-take-steps-strengthen-premarket-notification-510k-program-program-updates)
  - [FDA HFE 指南页](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-human-factors-information-medical-device-marketing-submissions)
  - [Federal Register 2026-10734（HFE 指南公告）](https://www.federalregister.gov/d/2026-10734)

### 12. MDUFA 用户费数额（FY2026 / FY2027）
下列为标准费（Small Business 费为减半或约 25% 档），第三方 510(k) 免缴用户费：

| 费用项目 | FY2026（2025-10-01 至 2026-09-30） | FY2027（2026-10-01 至 2027-09-30） |
|---|---|---|
| 企业注册年费（Establishment Registration） | $11,423 | $13,785（↑约 20.7%） |
| 510(k)（标准 / 小企业） | $26,067 / $6,517 | $28,653 / $7,163（↑约 9.9%） |
| 513(g) 分类请求 | $7,820 / $3,910 | $8,596 / $4,298 |
| De Novo 分类请求 | $173,782 / $43,446 | $191,020 / $47,755 |
| PMA / PDP / PMR / BLA | $579,272 / $144,818 | $636,732 / $159,183 |
| Panel-track 补充 | $463,418 / $115,855 | $509,386 / $127,347 |
| 180 天补充 | $86,891 / $21,723 | $95,510 / $23,878 |
| 实时补充 | $40,549 / $10,137 | $44,571 / $11,143 |
| 30 天通知 | $9,268 / $4,634 | $10,188 / $5,094 |
| III 类器械年度定期报告 | $20,275 / $5,069 | $22,286 / $5,572 |

- **FY2027 费率已由 Federal Register 正式确立（2026-08-17 本轮核实，原文逐项比对无误）**：公告《Medical Device User Fee Rates for Fiscal Year 2027》，**FR Doc 2026-15335 / 91 FR 48134 / Docket FDA-2026-N-7492**，发布日 2026-07-30，适用 **2026-10-01 至 2027-09-30**。原文 Table 5 关键数字：510(k) 标准费 **$28,653**、小企业费 **$7,163**（标准费的 25%，公告正文表述为"4.5% of standard fee"指的是其占 PMA 基准费比例）；年度机构注册费 **$13,785**（**无小企业减免**，较 FY2026 的 $11,423 涨约 20.7%）；513(g) **$8,596 / $4,298**（小企业为 50%）；De Novo **$191,020 / $47,755**；PMA/BLA 基准费 **$636,732 / $159,183**。
- **⚠️ 实务提醒**：**FY2026 小企业资格认定于 2026-09-30 收盘失效，须重新申请**（每财年须重新提交 MDUFA Small Business Certification）；若拟在 FY2026 内递交以锁定 $26,067 旧费率，须在 **2026-09-30 前完成缴费与提交**。
- **官方信源**：[FDA 医疗器械用户费页面](https://www.fda.gov/forindustry/userfees/medicaldeviceuserfee/default.htm) · [FY2027 费率公告（FR 2026-15335）](https://www.federalregister.gov/documents/2026/07/30/2026-15335/medical-device-user-fee-rates-for-fiscal-year-2027)

---

## 四、510(k) 项目自身的演变

### 4.1 三种 510(k) 类型
- **Traditional 510(k)**：标准路径，以一个或多个合法上市 predicate 器械证明实质等同（SE），通常需提交性能数据、比对分析等完整资料。
- **Abbreviated 510(k)**：适用于有 FDA 认可共识标准（recognized consensus standards）或 **FDA 指南性 Special Controls** 的情形，可用符合性声明/摘要替代部分数据。
- **Special 510(k)**：适用于**已合法上市器械的修改**（设计或标签变更），由同一制造商提交，性能数据非必需或可用成熟方法评估，并以设计控制流程产出的总结性信息作为 SE 依据；若 FDA 认定不适合，将转为 Traditional 510(k)（原接收日不变）。
- 三者**均须缴 510(k) 用户费**（第三方审评除外），且**均须以 eSTAR 提交**（除非获豁免）。

### 4.2 第三方审评（3P510k / Accredited Persons）
- 源自 1997 FDAMA 立法化、2002 MDUFMA 正式入法；认可第三方机构审评低-中风险 510(k) 并给初始分类建议，FDA 在收到建议后约 30 天内作出最终 SE/NSE 决定；**免缴 FDA 用户费**。目前约半数 510(k) 符合第三方审评资格，但实际利用率偏低。

### 4.3 eSTAR 电子化
- 2020-02 FDA 启动 eSTAR 自愿试点；**2023-10-01 起 510(k) 强制使用 eSTAR**（FD&C Act §745A(b)）；**2025-10-01 起 De Novo 强制**；**2026-06-01 发布 nIVD eSTAR 7.0 / IVD eSTAR 7.0 / PreSTAR 3.0**，模板内含 HF（人因）提交类别选择，与 2026-08-01 生效的 HFE 最终指南对齐。eSTAR 以交互式 PDF 内置完整性校验，显著降低 RTA（拒收）率。
- **递交前必做**：到 [FDA eSTAR 项目页](https://www.fda.gov/medical-devices/how-study-and-market-your-device/estar-program) 下载**当期最新模板**（FDA 不接受过期版本），勿复用历史项目的旧模板文件。

**官方信源**：
- [FDA eSTAR 510(k) 电子提交指南](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electronic-submission-template-medical-device-510k-submissions)
- [FDA 如何准备 Special 510(k)](https://www.fda.gov/medical-devices/premarket-notification-510k/how-prepare-special-510k)
- [FDA 第三方 510(k) 审评项目](https://www.fda.gov/medical-devices/premarket-submissions/510k-third-party-review-program)

---

## 五、为什么 1976 是合理的学习起点？——以及对今天 510(k) 实务的启示

### 5.1 为什么 1976 是合理起点
- **祖父条款（grandfathering）的历史意义**：1976 年修正案以 **1976-05-28** 为分界，将器械分为 preamendment（1976 年前已上市）与 postamendment（1976 年当日或之后首次上市）。preamendment 器械被"祖父化"，无需立即满足 PMA 即可继续销售——这一安排既避免了让海量存量器械集体退出市场，又确立了"新器械须走审评"的底线。
- **predicate 必须溯源到 preamendment 或已 clearance 器械**：510(k) 的"实质性等同"逻辑要求每个新器械都须依附于一条**可溯源的合法上市器械链**：要么直接对比 preamendment 器械，要么对比某已获 clearance/approval 的器械（而该器械本身又可继续上溯）。**没有合法 predicate，就没有 510(k) 路径**——这正是 De Novo（无 predicate 时的替代分类路径）存在的根本原因。
- 因此，理解 1976 年的分级、510(k)、preamendment/grandfathered 定义，是理解此后半个世纪所有 510(k) 演变（第三方审评、De Novo、eSTAR、HFE、QMSR）的**元数据基础**。

### 5.2 对今天 510(k) 实务的启示
1. **predicate 选择是战略起点**：选错或选多个弱关联 predicate（multi-predicate）会增加被质疑与上市后不良事件风险；应优先选择技术特征、预期用途高度匹配的单一合法 predicate（参考 FDA 2018 后"Best Practices for Selecting a Predicate Device"精神）。
2. **三类 HFE 框架（2026-08-01 起）要求早期人因规划**：HFE 活动须自设计控制阶段即纳入，并将底层数据留存于 QMS 备查；Category 3 须提交验证测试，Category 2 须提供书面论证，决策点 D 可用于成熟平台豁免测试。
3. **QMSR（2026-02-02 起）与 ISO 13485 接轨**：以 ISO 13485:2016 为底座建立 QMS，可同时满足美国 QMSR 与多数国际市场要求，降低合规成本；但须补全 FDA 特定叠加要求（投诉、维修、标签、MDR/UDI 关联）。
4. **eSTAR 是"第一道门槛"**：自 2023-10-01 起 510(k) 必须 eSTAR 提交，2026 年模板已含 QMSR 与 HFE 字段；资料组织与字段完整性直接决定能否通过 RTA 筛查。
5. **用户费与周期须前置规划**：FY2027 费用较 FY2026 普涨约 10%（注册年费涨约 21%）；第三方 510(k) 虽免用户费但适用范围有限；提交时点的财年选择可节省可观费用。
6. **最小负担与证据分级**：自 FDAMA（1997）确立、经 FDASIA/MDUFA 强化的"最小负担"原则，要求以与风险相称的证据支持 SE；2026 年的 Safety and Performance Based Pathway 等可选路径，正是该原则的延伸。

---

## 附：主要官方信源索引（按年份）
- 1976：[congress.gov S.510](https://www.congress.gov/bill/94th-congress/Senate-Bill/510) · [govinfo 90 Stat. 539](https://www.govinfo.gov/content/pkg/STATUTE-90/pdf/STATUTE-90-Pg539.pdf)
- 1990：[govinfo 104 Stat. 4511](https://www.govinfo.gov/content/pkg/STATUTE-104/pdf/STATUTE-104-Pg4511.pdf)
- 1997：[Federal Register 01-5611](https://www.federalregister.gov/d/01-5611) · [FDA 513(g) 指南](https://www.fda.gov/media/78456/download)
- 2002：[FDA MDUFMA](https://www.fda.gov/industry/medical-device-user-fee-amendments-mdufa-fees/medical-device-user-fee-and-modernization-act-2002-mdufma-pl-107-250)
- 2007：[congress.gov H.R.3580](https://www.congress.gov/bill/110th-congress/house-bill/3580)
- 2011：[FDA 510(k) 行动计划](https://www.fda.gov/about-fda/cdrh-reports/accomplishments-cdrh-plan-action-510k-and-science)
- 2012：[FDA MDUFA III 事实说明](https://www.fda.gov/regulatory-information/food-and-drug-administration-safety-and-innovation-act-fdasia/fact-sheet-medical-device-user-fee-amendments-2012)
- 2016：[FDA Cures Act 说明](https://www.fda.gov/news-events/congressional-testimony/implementing-21st-century-cures-act-2018-update-fda-and-nih-07242018)
- 2022：[FDA MDUFA V](https://www.fda.gov/industry/medical-device-user-fee-amendments-mdufa/medical-device-user-fee-amendments-2023-mdufa-v) · [承诺函 PDF](https://www.fda.gov/media/158308/download)
- 2024 / 2026：[Federal Register 2024-01709（QMSR）](https://www.federalregister.gov/documents/2024/02/02/2024-01709/medical-devices-quality-system-regulation-amendments) · [FDA QMSR FAQ](https://www.fda.gov/medical-devices/quality-management-system-regulation-qmsr/quality-management-system-regulation-frequently-asked-questions) · [FDA HFE 指南](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/content-human-factors-information-medical-device-marketing-submissions) · [Federal Register 2026-10734](https://www.federalregister.gov/d/2026-10734) · [FDA 用户费](https://www.fda.gov/forindustry/userfees/medicaldeviceuserfee/default.htm)

---

## 周度增量更新日志（FDA 官网自学自动化）

> 本节由周度自动化（automation-1786846192252，每周一 09:00）追加。每轮只记「自上轮以来的新增/变更」，不重述既有内容。信源限 fda.gov / federalregister.gov / congress.gov / govinfo.gov / open.fda.gov。

### 2026-08-17（第 2 轮｜距上轮 1 天，覆盖 2026 年 4–8 月回溯补漏）

**本轮结论：存在重要监管变化（2 项须立即落到实务动作）。**

| # | 类别 | 新增/变更内容 | 对 FXX 口罩 510(k) 的影响 | 信源 |
|---|---|---|---|---|
| 1 | 用户费 | **FY2027 费率正式公告**（2026-07-30）：510(k) $28,653 / 小企业 $7,163；注册年费 $13,785；513(g) $8,596/$4,298；De Novo $191,020/$47,755；PMA $636,732/$159,183。适用 2026-10-01 起 | **高**——直接决定报价与递交时点；FY2026 小企业资格 2026-09-30 失效须重申 | [FR 2026-15335（91 FR 48134）](https://www.federalregister.gov/documents/2026/07/30/2026-15335/medical-device-user-fee-rates-for-fiscal-year-2027) |
| 2 | eSTAR | **7.0 版（nIVD/IVD）+ PreSTAR 3.0 于 2026-06-01 发布**，含 HF 提交类别字段 | **高**——新提交须用 7.0 并选 HF Category | [FDA eSTAR 页](https://www.fda.gov/medical-devices/how-study-and-market-your-device/estar-program) |
| 3 | 生物相容性 | **ISO 10993-1:2025 获部分承认**（Rec# 2-313，排除 6.5.11.3 中"consumer products or"及 Clause 6.9）；**2018 版符合性声明可用至 2029-07-01**；2026-09-09 FDA 办生物相容性风险评估 Town Hall | **高**——口罩属完整皮肤接触，短期可继续引 2018 版，过渡窗口明确 | [认可标准库](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm) |
| 4 | 人因 HFE | 最终指南**发布日为 2026-05-29**（原记录只写"5 月"）；**新增 Decision Point D** | 中——口罩多为 Category 1/2，可用 D 点论证免总结性验证 | [FR 2026-10734（91 FR 32061）](https://www.federalregister.gov/d/2026-10734) |
| 5 | MDUFA VI | **谈判进入公开阶段**（2026-07-08 草案承诺信 + 2026-08-05 公开会议，评论截止 2026-08-07），覆盖 FY2028–2032，含 Third Party Review 章节 | 中——长期费率与 3P510k 政策，属跟踪项 | [FR 2026-13778（91 FR 42198）](https://www.federalregister.gov/documents/2026/07/08/2026-13778/medical-device-user-fee-amendments-public-meeting-request-for-comments) |
| 6 | 呼吸器政策 | **草案指南**《Compliance Policy for Certain NIOSH Approved Air-Purifying Respirators》（2026-04-20，评论期至 2026-06-22，未定稿），覆盖 878.4040 下 MSH 与 880.6260 | **不适用 FXX**，但同条法规下需跟踪定稿 | [govinfo FR 2026-07613](https://www.govinfo.gov/content/pkg/FR-2026-04-20/html/2026-07613.htm) |
| 7 | 豁免范围 | 最终指南《Intent To Exempt Certain Unclassified Medical Devices》（2026-06-05）+ 2026 年两份 Class II 豁免征询（2026-02377、2026-08499），**均不含 878.4040 / FXX** | 无——口罩仍须 510(k) | [FR 2026-11303](https://www.federalregister.gov/documents/2026/06/05/2026-11303/intent-to-exempt-certain-unclassified-medical-devices-from-premarket-notification-requirements) |
| 8 | QMSR 配套 | FAQ 于 2026-02-02 更新：7382.845/7383.001 同步停用；**无宽限期、即日执法**；可回溯审阅生效前记录；**内审/管理评审记录免查条款取消**；2026-04-01 办风险为本检查 Town Hall | 中——影响体系准备与工厂检查预案 | [QMSR FAQ](https://www.fda.gov/medical-devices/quality-management-system-regulation-qmsr/quality-management-system-regulation-frequently-asked-questions) |
| 9 | 国会立法 | **无已通过的器械新法**；仅 S. 4519《Medical Device Electronic Labeling Act》2026-05-13 引入参院 HELP 委员会（仅"引入"状态） | 无当期义务 | [govinfo BILLS-119s4519is](https://www.govinfo.gov/app/details/BILLS-119s4519is) |

**未发现变更（已核实）**：
- **FXX / 878.4040 本体**：分类仍为 Class II、510(k) 必需、GMP 不豁免、可走第三方审评；关联指南仍是 **2004 版《Surgical Masks - Premarket Notification [510(k)] Submissions》**；2026 年无新特殊控制、无 product code 变动、无豁免。
- **2024-01 无菌信息指南**：现行版未改，无勘误、无补充草案（VH₂O₂ 仍列 Established Category A）。
- **Safety and Performance Based Pathway**：仍为 15 个器械类型，2026 年未扩容，**不含外科口罩**。
- **Predicate 政策**：2023 年三份草案（含《Best Practices for Selecting a Predicate Device》）**仍为草案**，列于 CDRH FY2026 指南计划"Under Construction"，无最终版。

**本轮已纠正的错误说法（此前疑受二手资料污染，勿再引用）**：
1. ❌「ASTM F2100-26 已被 FDA 承认/强制，不换版将被拒」→ **无官方依据**；FXX 承认清单当前仍为 **F2100-23**。
2. ❌「eSTAR 6.2 于 2026-08-03 强制退役、7.0 内置 QMSR 术语」→ 官方页未载明，**待核实**。
3. ❌「QMSR 于 2026-08-26 生效」→ **错误**，实为 **2026-02-02**。
4. ⚠️「eSTAR 于 2026-02-02 更新至 v6.1 对齐 QMSR」→ 官方未载，**待核实**（已在第 11 目标注）。

**下轮（2026-08-24）跟踪项**：① MDUFA VI 公开会议（8/5）后是否发布修订承诺信；② 呼吸器合规政策草案是否定稿；③ ASTM F2100-26 / ISO 10993-7:2026 是否进入 FDA 认可清单（Recognition List #67 及后续 FR 公告）；④ 2026-09-09 生物相容性 Town Hall 材料；⑤ eSTAR 是否升 7.x 及旧版退役公告。

---

### 2026-08-24（第 3 轮｜距上轮 7 天）

**本轮结论：有监管更新但非颠覆性——核心是认可标准库更新 + 解决上轮 2 项"待核实"。**

| # | 类别 | 新增/变更内容 | 对 FXX 口罩 510(k) 的影响 | 信源 |
|---|---|---|---|---|
| 1 | 认可标准库 | **Recognition List #66 正式 FR 公告**（2026-08-24，91 FR 54715，FR Doc 2026-17229）：以新版本替换/撤回多项旧标准。关键：ISO 10993-1:2025（第6版，2025-11）认可号 **Rec# 2-313**（替换旧 2-258）；**ISO 10993-12:2021+AMD1:2025 认可号 Rec# 2-314**（替换旧 2-289）；另含 ISO 20417:2026-03（5-149）、IEC 60601-2-2（6-521）、ISO 10079-1:2022+AMD1:2026（1-203）等 | 中——口罩皮肤接触生物相容性评价可正式引用 2-313（2025 版）；10993-12 涉及样品制备，亦更新 | [FR 2026-17229（91 FR 54715）](https://www.federalregister.gov/d/2026-17229) |
| 2 | eSTAR | **v6.2 / PreSTAR v2.2 已于 2026-08-03 退役**（上轮"待核实"已解决）；当前强制版本 nIVD/IVD eSTAR **7.0**（2026-06-01）+ PreSTAR 3.0 | 高——新提交必须 7.0，旧版提交会被拒 | [FDA eSTAR 页](https://www.fda.gov/medical-devices/how-study-and-market-your-device/estar-program) |
| 3 | 纠正（待核实→已澄清） | **ASTM F2100-26 与 ISO 10993-7:2026 仍未获 FDA 承认**：List #66 公告的表1/表2 均未纳入二者；FXX 性能仍须引 **ASTM F2100-23（Rec# 6-492）**，EO 残留仍按 **ISO 10993-7:2008+AMD1:2019（Rec# 2-275）** 的 TAG/TAI 限值 | 高——维持上轮结论，网传"F2100-26 强制换版"不实 | [FR 2026-17229](https://www.federalregister.gov/d/2026-17229) · [认可标准库](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm) |

**未发现变更（已核实，截至 2026-08-24）**：
- **MDUFA VI**：8/5 公开会议后**无**修订承诺信或新 FR 通告；FDA 预计 2027-01-15 提交国会。属跟踪项，无当期义务。
- **呼吸器合规政策草案**（FR 2026-07613）：仍草案，未定稿；不适用 FXX。
- **新 FDA 指南**：2026-08-17 以来**无**外科口罩/无菌信息/生物相容性/HFE/QMSR/510(k) predicate 新终稿或草案。
- **FY2027 用户费**（FR 2026-15335）：无更正、无新公告，费率维持 510(k) $28,653 / 小企业 $7,163 / 注册年费 $13,785。
- **国会立法**：S.4519（Medical Device Electronic Labeling Act）仍仅"引入"状态，无新器械法案。
- **FXX / 878.4040 本体**：分类、特殊控制、豁免范围、Product Code 均无变动；关联指南仍为 2004 版外科口罩指南。

**本轮新掌握的信源/事件**：
- **2026-09-09 生物相容性风险评估 Town Hall**（三场系列 09-09 / 09-23 / 10-07，讨论 ISO 10993-1:2025）已发布预告，免报名：https://www.fda.gov/medical-devices/medical-devices-news-and-events/town-hall-biocompatibility-risk-assessment-09092026 （列为跟踪项，材料待会后公开）

**下轮（2026-08-31）跟踪项**：① openFDA `meta.last_updated` 是否再推进（当前 2026-08-10，FXX 总数仍 607、最新 clearance 2026-03-18，须回 accessdata 补查 3 月后空窗）；② MDUFA VI 承诺信是否发布；③ 呼吸器草案是否定稿；④ 2026-09-09 Town Hall 材料；⑤ ASTM F2100-26 / ISO 10993-7:2026 是否终进认可清单（下一批 List）；⑥ eSTAR 是否升 7.x。

---

### 2026-08-31（第 4 轮｜距上轮 7 天）

**本轮结论：无实质监管变化（平静周）——但有一个 30 天倒计时的钱袋子问题必须立刻决策。**

本轮检索范围与方法：Federal Register API 拉取 FDA 机构 2026-08-24 起全部文档（共 **18 篇，全部为 Notice，无 rule/proposed rule**）+ FDA 指南库按签发日倒序核查前 10 条 + eSTAR 官网 + congress.gov + openFDA 8 个设备端点实测。

#### ⏳ 倒计时（本轮唯一须立即行动项）

| 事项 | 截止日 | 距今 | 动作 |
|---|---|---|---|
| **FY2026 旧费率锁定** | **2026-09-30** | **30 天** | 若 B1 型口罩 510(k) 有可能在 9 月内提交，**必须在 9-30 前完成提交并缴费**，方可锁定 FY2026 的 **$26,067**（小企业 $6,517）；10-01 起自动适用 FY2027 的 **$28,653**（小企业 $7,163），标准费**多付 $2,586**。⚠️ 但注意：仅为省费而提交不成熟的资料会招致 RTA/AI Hold，得不偿失——**这是"进度是否已到位"的判断题，不是"要不要省钱"的判断题**。 |
| **小企业资格（SBD）每财年重申** | 财年切换 | 30 天 | FY2027 的小企业认定须**重新申请**（MDUFA 小企业资格不跨财年自动延续）。若拟走小企业费率，须提前备妥上一纳税年度收入证明。 |
| **ASTM F1862 旧版 -17 过渡期** | **2026-12-20** | 约 3.5 月 | 合成血穿透测试报告须按 **F1862/F1862M-24（Rec# 6-504）** 出，旧 -17 版报告 12-20 后失去 DoC 简化资格 |

信源：[FR 2026-15335 / 91 FR 48134（FY2027 费率）](https://www.federalregister.gov/d/2026-15335)

#### 本轮新增/确认条目

| # | 类别 | 内容 | 对 FXX 口罩 510(k) 的影响 | 信源 |
|---|---|---|---|---|
| 1 | 常规 PRA 通告 | **《Medical Devices; Reports of Removals and Corrections》**（2026-08-31，FR Doc 2026-17675）——21 CFR 806 召回/纠正报告的信息收集续期征求意见 | 低——不改变 510(k) 路径；但提示 806 报告义务是上市后必备动作，可纳入 PMS 程序文件引用 | [FR 2026-17675](https://www.federalregister.gov/documents/2026/08/31/2026-17675/agency-information-collection-activities-proposed-collection-comment-request-medical-devices-reports) |
| 2 | 常规 PRA 通告 | **《Allegations of Regulatory Misconduct to CDRH》**（2026-08-26，FR Doc 2026-17377）——向 CDRH 举报监管不当行为的信息收集续期 | 低——无申报影响；可作为了解 CDRH 申诉渠道的背景资料 | [FR 2026-17377](https://www.federalregister.gov/documents/2026/08/26/2026-17377/agency-information-collection-activities-proposed-collection-comment-request-allegations-of) |
| 3 | eSTAR（确认未变） | 当前版本仍为 nIVD/IVD **eSTAR 7.0** + **PreSTAR 3.0**（2026-06-01 发布），FDA eSTAR 页最后更新标注 June 1, 2026；v6.2 / PreSTAR 2.2 已于 2026-08-03 退役 | 高——**新提交必须用 7.0**，其内已内嵌 2026-05-29 HFE 指南要求（2026-08-01 起适用） | [FDA eSTAR 页](https://www.fda.gov/medical-devices/how-study-and-market-your-device/estar-program) |

#### 未发现变更（已核实，截至 2026-08-31）

- **新 FDA 指南：无。** 指南库按签发日倒序前 10 条（2026-08-11 至 08-28）全部为非器械中心条目：CVM 兽药复方（Draft CVM GFI #256B，08-28）、CVM 鱼类麻醉（08-25）、CDER 治疗等效性评价（08-21）、CBER 基因治疗 FAQ / 免疫制品效价（08-19）、CDER ANDA/505(b)(2)（08-17）等。**无任何外科口罩／无菌信息／生物相容性／HFE／QMSR／510(k) 相关新条目。**
- **规则变动：无。** 本窗口 FDA 18 篇文档**全部是 Notice**，无 rule 或 proposed rule 涉及 510(k)、premarket notification、device classification、21 CFR 878（surgical apparel）、sterilization、QMSR。
- **认可标准库：无 List #67。** FR 宽口径检索（term = recognized standards / Recognition List Number / modifications to the List，2026-08-20 起）仅命中上轮已收录的 **List #66（FR 2026-17229）**。四个关键标准状态维持：**ASTM F2100-23（6-492）**、**ASTM F1862-24（6-504）**、**ISO 10993-7:2008+AMD1:2019（2-275）**、**ISO 10993-1:2025（2-313，2018 版 DoC 可用至 2029-07-01）**；**ASTM F2100-26 与 ISO 10993-7:2026 仍未获承认。**
- **MDUFA VI 重新授权：无新进展。** 本窗口无 MDUFA / user fee 条目，无新公开会议、无修订承诺信；承诺信仍预计 **2027-01-15** 提交国会（上轮基线 FR 2026-13778）。
- **FY2027 用户费：无更正公告。** 费率维持，2026-10-01 生效（见上方倒计时）。
- **呼吸器合规政策草案（FR 2026-07613）：仍为草案，未定稿。** 本窗口 FR 检索「respirator」命中 0 篇。该草案仅覆盖 **MSH / 21 CFR 880.6260**，**不适用 FXX**（878.4040），影响间接。
- **国会立法：S.4519 无进展。** 《Medical Device Electronic Labeling Act》仍停留 2026-05-13 引入、送参议院 HELP 委员会状态。若将来通过，允许电子标签，对口罩**标签策略**有潜在影响，但不改变 510(k) 路径本身。链接：https://www.congress.gov/bill/119th-congress/senate-bill/4519 （注：congress.gov 对 curl 返回 **403** 反爬，须浏览器访问，非失效）
- **FXX / 878.4040 本体：无变动。** 分类、特殊控制、豁免范围、Product Code 均未变；关联指南仍为 2004 版外科口罩指南。

#### 跟踪项状态更新

- **2026-09-09 生物相容性风险评估 Town Hall**（三场系列 09-09 / 09-23 / 10-07，主题 ISO 10993-1:2025）：本窗口**无新议程或材料发布**。已核实：**免注册**，但**提问提交截止 2026-07-31 已过**（本轮新掌握，此前未记录）——即我们只能听、不能提问。因 FXX 口罩接触皮肤/黏膜、ISO 10993 系列为 510(k) 必备，**建议 09-09 参会听会**，会后取材料。页面：https://www.fda.gov/medical-devices/medical-devices-news-and-events/town-hall-biocompatibility-risk-assessment-09092026

**下轮（2026-09-07）跟踪项**：① **FY2026 费率窗口仅剩 3 周**，须复核提交进度决策；② FY2027 小企业资格（SBD）申请是否已启动；③ openFDA `meta.last_updated` 与 FXX 总数（本轮 2026-08-17 / 607，最新 clearance 仍 2026-03-18，**空窗已达 5.5 个月**）；④ Recognition List #67 是否发布（关注 ASTM F2100-26 / ISO 10993-7:2026）；⑤ 09-09 Town Hall 会后材料；⑥ MDUFA VI 承诺信；⑦ 呼吸器草案是否定稿。

---

> 注：本资料为自学整理，不构成法律意见；具体申报请以 FDA 最新指南、联邦公报与 21 CFR 原文为准。
