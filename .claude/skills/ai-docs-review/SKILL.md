---
name: ai-docs-review
description: 執行 P1 四個 Repo 的文件審查，依審查原則逐一分析並輸出結構化建議報告
allowed-tools: Read Glob Grep Bash Agent
sync: 此檔案與 P1-project/.claude/skills/ai-docs-review/SKILL.md 保持同步，修改後須同步更新並 push P1-project
---

請依照以下文件執行 P1 文件審查任務：

1. 讀取任務指令：`P1-project/docs/ai-review/AI-review-prompt.md`
2. 讀取審查清單：`P1-project/docs/ai-review/AI-review-doclist.md`

依指令中的 Phase 1-4 順序執行，完整輸出報告。
