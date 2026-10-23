# NB（公告机构）退回原因库：Top 15 缺陷与对策

> **用途**：TEAM-NB 统计约 **40% 首次提交需补充信息**，平均延误 3–6 个月。这些退回绝大多数不是「缺证据」，而是「证据摆的方式不对」。本库把 NB 最高频的 15 类缺陷整理成「现象→根因→对策→自检」——**提交前逐条过一遍，是 CE 一次拿证的核心动作**。
>
> 来源：TEAM-NB Position Paper BPG V3 (2025-04-09, 79页) + 行业 NB 审核实践归纳。

---

## Top 15 退回原因

### 1. GSPR 检查表不完整或无版本控制
- **典型表现**（NB 信里原文风格）："The GSPR checklist does not address all applicable requirements of Annex I."
- **根因**：23 条没列全；「不适用」无理由；无版本号/日期；证据引用只到文档级不到页码。
- **对策**：用六列标准格式（条款/要求/方法/证据文档号+页码/版本日期/不适用理由），逐条对照 `gspr-annex1-full-checklist.md`。
- **自检问题**：随便抽 3 行，证据引用能一次跳到确切页码吗？

### 2. 风险控制措施只写「见 IFU」
- **典型表现**："Risk control measures reference 'IFU' without specifying which information controls which risk."
- **根因**：风险文件与控制措施脱节；IFU 改了但风险文件没更新。
- **对策**：每条风险控制写「IFU 第 X 节第 X 条警示」式具体引用；IFU 版本变更触发风险文件复查。
- **自检问题**：每条残余风险，都能在 IFU 里找到对应那句话吗？

### 3. CER 评估者资质与利益声明缺失
- **典型表现**："Qualification and conflict-of-interest statements of the evaluator(s) are missing."
- **根因**：CER 由内部工程师签了字，无 CV、无临床资质、无利益声明。
- **对策**：附每位评估者 CV + 利益冲突声明；CER 须由具备临床资质的专家签署（TEAM-NB 明确要求）。
- **自检问题**：CER 签字页附 CV 了吗？

### 4. 等同器械论证不充分（三要素缺腿）
- **典型表现**："Equivalence in clinical/anatomical/physiological characteristics is not demonstrated."
- **根因**：只比了技术特征，没比临床/解剖/生理特征（MDCG 2020-5 三要素）。
- **对策**：按 MDCG 2020-5 附录逐项论证；不等同的部分须有补充数据弥补。
- **自检问题**：三要素各有一段独立论证吗？不等同处有数据补位吗？

### 5. 文献检索方法不可复现
- **典型表现**："The literature search methodology is not reproducible (no databases/date ranges/search strings)."
- **根因**：CER 里只列了 20 篇文献，没写怎么检索的。
- **对策**：PICO 问题拆解 + 数据库清单 + 检索式原文 + 检索日期 + 纳入/排除标准 + PRISMA 流程。
- **自检问题**：换个研究员按你写的检索式，能复现同样的文献集吗？

### 6. 测试报告只交摘要
- **典型表现**："Complete test reports are required; summaries are not acceptable."
- **根因**：以为摘要够了（TEAM-NB 明确：不收摘要/部分报告）。
- **对策**：全部测试报告交完整版，含原始数据、图表、偏差说明。
- **自检问题**：每份报告都带签名、日期、方法引用、原始数据吗？

### 7. 预期用途跨文档不一致
- **典型表现**："Intended purpose differs between the device description, IFU and application form."
- **根因**：多部门各写各的，没有主数据表。
- **对策**：建立「主数据表」（预期用途/型号/分类/软件版本唯一出处），其他文档引用编号。
- **自检问题**：把三份文档的预期用途并排读，逐字一致吗？

### 8. 软件生命周期证据缺口
- **典型表现**："Software architecture, unit/integration test evidence and traceability are insufficient (IEC 62304)."
- **根因**：只交了软件描述和系统测试，无架构图、无单元测试、无可追溯矩阵。
- **对策**：IEC 62304 全套：软件计划+需求+架构+单元/集成/系统 V&V+可追溯矩阵（需求↔设计↔代码↔测试）。
- **自检问题**：随机抽一个软件需求，能追到测试用例和结果吗？

### 9. 网络安全只有一句话
- **典型表现**："Section 17.4 compliance is addressed by a single statement referencing IEC 62304."
- **根因**：把 IT 安全当软件问题顺手带过。
- **对策**：威胁模型 + SBOM + 漏洞管理计划 + 安全测试证据 + IFU 中的安全信息（MDCG 2019-16）。
- **自检问题**：渗透测试报告或等效证据在档吗？IFU 里有没有安全配置说明？

### 10. PMS Plan 通用模板化
- **典型表现**："The PMS plan appears to be a generic template not tailored to this device."
- **根因**：套模板，没有本产品特有的指标/触发阈值/风险项。
- **对策**：PMS Plan 逐项定制：数据源（≥8 类）+ 本产品特有指标 + 触发阈值有依据（历史数据/风险文件联动）+ 责任人实名。
- **自检问题**：这份 PMS Plan 换个产品名还能用吗？能就不用。

### 11. PMCF 与 CER 脱节
- **典型表现**："The PMCF plan does not address the gaps identified in the clinical evaluation."
- **根因**：CER 说证据有 gap，PMCF 却还在做泛泛登记。
- **对策**：PMCF 的每一项都挂回 CER 的具体缺口/问题；中期报告回填 CER 更新。
- **自检问题**：CER 里列的每个 uncertainty，PMCF 里都有对应行动吗？

### 12. 标签/IFU 内容或语言不全
- **典型表现**："IFU does not contain all elements required by Annex I §23.3; translations incomplete."
- **根因**：23.3 清单没逐条对；成员国语言缺。
- **对策**：按 GSPR 23.1–23.4 逐条核对；销售所达成员国官方语言全覆盖。
- **自检问题**：23.3 的 IFU 清单逐条打勾了吗？每种语言版本受控吗？

### 13. UDI/EUDAMED 数据不一致
- **典型表现**："UDI-DI data in EUDAMED does not match the technical documentation."
- **根因**：EUDAMED 注册时手工填的数据与技术文档有出入。
- **对策**：EUDAMED 字段从主数据表生成；注册前与技术文档/DoC 三方核对。
- **自检问题**：BUDI-DI、分类、预期用途三处一致吗？

### 14. 设计变更未同步更新技术文档
- **典型表现**："Verification reports reference a design version different from the released device."
- **根因**：改图不改文档；测试版本与发布版本不一致。
- **对策**：变更影响评估流程：任何变更 → 触发 GSPR/风险/测试/CER 相关性复查 → 记录在案。
- **自检问题**：测试报告里的图纸版本号 = 发布版吗？

### 15. 外包/供应商过程未在技术文档描述
- **典型表现**："Outsourced processes and critical suppliers are not identified in the technical documentation."
- **根因**：技术文档只写自己厂里的事。
- **对策**：Annex II §3 设计与制造信息中列明关键供应商/外包过程及其控制方式。
- **自检问题**：灭菌/关键工序外包的，在文档里说了控制方式吗？

---

## 提交前 NB 视角模拟审核 20 问（抽检版）

1. 目录是否按 Annex II 结构组织、可搜索、带超链接索引？
2. 器械描述与 EUDAMED 注册数据一致吗？
3. GSPR 表 23 条齐全、六列完整、版本受控？
4. 风险管理：计划/报告/生产后信息三件套齐？5×5 矩阵三区域判定？
5. 每条风险控制是否具体（非「见 IFU」式）？
6. 生物学评价覆盖全部接触材料与接触时长？
7. 灭菌三支柱（验证/包装/货架寿命）齐全？
8. 软件：架构图、V&V 完整报告、可追溯矩阵？
9. 网络安全：威胁模型+SBOM+VMP+测试证据？
10. 可用性：URRA + 形成性 + 总结性（按风险）？
11. CER：检索可复现？评估者 CV？三要素等同论证？
12. PMCF 挂回 CER 缺口？
13. PSUR/PMS Plan 定制化、频率正确（IIa 2 年/IIb-III 1 年）？
14. 标签/IFU：23.x 清单 + 语言全覆盖？
15. UDI 数据与技术文档一致？
16. 测试报告全部完整版（非摘要）？
17. 引用标准现行版？旧版有 gap 分析？
18. 设计版本 = 发布版本？
19. 关键供应商/外包过程已披露？
20. 全部文档有编号+版本+日期+审批签字？

**≤19 项通过 → 修复后才可提交。**

---

*依据：TEAM-NB Position Paper BPG V3 (2025-04-09)；MDCG 2020-5（等同性）/ 2020-7（PMS/PMCF）/ 2020-13（CER）/ 2019-16（网络安全）；Reg (EU) 2017/745 Annex II/III。退回原因为行业归纳，占比为经验估算。*
