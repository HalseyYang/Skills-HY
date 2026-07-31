---
name: fda-guideline-search
description: '按治疗领域或主题搜索 FDA 行业指南。

  当用户请求 FDA 指导文件、法规指南，

  或询问特定疾病领域、药物开发

  或治疗类别（如肿瘤学、心脏病学、罕见疾病）的 FDA 要求时触发。

  也由关于 FDA ICH 指南、FDA 指导文件

  或法规合规要求的查询触发。'
version: "1.0.2"
category: Pharma
tags: []
author: AIPOCH
license: MIT
status: Draft
risk_level: High
skill_type: Hybrid (Tool/Script + Network/API)
owner: AIPOCH
reviewer: ''
last_updated: '2026-02-06'
displayName: "FDA 指南检索"
slug: fda-guideline-search
---

# FDA 指南检索

按治疗领域快速搜索和检索 FDA 行业指南。

## 功能特点

- 按治疗领域搜索 FDA 指南（肿瘤学、心脏病学、神经病学等）
- 按文件类型筛选（草案、最终版、ICH 指南）
- 下载并缓存指南文件
- 在文件内容中搜索

## 使用方法

### Python 脚本

```bash
python scripts/main.py --area <therapeutic_area> [options]
```

## 参数

| 参数 | 类型 | 默认值 | 必填 | 描述 |
|-----------|------|---------|----------|-------------|
| `--area` | string | - | 是 | 治疗领域（oncology、cardiology、rare-disease） |
| `--type` | string | all | 否 | 文件类型（all、draft、final、ich） |
| `--year` | string | - | 否 | 按年份筛选（例如，2023、2020-2024） |
| `--download` | flag | false | 否 | 下载 PDF 至本地缓存 |
| `--search` | string | - | 否 | 文件内搜索词 |
| `--limit` | int | 20 | 否 | 最大结果数（1-100） |

### 示例

```bash
# Search oncology guidelines
python scripts/main.py --area oncology

# Search for rare disease draft guidelines
python scripts/main.py --area "rare disease" --type draft

# Search with download
python scripts/main.py --area cardiology --download --limit 10
```

## 技术细节

- **来源**: FDA CDER/CBER Guidance Documents Database
- **API**: FDA Open Data / Web scraping with rate limiting
- **缓存**: Local PDF storage in `references/cache/`
- **难度**: 中等

## 输出格式

结果以结构化 JSON 格式返回：

```json
{
  "query": {
    "area": "oncology",
    "type": "all",
    "limit": 20
  },
  "total_found": 45,
  "guidelines": [
    {
      "title": "Clinical Trial Endpoints for the Approval of Cancer Drugs...",
      "document_number": "FDA-2020-D-0623",
      "issue_date": "2023-03-15",
      "type": "Final",
      "therapeutic_area": "Oncology",
      "pdf_url": "https://www.fda.gov/.../guidance.pdf",
      "local_path": "references/cache/..."
    }
  ]
}
```

## 参考资料

- [FDA 搜索策略](./references/search-strategy.md)
- [治疗领域映射](./references/area-mappings.json)
- [FDA API 文档](./references/fda-api-notes.md)

## 限制

- 速率限制为每分钟 10 次请求，以尊重 FDA 服务器
- 部分历史文件可能没有数字 PDF
- ICH 指南需要单独的搜索范围

## 风险评估

| 风险指标 | 评估 | 级别 |
|----------------|------------|-------|
| 代码执行 | 带工具的 Python 脚本 | 高 |
| 网络访问 | 外部 API 调用 | 高 |
| 文件系统访问 | 读写数据 | 中 |
| 指令篡改 | 标准提示指南 | 低 |
| 数据暴露 | 数据安全处理 | 中 |

## 安全检查表

- [ ] 无硬编码凭据或 API 密钥
- [ ] 无未授权文件系统访问（../）
- [ ] 输出不暴露敏感信息
- [ ] 已实施提示注入保护
- [ ] API 请求仅使用 HTTPS
- [ ] 输入已针对允许模式进行验证
- [ ] 已实施 API 超时和重试机制
- [ ] 输出目录限制在工作区内
- [ ] 脚本在沙盒环境中执行
- [ ] 错误消息已清理（无内部路径暴露）
- [ ] 依赖项已审计
- [ ] 无内部服务架构暴露
## 前提条件

无需额外的 Python 包。

## 评估标准

### 成功指标
- [ ] 成功执行主要功能
- [ ] 输出符合质量标准
- [ ] 优雅处理边缘情况
- [ ] 性能可接受

### 测试用例
1. **基本功能**：标准输入 → 预期输出
2. **边缘情况**：无效输入 → 优雅的错误处理
3. **性能**：大型数据集 → 可接受的处理时间

## 生命周期状态

- **当前阶段**: 草案
- **下次审查日期**: 2026-03-06
- **已知问题**: 无
- **计划改进**: 
  - 性能优化
  - 额外功能支持
