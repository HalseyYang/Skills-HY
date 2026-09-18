# FDA 注册路径策略

## 1. 先定义 subject device

将产品拆成以下监管维度：

- intended use / indications for use；
- target population；
- user / use environment；
- principle of operation；
- energy / material / delivery / measurement mechanism；
- hardware / software / accessory boundaries；
- diagnostic / monitoring / therapeutic claims；
- invasive / implantable / life-supporting / life-sustaining attributes；
- model/family differences。

所有后续 classification 和 predicate 检索均基于这些维度，不得只按商品名匹配。

## 2. Classification 与 pathway

按顺序执行：

1. 搜索可能的 regulation number、product code、device class 和 panel；
2. 打开 product code 详情页，核验 submission type、exemption 及 limitation of exemption；
3. 查看 special controls、相关 guidance 和 recognized standards；
4. 检索相近 510(k)、De Novo、PMA 产品；
5. 形成主路径以及必要的备选路径。

Class II 不等于自动需要 510(k)；必须核查 exemption。存在合适 legally marketed predicate 才能进入 510(k) SE 逻辑。缺乏合适 predicate 且风险适合 Class I/II 时评估 De Novo；高风险 Class III 或法规明确要求时评估 PMA。

## 3. 510(k) 类型

### Traditional 510(k)

作为新制造商、新产品或无法满足 Special 条件时的常规路径。

### Special 510(k)

只有在申请人对其**自身已合法上市的设备**进行设计或标签变更，且评估方法成熟、所需性能数据可用 summary / risk analysis 形式充分审查时才考虑。不得把“型号迭代”本身当成 Special 510(k) 的充分条件。

### Abbreviated 510(k)

如当前 FDA 仍适用该程序，且项目适合依赖 guidance、special controls 或 consensus standards，可作为备选；每次使用前需实时核验当前项目适用性。

## 4. Predicate strategy

内部至少形成三层判断：

### Primary Predicate

优先选择在 indications for use 和 technological characteristics 上与 subject device 最接近的 legally marketed device。

### Additional Predicate

只有在 FDA SE 框架允许且确有必要时使用。不得通过一个器械拼 intended use、另一个器械拼 technology 的方式构成 split predicate。

### Reference Device

可用于支持科学方法或标准参考值，也可作为技术讨论的辅助背景，但不能替代 Primary Predicate 建立 intended use 或 technological characteristics 的 substantial equivalence。

每个候选至少比较：

| 维度 | 要点 |
|---|---|
| Regulatory identity | product code / regulation / class / submission |
| Intended use | 使用目的、疾病、患者、用户、环境 |
| Technology | 原理、能量、材料、算法、结构 |
| Performance | 关键输出和规格 |
| Safety profile | 与差异相关的主要风险 |
| Evidence used | predicate 当时使用的 bench / animal / clinical evidence |
| Relevance | Primary / Additional / Reference / Similar only |

必须阅读公开 summary/decision 文件。只知道 K number 不能完成 Predicate 评估。

## 5. SE 风险评估

对每一项技术差异问：

1. 是否改变 intended use？
2. 是否改变 fundamental scientific technology 或引入新的安全有效性问题？
3. 差异能否通过 bench、software、animal、biocompatibility、electrical、usability 等数据解决？
4. 是否引入新的临床 performance claim？
5. predicate 或 reference 的 FDA 文件中是否有相同或相近差异的监管 precedent？

输出应明确哪些差异是低风险等同、哪些是关键 SE 风险。

## 6. 临床数据判断

不得直接根据器械类别或单一 predicate 下结论。

按以下顺序判断：

1. 法规、special controls 或 guidance 是否明确要求临床证据；
2. primary predicate 和近期同类设备是否提交 clinical data；
3. 如果提交，研究的具体目的是什么；
4. subject device 是否存在同样需要人体数据解决的问题；
5. bench / animal / software / comparative performance 能否覆盖；
6. intended use 或 claim 是否扩大到需要 clinical validation；
7. 是否存在相反 precedent；
8. 仍不确定时是否应通过 Pre-Sub 确认。

“FDA 同类产品曾做过临床”不等于本产品必做；“某 predicate 未做临床”也不等于本产品可保证免临床。

## 7. 中国/欧洲临床数据用于 FDA

若需要 clinical evidence，继续评估：

- 数据是否来自 OUS investigation；
- GCP、伦理、知情同意、数据完整性是否满足 FDA 接受条件；
- 患者、疾病谱、临床实践、终点和设备版本与美国申报是否具有可转移性；
- 是否存在美国特有因素需要 bridging；
- 是否需要 Pre-Sub 先确认接受性。

不得默认要求美国临床，也不得默认中国数据一定充分。

## 8. Evidence package

根据产品属性判断是否需要：

- bench / mechanical / functional performance；
- electrical safety / EMC；
- software documentation；
- cybersecurity；
- wireless / interoperability；
- biocompatibility；
- sterilization / microbiological / packaging / shelf life；
- reprocessing；
- human factors/usability；
- animal study；
- clinical performance；
- radiation-emitting product requirements；
- labeling / UDI implications。

Evidence package 必须由 device risk + predicate differences + claims 驱动，不可套用固定标准清单。

## 9. 并行合规义务

将“Premarket pathway”和“商业上市合规”分开。根据项目检查：

- QMSR；
- Establishment Registration / Device Listing 的适用主体和时点；
- foreign manufacturer 的 U.S. Agent；
- UDI；
- radiation-emitting electronic product reporting；
- cybersecurity statutory obligations；
- import / labeling / MDR reporting 等。

不得把 establishment registration/device listing 错写成一般 510(k) 递交前必须完成的技术准备步骤。

## 10. Pre-Sub 决策

出现以下情形时优先考虑 Pre-Sub：

- predicate strategy 不干净；
- 新机制或重大技术差异；
- 临床是否需要存在真实不确定性；
- 非临床方案复杂或存在多个可接受方法；
- 计划使用 OUS clinical data 且接受性存在疑问；
- 人因、软件、AI/ML、网络安全或新 claim 对证据要求影响重大。

Pre-Sub 问题应针对具体监管决策，例如“拟议 bench package 是否足以支持某技术差异”“FDA 是否认为拟议 clinical design 可支持某 claim”。避免让 FDA 替申请人做 classification 或用诱导式问题要求“同意无需临床”。
