# Automation: Git 自动同步 skills 目录

## 任务
检查 `~/.workbuddy/skills/` 的 Git 变更，有变更则 `git add . && git commit -m "Auto-sync: <date> skill updates" && git push origin main`。

## 关键环境事实（重要，每次运行先读）
- 仓库：`https://github.com/HalseyYang/Skills-HY.git`，分支 `main`。
- **2026-09-11 修复**：remote URL 原先内嵌了一个**已失效**的 classic PAT（`ghp_...`，GitHub API 返回 401）。
  该失效凭据会导致推送静默卡死（HTTP/2 + 无效凭据协商挂起，无任何输出，可挂 9 分钟以上）。
  已执行 `git remote set-url origin https://github.com/HalseyYang/Skills-HY.git` 移除内嵌凭据。
- **有效凭据来源**：Windows 凭据管理器（Git Credential Manager, `credential.helper=manager`），
  存有用户 `HalseyYang` 的有效 OAuth token（`gho_...`，API 200，对目标仓库有写权限）。
- 其他 git 配置：`http.sslbackend=openssl`；`http.postbuffer=524288000`；`http.lowspeedtime=999999`。

## 推送前必做的稳妥前缀
```
cd ~/.workbuddy/skills && GIT_TERMINAL_PROMPT=0 git -c http.version=HTTP/1.1 push origin main
```
- `GIT_TERMINAL_PROMPT=0`：避免无人值守时弹出图形化凭据输入框导致永久挂起。
- `-c http.version=HTTP/1.1`：绕开 Windows 上 Git 走 HTTP/2 时可能的推送挂起。

## 已知无关噪音
- `humanize-ppt` 是嵌套 git 仓库（gitlink 160000），但 `.gitmodules` 中**无对应 mapping**，
  其内部 `SKILL.md` 常处于 dirty 状态，父仓库始终显示 ` M humanize-ppt`。
  非本任务范围，**不要**尝试修复或清理。
- `git add .` 后若仍有残留，优先排查嵌套仓库/子模块，而非重复提交。

## 执行历史
- **2026-09-11**：79 项变更（73 修改 / 1 删除 / 5 新增，含新技能 `branded-16-9-html-deck`、`pptx-template-clean-rebuild`）。
  提交 `e9d28ee`。首次推送卡死 → 诊断出内嵌 PAT 失效 → 改用凭据管理器 + HTTP/1.1 → 推送成功
  （`<sha>..e9d28ee main -> main`），remote/local HEAD 一致。已修复 remote URL 并清理临时文件。
- **2026-09-18**：规模最大的一次。834 files changed, +10217 / -143096。
  主要为大批旧 skill 目录整体删除（canvas-design / nuwa-skill / huashu-design / brainstorming /
  regulatory-affairs-* / mdr-745-specialist 等），新增 `bioray-ppt-delivery`、`fda-510k-pathway`、
  `hfe-human-factors`、`mdr-tech-doc-generator`、`medical-device-clinical-evaluation`、
  `medical-device-techfile-sted`、`pms-vigilance-minder`、`standard-interpretation`、
  `wechat-topic-research`、`global-device-safety-surveillance`。提交 `203d0fe`，
  首次推送即成功（`e9d28ee..203d0fe main -> main`，HTTP/1.1 前缀生效，耗时仅 5s）。
  工作树干净。
  经验补充：`GIT_TERMINAL_PROMPT=0 git -c http.version=HTTP/1.1 push` 前缀目前稳定，无需重试逻辑；
  本次全流程（add/commit/push）后台执行合计约 12s。

## 记录习惯
- 每次运行：先读本文件；结束后仅追加一行执行历史摘要（日期 / 变更规模 / commit sha / 是否成功）。
- 不写入完整输出或文件清单正文。
