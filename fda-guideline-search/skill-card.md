## 描述: <br>
按治疗领域或主题搜索 FDA 行业指南。 <br>

本技能仅供演示，不用于生产环境。 <br>

## 发布者: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### 许可证/使用条款: <br>
MIT-0 <br>


## 使用场景: <br>
法规事务、临床开发及代理开发人员可使用本技能，按治疗领域、文件类型、年份和关键词探索 FDA 和 ICH 指南搜索工作流。结果应视为非权威性演示输出，在法规工作中使用前须直接对照 FDA 或 ICH 来源进行验证。 <br>

### 部署地理范围: <br>
全球 <br>

## 已知风险与缓解措施: <br>
风险：合成的 FDA 指南结果可能被作为真实的法规搜索结果呈现。 <br>
缓解措施：将输出视为非权威性演示数据，在依赖任何引用的指南前直接通过 FDA 或 ICH 来源进行验证。 <br>
风险：本技能可执行网络请求并将下载的文件写入本地缓存。 <br>
缓解措施：在沙盒工作区中运行，审查缓存/输出路径，仅在需要时启用下载功能。 <br>
风险：不完整或过时的搜索结果可能影响法规或医疗开发决策。 <br>
缓解措施：要求具备资质的法规审查，并以官方来源文件作为决策记录。 <br>


## 参考资料: <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/fda-guideline-search) <br>
- [FDA 搜索策略](references/search-strategy.md) <br>
- [治疗领域映射](references/area-mappings.json) <br>
- [FDA API 文档说明](references/fda-api-notes.md) <br>
- [FDA Guidance Index](https://www.fda.gov/regulatory-information/search-fda-guidance-documents) <br>
- [FDA Drug Guidance Documents](https://www.fda.gov/drugs/guidance-compliance-regulatory-information/guidances-drugs) <br>
- [ICH Guidelines Database](https://database.ich.org/home) <br>
- [openFDA APIs](https://open.fda.gov/apis/) <br>


## 技能输出: <br>
**输出类型:** [JSON、文件、Shell 命令、指南] <br>
**输出格式:** [Python CLI 输出的结构化 JSON，启用下载时可选缓存 PDF 文件。] <br>
**输出参数:** [1D] <br>
**与输出相关的其他属性:** [可能发生速率限制的外部请求和本地缓存写入；除非更改实现以检索和验证实际 FDA 或 ICH 记录，否则报告的指南结果为非权威性演示数据。] <br>

## 技能版本: <br>
0.1.0 (source: server release evidence) <br>

## 伦理考量: <br>
用户应评估本技能是否适合其环境，在依赖任何生成或修改的文件前进行审查，并在部署前应用所在组织的安全、保障和合规要求。 <br>
