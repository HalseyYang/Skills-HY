# 国内反爬来源 - web_search 补充操作手册

## 背景

以下国内医疗器械监管网站存在反爬机制（HTTP 412 / JS渲染保护），无法被 Python 脚本直接抓取。
每次执行法规周报时，AI 需要通过 `web_search` 工具搜索最新动态，并将结果整理为标准 JSON 格式。

---

## 反爬来源列表

| 来源ID | 名称 | 网址 |
|--------|------|------|
| `nmpa` | 国家药品监督管理局 | https://www.nmpa.gov.cn/ylqx/index.html |
| `cmde_main` | 器械审评中心 | https://www.cmde.org.cn/ |
| `cmde_report` | 审评报告 | https://www.cmde.org.cn/xwdt/shpbg/index.html |
| `cmde_faq` | 共性问题 | https://www.cmde.org.cn/splt/ltgxwt/index.html |
| `cmde_forum` | CMDE论坛 | https://www.cmde.org.cn/splt/index.html |
| `nifdc_standard` | 中检院标准管理中心 | https://www.nifdc.org.cn/nifdc/bshff/ylqxbzhgl/index.html |
| `ydcmdei` | 器械审评中心（长三角） | https://www.ydcmdei.org.cn/ |
| `mdei_gba` | 器械审评中心（大湾区） | https://www.mdei.org.cn/ |

---

## web_search 查询模板

每个来源对应以下搜索查询（将 `{YEAR}` `{MONTH}` 替换为报告周期所在年月）：

```
nmpa:          site:nmpa.gov.cn 医疗器械 通知 公告 指导原则 {YEAR}年{MONTH}月
cmde_main:     site:cmde.org.cn 器械审评 最新 通知 指南 {YEAR}年{MONTH}月
cmde_report:   site:cmde.org.cn 审评报告 {YEAR}年{MONTH}月
cmde_faq:      site:cmde.org.cn 共性问题 解答 {YEAR}年{MONTH}月
cmde_forum:    site:cmde.org.cn 论坛 讨论 最新 {YEAR}年{MONTH}月
nifdc_standard:site:nifdc.org.cn 器械标准 征集 发布 {YEAR}年{MONTH}月
ydcmdei:       site:ydcmdei.org.cn 长三角器械审评 {YEAR}年{MONTH}月
mdei_gba:      site:mdei.org.cn 大湾区器械审评 {YEAR}年{MONTH}月
```

---

## 补充条目 JSON 格式

搜索结果需整理为如下格式，保存到 `scripts/reports/web_search_supplement_YYYYMMDD.json`：

```json
[
  {
    "title": "关于XXX的通知",
    "url": "https://www.nmpa.gov.cn/...",
    "source": "国家药品监督管理局",
    "publish_date": "2026-04-18",
    "region": "CN",
    "tags": ["通知", "指导原则"],
    "summary": "主要内容摘要",
    "impact": "合规影响说明"
  }
]
```

---

## 调用方式

生成补充文件后，传入追踪脚本：

```bash
python scripts/run_tracker.py --web-search-items scripts/reports/web_search_supplement_20260420.json
```

---

## 注意事项

1. **日期过滤**：只收录报告周期内（本周四00:00 ~ 下周四23:59）的条目
2. **去重**：已在历史记录中的条目将被自动过滤
3. **标签提取**：可参考 parsers.py 中的 `extract_tags()` 函数
4. **region 字段**：国内来源统一填 `"CN"`
