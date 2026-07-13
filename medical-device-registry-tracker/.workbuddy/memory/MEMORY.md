# 长期记忆

## IMA 知识库信息（重要）

**上传报告到知识库的正确流程**：
1. 笔记模块创建笔记：`POST https://ima.qq.com/openapi/note/v1/import_doc`
   - Body: `{"title": "标题", "content": "内容", "content_format": 1}`
   - 返回格式：`{"code": 0, "data": {"note_id": "xxx"}}`
2. 知识库模块关联笔记：`POST https://ima.qq.com/openapi/wiki/v1/add_knowledge`
   - Body: `{"media_type": 11, "note_info": {"content_id": "<note_id>"}, "title": "标题", "knowledge_base_id": "<kb_id>"}`
   - 返回格式：`{"code": 0, "data": {"media_id": "xxx"}}`

**IMA 知识库 ID（通过 get_addable_knowledge_base_list 获取）**：
- 「MD法规更新汇总」→ `ihJNh4Nl87Wqv-XLfXyOJSW1NMOBnVnk-HBnlcYgL4o=`
- 「FDA认证汇总知识库」→ `M_daNwQAaqov4X8CLnjCOguVG2lqiWLO1vbxpAW3K2c=`
- 「其他地区」→ `7fqkqco92Xs-7wGCYYKaHSJkxEUUOaw9gdxAkAVMQx0=`
- 「CE与FDA法规解读」→ `sulzXmP_VIFmLOvFjr_wTZLdJPUEpfpzAKV4wdmHOU0=`

**踩坑**：
- 知识库 API 有两套：笔记模块（`/openapi/note/v1/`）和知识库模块（`/openapi/wiki/v1/`）
- `import_doc` 是笔记模块的接口，不是 wiki 模块
- 凭证文件 `~/.config/ima/client_id` 和 `api_key` 是 UTF-16 编码，Python 读取时需指定编码
- 搜索知识库用 `search_knowledge_base`（但返回结构有时 `id` 为 None）；获取可添加知识库用 `get_addable_knowledge_base_list`（这个返回正确 ID）
- **Node.js 直接调用 IMA API 时，HTTP 头必须用 `ima-openapi-clientid` 和 `ima-openapi-apikey`（小写+中划线）**，不能用 `clientid`/`apiKey`

## 法规追踪 Skill 配置

**抓取策略**：
- web_fetch 对 FDA.gov/CMDE/NMPA 超时是长期问题，应默认 web_search 为主渠道
- 遇到 web_fetch 失败立即切 web_search，不要重试
- 各地区关键媒体（Mintz、RAPS、MedTech Dive）是很好的摘要来源

**本周发现的系统性漏检**：
- **OJEU (Official Journal) 未纳入监控源** → (EU) 2026/977（5月5日发布）完全漏检
  - 修复方案：在 sources.json EU 区段增加 eur-lex.eu 静态来源，或在 web_search 关键词补充法规编号
- **Team-NB 从未实际抓取** → sources.json 中 teamnb 配置 `web_fetch_status: untested`，需验证
- **COM(2025)1023 URL 配置错误** → 指向了 Press Release 而非提案文本
  - 正确 URL：`https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC1023`
- **FDA 检索策略不够宽** → 仅依赖 web_fetch + web_search 兜底，但法规编号形式（如 2026/977）容易被忽略

**凭证编码**：Python 读取 `~/.config/ima/*.txt` 时需用 UTF-16 编码尝试
