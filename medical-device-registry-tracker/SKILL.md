---
name: medical-device-registry-tracker
description: >
  医疗器械法规追踪 Skill。自动检索中国(NMPA/CMDE)、欧盟(EC/MDR/MDCG)、美国(FDA)、加拿大(Health
  Canada)等地区的医疗器械法规更新，生成汇总报告并上传到 IMA 知识库。每周五自动执行。

  使用场景： - "帮我追踪本周医疗器械法规更新" - "生成最新的法规周报" - "查看本周FDA指南动态" - "追踪欧盟MDR指南更新" -
  自动化：每周五 8:30 自动检索并上传到 IMA 知识库「MD法规更新汇总」
disable: true
---

# 医疗器械法规追踪 Skill

## 概述

本 Skill 提供医疗器械法规动态追踪功能，覆盖以下地区和来源：

### 覆盖区域

| 区域 | 来源 | 说明 |
|------|------|------|
| 🇨🇳 中国 | NMPA、CMDE、中检院等 | 注册审批、指导原则、标准文件 |
| 🇪🇺 欧盟 | EC Health、Team NB、IMDRF | MDR、IVDR、MDCG指南、协调标准 |
| 🇺🇸 美国 | FDA CDRH | 指南文件、召回、安全警报 |
| 🇨🇦 加拿大 | Health Canada | 指南、最新消息 |

### 法规来源配置

所有来源配置存储在 `config/sources.json`，包含：
- URL 地址
- 页面类型（static/dynamic）
- 解析器选择
- 区域分类

## 核心流程

### 1. 日期范围计算

使用 `date_utils.py` 模块计算上周五到本周五的日期范围：

```
上周五 00:00:00 (北京时间) ~ 本周五 23:59:59 (北京时间)
```

主要函数：
- `get_week_date_range()`: 获取本周期的起止日期
- `is_within_date_range()`: 判断日期是否在范围内
- `parse_date()`: 解析多种日期格式

### 2. 网页抓取方式

本 Skill 支持两种抓取方式，根据来源特性选择：

#### 方式A：Web Fetch API（推荐，已验证）

**直接使用 AI 工具抓取，无需脚本**：

| 来源 | URL | 状态 |
|:-----|:----|:-----|
| 🇪🇺 EU/EC | `https://health.ec.europa.eu/medical-devices-sector/latest-updates_en` | ✅ 成功 |
| 🇨🇦 Health Canada | `https://www.canada.ca/en/health-canada/services/drugs-health-products/medical-devices/what-new.html` | ✅ 成功 |
| 🌍 IMDRF | `https://www.imdrf.org/documents` | ✅ 成功 |
| 🇺🇸 FDA 召回 | `https://www.fda.gov/medical-devices/medical-device-safety/medical-device-recalls` | ✅ 成功 |
| 🇨🇳 CMDE | `https://www.cmde.org.cn/` | ⚠️ 反爬虫保护 |

**执行方式**：
```
使用 web_fetch 工具直接抓取网页内容
```

#### 方式B：Python 脚本

使用 `parsers.py` 模块抓取各来源网页：

```python
from parsers import fetch_all_sources_with_webfetch_tracking, fetch_page

# 抓取所有配置来源（自动追踪需要AI工具补抓的来源）
all_items, web_fetch_sources = fetch_all_sources_with_webfetch_tracking(
    config, start_date, end_date
)
# 如果 web_fetch_sources 非空，说明有来源需要 AI web_fetch 工具补抓
```

**抓取策略**：
- `type="static"` → requests + BeautifulSoup（直接抓取）
- `type="dynamic"` → Playwright（JS渲染页面）
- `type="web_fetch"` → **生成待补抓清单，由 AI web_fetch 工具处理** ⚠️
  - 脚本会在 `scripts/reports/` 目录生成 `web_fetch_pending_{start}_{end}.json`
  - AI 读取该文件，对每个 URL 执行 web_fetch 工具
  - 将抓取结果保存为 `web_fetch_supplement_{start}_{end}.json`
  - 然后重新运行 `run_tracker.py --web-fetch-items <该json文件>`
- 静态页面：使用 `requests` + `BeautifulSoup`
- 动态页面（JS渲染）：使用 `Playwright`
- 请求间隔：1秒（礼貌性延迟）
- 超时：30秒

### 3. 内容解析

各来源使用专用解析器：

| 解析器 | 适用来源 |
|--------|----------|
| `parse_nmpa()` | NMPA 药监局 |
| `parse_cmde()` | CMDE 器械审评中心 |
| `parse_ec_health()` | 欧盟 EC Health |
| `parse_fda()` | FDA 相关页面 |
| `parse_ca_health()` | Health Canada |
| `parse_imdrf()` | IMDRF |
| `parse_teamnb()` | Team NB |

**解析字段**：
- `title`: 标题
- `url`: 原文链接
- `source`: 来源名称
- `publish_date`: 发布日期
- `tags`: 自动提取的标签（如「征求意见」「MDR」「FDA」等）

### 4. 去重机制

使用 `deduplicator.py` 模块管理本地去重记录：

```python
from deduplicator import RegistryDeduplicator

dedup = RegistryDeduplicator()

# 检查是否已推送（必须传入 source 才能正确去重）
if dedup.is_seen(url="...", title="...", source="中检院公告通知"):
    print("已推送过，跳过")

# 过滤新条目
new_items = dedup.filter_new(all_items)

# 添加新记录
dedup.add(url="...", title="...", source="...", region="CN")
```

**去重策略（2026-04-24 修复）**：
- 使用「来源 + URL」和「来源 + 标准化标题」**复合键**去重
- 同一来源的相同 URL **或**相同标题才视为重复
- 不同来源的相同 URL/标题互不影响
- 解决了 EU 来源 **in-place 更新**（URL 不变但内容/日期更新）被误拦的问题
- 存储位置：`data/seen_registry.json`

### 5. 报告生成

使用 `report_generator.py` 模块生成 Markdown 报告：

```python
from report_generator import ReportGenerator

gen = ReportGenerator(start_date, end_date)

# 添加条目
gen.add_item("CN", {"title": "...", "source": "...", ...})
gen.add_item("EU", {...})

# 生成报告
report_content = gen.generate()

# 保存到文件
gen.save(Path("output.md"))
```

**报告格式**（符合用户样例）：
1. **概览统计表**：各区域新增数量
2. **区域法规详情**：按区域分类，每条包含标题、来源、日期、链接、摘要、合规影响
3. **历史记录更新**：本期新增条目汇总
4. **抓取状态说明**：各来源抓取状态

### 6. IMA 上传

使用 IMA OpenAPI 将报告作为笔记上传到知识库：

**目标知识库**：
- 名称：MD法规更新汇总
- ID（通过 `get_addable_knowledge_base_list` 获取）：`ihJNh4Nl87Wqv-XLfXyOJSW1NMOBnVnk-HBnlcYgL4o=`

**上传流程（两步，必须按顺序）**：

> ⚠️ IMA 有两套 API，切勿混淆：
> - **笔记模块**：`/openapi/note/v1/` — 管理笔记内容
> - **知识库模块**：`/openapi/wiki/v1/` — 管理知识库条目

**Step 1 — 创建笔记**（笔记模块）：
```
POST https://ima.qq.com/openapi/note/v1/import_doc
Body: {"title": "标题", "content": "报告内容", "content_format": 1}
返回: {"code": 0, "data": {"note_id": "xxx"}}
```
> 注意：返回字段用 `code=0`（非 `retcode=0`），笔记 ID 在 `data.note_id`

**Step 2 — 关联到知识库**（知识库模块）：
```
POST https://ima.qq.com/openapi/wiki/v1/add_knowledge
Body: {
  "media_type": 11,
  "note_info": {"content_id": "<note_id>"},
  "title": "标题",
  "knowledge_base_id": "ihJNh4Nl87Wqv-XLfXyOJSW1NMOBnVnk-HBnlcYgL4o="
}
返回: {"code": 0, "data": {"media_id": "xxx"}}
```

**凭证配置**：
```bash
# 配置文件（凭证文件为 UTF-16 编码，Python 读取时需指定编码）
mkdir -p ~/.config/ima
echo "your_client_id" > ~/.config/ima/client_id
echo "your_api_key" > ~/.config/ima/api_key

# 环境变量（优先级高于配置文件）
export IMA_OPENAPI_CLIENTID="your_client_id"
export IMA_OPENAPI_APIKEY="your_api_key"
```

> ⚠️ 凭证文件为 **UTF-16 编码**，Python 读取示例：
> ```python
> with open(path, "rb") as f:
>     raw = f.read()
> for enc in ["utf-16", "utf-8", "gbk"]:
>     try: client_id = raw.decode(enc).strip(); break
>     except: continue
> ```

**Python 上传脚本已集成在 `scripts/ima_upload_report.py`**，可独立运行或通过 `run_tracker.py` 自动调用。

## 执行方式

### 手动执行

```bash
# 完整执行（抓取 + 上传）
python scripts/run_tracker.py

# 仅测试抓取，不上传
python scripts/run_tracker.py --dry-run

# 指定参考日期
python scripts/run_tracker.py --date 2026-04-10
```

### 自动化执行

通过 WorkBuddy 自动化配置每周五 8:30 执行：

```
触发时间: 每周五 08:30 (北京时间)
执行命令: python scripts/run_tracker.py
工作目录: ~/.workbuddy/skills/medical-device-registry-tracker
```

## 依赖要求

### 必需依赖
```bash
pip install requests beautifulsoup4
```

### 可选依赖（增强抓取能力）
```bash
# JS 渲染支持
pip install playwright
playwright install chromium
```

## 文件结构

```
medical-device-registry-tracker/
├── SKILL.md                    # Skill 定义
├── config/
│   └── sources.json            # 法规来源配置
├── scripts/
│   ├── run_tracker.py          # 主执行脚本
│   ├── date_utils.py           # 日期工具
│   ├── deduplicator.py         # 去重模块
│   ├── report_generator.py     # 报告生成
│   └── parsers.py              # 网页解析器
├── data/                       # 数据存储
│   └── seen_registry.json      # 已推送记录
└── reports/                    # 生成的报告
```

## 注意事项

1. **时区处理**：所有日期计算基于北京时间 (UTC+8)
2. **反爬策略**：
   - 使用真实 User-Agent
   - 请求间隔 1 秒
   - 失败自动重试
3. **IMA 凭证**：首次使用需配置 API 凭证
4. **去重安全**：本地记录不会自动清理，可手动编辑 `data/seen_registry.json`

## 故障排查

### 抓取失败
```bash
# 检查依赖
python -c "import requests, bs4; print('OK')"

# 测试网络
curl -I https://www.nmpa.gov.cn

# 启用调试模式
python scripts/parsers.py  # 直接运行解析器测试
```

### IMA 上传失败
```bash
# 检查凭证
cat ~/.config/ima/client_id
cat ~/.config/ima/api_key

# 测试 API
curl -X POST https://ima.qq.com/openapi/note/v1/import_doc \
  -H "ima-openapi-clientid: ..." \
  -H "ima-openapi-apikey: ..." \
  -H "Content-Type: application/json" \
  -d '{"title":"test","content":"test","content_format":1}'
```

## 更新日志

- 2026-04-24（下午）:
  - **IMA 上传流程修正**：
    - 知识库名称从占位符 `MD 法规更新-Testing` 更正为 `MD法规更新汇总`
    - 补充正确的 KB ID：`ihJNh4Nl87Wqv-XLfXyOJSW1NMOBnVnk-HBnlcYgL4o=`（通过 `get_addable_knowledge_base_list` 获取）
    - 完整记录两步上传流程（笔记模块 → 知识库模块），包括返回格式说明（`code=0` 而非 `retcode=0`）
    - 补充凭证文件 UTF-16 编码读取方法
    - 修正 curl 示例 URL（`/v1/` → `/v1/`，路径原已正确，补全 Content-Type header）
    - 关联上传脚本：`scripts/ima_upload_report.py`（Step 1 创建笔记 + Step 2 关联知识库）
- 2026-04-24:
  - **去重逻辑重构**（`deduplicator.py`）：
    - 旧策略：`is_seen()` 用 URL OR title 任一匹配即过滤
    - 新策略：改为「来源 + URL」和「来源 + 标准化标题」复合键去重
    - 解决了 EU 来源 in-place 更新被误拦的核心 bug
    - `filter_new()` 现在传入 `source` 参数，确保去重键正确构建
  - **EU 来源URL更新**（`sources.json`）：
    - `ec_guidance`（MDCG指南）：原URL已404，更新为 `/medical-devices-sector-new-regulation/` 路径
  - **新增4个EU来源**（`sources.json`，类型：web_fetch）：
    - `ec_emdn` — EMDN欧洲医疗器械命名法官方页（含MDCG 2021-12 EMDN FAQ）
    - `ec_mdr_revision` — EU MDR/IVDR Targeted Revision提案页（COM/2025/800，170页改革）
    - `ec_borderline` — 边境分类手册（含数字健康产品边界判定，2026年更新）
    - `ec_clinical_national` — 成员国临床试验国家要求（2026年更新）
    - `ec_mir_xsd` — 制造商不良事件报告XSD/SB 11154（EUDAMED警戒模块）
  - **新增2个US/CA来源**（`sources.json`）：
    - `fda_safety_comm` — FDA医疗器械安全通讯（Safety Communications专用页面）
    - `ca_announcements` — Health Canada医疗器械专项公告页面
    - 注：用户提供的FDA CDRH新闻链接已确认配置正确 ✅
  - **web_fetch_urls 更新**：新增 `new_eu_2026` 和 `new_us_ca_2026` 列表
  - **web_fetch来源处理流程重构**（`run_tracker.py` + `parsers.py`）：
    - **根因**：`fetch_source()` 对 `type="web_fetch"` 来源静默返回 `[]`，导致FDA CDRH新闻等来源被漏抓（AI工具从未收到这些URL）
    - **修复**：新增 `fetch_all_sources_with_webfetch_tracking()` 函数，追踪所有 web_fetch 来源并生成 `web_fetch_pending_{日期}.json` 清单
    - 脚本现在会明确打印 `[⚠️ 需AI补抓]` 提示，列出所有需要 AI web_fetch 工具处理的来源
    - `run_tracker.py` 支持 `--web-fetch-items` 参数注入 web_fetch 补充结果
    - 兼容旧接口：`fetch_all_sources()` 仍然可用，内部委托新函数
- 2026-04-14:
  - **重大更新**：新增 Web Fetch API 直接抓取方式
  - sources.json 添加 `web_fetch_status` 字段标记可用来源
  - 已验证可用：EU/EC、Health Canada、IMDRF、FDA 召回页面
  - CMDE 因反爬虫保护需继续使用 Playwright 或手动访问
- 2026-04-14: 初始版本，支持 CN/EU/US/CA 四大区域
