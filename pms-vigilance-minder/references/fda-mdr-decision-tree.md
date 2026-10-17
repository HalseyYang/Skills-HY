# FDA 医疗器械警戒（MDR）报告决策树（21 CFR Part 803）

> **用途**：美国市场的警戒规则与 EU 不同，制造商最常栽在「判定」和「起算点」上。本文件给 FDA MDR 报告的可执行决策流。

---

## 1. 三步判定：是否 reportable

```
事件收到（投诉/不良事件/服务记录/文献）
   │
   ▼
① 事件是否与器械相关？（器械可能是原因/促成因素）
   │ 否 → 记录在投诉系统，不报
   ▼ 是
② 后果是否达到 death / serious injury / malfunction？
   │
   ├─ death ────────────────┐
   ├─ serious injury ───────┤
   │  （life-threatening、永久/显著损伤、需介入防止永久损伤）│
   │                        ▼
   │              ③ 是否需要采取补救行动？
   │                   │
   │                   ├─ 是 → 【5-day report】
   │                   └─ 否 → 【10-day report】
   │
   └─ malfunction ──────────┐
       （可能促成 death/serious injury 若复发）│
                              ▼
                     【30-day report】（malfunction 类）
```

## 2. 三类报告时限（21 CFR 803.50/803.53）

| 类型 | 触发 | 时限 | 提交方式 |
|------|------|------|---------|
| **5-day report** | 事件需采取补救行动（recall/repair/modify/notify）且被 FDA 要求报告；或事件导致死亡/严重伤害且需补救 | **5 个工作日** | eMDR |
| **10-day report** | 器械可能已/可能导致 death 或 serious injury | **10 个工作日** | eMDR |
| **30-day report** | 器械 malfunction 且可能促成 death/serious injury | **30 个工作日** | eMDR |

**起算点**：制造商**首次获知**事件的日期（any employee 获知即启动）——与 EU 一致。

## 3. 报告内容必备（803.50）

1. 患者信息（匿名化：年龄/性别/体重）
2. 事件描述 + 时间线
3. 器械信息：型号/批号/序列号/UDI/使用日期/失效日期
4. 器械是否取出/送回 + 状态
5. 事件后果（death/serious injury/malfunction + 细节）
6. 补救行动描述
7. 制造商评估与初步结论
8. 报告人信息 + 联系方式

## 4. 汇总报告

- **季度汇总**：30-day 类事件可按季度汇总提交
- **年度汇总**：部分类别的年度趋势报告
- **用户设施（医院）报告**：death → 10 工作日报 FDA + 制造商；serious injury → 10 工作日报制造商

## 5. 常见错误（483/警告信高频）

| 错误 | 后果 |
|------|------|
| 起算点用「事件发生日」而非「首次获知日」 | 系统性迟报 |
| 「serious injury」判定过严（漏报） | 最严重的违规类型 |
| 补救行动未在 5 个工作日内启动报告 | 逾期 |
| 报告内容缺器械 UDI/序列号 | 无法追溯 |
| 投诉系统与 MDR 系统两套数据不一致 | 检查时对不上 |

---

*依据：21 CFR Part 803（MDR Reporting）；FDA Guidance "Medical Device Reporting for Manufacturers"（现行版）；eMDR 电子提交要求。*
