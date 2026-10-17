# EUDAMED 注册步骤详解（PMS 视角）

> 依据：Commission Decision (EU) 2025/2371 + MDR/IVDR Article 29-31
> PMS 相关性：警戒报告、PSUR、FSCA 的提交主体身份都挂在 Actor 模块的 SRN 上——SRN 是 PMS 体系的"身份证"。

## 一、模块与强制时间线

| 模块 | 强制日期 | PMS 相关动作 |
|------|---------|-------------|
| **Actor 注册（ACT）** | ✅ 2026-05-28 | 制造商 + AR + 进口商获 **SRN**——警戒报告提交主体 |
| **UDI / 器械注册** | 新器械 ✅ 2026-05-28；遗留器械 ⏳ 2026-11-28 | 器械级 PMS 数据（投诉/事件）按 UDI-DI 归集 |
| **NB 与证书** | 新证书 ✅ 2026-05-28 起；旧证书 ⏳ 2027-05-28 | PSUR 提交对象、NB 监督审核范围 |
| **市场监督（MSU）** | ✅ 2026-05-28 | 主管当局侧，FSCA/ Trend Report 接收 |
| **警戒与上市后监督（VPMS）** | 📅 开发中（可能 2027） | 就绪后严重事件/FSCA 经 EUDAMED 提交 |

## 二、注册流程

```
1. Actor 模块注册（制造商 + AR）→ 主管机构验证 → 获得 SRN
        │  ⚠️ SRN 必须在器械投放市场之前完成
        ▼
2. UDI/DEV 模块注册器械（UDI-DI + Basic UDI-DI + EMDN + 120+ 字段）
        │  ⚠️ 无有效 SRN 无法进入器械注册
        ▼
3. NB 上传并链接证书 → 状态 "Submitted" → "Registered"
        ▼
4. PMS 体系按 SRN + UDI-DI 归集数据，警戒报告经 PRRC 提交
```

## 三、PMS 实操要点

- **SRN 是警戒报告提交主体**：PRRC 以制造商 SRN 名义提交严重事件、FSCA、Trend Report
- **数据一致性**：PMS 系统中的器械标识（UDI-DI）须与 EUDAMED 注册、技术文档、DoC 完全一致
- **遗留器械 2026-11-28 截止**：未完成注册的器械不得合法投放，其 PMS 义务主体身份断裂
- **swissdamed 不互通**：覆盖瑞士的企业须单独注册 + 单独 CH Rep，PMS 数据分开维护
- **NB 产能**：技术文档评估实际周期 13-18 个月；自 2027-02-25 起 NB 时限法定化（Reg (EU) 2026/977：申请审查+签约 30 天 / QMS 审核 120 天 / 技术文档 90 天 / 发证 20 天）

> 来源：health.ec.europa.eu/medical-devices-eudamed；专家团 regulatory-radar 2026-08-29 整理。
