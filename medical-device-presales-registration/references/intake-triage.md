# 输入提取与项目分诊

## 0. Target Market Gate — 必须先执行

在任何法规检索、分类判断或路径设计之前，先确认目标申报市场。

### 可直接进入分析的情形

- 用户本次明确指定 FDA/美国；
- 用户本次明确指定 CE/EU MDR/欧盟；
- 用户明确指定中国/NMPA或其他市场；
- 用户明确要求中美欧、FDA+CE 或其他多市场组合；
- 当前对话中**同一产品、同一任务**已经明确市场，且用户是在继续该任务。

### 必须先询问的情形

用户只说“评估这个产品”“测试一下这个产品”“看看注册路径”“帮我分析”，且当前任务没有明确目标市场。

此时只问一个问题：

> 这次主要评估哪个市场：FDA、EU MDR，还是中美欧/其他市场？

在用户确认前，不自行默认 FDA、EU MDR 或多市场，也不启动大规模法规检索和完整方案生成。

### 新产品切换规则

若用户在同一对话中切换到一个新产品，上一产品的目标市场不能自动继承。只有用户明确说“这个也按FDA”“同样做欧盟”等，才沿用市场范围。

## 1. 输入优先级

产品事实按以下顺序使用：

1. 用户本次明确说明；
2. 用户上传的说明书、规格书、标签、技术文件、测试或临床资料；
3. 制造商公开官方资料；
4. 其他公开信息只能用于补充线索，不得覆盖用户产品资料。

若用户资料内部冲突，标记冲突并指出具体字段；不要自行选择一个版本当事实。

## 2. 内部事实台账

至少提取：

- 产品名称、型号、系列差异；
- intended use / indications / target population / users / use environment；
- 工作原理和作用机制；
- 关键结构、材料、输出参数和关键性能；
- invasive / implantable / active / measuring / monitoring / diagnostic / therapeutic 属性；
- sterile / reusable / single-use / shelf life / packaging；
- software / algorithm / AI / cloud / mobile / wireless / interoperability；
- patient-contacting parts 和接触类型；
- 已有测试、动物、临床、可用性和上市后数据；
- 已获批国家或已有证书；
- 多型号之间的差异。

每项标记为 `Source-confirmed / Officially verified / Analysis / Pending`。

## 3. 市场确认后什么时候提问

先判断缺失信息是否会改变：

- device qualification；
- classification；
- submission pathway；
- clinical requirement；
- core testing scope；
- 是否需要另一个 submission。

若不会，继续做条件式评估，不停下来问细节。

默认只保留一个最重要开放问题放在最终输出末尾；只有多个独立 blocker 确实使路径无法形成时才集中追问。

## 4. 多型号产品

不得只记录型号名称。必须判断：

- 是否具有相同 intended use；
- 核心作用机制是否一致；
- 关键技术差异是否引入不同风险；
- 是否可以放在同一 FDA submission / CE family；
- 哪些型号适合作为代表型号或 worst case；
- 不同型号是否会触发不同测试或标签。

若现有资料不足以支持系列合并，只能写“初步可考虑同一系列申报，需基于型号差异矩阵进一步确认”。

## 5. 商务信息按需收集

仅在用户要求报价或正式报价内容时，再收集：客户名称、签约主体、服务范围、服务费、税率、币种、第三方费用、目标启动时间等。

完整售前注册评估即使没有报价信息，也应生成法规策略 Final DOCX；报价区块可省略或标记“待商务确认”。
