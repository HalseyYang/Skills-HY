# FDA API 文档说明

## 官方 FDA API

### 1. openFDA API
- **基础 URL**: https://api.fda.gov
- **文档**: https://open.fda.gov/apis/
- **范围**: 药物不良事件、标签、召回、执法报告
- **指南**: 有限 - 不包含完整的指导文件

### 2. FDA Data Catalog
- **URL**: https://catalog.data.gov/organization/fda-gov
- **格式**: CKAN API
- **范围**: 数据集元数据，非完整文本文件

## 指导文件访问

### 当前限制
FDA 目前**不**提供专门用于指导文件的公共 REST API。推荐方法：

1. **网页抓取**（已在本技能中实现）
   - 解析来自 https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs 的 HTML
   - 遵守速率限制（每分钟 10 次请求）
   - 在本地缓存结果

2. **FDA 电子邮件更新**
   - 订阅指导文件更新
   - https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs

3. **FDA RSS 订阅**
   - 可用于新指导公告
   - XML 格式用于自动化处理

## ICH 指南访问

### ICH API
- **URL**: https://database.ich.org
- **格式**: 带可下载 PDF 的网页界面
- **API**: 无可用的公共 REST API
- **访问**: 手动下载或网页抓取

## 认证

### openFDA API
- 基本使用无需 API 密钥
- 速率限制：每个 IP 每天 1000 次请求
- 通过 API 密钥注册可获得更高限制

### FDA Cloud
- 某些数据集需要认证
- 不适用于指导文件

## 数据结构

### 指南文件字段
```json
{
  "document_number": "FDA-YYYY-D-NNNN",
  "title": "Guidance Title",
  "issue_date": "YYYY-MM-DD",
  "type": "Draft|Final|ICH",
  "therapeutic_area": "Area Name",
  "pdf_url": "https://...",
  "html_url": "https://...",
  "docket_number": "FDA-YYYY-D-NNNN",
  "contact": "division@fda.hhs.gov"
}
```

## 最佳实践

1. **缓存**: 在本地存储下载的 PDF
2. **速率限制**: 永不超过每分钟 10 次请求
3. **错误处理**: 处理 429（速率限制）和 503（不可用）响应
4. **User-Agent**: 清楚标识您的应用程序
5. **遵守 robots.txt**: 在实施爬虫前检查

## 未来增强

监控 FDA API 公告以获取：
- 官方指导文件 API
- 新文件的 Webhook 支持
- 用于复杂查询的 GraphQL 端点
- 批量数据下载

## 参考资料

- FDA API 文档: https://open.fda.gov/apis/
- FDA 开发者资源: https://www.fda.gov/forindustry/datastandards/
- ICH 指南数据库: https://database.ich.org
