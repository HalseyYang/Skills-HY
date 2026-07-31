# FDA 指南搜索策略

## 数据来源

### 主要来源
1. **FDA CDER 指导文件**
   - URL: https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs
   - 包含药物开发和审查指南

2. **FDA CBER 指导文件**
   - URL: https://www.fda.gov/vaccines-blood-biologics/guidance-compliance-regulatory-information-biologics/guidances-biologics
   - 包含生物制品和血液制品指南

3. **ICH 指南**
   - URL: https://database.ich.org/home
   - FDA 采用的国际协调指南

## 搜索方法

### 1. 治疗领域映射
- 将用户输入标准化为标准治疗领域名称
- 使用关键词扩展进行全面匹配
- 支持部分匹配和别名

### 2. 文件筛选
- 按类型：草案、最终版、ICH
- 按日期：单一年份或日期范围
- 按内容：标题内的全文搜索

### 3. 速率限制
- FDA 服务器每分钟最多 10 次请求
- 请求之间 6 秒延迟
- 遵守 robots.txt 和服务器响应时间

## 实现说明

### 当前方法
- 使用 urllib 的 Python 脚本进行 HTTP 请求
- 基于正则表达式的 HTML 解析（用于可靠性）
- 本地 JSON 缓存
- 用于演示的模拟数据结构

### 生产增强路径
1. 使用 BeautifulSoup 进行可靠的 HTML 解析
2. 实现 FDA OpenFDA API 集成
3. 使用 SQLite/Elasticsearch 添加全文索引
4. PDF 文本提取用于内容搜索

## 已知限制

1. FDA 不为所有指导文件提供完整的公共 API
2. 部分历史文件缺少数字 PDF
3. 文件编号和 URL 可能会更改
4. ICH 指南需要单独的数据库访问

## 参考链接

- FDA Guidance Index: https://www.fda.gov/regulatory-information/search-fda-guidance-documents
- FDA Drug Guidance: https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs
- ICH Guidelines: https://database.ich.org/home
