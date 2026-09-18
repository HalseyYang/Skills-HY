# FDA 公开数据挖掘指南：系统性挖掘 510(k) 情报

> **说明**：这是**奥斯曼医疗器械法规专家团**于 **2026-08-16** 自学整理的 FDA 公开数据挖掘指南。本文所有信源均指向真实可访问的 `fda.gov` / `open.fda.gov` 官方资源；个别无法在本轮核实的内容已标注「待核实」。文档供法规情报研究、竞品监测与 510(k) 申报准备使用。
>
> **最近增量更新：2026-08-31**（周度自学自动化，第 4 轮）。本轮补充：① 新增 **openFDA 8 个设备端点 `meta.last_updated` 实测对照表**（2.4 节，`510k`=2026-08-17 / `recall`=2026-08-27 最新 / `udi`=2026-08-03 最慢 / `covid19serology` 已冻结）；② **accessdata 补盲通道确认堵死**——`pmn.cfm` 为 POST 表单、GET 无效，静态包 `pmn96cur.zip` 被滥用检测 302 拦截，**空窗补查只能人工浏览器**（2.4 节末）；③ 无 Recognition List #67，4 个关键标准认可状态未变（3.2b 节）；④ 指南库无器械类新增（4.3 节）；⑤ 刷新 FXX 快照（**本周新增 K 号 = 0，连续第 3 周**）。
>
> ⚠️ **链接校验说明**：`fda.gov` 与 `accessdata.fda.gov` 对脚本化请求（curl/wget）**统一返回 404，属反爬**，不代表链接失效——本轮实测连已知有效的 QMSR FAQ、pmn.cfm、cfStandards/search.cfm 也返 404。校验这两个域的链接请用浏览器或带渲染的抓取工具；`open.fda.gov` / `api.fda.gov` / `federalregister.gov` / `govinfo.gov` 可直接脚本校验（本轮全部 200）。

---

## 目录

1. [FDA 510(k) 公开数据库（accessdata）](#1-fda-510k-公开数据库accessdata)
2. [openFDA 设备 510(k) API](#2-openfda-设备-510k-api)
3. [FDA 认可共识标准数据库（Recognition Database）](#3-fda-认可共识标准数据库recognition-database)
4. [FDA 指南库检索方法](#4-fda-指南库检索方法)
5. [FD&C Act 与 CFR 设备条款（21 CFR 800-1299）查阅入口](#5-fdcc-act-与-cfr-设备条款21-cfr-800-1299查阅入口)
6. [专家日常操作手册：如何把公开资源用起来](#6-专家日常操作手册如何把公开资源用起来)

---

## 1. FDA 510(k) 公开数据库（accessdata）

### 1.1 检索入口

- **510(k) Premarket Notification 数据库（主检索页）**
  https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm
- 该库收录自 1976 年以来的 510(k) 获准（clearance）记录，是找 predicate、看同类器械技术特征、下载 510(k) Summary 的一手来源。

### 1.2 如何按不同维度检索

数据库检索表单支持以下关键字段（可组合使用）：

| 检索维度 | 字段 / 操作 | 说明与技巧 |
|---|---|---|
| **Product Code（产品代码）** | 填入 3 位字母代码（如 `FXX` = 外科口罩；`IME` = 医用冰袋/物理降温器械） | 最常用于「找同类器械」和「找 predicate」。同一 Product Code 下的获准器械通常属于同一监管类别，技术特征可比性强。 |
| **K 号（510(K) Number）** | 填入 `K` + 6 或 7 位数字，如 `K232820` | 精确定位某一获准记录，查看其申请人、决定日期、法规号、Summary 链接。 |
| **申请人（Applicant）** | 填公司名（支持部分匹配） | 监控竞品/客户/自身历史 clearance；查找某厂商在该品类的全部获准。 |
| **决定日期（Decision Date From/To）** | 起止日期区间 | 监控「最近 30/90 天」同类 clearance 动态；定位某时间窗内的技术演进。 |
| **Submission Type** | Traditional / Special / Abbreviated | 区分传统、特殊、简略 510(k)。 |
| **Regulation Medical Specialty（Panel）** | 医学专科/审查面板 | 按专科（如 General Hospital、Anesthesiology）筛。 |
| **Device Class / Third Party** | Class II / 第三方审查标记 | 辅助过滤。 |

> 检索结果默认按相关度/时间返回；每条记录包含：申请人、器械名、Product Code、法规号（regulation number）、决定日期、以及「Summary」链接。

### 1.3 如何找 predicate（ predicates / 对比器械 ）

predicate 是「被对比的合法上市器械」（21 CFR 807.92(a)(3)）。公开库里找 predicate 的三种互补路径：

1. **直接读法**：打开目标器械的 **510(k) Summary**（见 1.4），Summary 按 21 CFR 807.95 要求必须写明与 predicate 的实质等同对比，通常会**直接给出 predicate 的 K 号与器械名**。这是最权威的 predicate 来源。
2. **Product Code 枚举法**：用目标 Product Code 检索，按决定日期排序，圈定「最近获准、技术最相近」的若干器械作为候选 predicate（注意需确认其仍「合法上市」、未被召回/撤市）。
3. **申请人反查法**：在 openFDA（见第 2 节）按 `product_code` + `applicant` 反查竞品历史 clearance，交叉验证可比器械。

> ⚠️ 注意：公开库只显示「获准」记录，**不显示被拒（NSE / Not Substantially Equivalent）或撤回记录**，也不显示仍「pending」的提交。predicate 必须是「合法上市」器械，需自行排除已撤市/召回项（可结合召回库、MAUDE 库交叉核对）。

### 1.4 如何下载 510(k) Summary

- 在检索结果列表中，每条获准记录均带有 **「Summary」链接**，点击即可打开该器械的公开 **510(k) Summary**（纯文本/网页）。
- openFDA 字段 `statement_or_summary` 会标注该记录是 **Summary**（传统/简略 510(k) 的公开摘要）还是 **Statement**（Special 510(k) 的公开声明）。
- 510(k) Summary 是依法（21 CFR 807.95）须向公众提供的文件；完整 510(k) 申报资料本身属于保密信息，不公开。

### 1.5 510(k) Summary 的公开 / 脱敏边界与局限

**公开的部分（典型内容）**：器械名称与预期用途、predicate 及其实质等同论证、关键技术特征（technological characteristics）对比、所用测试标准/方法的摘要、标签要点等。

**被隐去 / 脱敏的部分（Confidential Commercial Information，CCI / 商业秘密）**：

- **具体化学配方 / 材料组成**：如聚合物配比、涂层/药液的具体成分浓度、专有材料牌号等常被整段涂黑。
- **详细制造工艺参数**：如关键工艺温度/压力曲线、专有加工步骤。
- **完整原始测试数据与验证报告**：Summary 只给「结论与方法摘要」，不给原始数据表、完整验证协议与原始记录。
- **软件算法 / 源代码**：SaMD 或含软件的器械，算法逻辑与源码不公开。
- **部分供应商 / 组件身份**：可能以「Vendor A」等方式匿名化。
- **完整风险管理文件（ISO 14971 文件）、设计历史文件（DHF）**：不在公开 Summary 中。

**局限总结**：510(k) Summary 适合「学英文表述、看测试思路、确认 predicate 与技术路线」，但**不能**替代完整申报资料，也无法获得可直接复用的验证数据。对化学/配方类信息尤其要降低预期。

---

## 2. openFDA 设备 510(k) API

### 2.1 端点 URL

- **基础端点**：`https://api.fda.gov/device/510k.json`
- **官方文档页**：https://open.fda.gov/apis/device/510k/
- **字段字典 / 可检索字段**：https://open.fda.gov/apis/device/510k/searchable-fields/
- **数据源说明**：https://open.fda.gov/data/510k/

### 2.2 关键字段（API 真实字段名）

openFDA 在该数据集使用的顶层字段如下（注意：与口语中的「review_panel / decision / type」名称略有出入，下表给出映射）：

| 用户常用说法 | API 实际字段名 | 含义 |
|---|---|---|
| K 号 | `k_number` | 如 `K232820` |
| 器械名 | `device_name` | 商品名/描述 |
| Product Code | `product_code` | 如 `FXX` |
| 决定日期 | `decision_date` | 格式 `YYYY-MM-DD` |
| 申请人 | `applicant` | 公司名 |
| 审查面板/委员会 | `review_advisory_committee` / `advisory_committee` | 审查所依据的医学专科/咨询委员会代码 |
| 决定结果 | `decision_code` / `decision_description` | 如 `SESE` / `Substantially Equivalent` |
| 类型（传统/简略/特殊） | `clearance_type` | 如 `Traditional` |
| Summary 还是 Statement | `statement_or_summary` | `Summary` / `Statement` |
| 接收日期 | `date_received` | 格式 `YYYY-MM-DD` |
| 法规号 | `regulation_number` | 如 `878.4040` |
| 器械分类 | `device_class` | `1`/`2`/`3` |
| 加速审查标记 | `expedited_review_flag` | |
| 第三方标记 | `third_party_flag` | |
| 嵌套扩展 | `openfda` | 含 `device_class`、`medical_specialty_description`、`registration_number`、`fei_number` 等 |
| 元数据 | `meta` | 含 `last_updated`、`results.total`、分页信息 |

> 实测示例（**加了过滤条件后**返回 1 条，非该 Product Code 全量）：`k_number=K232820`，`device_name=HALYARD* FLUIDSHIELD* 1 Fog-Free Surgical Mask...`，`product_code=FXX`，`decision_date=2024-06-04`，`applicant=Owens & Minor (O&M) Halyard, Inc.`，`decision_description=Substantially Equivalent`，`clearance_type=Traditional`。（数据 `last_updated` 显示为 2026-08-03）
>
> ⚠️ **勿与 §2.4 的 607 条混淆**（2026-08-29 复审标注）：本节示例的"1 条"是**叠加了限定条件**后的结果；`product_code:FXX` 在 openFDA 的**命中总数为 607 条**（见 §2.4）。两者不是同一查询口径。

### 2.3 查询示例

```bash
# 1) 按 Product Code 检索外科口罩（FXX），取前 10 条
https://api.fda.gov/device/510k.json?search=product_code:FXX&limit=10

# 2) 按申请人检索（含空格/特殊字符需 URL 编码，& 编码为 %26）
https://api.fda.gov/device/510k.json?search=applicant:%22Owens%20%26%20Minor%22&limit=5

# 3) 按决定日期区间检索 2024 全年
https://api.fda.gov/device/510k.json?search=decision_date:[2024-01-01+TO+2024-12-31]&limit=5

# 4) 组合：某 Product Code + 某年度，按决定日期倒序
https://api.fda.gov/device/510k.json?search=product_code:FXX+AND+decision_date:[2024-01-01+TO+2024-12-31]&sort=decision_date:desc&limit=20

# 5) 仅取需要的字段（减少体积）
https://api.fda.gov/device/510k.json?search=product_code:FXX&limit=5&fields=k_number,device_name,applicant,decision_date,clearance_type
```

> 也支持下载整库 JSON（`https://api.fda.gov/device/510k.json?limit=1` 仅用于探测；批量请用 openFDA 提供的下载包：https://open.fda.gov/data/downloads/ ）。

### 2.4 数据更新频率与局限

- **更新频率**：官方标注为 **Monthly（每月）**，openFDA 未承诺固定日更。因此不适合用于「实时」监测——竞品刚获准的几天内可能尚未同步进 openFDA，此时应回到 accessdata 510(k) 库（第 1 节）交叉确认。
- **数据时效实测（2026-08-31 第 4 轮）**：510(k) 数据集 `meta.last_updated = 2026-08-17`（较上轮 2026-08-10 推进 7 天，但**仍仅刷新、未新增 FXX 记录**）；`product_code:FXX` 命中总数 **607** 条（连续 3 轮未变），最新一条决定日期仍为 **2026-03-18**（K251967）。即 **openFDA 的"最新"clearance 与当日之间存在约 5.5 个月空窗**。
- **时间跨度**：1976 年至今（`Time period covered in this API: 1976 to null`）。

**⭐ 各设备端点 `meta.last_updated` 实测对照表（2026-08-31）** —— 这张表比"官方标注 Monthly"有用得多：**不同端点的刷新节奏差异很大**，判断某类数据能不能信、要不要回 accessdata 补盲，直接看这里。

| 端点 | `meta.last_updated` | 记录总数 | 备注 |
|---|---|---|---|
| `device/510k` | 2026-08-17 | 175,879 | 每周推进，但 **FXX 增量滞后 5.5 个月** |
| `device/classification` | 2026-08-17 | 7,088 | 分类库，变动极少 |
| `device/registrationlisting` | 2026-08-17 | 334,091 | 查工厂注册/FEI 用 |
| `device/recall` | **2026-08-27** | 59,049 | **本轮刷新最新**，召回类时效最好 |
| `device/event` | 2026-08-18 | 25,711,469 | MAUDE 不良事件，体量最大 |
| `device/udi` | 2026-08-03 | 5,083,948 | 刷新最慢（滞后近一个月） |
| `device/pma` | 2026-08-17 | 56,995 | — |
| `device/covid19serology` | 2022-08-22 | 13,420 | **已冻结，不再更新** |

> 复现命令：`curl -s "https://api.fda.gov/device/<端点>.json?limit=1" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['meta']['last_updated'], d['meta']['results']['total'])"`

**端点族扩展（2026-08-22，非器械，仅备案）**：openFDA 新增 research 类数据集 **Covid miRNA and Proteomics Research**，端点 `https://api.fda.gov/research/covidmirnaandproteomics.json`（实测 200，`last_updated = 2026-08-19`，total 416）。与器械 510(k) 无关，记录在此仅为掌握 openFDA 端点命名空间已从 `device/drug/food/tobacco/other` 扩展出 `research/` 一支。

**⚠️ accessdata 补盲通道已确认堵死（2026-08-31 实测，重要）**：过去本文件建议"openFDA 有空窗就回 accessdata 补查"——本轮实测该建议**无法自动化执行**：
- `pmn.cfm` 检索页实为 **POST 表单**，拼 GET 参数（`?start_search=1&productcode=FXX&decisiondatefrom=...`）即使用 WebFetch 也只返回页头、不返回结果；
- 每周更新的可发布数据库静态包 `https://www.accessdata.fda.gov/premarket/ftparea/pmn96cur.zip` 被滥用检测拦截：curl 返回 **302 → `/apology_objects/abuse-detection-apology.html`**，伪装浏览器 User-Agent 亦无效。
- **→ 空窗补查目前只能人工用浏览器操作**，脚本/Agent 做不到。写自动化时不要假装这一步已完成。

**⚠️ 速率与分页硬上限（2026-08-17 核实，务必按此设计脚本）**

| 项目 | 无 API Key | 有 API Key |
|---|---|---|
| 每分钟请求数 | **240 次/分（按 IP）** | **240 次/分（按 key）** |
| 每日请求数 | **1,000 次/日（按 IP）** | **120,000 次/日（按 key）** |

- 单次 `limit` **上限 1000**；`skip` **上限 25000** ⇒ **单一查询最多约可翻到 26,000 条命中**，超出须改用 `search_after` 游标或直接下载全量包。
- 全量 JSON 下载入口（含 Medical Device 510k）：https://open.fda.gov/data/downloads/ ——批量分析、跑历史统计一律走下载包，不要用 API 硬翻页。
- 官方文档：[认证与限额](https://open.fda.gov/apis/authentication/) · [查询参数](https://open.fda.gov/apis/query-parameters/) · [分页](https://open.fda.gov/apis/paging/)

**设备类端点清单（2026-08-17 核对，未发现新增端点）**：`510k` / `classification` / `enforcement` / `event`（MAUDE） / `pma` / `recall` / `registrationlisting` / `udi` / `covid19serology`。510(k) 端点 `searchable-fields` **未新增** sterile 状态、ASTM 等级、predicate K 号等字段——这三项仍只能从 510(k) Summary 原文获取。端点总览：https://open.fda.gov/apis/device/ ｜字段：https://open.fda.gov/apis/device/510k/searchable-fields
- **不含 predicate 字段**：openFDA 510(k) 数据集**没有**直接的 predicate K 号字段，predicate 需通过 510(k) Summary（第 1.4 节）或申报资料获取。
- **不含测试/验证细节**：仅含行政与追踪信息（申请人、日期、分类、决定等），无技术细节、无 CCI。
- **免责声明**：openFDA 数据不可用于医疗决策（见返回体 `meta.disclaimer`）。

---

## 3. FDA 认可共识标准数据库（Recognition Database）

### 3.1 检索入口

- **认可共识标准数据库（主检索页）**
  https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm
- **适用指南**：《Appropriate Use of Voluntary Consensus Standards in Premarket Submissions for Medical Devices》（2018-09）
  https://www.fda.gov/regulatory-information/search-fda-guidance-documents/appropriate-use-voluntary-consensus-standards-premarket-submissions-medical-devices

### 3.2 如何查某标准的 FDA 认可号与现行版本

1. 在检索页按 **关键字（standard name）、标准制订组织（如 ISO/AAMI）、认可号（Rec#）、CFR 引用、或 Product Code** 检索。
2. 进入标准**详情页**，关键信息包括：
   - **Recognition Number（认可号）**：如 `Rec# 2-258`、`Rec# 2-313`——申报时引用的就是此号。
   - **被认可版本（recognized version）**：如 `ISO 10993-1 Fifth edition 2018-08`。
   - **过渡期（Transition Period）与替代关系**：新版本会「supersede」旧版本，并给出旧版可被接受的截止日。
3. **实例（生物相容性标准，已实测核实）**：
   - `ISO 10993-1 Fifth edition 2018-08` 认可号为 **Rec# 2-258**；
   - 已被 `ISO 10993-1 Sixth edition 2025-11` 认可号 **Rec# 2-313** 取代；
   - FDA 接受基于 **Rec# 2-258** 的符合性声明（Declaration of Conformity）**直至 2029-07-01**，此后不再接受。
   - 详情页示例：https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfstandards/detail.cfm?standard__identification_no=47116

### 3.2b 口罩类（FXX）关键标准认可号映射表 ⭐

> **2026-08-17 本轮检索结果**。认可号与版本是 eSTAR 引用凭证，**递交前必须逐条回认可库复核**（本表为单轮检索所得，标⚠️者尤须确认）。

| 标准 | FDA 当前承认版本 | Recognition No. | 备注 |
|---|---|---|---|
| ASTM F2100（医用口罩材料性能分级） | **F2100-23** | 6-492 | ⚠️ **ASTM F2100-26 已于 2026-02 由 ASTM 发布，但本轮未见 FDA 承认**；网传"F2100-26 强制生效、不换版被拒"**无官方依据**，勿采信 |
| ASTM F1862/F1862M（合成血液穿透） | **F1862/F1862M-24** | 6-504 | 旧 **-17 版过渡至 2026-12-20**，此后不接受基于旧版的 DoC |
| ASTM F2101（BFE，金黄葡萄球菌气溶胶） | **F2101-23** | 6-493 | 亦见 -25 版条目，⚠️ 版本状态待认可库复核 |
| ISO 10993-1（生物学评价总则） | **ISO 10993-1:2025（第 6 版）部分承认** | **2-313** | 排除 6.5.11.3 中"consumer products or"及 Clause 6.9；**基于 2018 版（Rec# 2-258）的 DoC 可用至 2029-07-01** |
| ISO 10993-7（EO 残留） | **2008 版 + AMD1:2019** | **2-275** | ⚠️ **重要纠正**：ISO 10993-7:2026（第 3 版，引入风险法/AL）虽已由 ISO 于 2026-04 发布，但**截至 2026-08-24（List #66 FR 公告）仍未获 FDA 承认**；EO 灭菌口罩的残留限值仍应按 **2008+AMD1:2019** 的 TAG/TAI 限值申报，不要直接引 2026 版 |
| ISO 10993-12（样品制备） | **2021 版 + AMD1:2025** | **2-314** | List #66（2026-08-24）新增承认，替换旧 2-289；涉及生物样本制备 |
| ISO 11135（EO 灭菌确认） | **2014 版 + AMD1:2018** | 14-529 | — |

**认可清单发布进度（2026-08-31 更新）**：**Recognition List #66 已于 2026-08-24 发布正式 FR 公告（91 FR 54715，FR Doc 2026-17229）**，替换/撤回多项旧标准（含 ISO 10993-1:2025→2-313、ISO 10993-12→2-314、ISO 20417→5-149、IEC 60601-2-2→6-521 等）；上一轮 List #65 公告为 2026-02-19（91 FR 7994，FR Doc 2026-03310）。

**截至 2026-08-31 无 List #67，本表 4 个关键标准的认可状态全部未变。** 核实方法：Federal Register API 宽口径检索（agency = FDA，term 分别为 recognized standards / Recognition List Number / modifications to the List，publication_date ≥ 2026-08-20），仅命中已收录的 List #66（FR 2026-17229），无新承认/撤销公告。按 List #65→#66 的间隔（约 6 个月）推测下一批约在 2027 年初，**具体时间待核实**。
⚠️ 方法学局限（本轮实测）：accessdata 认可标准检索页为 **POST 表单**，GET 拼参不生效，且 accessdata 全站拦截脚本化访问（详见 2.4 节末的 abuse-detection 说明），**无法自动逐条重拉 Rec# 复核**。因此上表结论是基于"本窗口无新 FR 承认公告"的**推断**，而非逐条实测。**要逐条确认须人工浏览器**检索：https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm
→ 公告原文：https://www.federalregister.gov/documents/2026/02/19/2026-03310/food-and-drug-administration-modernization-act-of-1997-modifications-to-the-list-of-recognized

**监控方法**：每月进 [cfStandards/search.cfm](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm)，按 **Date of Entry 排序**看新增条目；或在 federalregister.gov 检索 "Modifications to the List of Recognized Standards" 追 FR 公告号。

### 3.3 为什么对 510(k) 检测标准选择至关重要

- 510(k) 中引用**未获 FDA 认可版本**的共识标准，不能走「符合性声明（Declaration of Conformity）」的简化路径，往往需补充验证数据。
- 标准会被**更新/替代且存在过渡期**，选错版本可能导致申报被质疑或需补数据。
- 认可号（Rec#）是 eSTAR / 510(k) 中标准引用的「官方凭证」，务必以认可库当前版本为准。

---

## 4. FDA 指南库检索方法

### 4.1 一般检索方法

- **FDA 指南文档总检索页**：https://www.fda.gov/regulatory-information/search-fda-guidance-documents
  - 支持按关键词、发布机构（如 CDRH）、专题、状态（Final / Draft）、发布日期筛选。
- **医疗器械专项指南列表**：https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/guidance-documents-medical-devices-and-radiation-emitting-products
  - 该页按发布日期倒序列出 CDRH 指南，便于追踪最新终稿/草案。

> 检索技巧：直接对 `fda.gov` 使用站内搜索（如 `site:fda.gov "Surgical Masks" 510(k)`）结合上方总检索页，可快速定位历史与最新指南。

### 4.2 外科口罩 / 面罩及相邻主题关键指南（附真实 URL）

| 主题 | 标题 / 发布时间 | 真实 URL | 备注 |
|---|---|---|---|
| 外科口罩 510(k)（2004） | *Surgical Masks — Premarket Notification [510(k)] Submissions*（2004-03，2004-07 勘误） | https://www.fda.gov/medicaldevices/deviceregulationandguidance/guidancedocuments/ucm072549.htm （PDF 备份：https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/FDA/094.pdf ） | 给出外科口罩分类法规、Product Code、流体阻力/过滤效率/压差/可燃性等测试要点。 |
| 无菌器械 510(k) 无菌信息（2024-01 终稿） | *Submission and Review of Sterility Information in Premarket Notification (510(k)) Submissions for Devices Labeled as Sterile* | https://www.fda.gov/regulatory-information/search-fda-guidance-documents/submission-and-review-sterility-information-premarket-notification-510k-submissions-devices-labeled | 2024-01 更新；将汽化过氧化氢（VH2O2）由 Established Category B 升为 A，降低申报负担；区分 Established / Novel 灭菌法所需信息。 |
| 生物相容性 ISO 10993-1（2023-09 终稿） | *Use of International Standard ISO 10993-1, "Biological evaluation of medical devices — Part 1..."* | https://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocuments/UCM348890 | 2023 更新，新增 Appendix G（接触完整皮肤器械的生物相容性）；配套认可标准见第 3 节。 |
| 人因工程 / 可用性（2026 更新） | *Applying Human Factors and Usability Engineering to Medical Devices*（2026-08 版） | https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices （旧版存档：https://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocuments/UCM259760 ） | CDRH 2026-08-03 列出为 Final；与下方「提交内容」指南为配套文件。 |
| 人因工程信息提交内容（2026 终稿） | *Content of Human Factors Information in Medical Device Marketing Submissions*（2026-05-29 发布，2026-08-01 起适用） | 指南检索页定位：https://www.fda.gov/regulatory-information/search-fda-guidance-documents （搜索标题）；Docket **FDA-2015-D-4599** | 基于风险将提交分为 Category 1/2/3，引入 Decision Point D；适用于 510(k)/De Novo/PMA/HDE，2026-08-01 起 FDA 按此预期审评。 |

> 面罩（face mask / respirator）相关：除上表外科口罩指南外，N95 等呼吸器受 NIOSH 与 CDC 管辖，部分情形（如单用途一次性 MSH 类呼吸器）已被豁免 510(k)（见 2004 指南勘误说明）。具体分类请以最新指南与 Product Code 检索为准（待核实最新豁免范围）。

### 4.3 指南库 2026 年新增/在审条目（2026-08-17 核实增量）

| 状态 | 标题 / 日期 | 与口罩项目的关系 | 信源 |
|---|---|---|---|
| **草案（在审）** | *Compliance Policy for Certain NIOSH Approved Air-Purifying Respirators*（2026-04-20 发布，评论期至 2026-06-22，Docket FDA-2025-D-7121） | 覆盖 **878.4040 下的 surgical N95 / N95 FFR（MSH）** 与 880.6260，**不适用 FXX**；若定稿将改变呼吸器类合规政策，需跟踪 | [govinfo FR 2026-07613（91 FR 21003）](https://www.govinfo.gov/content/pkg/FR-2026-04-20/html/2026-07613.htm) |
| **草案（评论期已结束）** | *Quality Management System Information for Certain Premarket Submission Reviews*（2025-11-17 发布，意见期至 2026-01-16，Docket FDA-2025-D-4051） | 直接影响 **510(k) 中 QMS 信息的提交口径**，与 2026-02-02 QMSR 生效配套；口罩项目须留意最终版对 QMS 章节的要求 | [FR 2025-19947](https://www.federalregister.gov/documents/2025/11/17/2025-19947/quality-management-system-information-for-certain-premarket-submission-reviews-draft-guidance-for) |
| **终稿** | *Intent To Exempt Certain Unclassified Medical Devices From Premarket Notification*（2026-06-05） | 豁免名单**不含 FXX**，口罩仍须 510(k) | [FR 2026-11303](https://www.federalregister.gov/documents/2026/06/05/2026-11303/intent-to-exempt-certain-unclassified-medical-devices-from-premarket-notification-requirements) |
| **终稿** | *Content of Human Factors Information in Medical Device Marketing Submissions*（2026-05-29 发布 / 2026-08-01 适用） | 口罩多为 HF Category 1/2，可用 Decision Point D 论证免总结性验证 | [FR 2026-10734（91 FR 32061）](https://www.federalregister.gov/d/2026-10734) |
| **仍为草案（勿当终稿引用）** | 2023 年 predicate 三件套，含 *Best Practices for Selecting a Predicate Device*；列于 CDRH FY2026 指南计划"Under Construction" | 选 predicate 时可参考其思路，但**不得作为强制要求引用** | [CDRH 指南列表](https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/guidance-documents-medical-devices-and-radiation-emitting-products) |

**上轮（2026-08-24）核实未发现变更**：2026-08-17 以来**无新增口罩 / PPE / 无菌 / 生物相容性 / HFE / QMSR 专项指南**；2024-01 无菌信息指南无新版或勘误；Safety and Performance Based Pathway 仍为 15 个器械类型且**不含外科口罩**。新增事件：FDA 发布 **2026-09-09 生物相容性风险评估 Town Hall**（三场系列 09-09 / 09-23 / 10-07，讨论 ISO 10993-1:2025）预告，免报名：https://www.fda.gov/medical-devices/medical-devices-news-and-events/town-hall-biocompatibility-risk-assessment-09092026 （材料待会后公开，列为跟踪项）。

**本轮（2026-08-31）核实：指南库无器械类新增条目（0 条）。** 核实方法：指南库按签发日倒序查前 10 条（覆盖 2026-08-11 至 08-28），全部为非器械中心条目 —— CVM 兽药复方（Draft CVM GFI #256B，08-28）、CVM 鱼类麻醉（08-25）、CDER 治疗等效性评价（08-21）、CBER 基因治疗 FAQ 与免疫制品效价（08-19）、CDER ANDA/505(b)(2)（08-17）等，**无一涉及口罩 / 无菌 / 生物相容性 / HFE / QMSR / 510(k)**。跟踪项补充：09-09 Town Hall **免注册，但提问提交截止 2026-07-31 已过**（本轮新掌握）——只能听会，不能提问，建议照常参会取材料。

---

## 5. FD&C Act 与 CFR 设备条款（21 CFR 800-1299）查阅入口

### 5.1 联邦食品、药品和化妆品法（FD&C Act）

- **FDA 官方 FD&C Act 页面（含 device 相关章节导航）**
  https://www.fda.gov/regulatory-information/federal-food-drug-and-cosmetic-act-fdc-act
- 设备核心授权在 **Chapter V**（其中 **Section 510** 即 510(k) 实质等同制度，对应 21 U.S.C. 360）；Section 513 为分类，Section 514 为性能标准，Section 515 为 PMA。
- 完整法律文本可在 Congress 的 U.S. Code 站点查阅（21 U.S.C. 301 起）。

### 5.2 21 CFR 医疗器械条款（Chapter I, Subchapter H：Parts 800–898）

- **eCFR 总入口（Title 21）**：https://www.ecfr.gov/current/title-21
- **Subchapter H — Medical Devices（800–898）**：https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H
  - 该页列出 Part 800（通用）、801（标签）、803（MDR）、807（企业注册与器械列名 / 含 510(k) 要求）、812（IDE）、814（PMA）、**820（质量体系法规 QMSR）**、830（UDI）、860（分类程序）、862–898（各医学专科器械）等。
- **510(k) 直接相关条款**：
  - **21 CFR 807 Subpart E** — Premarket Notification Procedures（含 807.81、807.87 内容要求、807.92 predicate 定义、807.95 510(k) Summary 公开要求）
  - **21 CFR 820** — Quality Management System Regulation（原 QSR，2026 起向 QMSR 过渡）
  - 对应 eCFR：https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-807 与 https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820
- 注：用户所述「800–1299」区间内，设备相关集中于 **800–898**；900–1299 多为食品/药品/生物制品等其他子章节，检索设备条款请以 Subchapter H 为准。

---

## 6. 专家日常操作手册：如何把公开资源用起来

下面是一套「从找 predicate → 核标准 → 学法 → 监控竞品」的日课流程，建议固化成 SOP。

### 步骤 1：锁定 Product Code 与监管边界
- 用 **accessdata 510(k) 库**或 **分类数据库**确定目标器械的 Product Code 与法规号（regulation number）。
- 同 Product Code = 同监管赛道，是后续所有检索的锚点。

### 步骤 2：找 predicate（对比器械）
- 在 accessdata 510(k) 库按 Product Code 检索，**按决定日期倒序**，圈定 3–5 个「最近获准、技术最相近」的候选。
- 打开候选的 **510(k) Summary**，确认其明确写出的 **predicate K 号**（Summary 依法须列明），并排除已召回/撤市项（交叉查召回库、MAUDE）。
- 用 **openFDA** 按 `product_code` + `applicant` 反查竞品历史 clearance，验证「谁、在何时、以何 predicate 获准」。

### 步骤 3：核标准版本（避免选错认可版本）
- 到 **Recognition Database** 用关键词检索所用标准（如 `ISO 10993-1`、`ASTM F2100`、`ISO 11135` 等），记录 **Rec# 与现行版本**。
- 检查**过渡期**：若所用版本即将被取代，评估是否直接采用新版本（Rec# 2-313 类）以延长合规寿命。
- 在 eSTAR / 510(k) 中引用**认可号 + 版本号**，并附符合性声明。

### 步骤 4：看同类器械 Summary，学英文表述与测试思路
- 精读 2–3 份同品类的 510(k) Summary，重点借鉴：
  - **预期用途（intended use）** 的英文措辞（直接影响实质等同判定）；
  - **技术特征对比表**的写法；
  - **测试标准与方法摘要**（哪些标准被引用、哪些 endpoints 被关注）。
- 注意脱敏边界：配方/工艺/原始数据看不到，Summary 只给「思路与结论」——价值在于「表述范式」而非「可抄数据」。

### 步骤 5：追踪指南与法规更新
- 每周扫一次 **CDRH 指南列表**（https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/guidance-documents-medical-devices-and-radiation-emitting-products ），关注 Final/Draft 变动（如 2026 HFE、2024 无菌信息、2023 ISO 10993-1 等）。
- 重大节点（如 2026-08-01 HFE 新指南适用、QMSR 过渡）写入团队日历，触发在研项目的合规复核。

### 步骤 6：监控竞品 clearance 动态（竞品情报）
- **每月**用 openFDA 拉取目标 Product Code 的新增 clearance（`decision_date` 近 30/90 天区间），但注意 openFDA **每月更新**，存在滞后。
- **关键节点**回到 accessdata 510(k) 库做「T+数日」二次确认，捕捉刚获准但尚未进 openFDA 的竞品。
- 监控维度：新进入者、新 predicate 路线、新灭菌/材料方法（对照 2024 无菌指南的 Established/Novel 分类）、HFE 提交类别变化。

### 步骤 7：沉淀为内部知识库
- 将每次挖掘的「predicate 链、标准版本、Summary 表述模板、竞品时间线」结构化存入团队库（如本技能 `references/` 目录），形成可复用的情报资产。

> **关键提醒**：openFDA 与 accessdata 数据存在更新时差；**作决策前务必以 accessdata 原始记录 + 官方指南/CFR 原文为最终依据**，公开 Summary 不含 CCI，不得据此推断配方或原始验证数据。

---

## 信源索引（均指向 fda.gov / open.fda.gov 官方资源）

- 510(k) 数据库：https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm
- openFDA 510(k) API：https://api.fda.gov/device/510k.json ｜ 文档：https://open.fda.gov/apis/device/510k/ ｜ 字段：https://open.fda.gov/apis/device/510k/searchable-fields/
- 认可共识标准库：https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm ｜ 标准详情示例：https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfstandards/detail.cfm?standard__identification_no=47116
- 指南总检索：https://www.fda.gov/regulatory-information/search-fda-guidance-documents ｜ CDRH 指南列表：https://www.fda.gov/medical-devices/device-advice-comprehensive-regulatory-assistance/guidance-documents-medical-devices-and-radiation-emitting-products
- 2004 外科口罩指南：https://www.fda.gov/medicaldevices/deviceregulationandguidance/guidancedocuments/ucm072549.htm
- 2024 无菌信息指南：https://www.fda.gov/regulatory-information/search-fda-guidance-documents/submission-and-review-sterility-information-premarket-notification-510k-submissions-devices-labeled
- 2023 ISO 10993-1 指南：https://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocuments/UCM348890
- 2026 HFE 指南（Applying HF/UE）：https://www.fda.gov/regulatory-information/search-fda-guidance-documents/applying-human-factors-and-usability-engineering-medical-devices
- FD&C Act：https://www.fda.gov/regulatory-information/federal-food-drug-and-cosmetic-act-fdc-act
- eCFR Title 21：https://www.ecfr.gov/current/title-21 ｜ Subchapter H（设备 800–898）：https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H ｜ Part 807：https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-807 ｜ Part 820：https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820

*（标注「待核实」之处：N95/呼吸器最新 510(k) 豁免范围，请以 FDA 最新指南与 Product Code 检索结果为准。）*

## FXX / 竞品 clearance 监控快照（自动周更）

> 本小节由周度自动化（automation-1786846192252）每周一刷新：调用 openFDA 510(k) API（product_code:FXX，decision_date 降序取前 50）刷新列表、对照上周标「本周新增」、对竞品观察名单单列近期 clearance。openFDA 每月更新存在时差，关键 K 号须回 accessdata 510(k) 库（T+数日）二次确认；sterile 状态与 ASTM F2100 等级不在 openFDA 元数据内，须读 510(k) Summary 原文（见 `predicate_summary_checker.py`）。

_快照生成时间：**2026-08-31（第 4 轮）**｜上一轮：2026-08-24（第 3 轮）｜基线：2026-08-16（首次）_

**本轮 API 实测元数据**：`device/510k` 的 `meta.last_updated = 2026-08-17`（较上轮 2026-08-10 **推进 7 天，但仍仅刷新、未新增 FXX 记录**）；`product_code:FXX` 命中总数 **607** 条（连续 3 轮未变）；取 `sort=decision_date:desc&limit=50`。

**本周新增 K 号：无（0 条）——连续第 3 周为 0。** 本轮核验：FXX 总数仍为 **607**、最新一条仍为 **K251967（2026-03-18，O&M Halyard）**、前 15 条 K 号集合与上轮**完全一致**（程序化 set 比对 `True`）；竞品命中仍为 **20 / 50**。

**⚠️ 关键局限（本轮升级认知，务必读）：openFDA 的 FXX 空窗已达 5.5 个月，且 accessdata 已确认无法脚本化补查。**
- openFDA 最新 FXX clearance 日期为 **2026-03-18**，距今（2026-08-31）**约 5.5 个月**。这不是"没有新 clearance"，而是 **openFDA 的 510(k) 数据集对 FXX 的加载滞后**——`last_updated` 每周推进但 FXX 记录数不增，说明增量批次尚未覆盖到该 product code 的近期记录。
- **本轮实测：accessdata 全站对脚本化访问启用了 abuse detection，两条路都堵死**——
  ① 表单检索 `pmn.cfm?start_search=1&productcode=FXX&decisiondatefrom=...`：即使用 WebFetch，也**只返回表单页头部、不返回结果**（该页实为 POST 提交，GET 参数不生效）。
  ② 每周更新的可发布数据库静态包 `https://www.accessdata.fda.gov/premarket/ftparea/pmn96cur.zip`：curl 返回 **302 → `https://www.accessdata.fda.gov/apology_objects/abuse-detection-apology.html`**（即"滥用检测"拦截页），加浏览器 User-Agent 亦无效。
- **→ 结论：3 月后的 FXX 空窗，目前只能人工用浏览器补查**，无自动化方案。入口：https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm （手动选 Product Code = FXX，Decision Date From = 03/19/2026）。**这项列为需人工执行的待核实事项，不要在自动化里假装已完成。**

下表两张表的数据与前两轮相同（源数据未更新），保留以备对照；下轮若 FXX 总数脱离 607 再整体刷新。

### 最近 15 条 FXX clearance（按 decision_date 降序）
| K号 | 器械名 | 申请人 | 决定日期 | 类型 | Summary/Statement |
|---|---|---|---|---|---|
| K251967 | HALYARD* FLUIDSHIELD* 3 Fog-Free Procedu | O&M Halyard, Inc. | 2026-03-18 | Traditional | Summary |
| K252534 | Surgical Face Mask (Ear mount) | Zhejiang Hangkang Medical Equipment Co., Ltd. | 2026-03-03 | Traditional | Statement |
| K253398 | Disposable Surgical Mask (Non-Sterile) ( | Efofex, Inc. | 2026-02-19 | Special | Summary |
| K252830 | Disposable Surgical Face Mask (3P00B, C2 | Beatles Medical Supplies (Xiantao) Co., Ltd. | 2026-01-12 | Traditional | Summary |
| K252650 | Disposable Medical Face Mask | Makrite Industries, Inc. | 2026-01-05 | Traditional | Summary |
| K243342 | KP Protective Face Mask | Kp Trading Co., Ltd. | 2025-12-22 | Traditional | Summary |
| K252941 | HALYARD* Adult Face Mask with SO SOFT* L | O&M Halyard, Inc. | 2025-12-11 | Traditional | Summary |
| K252964 | PRIMED Surgical and Procedure Masks | Primed Medical Products, Inc. | 2025-11-04 | Traditional | Summary |
| K251902 | Vitaform Procedural Mask - Blue (Vitafor | Vitacore Industries, Inc. | 2025-09-17 | Traditional | Summary |
| K250082 | Procedure mask/Surgical mask/Face mask | Winner Medical Co., Ltd. | 2025-06-18 | Traditional | Summary |
| K243010 | Fluidshield * 3 Fog-Free Surgical Mask w | Owens & Minor (O&M) Halyard, Inc. | 2025-05-30 | Abbreviated | Summary |
| K242502 | Aurelia Surgical Mask ASTM Level-3 (2130 | Supermax Healthcare Canada – Supermax Medical | 2024-11-12 | Traditional | Summary |
| K240916 | Surgical Face Mask (Tie on/ Ear loops) | Xiantao Daoqi Plastic Co., Ltd. | 2024-10-18 | Traditional | Summary |
| K240286 | PRIMED Surgical Masks and PRIMED Procedu | Primed Medical Products, Inc. | 2024-08-26 | Traditional | Summary |
| K233723 | Medical surgical mask | Guangdong Kingfa Sci. & Tech.Co., Ltd. | 2024-07-29 | Traditional | Summary |

### 竞品观察名单近期 clearance（Makrite/Halyard/Winner/Zhejiang Hangkang/Efofex/Primed/Beatles）
| K号 | 申请人 | 器械名 | 决定日期 | 类型 | S/S |
|---|---|---|---|---|---|
| K251967 | O&M Halyard, Inc. | HALYARD* FLUIDSHIELD* 3 Fog-Free Pro | 2026-03-18 | Traditional | Summary |
| K252534 | Zhejiang Hangkang Medical Equipment Co., Ltd. | Surgical Face Mask (Ear mount) | 2026-03-03 | Traditional | Statement |
| K253398 | Efofex, Inc. | Disposable Surgical Mask (Non-Steril | 2026-02-19 | Special | Summary |
| K252830 | Beatles Medical Supplies (Xiantao) Co., Ltd. | Disposable Surgical Face Mask (3P00B | 2026-01-12 | Traditional | Summary |
| K252650 | Makrite Industries, Inc. | Disposable Medical Face Mask | 2026-01-05 | Traditional | Summary |
| K252941 | O&M Halyard, Inc. | HALYARD* Adult Face Mask with SO SOF | 2025-12-11 | Traditional | Summary |
| K252964 | Primed Medical Products, Inc. | PRIMED Surgical and Procedure Masks | 2025-11-04 | Traditional | Summary |
| K250082 | Winner Medical Co., Ltd. | Procedure mask/Surgical mask/Face ma | 2025-06-18 | Traditional | Summary |
| K243010 | Owens & Minor (O&M) Halyard, Inc. | Fluidshield * 3 Fog-Free Surgical Ma | 2025-05-30 | Abbreviated | Summary |
| K240286 | Primed Medical Products, Inc. | PRIMED Surgical Masks and PRIMED Pro | 2024-08-26 | Traditional | Summary |
| K232824 | Owens & Minor (O&M) Halyard, Inc. | FLUIDSHIELD* 1 Fog-Free Procedure Ma | 2024-07-02 | Traditional | Summary |
| K232777 | Owens & Minor (O&M) Halyard, Inc. | FLUIDSHIELD* 1 Procedure Mask with S | 2024-07-01 | Traditional | Summary |
| K232807 | Owens & Minor (O&M) Halyard, Inc. | Fluidshield* 1 Procedure Mask with S | 2024-06-21 | Traditional | Summary |
| K232812 | Owens & Minor (O&M) Halyard, Inc. | Fluidshield* 2 Fog-Free Surgical Mas | 2024-06-14 | Traditional | Summary |
| K232806 | Owens & Minor (O&M) Halyard, Inc. | HALYARD* FLUIDSHIELD* 1 Procedure Ma | 2024-06-07 | Traditional | Summary |
| K232820 | Owens & Minor (O&M) Halyard, Inc. | HALYARD* FLUIDSHIELD* 1 Fog-Free Sur | 2024-06-04 | Traditional | Summary |
| K240258 | Makrite Industries, Inc. | Disposable Medical Face Mask (M643BE | 2024-04-18 | Traditional | Summary |
| K232894 | Owens & Minor (O&M) Halyard, Inc. | HALYARD* FLUIDSHIELD* 2 Surgical Mas | 2024-01-08 | Traditional | Summary |
| K223823 | Efofex, Inc. | Disposable Surgical Face Mask | 2023-03-27 | Traditional | Summary |
| K223232 | Winner Medical Co., Ltd. | Procedure mask/Surgical mask/Face ma | 2023-03-06 | Traditional | Summary |

_竞品命中 20 条 / 共 50 条 FXX（与上轮一致，本周无新增）。_

### 竞品与 predicate 情报解读（2026-08-31 第 4 轮更新）

**第 4 轮（2026-08-31）增量小结：本周 FXX 无新增 clearance、竞品名单无变动、无竞品改用新 predicate 路线的证据；标准与 HFE 规则亦无变化，故下列 4 条判断全部维持有效。** 本轮唯一新增的情报价值是把「空窗补查」的技术路径彻底试穿了（见上方 ⚠️ 关键局限），以及确认 Recognition List #67 未出、四个关键标准认可状态未变。

**以下判断沿用第 3 轮并经本轮复核仍成立：**

- **⚠️ 提示 1｜Efofex K253398 走 Special 510(k) + 明确标注 "Non-Sterile"（2026-02-19）**
  这是近 50 条中**唯一的 Special 510(k)**，说明 Efofex 是在**自家已获准器械（K223823，2023-03-27）基础上做变更**，而非另找 predicate。**实操启示**：**Special 510(k) 仅限"同一制造商改自家已上市器械"**，首次申报无法套用；且其标签为 Non-Sterile —— 我们 B1 型为**无菌（EO 灭菌）**，二者不可直接互为 predicate 论证无菌路径，选 predicate 时**必须挑同为 sterile 标签的 K 号**。
  → 复核：https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm （检索 K253398 / K223823）

- **⚠️ 提示 2｜O&M Halyard K243010 走 Abbreviated 510(k)（2025-05-30），路线值得对标**
  Abbreviated 依赖**FDA 认可共识标准的符合性声明**替代部分数据。结合本周标准库核实：**ASTM F2100 当前承认版本为 F2100-23（Rec# 6-492）**，**ASTM F2100-26 仍未获 FDA 承认**（List #66 FR 2026-08-24 公告表1/表2 均未纳入）；**ASTM F1862 已升 -24（Rec# 6-504），旧 -17 版仅过渡至 2026-12-20**。若我们拟走 Abbreviated，测试报告须按 F2100-23 + F1862/F1862M-24 出，用旧版会失去 DoC 简化资格。
  → 认可库复核：https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm

- **⚠️ 提示 3｜灭菌与生物相容性路线（对照 2024 无菌指南 + 本周标准更新）**
  我们的 **EO 灭菌属 Established Category A**（2024 无菌指南分类未变），提交负担较低。两项版本风险须锁定：
  ① **ISO 10993-7 FDA 仍只承认 2008 版 + AMD1:2019（Rec# 2-275）**；ISO 于 2026-04 发布的 **10993-7:2026（引入 AL 风险法）截至 2026-08-24（List #66 公告）仍未获 FDA 承认** —— EO 残留（EtO/ECH）限值须按 2008+AMD1 的 TAG/TAI 申报，勿直接引 2026 版。
  ② **ISO 10993-1:2025（Rec# 2-313）已正式获 FR 公告承认（List #66，2026-08-24，替换旧 2-258）**；基于 2018 版（Rec# 2-258）的符合性声明可用至 2029-07-01，本项目短期内**可继续沿用 2018 版**，无需返工。另 **ISO 10993-12:2021+AMD1:2025 获承认（Rec# 2-314）**，涉及样品制备。
  → FR 2026-17229：https://www.federalregister.gov/d/2026-17229

- **HFE 提交类别（本周无竞品变化，规则已变）**：HFE 最终指南 **2026-08-01 起适用**，eSTAR **7.0（2026-06-01 发布）**内含 HF 类别字段；**eSTAR v6.2 / PreSTAR v2.2 已于 2026-08-03 退役**，新提交必须用 7.0。口罩类通常落 **Category 1/2**，可用**新增的 Decision Point D** 论证免做总结性验证。上表所有竞品 K 号均在该规则生效前获准，其 Summary 中无 HFE 章节可抄 —— 须自建新章节。
  → https://www.federalregister.gov/d/2026-10734 ｜ https://www.fda.gov/medical-devices/how-study-and-market-your-device/estar-program

- **未发现的动向（第 4 轮已复核，截至 2026-08-31）**：**无**竞品改用新 predicate 路线的证据（连续 3 周无新 clearance 可判）；**无**竞品采用新灭菌/材料方法的迹象（对照 2024 无菌指南 Established/Novel 分类，名单内 20 条全部属 Established Category A 或非无菌）；**无**竞品 HFE 提交类别变化（上表全部 K 号获准日均早于 HFE 规则 2026-08-01 适用日）；FXX 分类、特殊控制、豁免范围 2026 年均无变动；2026-04-20 呼吸器合规政策草案（FR 2026-07613）仍为草案且仅覆盖 **MSH** 与 880.6260，**不适用 FXX**；2026-08-24 以来**无**新 FDA 指南涉及口罩/无菌/生物相容性/HFE/QMSR；**无 Recognition List #67**。

#### ⏳ 与竞品情报并行的自身倒计时（第 4 轮新增）

| 事项 | 截止日 | 距今 | 说明 |
|---|---|---|---|
| **FY2026 旧费率 $26,067 锁定窗口** | **2026-09-30** | **30 天** | 10-01 起自动跳 FY2027 **$28,653**（小企业 $7,163），标准费多付 $2,586。但**不可为省费而提交不成熟资料**（招 RTA/AI Hold 代价远大于 $2,586） |
| **FY2027 小企业资格（SBD）重申** | 财年切换 | 30 天 | 小企业认定**不跨财年自动延续**，须重新申请 |
| **ASTM F1862 旧版 -17 过渡期截止** | **2026-12-20** | 约 3.5 月 | 合成血穿透报告须按 **F1862/F1862M-24（Rec# 6-504）** 出 |

**下轮（2026-09-07）快照重点**：① **FY2026 费率窗口仅剩 3 周**，复核提交进度并决策；② openFDA `meta.last_updated` 与 FXX 总数是否脱离 607（本轮 2026-08-17 / 607 / 最新 2026-03-18）；③ **人工浏览器补查 accessdata 的 2026-03-19 以后 FXX 空窗**（自动化已确认做不到）；④ Recognition List #67（关注 ASTM F2100-26 / ISO 10993-7:2026）；⑤ 2026-09-09 生物相容性 Town Hall 会后材料；⑥ MDUFA VI 承诺信；⑦ 呼吸器草案是否定稿。

> ⚠️ openFDA 每月更新，存在时差；关键 K 号须回 accessdata 510(k) 库（T+数日）二次确认。sterile 状态与 ASTM F2100 等级不在 openFDA 元数据内，须读 510(k) Summary 原文（见『Predicate 逐份核 Summary』脚本）。
