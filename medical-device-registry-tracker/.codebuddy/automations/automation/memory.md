# 医疗器械法规追踪 - 自动化执行记录

## 2026-04-17 (周五)

### 执行结果
- 状态: ✅ 报告生成成功，✅ IMA上传成功
- 抓取: 17条法规（13条自动抓取 + 4条用户补充）
- 来源分布:
  - 中国法规: 13条 (中检院)
  - 欧盟法规: 1条 (DG SANTE Newsletter补充)
  - 美国FDA法规: 3条 (Federal Register补充)
  - 加拿大: 0条
- 报告周期: 2026-04-10 ~ 2026-04-17
- IMA上传: ✅ 完整版报告已上传

### 已修复问题
1. **抓取源配置问题**:
   - FDA: 添加了 Federal Register 来源 (fda_federal_register)
   - 欧盟: 添加了 DG SANTE Newsletter 来源 (ec_sante_newsletter)
2. **IMA权限**: 之前偶发失败，现在正常

### 重要发现
- FDA 召回页面 ≠ 法规分类！真正的分类法规发布在 **Federal Register**
- 欧盟 EMA 试点项目来自 **DG SANTE newsletter**，不在 EC 主页

---

## 配置更新记录 (2026-04-17)

### 新增来源
- `ec_sante_updates`: DG SANTE最新动态 (https://health.ec.europa.eu/latest-updates_en)
- `ema_events`: EMA即将举行的活动 (https://www.ema.europa.eu/en/events/upcoming-events)
- `fda_federal_register`: FDA Federal Register 法规分类

### 类型变更
- `fda_cdrh`: dynamic → web_fetch（使用 web_fetch 工具成功抓取）

### 关键技术发现
- **web_fetch 工具**可以抓取需要 JS 渲染的页面（FDA CDRH、EMA Events）
- Python Playwright 在 Windows 上有 greenlet DLL 兼容性问题，改用 web_fetch 工具方案
- FDA CDRH 页面返回完整新闻列表（标题、日期、类型、摘要）

---

## 测试结果 (2026-04-17 上午)

### 本周最终抓取统计
- 中国法规: 13条 (中检院)
- 欧盟法规: 5条 (DG SANTE + MDCG + 协调标准 + EMA活动)
- 美国FDA法规: 10条 (3条Federal Register + 7条CDRH新闻)
- **合计: 28条**

### 技术验证
- ✅ web_fetch工具可成功抓取FDA CDRH页面
- ✅ web_fetch工具可成功抓取EMA Events页面
- ✅ web_fetch工具可成功抓取EC最新动态页面
- ⚠️ Python脚本不支持web_fetch类型来源，需在主会话中处理

### IMA上传
- ✅ 完整版报告已上传到「MD法规更新-Testing」

---

---

## 2026-04-20 (周一，本周首次执行)

### 执行结果
- 状态: ✅ 报告生成成功，✅ IMA上传成功
- 报告周期: 2026-04-17 ~ 2026-04-24
- 新增条目: 7条（Python脚本2条 + web_fetch补充5条）
- 来源分布:
  - 中国法规: 1条（中检院标准征集）
  - 欧盟法规: 0条（本周期EC无新发布）
  - 美国FDA法规: 5条（CDRH：指南草案1+安全通报1+召回1+纠错2）
  - EMA活动: 1条（突破性医疗器械信息交流会 04-24）
  - 加拿大: 0条
- IMA上传: ✅ note_id: 7451879009168326，media_id已生成
- 去重记录: 30 → 37条

### 关键技术备注
- 周一执行需指定 --date 2026-04-25 才能得到本周04-17~04-24日期范围
- IMA add_knowledge偶发"没有权限"错误：第一次失败，重试后成功（code: 0）
- NMPA: HTTP 412持续拦截
- Canada.ca: 本周期确认无新发布

---

## 2026-04-20 (周一 - 完整自动化测试)

### 执行结果（web_search 自动补充版）
- 状态: ✅ 报告生成成功，✅ IMA上传成功
- 报告周期: 2026-04-17 ~ 2026-04-24
- 新增条目: 13条（Python脚本4条 + web_search补充14条注入后去重得9条）
- 来源分布:
  - 中国法规: 13条（NMPA 3 + CMDE 4 + 中检院标准 3 + 大湾区 2 + 长三角 2）
  - 欧盟法规: 0条
  - 美国FDA法规: 0条
  - 加拿大: 0条
- IMA上传: ✅ note_id: 7451888920297855
- 去重记录: 37 → 50条

### 自动化流程验证
- ✅ Step1: `run_tracker.py --dry-run` → 生成 pending JSON
- ✅ Step2: AI 读取 pending JSON → 对8个反爬来源执行 web_search
- ✅ Step3: AI 整理搜索结果为标准 JSON → 保存 supplement 文件
- ✅ Step4: `run_tracker.py --web-search-items <json>` → 生成最终报告 + IMA上传
- 全程无需人工干预

### 关键改进
- 新增国内来源: nifdc_standard、cmde_forum、ydcmdei、mdei_gba
- 所有反爬来源统一由 web_search 兜底
- 报告命名加生成日期: regulatory_update_YYYYMMDD_YYYYMMDD_generatedYYYYMMDD.md

---

## 2026-04-24 (周五，本周例行执行)

### 执行结果
- 状态: ✅ 报告生成成功，✅ IMA上传成功
- 报告周期: 2026-04-17 ~ 2026-04-24
- 抓取: 33条（Python脚本25条 + web_search注入8条），过滤后新增 2 条
- 来源分布:
  - 中国法规: 9条（中检院公告）+ 8条 web_search（部分被历史去重拦截）
  - 欧盟法规: 16条（DG SANTE 3 + EC新闻 3 + MDCG 5 + 协调标准 1 + Team NB 4）
  - 美国FDA法规: 0条（CDRH/fda_recalls 均为 web_fetch 需AI处理，本周期无新条目）
  - 加拿大: 0条（Canada.ca 持续超时）
- IMA上传: ✅ note_id: 7453246004156084
- 去重记录: 69 → 71条

### 本周亮点条目
- CN: 医疗器械警戒质量管理规范（试行）发布
- CN: 医疗器械定期风险评价报告审核指南（试行）发布
- CN: 2026年国家医疗器械抽检产品检验方案
- CN: CMDE发布5项有源医疗器械注册审查指导原则（血管内超声、激光治疗设备等）
- EU: MDCG 发布多份指南文件

---

## 2026-04-24 补充执行（用户要求完整版）

### 执行结果
- 状态: ✅ 完整版报告生成成功，✅ IMA上传成功
- 报告周期: 2026-04-17 ~ 2026-04-25
- 总条目: **41条**（不过滤去重，全部纳入）
- 来源分布:
  - 中国法规: 18条（中检院10 + web_search补充8）
  - 欧盟法规: 23条（DG SANTE 3 + EC新闻 3 + MDCG 8 + Team NB 4 + 额外补充 7）
- IMA上传: ✅ note_id: 7453261212699682，媒体ID已生成，关联知识库「MD法规更新-Testing」

### 本次新增的EU重要条目（之前被dedup拦截）
1. **MDCG 2021-12 Rev.1** — EMDN FAQ（EMDN命名法常见问题）
2. **EU MDR/IVDR Targeted Revision (COM/2025/800)** — 170页改革提案核心内容：
   - III类/IIb植入器械证书有效期延长至2030年6月30日
   - Article 4新增Rule 11（AI/ML SaMD分类）
   - UDI数据库全面整合、优化临床证据要求
   - MDR Article 120(2c) 延长过渡期
3. **MDCG 2021-24 Rev.1** — 医疗器械分类指南更新（含Rule 11软件分类）
4. **Manual on Borderline 2026年更新** — 数字健康产品与医疗器械边界判定
5. **Member States' National Requirements 2026更新** — 临床试验国家要求
6. **制造商不良事件报告XSD/SB 11154** — EUDAMED警戒模块标准化
7. **MDCG 2020-16 Rev.3** — IVDR分类规则第3版修订

### 发现的问题
- **EU网站大规模改版**：原MDCG/EC URL全部404，需用web_search重新定位正确链接
- **去重逻辑缺陷**：EU来源为 in-place 更新（同一URL替换新版本），导致重复URL被dedup错误拦截

### 待修复项
- [ ] 去重逻辑：增加 `source + title` 或 `source + date` 双重去重，防止 in-place 更新被误拦
- [ ] EU来源：添加 EC Commission 提案页面为独立来源
- [ ] EMDN：添加 EMDN 官方页面为独立来源

---

## 历史摘要

| 日期 | 报告周期 | 条目 | IMA上传 | 备注 |
|------|---------|------|---------|------|
| 2026-04-17 | 2026-04-10~04-17 | 28 | ✅ 成功 | 首次完整运行 |
| 2026-04-20 早 | 2026-04-17~04-24 | 7 | ✅ 成功 | 仅部分来源 |
| 2026-04-20 午 | 2026-04-17~04-24 | 13 | ✅ 成功 | web_search自动补充全量 |
| 2026-04-24 早 | 2026-04-17~04-24 | 2 | ✅ 成功 | 例行执行 |
| **2026-04-24 补** | **2026-04-17~04-25** | **41** | ✅ 成功 | **完整版（不过滤去重）** |
