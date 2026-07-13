# FDA 申报路径决策树

本文档提供 FDA 医疗器械申报路径的完整决策框架，涵盖 510(k)、De Novo、PMA 以及 Breakthrough Device Designation (BDD) 四大通道。

---

## 一、通道概览对比

| 维度 | 510(k) | De Novo | PMA | BDD（可叠加） |
|------|--------|---------|-----|--------------|
| **适用条件** | 有 predicate device，substantially equivalent | 无 predicate，novel 且 low-moderate risk | 无 predicate，Class III high risk | 严重疾病 + 未满足需求 + 突破性 |
| **器械分类** | Class I / II | Class I / II / III（自限） | Class III（通常） | 任意高风险器械 |
| **证据要求** | SE comparison + performance testing | Risk-based assessment + clinical数据 | 完整临床试验数据 | 更少初期数据，但需明确unmet need |
| **FDA审评时间** | 90天（目标） | 150天（目标） | 180天+（通常更长） | 与510k/De Novo/PMA并行 |
| **User Fee（2024）** | $21,760 | $134,676 | $425,000+ | 无额外费用（但需先满足主通道） |
| **临床要求** | 通常无需临床试验 | 视产品风险而定 | 通常需要IDE临床试验 | 需要有证据支撑breakthrough claim |
| **申报前准备** | Predicate搜索 + SE对比 | 风险分析 + 可能需要Pre-Sub | 完整IDE临床试验 | 明确的unmet need论证 |

---

## 二、主决策树

```
Start: 器械基本信息
│
├── 器械是否有已上市predicate（功能/适应症基本相同的已批准器械）？
│   │
│   ├── YES → 考虑 510(k) 通道
│   │   │
│   │   ├── 器械是否仅涉及生产/制造变更，无设计/性能变更？
│   │   │   ├── YES → Special 510(k)（30天审评）
│   │   │   └── NO → 继续判断
│   │   │
│   │   ├── 是否有FDA recognized consensus标准可证明符合性？
│   │   │   ├── YES → Abbreviated 510(k)（30天审评）
│   │   │   └── NO → Traditional 510(k)（90天审评）
│   │   │
│   │   └── 设计/性能变更是否存在，但 predicate SE 仍可论证？
│   │       ├── YES → Traditional 510(k)（90天审评）
│   │       └── NO → 转向下方，无 predicate 路径
│   │
│   └── NO → 继续判断
│
├── 该器械是否为 novel 技术，无现有 predicate？
│   │
│   ├── 该 novel 技术是否属于 low-to-moderate risk（即使Class III）？
│   │   ├── YES → De Novo 通道
│   │   │   ├── 是否已有足够的非临床数据支撑风险评估？
│   │   │   │   ├── YES → 直接提交 De Novo
│   │   │   │   └── NO → 建议先提交 Pre-Sub 获取FDA反馈
│   │   │   │
│   │   │   └── 是否值得同时申请 BDD？
│   │   │       ├── YES → 在 De Novo 基础上并行申请 BDD
│   │   │       └── NO → 单独走 De Novo
│   │   │
│   │   └── NO（high risk，无 predicate，无 SE 可能）→ PMA 通道
│   │       │
│   │       └── 是否已启动 IDE 临床试验？
│   │           ├── YES → PMA 准备中，关注FDA审评动态
│   │           └── NO → 强烈建议先提交 Pre-Sub 确认PMA要求
│   │
│   └── 不确定 risk level → Pre-Sub 流程
│
└── 是否已确认有 predicate 但 SE 论证存在争议？
    └── YES → Pre-Sub 流程（建议Q-Sub获取FDA Pre-Sub meeting）
```

---

## 三、510(k) 详细决策

### 3.1 三类 510(k) 适用条件

| 类型 | 触发条件 | 审评目标 | 证据重点 |
|------|---------|---------|---------|
| **Traditional 510(k)** | 设计/性能变更，predicate SE 可论证 | 90天 | SE comparison + performance testing |
| **Abbreviated 510(k)** | 依据 consensus 标准符合性 | 30天 | 符合FDA recognized standards清单 |
| **Special 510(k)** | 仅制造变更，无设计/性能变更 | 30天 | 变更是已验证的，生产工艺变更不影响device |

### 3.2 Substantial Equivalence 判断标准

**必须同时满足**：
1. **Intended Use 相同**：目标适应症、使用环境、患者人群不能有实质差异
2. **Technological Characteristics 相同或不等但同等安全有效**：
   - 使用相同材料/组件
   - 相同设计原理
   - 相同制造工艺

**常见SE被挑战原因**：
- Intended use 扩宽（新增适应症或人群）
- 技术特征改变（如涂层材料、药物洗脱机制 vs 裸金属）
- 新 technology 引入（无充分数据证明与 predicate 等效）

### 3.3 Predicate 搜索策略

1. 访问 FDA 510(k) Database: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm
2. 按 product code (PMA六位代码) 搜索同类器械
3. 按 indication keywords 搜索
4. 筛选近期获批（5年内）的 predicate
5. 确认 predicate 的 K-number 和 clearance date

---

## 四、De Novo 详细决策

### 4.1 De Novo 核心要求

**De Novo 适合**：无 predicate 的 novel 器械，但 FDA 认为其 risk profile 适合通过 De Novo 建立新的 regulatory pathway。

**必须满足**：
- 无合法 predicate（510(k) 不可行）
- 不是 Class III high risk 或可以合理论证属于 low-moderate risk
- 风险可以通过一般性 controls 管控（General Controls）

### 4.2 De Novo vs PMA 决策

```
是否可以通过一般性 controls 管控器械风险？
│
├── YES → De Novo
│   └── 风险是否可以通过 Special Controls 进一步细化管控？
│       ├── YES → Class II De Novo（含 Special Controls）
│       └── NO → Class I De Novo（仅 General Controls）
│
└── NO（一般性 controls 不足以管控风险）
    └── PMA（Class III）
```

### 4.3 De Novo Pre-Sub 建议

**强烈建议在提交 De Novo 前先进行 Pre-Sub**：
- FDA 会给出 device-specific recommendations
- 确认是否有必要进行临床试验
- 确认器械分类是否准确
- 避免提交后发现路径错误导致重新设计

---

## 五、PMA 详细决策

### 5.1 PMA 适用场景

- 无 predicate 且 high risk (Class III)
- 植入人体且支撑/维持生命
- 存在潜在致伤风险且无法通过一般性/Special Controls管控

### 5.2 PMA 类型

| 类型 | 适用场景 |
|------|---------|
| **Traditional PMA** | 全新 Class III 器械，无 IDE 临床试验历史 |
| **Modular PMA** | 大型复杂器械，分模块提交 |
| **PMA Supplement** | 已批准 PMA 的变更申请 |

### 5.3 PMA 临床要求

- 通常需要 IDE (Investigational Device Exemption) 临床试验
- 临床试验需符合 21 CFR Part 812
- 临床终点需预先与 FDA 达成一致
- FDA 可能要求至少一项随机对照试验（RCT）

### 5.4 PMA 申报前策略

**强烈建议**：在 PMA 申报前完成以下步骤：

1. **Pre-Sub meeting**：与 FDA 讨论临床试验设计、终点选择、样本量
2. **IDE 批准**：完成临床试验
3. **FDA 对临床方案的书面意见**：确保临床数据可被 FDA 接受

---

## 六、BDD（突破性器械认定）

### 6.1 BDD 与主申报通道的关系

**BDD 不是独立的申报通道**，而是叠加在 510(k)、De Novo 或 PMA 上的**加速认定**。

```
主申报通道（510k / De Novo / PMA）
         ↓
是否满足 BDD 条件？
    ├── YES → 同步提交 BDD request，享受优先审评和互动支持
    └── NO → 单独走主申报通道
```

### 6.2 BDD 四大认定标准（满足其一即可）

| Criterion | 中文描述 | 论证难度 |
|-----------|---------|---------|
| **Breakthrough Technology** | 代表突破性技术 | 高（需证明技术创新性临床价值） |
| **No Approved Alternatives** | 无已批准替代方案 | 中（需充分覆盖竞品 landscape） |
| **Significant Advantages** | 比现有替代方案有显著优势 | 高（需临床证据支撑） |
| **Best Interest of Patients** | 加快可及性符合患者利益 | 中（需患者群体临床紧迫性数据） |

### 6.3 BDD 战略价值

| 价值 | 说明 |
|------|------|
| **优先审评** | FDA 分配更多资源，审评速度更快 |
| **加强互动** | FDA 更愿意与申请方进行正式互动（Priority Interact） |
| **滚动审评** | 可在申报过程中与 FDA 持续沟通，而非等最终决定 |
| **上市后灵活性** | FDA 可能允许在更灵活的条件下批准上市 |

### 6.4 BDD vs 传统路径的决策

```
该器械是否属于以下情况？
├── 严重危及生命或不可逆致残的疾病/状况？
│   └── YES → 值得评估 BDD，继续判断
│       └── NO → BDD 价值有限，考虑传统路径
│
├── 是否存在未被满足的临床需求？
│   └── YES → 继续判断 BDD 可行性
│       └── NO → BDD 难以论证，考虑传统路径
│
└── 是否有初步证据支撑突破性 claim？
    ├── YES → BDD 是值得争取的战略选择
    └── NO（仅有理论优势，无数据支撑）
        └── BDD 风险较高，建议先完善证据再申请
```

详细 BDD 战略评估见 [fda-bdd-strategy.md](fda-bdd-strategy.md)

---

## 七、Pre-Sub (Pre-Submission) 流程

### 7.1 何时使用 Pre-Sub

- 申报路径不明确
- 需要 FDA 对临床试验设计的书面反馈
- predicate 选择存在争议
- 创新器械希望提前获得 FDA 建议
- De Novo 提交前（强烈建议）

### 7.2 Pre-Sub 类型

| 类型 | FDA反馈形式 | 时间 |
|------|-----------|------|
| **Meeting** | 面对面/视频会议 | 会议前5天收到FDA议程 |
| **Written Response** | 书面回复 | 70天内 |
| **Teleconference** | 电话会议 | 21天内 |

### 7.3 Pre-Sub 准备清单

1. 明确 Pre-Sub 的具体问题（建议不超过3-5个核心问题）
2. 准备器械描述、预期用途、申报路径计划
3. 如涉及临床试验，准备试验方案草案
4. 提交 Pre-Sub package（含 Q-Sub Cover Sheet）
5. 预约 FDA 会议

---

## 八、综合路径推荐流程图

```
                    ┌─────────────────────────┐
                    │  器械基本信息 + 适应症   │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │  有无 predicate device？ │
                    └───────────┬─────────────┘
                      YES       │       NO
                    ┌────┴────┐  │
                    ▼         ▼  ▼
              ┌─────────┐  ┌──────────────────┐
              │ 510(k)  │  │ Novel器械 + risk? │
              │ 可行？   │  └────────┬─────────┘
              └───┬────┘     LOW-MOD  │  HIGH
                  │ YES  ┌──────┴──────┐
                  │      ▼             ▼
                  │  ┌──────┐       ┌──────┐
                  │  │De Novo│       │ PMA  │
                  │  └──┬───┘       └──┬───┘│
                  │     │              │    │
                  │     ▼              ▼    │
                  │  ┌─────────────┐ ┌─────┐ │
                  │  │ 值得申请BDD？│ │IDE? │ │
                  │  └──┬──────┬───┘ └──┬──┘ │
                  │     │YES   │NO      │YES  │NO
                  │     ▼      ▼        ▼     ▼
                  │  ┌────┐  ┌────┐  ┌────┐ ┌─────┐
                  │  │BDD+│  │单线│  │PMA │ │Pre-Sub│
                  │  │De Novo│De Novo│ │准备 │ │探索  │
                  │  └────┘  └────┘  └────┘ └─────┘
                  │
                  │NO（SE无法论证）
                  ▼
           ┌──────────────┐
           │  Pre-Sub     │
           │  重新评估路径 │
           └──────────────┘
```

---

*本文件为 FDA 路径决策参考，具体路径选择需结合产品特性和 FDA 最新指南综合判断。*
