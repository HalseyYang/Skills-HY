name: ima-wechat-batch-uploader
description: Batch upload WeChat official account articles (from CSV) to IMA knowledge base with filtering and categorization support. Used when the user wants to import WeChat public account articles to a specific IMA knowledge base folder.
agent_created: true
---

# IMA 微信公众号文章批量上传器

将公众号文章 CSV 批量筛选并上传至 IMA 知识库指定文件夹。

## 触发条件

当用户有以下任一意图时激活此技能：
- 将 CSV 中的公众号文章批量上传到 IMA 知识库
- 筛选公众号文章后导入知识库
- 批量导入微信文章链接到 IMA
- 将公众号文章分类上传到指定知识库文件夹

## 前置要求

- 环境变量 `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY` 已设置（或 `~/.config/ima/client_id` 和 `api_key` 文件存在）
- 目标知识库和文件夹已存在
- CSV 文件包含 `title` 和 `url` 列

## 关键注意事项（必读）

### 1. URL 中的 `&` 不能编码为 `&amp;`

CSV 中读取的 URL 可能包含 `&amp;`（HTML 实体编码），**必须**在导入前替换回 `&`（原始 `&` 字符）。否则 IMA 服务端无法正确解析微信公众号文章，导致标题显示为 URL、内容无法打开。

```javascript
const cleanUrl = rawUrl.replace(/&amp;/g, '&');
```

### 2. `import_urls` 接口每次最多 10 个 URL

必须分批次导入，每批不超过 10 个 URL。建议每批间隔 2 秒。

### 3. API 知识库 ID 与 MCP 知识库 ID 不同

- `search_knowledge_base` 返回的 `id` 字段（如 `7446108976476732`）是**展示 ID**，API 操作不可用
- 必须在 `get_knowledge_base` 或 `get_knowledge_list` 中获取 `kb_id` 字段（如 `VUJ-nc8nXeEQWHi9xrAIvk8VYmN8Lp39W1JCM777NQ4=`），这才是 API 可用的知识库 ID

## 完整工作流程

### Step 1: 筛选文章

读取 CSV，根据标题关键词排除非法规类文章，生成待上传列表和排除清单。

默认排除关键词：
```
招聘、热招职位、节日、五一、新春快乐、抽奖、问卷、
和BSI一起、BSI人、医疗最新使命、邀请函、相约、CMEF、
展会、倒计时、收官、圆满落幕、同愿、并肩、携、助力可持续发展、
报名表、报名 |、报名倒计时、课程限时、新课推荐、最新课表、经典课程、培训报名
```

用户可自定义排除关键词。

执行脚本：
```bash
node scripts/filter_csv.js <csv_path> [exclude_keywords_file] [output_dir]
```

输出：
- `filtered_articles.json` — 保留的文章列表（`title`, `url`）
- `excluded_articles.json` — 被排除的文章列表（`title`, `reason`）
- `upload_list.txt` — 纯文本预览，方便用户确认

### Step 2: 用户确认筛选结果

将 `upload_list.txt` 展示给用户，确认是否排除正确。用户确认后再执行上传。

### Step 3: 获取知识库信息

1. 用 `search_knowledge_base` 搜索目标知识库名称，获取 `id`（展示 ID）
2. 用 `get_knowledge_base` 传入该 `id`，获取 `kb_id`（API 可用 ID）
3. 用 `get_knowledge_list` 遍历知识库，定位目标文件夹的 `folder_id`

### Step 4: 批量上传

执行脚本：
```bash
node scripts/batch_upload.js <filtered_articles.json> <kb_id> <folder_id> [batch_size]
```

参数：
- `filtered_articles.json` — Step 1 生成的保留文章列表
- `kb_id` — API 可用的知识库 ID（Base64 格式）
- `folder_id` — 目标文件夹 ID（如 `folder_7476093149796694`）
- `batch_size` — 每批数量，默认 10（最大 10）

脚本行为：
1. 读取 `filtered_articles.json`
2. 将 `url` 中的 `&amp;` 替换为 `&`
3. 按 batch_size 分批次调用 `import_urls` 接口
4. 每批间隔 2 秒，避免限流
5. 输出每批的上传结果（成功/失败/媒体 ID）

### Step 5: 验证上传结果

上传完成后，用 `get_knowledge_list` 查询目标文件夹，检查：
- 文章总数是否正确
- 标题是否显示正常（不是 URL 格式）
- 是否有文章仍在解析中

## 接口参考

| 接口 | 用途 | 关键参数 |
|------|------|---------|
| `search_knowledge_base` | 按名称搜索知识库 | `query`, `limit` |
| `get_knowledge_base` | 获取知识库详情（含 `kb_id`） | `ids` |
| `get_knowledge_list` | 浏览知识库内容/文件夹 | `knowledge_base_id`, `folder_id`, `limit`, `cursor` |
| `import_urls` | 批量导入网页链接 | `knowledge_base_id`, `folder_id`, `urls`（1-10 个） |

## 故障排查

### 问题：上传后标题显示为 URL
**原因**：URL 中的 `&` 被编码为 `&amp;`  
**解决**：确保上传前执行 `url.replace(/&amp;/g, '&')`

### 问题：点击文章显示"参数错误"
**原因**：IMA 服务端无法解析微信公众号文章（需要微信环境）  
**解决**：确认 URL 格式正确（`&` 未编码）。如果仍然失败，说明该文章无法通过 API 导入，建议手动在 IMA 客户端中导入。

### 问题：API 返回 "skill auth failed"
**原因**：凭证是 ima-mcp 的凭证，不是 ima-skill 的 OpenAPI 凭证  
**解决**：获取 IMA OpenAPI 的 Client ID 和 API Key（https://ima.qq.com/agent-interface）

### 问题："invalid knowledge_base_id"
**原因**：使用了展示 ID 而不是 API 可用的 `kb_id`  
**解决**：通过 `get_knowledge_base` 获取正确的 `kb_id`

## 脚本说明

### `scripts/filter_csv.js`

筛选 CSV 文件中的文章，排除非法规类内容。

```bash
node scripts/filter_csv.js <csv_path> [exclude_keywords_file] [output_dir]
```

- `exclude_keywords_file` — 每行一个关键词的文本文件，可选
- `output_dir` — 输出目录，默认当前目录

### `scripts/batch_upload.js`

批量上传文章到 IMA 知识库。

```bash
node scripts/batch_upload.js <articles_json> <kb_id> <folder_id> [batch_size]
```

- `articles_json` — filter_csv.js 生成的 `filtered_articles.json`
- `kb_id` — API 知识库 ID（如 `VUJ-nc8nXeEQWHi9xrAIvk8VYmN8Lp39W1JCM777NQ4=`）
- `folder_id` — 目标文件夹 ID（如 `folder_7476093149796694`）
- `batch_size` — 每批数量，默认 10
