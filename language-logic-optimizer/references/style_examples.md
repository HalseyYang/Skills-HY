# Style Reference: Scenario-Specific Examples

## WeChat Message / Voice Transcript

**Input (messy):**
> 对了那个CE项目的事，我觉得吧，现在时间挺紧的，然后团队那边人手也不太够，要不我们跟客户沟通一下看能不能延期两周，或者至少先把Part A交了，Part B后面再说，因为Part A其实已经差不多了

**Output:**
> CE项目进度建议：
>
> 目前时间紧、人手不足，建议跟客户沟通两个方案：
> 1. **整体延期两周**
> 2. **先交 Part A，Part B 后补**（Part A 基本完成，可行性较高）
>
> 你倾向哪个方向？我来准备沟通材料。

---

## Work Email / Report

**Input (messy):**
> Hi team, just want to update on the clinical evaluation status. So basically the CER report is almost done, we finished the literature search part last week, and the clinical data analysis is about 80% complete. The problem is we're still waiting on some PMCF data from the sponsor, which might delay the final review. Also I think we need to set up a meeting with the NB to clarify some classification questions before we submit. Let me know your thoughts.

**Output:**
> Team,
>
> **Clinical Evaluation Status Update**
>
> | Workstream | Status | Note |
> |------------|--------|------|
> | Literature search | ✅ Complete | — |
> | Clinical data analysis | 🔄 80% | On track |
> | CER report (final) | ⏸ Pending | Waiting on PMCF data from sponsor |
>
> **Action needed:**
> - **PMCF data**: Sponsor to provide by [date] — any update on timeline?
> - **NB classification**: Need to schedule a call with the NB to clarify classification questions before submission
>
> Proposed: Set up NB call next week. Please confirm availability.

---

## Review Comments / Tech Discussion

**Input (messy):**
> 我看了这个FMEA，有几个问题。第一个是severity的评分我觉得偏高了，比如这个过热的风险，实际使用中几乎不会出现因为有多重保护，所以severity应该降到3或者4。然后failure mode的描述不太一致，有的写得像effect有的写得像cause，建议统一一下格式。还有就是RPN的acceptance criteria没定义，不知道多少算可接受多少需要采取措施。

**Output:**
> FMEA 审核意见：
>
> **1. Severity 评分偏高**
> - 示例：过热风险 — 实际有多重保护措施，发生概率极低
> - 建议：Severity 从当前值降至 3-4
>
> **2. Failure mode 描述不一致**
> - 现状：部分描述写的是 effect，部分写的是 cause，混淆了层级
> - 建议：统一为 cause → failure mode → effect 的三段式描述
>
> **3. RPN 可接受标准缺失**
> - 现状：未定义 RPN threshold，无法判断哪些需采取改进措施
> - 建议：明确 RPN acceptance criteria（如 RPN > X 需 CAPA）

---

## Brainstorm / Draft Notes

**Input (messy):**
> 新产品线想法，我想做那个家用的便携式血氧仪，因为疫情之后大家对健康监测更关注了，而且技术现在也成熟了，成本低。但是竞争也很激烈啊，主要是鱼跃和迈瑞这些大厂，我们作为小公司怎么打？可能要走差异化路线，比如老人用的简化版，或者连接手机APP的数据追踪功能。还有就是认证的问题，国内NMPA二类应该可以，但想出口的话FDA和CE都要考虑，成本和时间都要算进去。

**Output:**
> **新产品线构想：家用便携式血氧仪**
>
> **市场判断**
> - 疫后健康意识提升，家用监测需求增长
> - 技术成熟，成本可控
> - 竞争激烈（鱼跃、迈瑞等头部企业占据主流）
>
> **差异化方向（初步）**
> - 老年人群：极简操作，大字体显示
> - 数据追踪：手机 APP 连接，趋势分析
>
> **监管路径**
> - 国内：NMPA 二类医疗器械
> - 出口：FDA（美国）、CE（欧盟）— 需评估时间和成本投入
>
> ⚠️ 待解决：差异化方向需进一步做竞品分析和用户调研，确认市场切入点
