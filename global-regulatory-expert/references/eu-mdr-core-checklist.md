# EU MDR 2017/745 核心核查清单

本文档提供 EU MDR 2017/745 技术文档的完整核查框架，从**申请方首席顾问**视角，识别技术文件中的关键缺陷和补强方向。与 `medical-device-mdr-auditor`（纯审计检查）不同，本文侧重**战略补强**：告诉申请方哪些问题会导致 NB 发补，以及如何提前准备。

---

## 一、MDR 合规核查概览

### 1.1 核心法规架构

```
EU MDR 2017/745 体系
│
├── Article 1-123（实体法条款）
│   ├── Article 8-13：符合性评估路径选择
│   ├── Article 20：器械注册（EUDAMED）
│   ├── Article 26-29：制造商义务
│   ├── Article 56：技术文档要求
│   ├── Article 61：临床评价
│   ├── Article 83-86：上市后监督（PMS）
│   └── Article 87-92：警戒与上报
│
├── Annex I：General Safety and Performance Requirements (GSPR)
│   ├── Chapter 1：通用要求（§1-§9）
│   ├── Chapter 2：设计制造要求（§10-§22）
│   └── Chapter 3：GSPR 关于标签和IFU（§23）
│
├── Annex II：技术文档结构
├── Annex III：PMS 技术文档
│   ├── Part A：PMS 计划
│   └── Part B：PMCF 计划
├── Annex IV-VII：符合性评估程序
├── Annex VIII：分类规则
├── Annex IX：基于质量管理和技术评估的符合性评估（含 CER 要求）
├── Annex X：基于产品验证的符合性评估
└── Annex XI：基于生产质量保证的符合性评估
```

### 1.2 不同类别器械的关键差异

| 器械类别 | 符合性评估路径 | NB 介入程度 | 临床要求 | 文档审核深度 |
|---------|--------------|------------|---------|------------|
| **Class I (非灭菌/非测量/非重复使用)** | 自我声明（Annex I + IV） | 无 NB 介入 | 基础 | 低 |
| **Class I (灭菌/测量/重复使用)** | Annex V/VI + NB 审核 | 部分审核 | 基础 | 中 |
| **Class IIa** | Annex IX（含Part A审核）或 Annex XI | NB 审核技术文档 | 需 CER | 中-高 |
| **Class IIb** | Annex IX（含Part A审核）或 Annex X/XI | NB 深度审核 | 需完整 CER | 高 |
| **Class III** | Annex IX（含Part A+B深度审核）或 Annex X | NB 最深度审核 | 需最完整 CER | 最高 |

---

## 二、GSPR (Annex I) 逐项核查清单

### 2.1 Chapter 1：通用要求 (§1-§9)

| # | GSPR 条款 | 核查要点 | 常见缺陷 |
|---|----------|---------|---------|
| §1 | 器械不得危害健康或安全 | Benefit-risk 分析完整性 | 仅有 benefit 描述，无结构化 risk 评估 |
| §2 | 设计和制造应以安全为先 | Risk management file 与设计的关联性 | RMF 与实际设计决策脱节 |
| §3 | 高风险器械应有单个防护措施，系统应有多重防护 | §3.2/§3.3 核查 | 缺少单一故障分析 |
| §4 | 制造商应采用适当管理体系 | QMS 有效性证据 | QMS 文件与实际执行不符 |
| §5 | 预期使用寿命内器械应保持安全有效 | 老化测试、寿命验证 | 声称寿命无测试数据支撑 |
| §6 | 预期受益应大于残余风险 | §6 量化受益 vs §3.4 残余风险 | benefit-risk 逻辑不闭环 |
| §7 | 化学/物理/生物学特性 | Biocompatibility、Chemical characterization | 缺少充分性论证 |
| §8 | 感染和微生物污染 | EO 残留、灭菌验证、生物负荷 | 灭菌参数变更无再验证 |
| §9 | 制造与环境 | 环境控制、交叉污染防护 | 生产环境监测数据不完整 |

### 2.2 Chapter 2：设计与制造要求 (§10-§22)

| # | GSPR 条款 | 核查要点 | 常见缺陷 |
|---|----------|---------|---------|
| §10 | 化学/物理/生物学特性 | Material characterization、longevity data | 材料供应商变更无评估 |
| §11 | Infection and contamination | 重复使用器械 reprocessing validation | 临床使用中 reprocessing 实践与验证不符 |
| §12 | Devices with a measuring function | 测量精度、测量范围、校准要求 | 临床环境中测量准确性验证缺失 |
| §13 | Protection against radiation | 辐射安全、诊断器械输出剂量 | 非预期辐射暴露评估缺失 |
| §14 | Devices incorporating electronic systems | Software lifecycle、cybersecurity | 软件版本管理混乱、SBOM 缺失 |
| §15 | Active devices and accessories | Fail-safe design、alarm systems | 失效模式分析不完整 |
| §16 | Protection against electrical shock | Electrical safety testing | 实际使用环境的 electrical safety 验证缺失 |
| §17 | Protection against械被认作药物 | 药物/药物组合器械边界 | 边界情况分类论证缺失 |
| §18 | Protection against harmful substances | 组织/细胞 exposure 评估 | 残留物/降解产物评估不充分 |
| §19 | Protection against features that obstruct lawful use | Anti-theft/anti-counterfeiting | 临床可及性与防伪的平衡缺失 |
| §20 | Information on label and IFU | Label 内容、IFU 可读性 | IFU 未按目标市场语言准备 |
| §21 | Clinical benefit | §21.1 宣称临床获益的证据要求 | 临床获益声明无充分数据支撑 |
| §22 | Manufacturers shall take account of generally acknowledged state of the art | 采用标准说明、state of the art 评估 | 未记录与最新标准的差距 |

---

## 三、技术文档结构核查 (Annex II)

### 3.1 Annex II 完整清单

| # | 章节 | 核查要点 | 常见缺陷 |
|---|------|---------|---------|
| 1 | Device description and specification | 完整描述、变体/配件、与其他产品关系、适应症 | 适应症与风险分析不匹配 |
| 2 | Information to be supplied by the manufacturer | 标签、IFU、所有语言版本 | 临床使用环境与 IFU 描述不一致 |
| 3 | Design and manufacturing information | 设计阶段、 manufacturing sites、供应链 | 设计变更追溯链缺失 |
| 4 | General safety and performance requirements | GSPR 逐条核查矩阵 | 逐条对应不完整，缺少 gap 分析 |
| 5 | Benefit-risk analysis and risk management | §6/§3.4 对应、Risk- Benefit 闭环 | benefit-risk 量化不充分 |
| 6 | Product verification and validation | 临床前测试、临床评价链接 | 测试与 claim 关联性不清晰 |

### 3.2 Product Verification & Validation 详细要求

```
V&V 核查框架：

1. 临床前测试（Pre-clinical）
   ├── 生物相容性（ISO 10993 系列）
   │   ├── 细胞毒性、致敏性、刺激性
   │   ├── 全身毒性（急性/亚慢性）
   │   ├── 植入试验（如适用）
   │   └── 材料介导的致热原性
   │
   ├── 功能性能测试
   │   ├── 设计验证（design verification）
   │   ├── 设计确认（design validation）
   │   └── 性能测试（bench testing）
   │
   ├── 电气安全与电磁兼容（如适用）
   │   ├── IEC 60601-1 系列
   │   └── EMC 测试（IEC 60601-1-2）
   │
   ├── 软件验证（如适用）
   │   ├── IEC 62304 软件生命周期
   │   └── 软件级别（Class A/B/C）
   │
   └── 灭菌验证（如适用）
       ├── ISO 11135（EO 灭菌）
       ├── ISO 11137（辐射灭菌）
       └── ISO 17665（湿热灭菌）

2. 临床评价（Clinical Evaluation）
   └── 见第四章 CER 专项核查

3. 临床随访（PMCF）
   └── 见第五章 PMCF/PMS 专项核查
```

---

## 四、临床评价报告 (CER) 专项核查

### 4.1 CER 法定要求 (MDR Article 61 & Annex XIV)

**CER 是 MDR 核查中最容易被 NB 发补的部分**，必须逐项核查。

| # | CER 要素 | 核查标准 | 常见缺陷 |
|---|---------|---------|---------|
| A.1 | 临床评价计划 (CEP) | 是否明确评价目的、范围、方法？是否定义了等效性路径？ | CEP 与实际评价方法不一致 |
| A.2 | 等效性论证（如走等效性路径） | 临床/技术/生物学等效性逐项对比 | 等效性数据不足，关键数据缺失 |
| A.3 | 临床数据 | 检索策略、纳入排除标准、数据质量评估 | 检索策略不系统，数据来源单一 |
| A.4 | 临床数据分析 | 符合 MDR Annex XIV Part A §3 的分析框架 | 数据分析与 claim 关联性不清晰 |
| A.5 | 临床获益-风险结论 | §6 benefit 与 §3.4 risk 的量化对比 | benefit-risk 逻辑不闭环 |
| A.6 | 剩余风险和不确定性 | 不确定性说明、后续数据收集计划 | 声称无不确定性，未提出 PMCF 需求 |

### 4.2 MDR 对比 MDD 的 CER 要求升级

| 维度 | MDD (旧) | MDR (新) | 应对策略 |
|------|---------|---------|---------|
| 等效性要求 | 较为宽松 | 严格要求，Annex XIV §3 逐项对比 | 等效性论证需更详细数据，临床数据几乎不可复用 |
| 临床数据要求 | 可接受单一文献 | 需系统评价，等效性论证需持续数据支撑 | 建立完整的临床数据管理系统 |
| PMCF 要求 | 非强制 | Article 83-86 强制要求，PMCF 计划不可省略 | 提前规划上市后临床随访 |
| benefit-risk | 简单定性 | MDR §6 要求量化 benefit vs residual risk | 建立量化benefit-risk框架 |

### 4.3 临床数据来源优先级 (MDR Article 61(1))

```
数据来源优先级：
1. 器械本身临床调查数据（最高权重）
2. 等效器械临床调查数据（需充分论证等效性）
3. 科学文献（peer-reviewed）+ 等效性论证
4. 临床经验数据（PMCF/PMS 积累）
```

### 4.4 等效性论证核查 (Annex XIV Part A §3)

**等效性三维度对比矩阵**：

| 维度 | 需要对比的内容 | 数据要求 | 常见缺陷 |
|------|--------------|---------|---------|
| **临床** | 相同临床状态、相似使用者、相似使用部位、相似预期用途 | 临床结果数据、适应症、使用环境对比 | 适应症不完全相同，使用环境差异 |
| **技术** | 相同设计原理、制造工艺、材料、使用条件、部署方法 | 设计规格、材料规格、测试数据对比 | 涂层技术差异导致不等效 |
| **生物学** | 使用相同材料/物质，与人体组织接触特性相同 | 材料 characterization、生物相容性数据 | 药物洗脱机制导致不等效 |

**等效性论证红线**：
- Class III 和 Class IIb 植入器械的等效性论证要求最严格
- 单纯声称"类似原理"不可接受，必须逐维度数据对比
- 药物洗脱器械几乎不可能与裸金属器械论证等效

---

## 五、PMCF/PMS 计划专项核查

### 5.1 MDR PMS 要求概览

| Article | 内容 | 适用类别 |
|---------|------|---------|
| Article 83 | PMS 系统（主动收集数据） | 所有类别 |
| Article 84 | PMS 计划 | 所有类别 |
| Article 86 | PSUR（定期安全更新报告） | IIa 及以上 |
| Annex III | PMS/PMCF 技术文档 | IIa 及以上 |

### 5.2 Annex III PMS Plan 核查

| # | PMS 要素 | 核查要点 | 常见缺陷 |
|---|---------|---------|---------|
| A.1 | PMS 数据收集主动性 | 是否建立了主动收集机制？ | 仅依赖被动投诉，无主动监测 |
| A.2 | 严重事件和 field safety corrective action (FSCA) 上报 | 是否符合 Article 87-92 要求？ | 上报时间节点不合规 |
| A.3 | 非严重事件和不良趋势 | 趋势分析阈值是否定义？ | 阈值设置不合理，无法识别真实趋势 |
| A.4 | 上市后临床随访报告 | PMCF 计划是否与 CER 中识别的不确定性对应？ | PMCF 计划与 CER 差距分析脱节 |
| A.5 | 警戒系统有效性 | 是否定期评估警戒系统运行？ | 仅有 SOP，无执行证据 |

### 5.3 PMCF Plan 核查 (Annex XIV Part B)

| # | PMCF 要素 | 核查要点 | 常见缺陷 |
|---|---------|---------|---------|
| B.1 | PMCF 目标和方法 | PMCF 方法与 CER 中识别的剩余不确定性是否对应？ | PMCF 方法无法回答 CER 中的关键问题 |
| B.2 | PMCF 时间节点 | 是否规定了定期评估？ | 无明确节点，持续拖延 |
| B.3 | 数据来源 | PMCF 数据是否可支撑器械 benefit-risk 更新？ | 数据质量无法满足评估需求 |
| B.4 | PMCF 评估报告 | 是否定期更新 CER？ | PMCF 做完不更新 CER |

---

## 六、MDR vs FDA 临床要求核心差异

详细对比矩阵见 [fda-mdr-gap-matrix.md](fda-mdr-gap-matrix.md)，以下为最关键差异：

| 维度 | FDA | EU MDR | 战略影响 |
|------|-----|--------|---------|
| **临床证据来源** | 可以接受单一 predicate + SE 对比 | 需完整的临床评价，CER 不可省略 | FDA 510(k) 临床要求通常低于 MDR |
| **等效性论证** | 510(k) SE 对比相对宽松 | MDR 等效性要求极其严格，Class III/IIb 植入物几不可复用他厂数据 | 在 MDR 体系下，几乎必须走临床调查路径 |
| **PMCF** | 非强制 | 所有 Class IIa 及以上强制要求 | 需要提前规划上市后临床随访 |
| **临床终点** | FDA 与申办方协商确定 | MDR 要求与 GSPR benefit 对应 | 临床方案设计需同时满足两地要求 |
| **上市后灵活性** | 510(k)/PMA 获批后相对稳定 | MDR Article 83-86 持续监管，PSUR 定期更新 | MDR 合规成本是长期持续投入 |

---

## 七、NB 审评常见发补类型

| 发补类型 | NB 通常会问什么 | 如何预防 |
|---------|----------------|---------|
| **GSPR gap** | "§X 条款的符合性未提供充分证据" | 逐条 GSPR 核查，每条都要有对应的证据文件 |
| **CER 不足** | "等效性论证不充分" / "临床数据质量不足" | 提前规划临床评价策略，不要在 NB 审评前才仓促完成 |
| **PMCF 不充分** | "CER 中识别的剩余不确定性，PMCF 计划无法解决" | PMCF 方法需与 CER 中关键问题一一对应 |
| **Benefit-Risk 闭环缺失** | "benefit-quantification 与 residual-risk 对比不充分" | 建立量化 benefit-risk 框架，而非泛泛定性描述 |
| **变更追溯** | "该设计变更未体现在风险管理文件中" | 建立变更控制流程，确保 RMF 与设计同步更新 |

---

## 八、MDR 技术文档自审模板

### 8.1 MDR 合规自审报告模板

```markdown
# MDR 合规自审报告
- 器械名称：
- MDR 分类：
- 符合性评估路径：
- 审评机构（NB）：
- 自审日期：

## 总体合规状态

| 维度 | 状态 | 优先级 |
|------|------|--------|
| Annex I GSPR |  |  |
| Annex II 技术文档 |  |  |
| Annex III PMS Plan |  |  |
| Annex XIV CER |  |  |

## 关键缺陷清单

| # | 缺陷描述 | MDR 条款 | 补强行动 | 责任人 | 截止日期 |
|---|---------|---------|---------|--------|---------|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |

## NB 交互计划

| 阶段 | 内容 | 预计时间 |
|------|------|---------|
| 预提交 |  |  |
| 正式提交 |  |  |
| 发补响应 |  |  |
| 认证决定 |  |  |
```

---

*本文档为 MDR 合规核查参考，具体要求以 EU MDR 2017/745 最新版本及 MDCG 指导文件为准。*
