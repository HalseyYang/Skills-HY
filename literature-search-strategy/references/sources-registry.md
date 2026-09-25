# 器械与厂家信息核查 —— 权威源清单与检索技巧

> 配套 `../SKILL.md` 的 Step 0 使用。实用原则：**能用 API 就别抓网页**。

---

## A 组　企业与并购沿革

| 来源 | URL | 能查到什么 | 性质 |
|---|---|---|---|
| SEC EDGAR 全文检索 | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany | 上市公司 8-K（重大事件）、10-K（年报并购附注） | 一手 |
| 企业投资者关系页 | 各公司 IR 站点，如 https://investor.integralife.com | 8-K 原文、收购协议附件、新闻稿 | 一手 |
| 企业新闻中心 | 如 http://newsroom.medtronic.com | 并购完成公告、交易金额、交割日 | 一手 |
| 企业官网 About / History | 各公司官网 | 品牌沿革、事业部设置 | 一手（但可能简略） |
| Wikipedia 企业条目 | https://en.wikipedia.org | 并购时间线速览 | 二手（用于快速定位，需一手核实） |
| Mergr M&A 数据库 | https://mergr.com | 交易日期、金额、买方卖方 | 二手（日期通常准确，可交叉验证） |

**技巧**：并购信息优先找 **8-K**（重大事件即时披露）而非 10-K。
8-K 里会有收购协议全文与交易金额；10-K 的 "Acquisitions" 附注则给出会计确认口径。
两者都有时，交割日以 8-K / 新闻稿为准，金额口径以 10-K 为准。

---

## B 组　美国 FDA

### B1　openFDA API（首选，无需密钥，返回 JSON）

| 端点 | URL 模板 | 用途 |
|---|---|---|
| 510(k) | `https://api.fda.gov/device/510k.json?search=device_name:%22{产品名}%22&limit=100` | 按产品名查全部 510(k) |
| 510(k) 反查同类 | `https://api.fda.gov/device/510k.json?search=product_code:%22{CODE}%22+AND+device_name:%22{关键词}%22&limit=100` | **发现同品种候选** |
| 510(k) 聚合统计 | `https://api.fda.gov/device/510k.json?search=...&count=applicant.exact&limit=50` | 按申请人计数，看竞争格局 |
| 设备分类 | `https://api.fda.gov/device/classification.json?search=product_code:%22{CODE}%22` | Product Code → 设备名、21 CFR、分类、审评组 |
| PMA | `https://api.fda.gov/device/pma.json?search=...` | PMA 批准的器械 |
| UDI / GUDID | `https://api.fda.gov/device/udi.json?search=...` | 器械唯一标识、GMDN 代码 |
| 不良事件 | `https://api.fda.gov/device/event.json?search=...` | 上市后安全信号 |
| 召回 | `https://api.fda.gov/device/recall.json?search=...` | 召回记录 |

**510(k) 返回的关键字段**：
`k_number`（K 号）、`device_name`（设备名）、`applicant`（申请人）、
`product_code`、`decision_date`（决定日期）、`decision_description`（如 Substantially Equivalent）、
`decision_code`（SESE / DENY 等）、`city` / `state`、`date_received`、`submission_type_id`。

**⚠ openFDA 510(k) 数据集不含 predicate 字段。** 要拿对比器械（Predicate Device）
必须去 accessdata 网页端人工读，或下载 510(k) Summary PDF。

**技巧**：`search` 支持 `+AND+` / `+OR+` / `+NOT+`，字段名后加 `.exact` 做精确匹配；
`count=字段名.exact` 做聚合。返回体 `meta.last_updated` 会告诉你数据新鲜度。

### B2　FDA 网页端（需浏览器，程序化请求会被拒）

| 页面 | URL 模板 | 能查到什么 |
|---|---|---|
| 510(k) 详情 | `https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K{号码}` | **Predicate Device**、Indications for Use 全文、510(k) Summary |
| 510(k) Summary PDF | `https://www.accessdata.fda.gov/cdrh_docs/pdf{YY}/K{号码}.pdf` | 实质等同对比表全文 |
| 器械总库 | https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/device.cfm | 按 product code 浏览 |
| GUDID | https://accessgudid.nlm.nih.gov/ | UDI-DI、GMDN 代码 |

---

## C 组　中国 NMPA

| 来源 | URL | 能查到什么 | 性质 |
|---|---|---|---|
| NMPA 数据查询（总入口） | https://www.nmpa.gov.cn/datasearch/home-index.html | 注册证号、注册人、适用范围、结构组成、型号 | 一手 |
| 医疗器械电子申报（eRPS） | https://erps.nmpa.gov.cn | 申报目录 | 一手 |

**⚠ NMPA 数据查询对程序化请求返回 HTTP 412。**
必须浏览器人工访问。退而求其次可用第三方转载（贝登医疗、环球医药网、药智网等），
但一律标注**二手·待 NMPA 官网复核**。

**⚠ 同一品牌名下可能存在多张证，适用范围完全不同。**
必须在核查阶段把全部证列出并比对适用范围，再让用户确认申报对象。
实例：某进口射频消融产品有两张证 ——
`注册证 A`（软组织消融：经皮/腹腔镜/外科手术中的凝血和消融）与
`注册证 B`（骨转移瘤疼痛：骨内肿瘤组织消融，不用于颅骨）。
若不看证只按品牌检索，部位词会混进另一适应证的词。

---

## D 组　欧盟与其他

| 来源 | URL | 能查到什么 |
|---|---|---|
| EUDAMED | https://ec.europa.eu/tools/eudamed | 欧盟器械注册、经济运营者、证书 |
| NANDO | https://webgate.ec.europa.eu/single-market-compliance-space/#/notified-bodies | 公告机构编号与资质范围 |
| 各国监管机构 | MHRA / Health Canada / TGA / ANVISA / PMDA 等 | 当地注册记录 |

---

## E 组　编码与术语标准

| 来源 | URL | 能查到什么 |
|---|---|---|
| GMDN Agency | https://www.gmdnagency.org/ | GMDN 术语代码与定义 |
| FDA GUDID | https://accessgudid.nlm.nih.gov/ | UDI-DI 与 GMDN 对照 |
| UMLS / MeSH | https://www.nlm.nih.gov/mesh/ | 用于 PubMed 主题词扩展 |

---

## 反爬实测记录（2026-09-03）

| 目标 | 程序化请求结果 | 应对 |
|---|---|---|
| `api.fda.gov`（openFDA API） | ✅ 200，正常返回 JSON | **首选通道** |
| `www.accessdata.fda.gov`（网页 + PDF） | ❌ HTTP 418 | 浏览器人工读取；或用 WebSearch 找转载 |
| `www.medtronic.com` | ❌ 返回 "Incorrect Browser" 拦截页 | 浏览器人工访问 |
| `www.nmpa.gov.cn/datasearch` | ❌ HTTP 412 | 浏览器人工访问 |
| SEC EDGAR / 企业 IR 页 | ✅ 多数可访问 | 一手并购信息主通道 |
| Wikipedia / 行业站点 | ✅ 可访问 | 用于定位线索，结论需一手核实 |

**结论**：监管数据库分两类 —— 有 API 的（openFDA）走 API；
只有网页的（accessdata、NMPA）一律浏览器人工核对，拿不到就退二手源并明确标注「待复核」。

---

## 检索顺序建议

```
1. openFDA 510(k) 按产品名检索      → 产品英文全名 + 厂家历史名称（applicant 去重）
2. openFDA classification 按 product code → 分类代码、21 CFR、管理类别
3. openFDA 510(k) 按 product code 反查   → 同品种器械候选
4. SEC EDGAR / 企业 IR             → 并购沿革一手证据
5. NMPA 数据查询（浏览器）           → 注册证、适用范围、型号
6. accessdata（浏览器）             → Predicate Device、Indications for Use 全文
7. GUDID / GMDN                   → 术语代码
```

每一步的结果都写进溯源表，附完整 URL 与置信度。
