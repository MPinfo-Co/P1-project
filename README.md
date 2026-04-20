# MP-Box 專案總導覽

> 本文件是 P1 專案的總入口，所有文件的起點從這裡開始。

MP-BOX 是一套面向企業用戶的 AI 應用平台，協助企業解決資安日誌解讀、專家知識管理、ERP 操作自動化、企業營運解讀等作業難題。

---


## 重要文件索引

| Repo | 路徑/文件 | 用途 |
|------|----------|------|
| P1-project | [CLAUDE.md](CLAUDE.md) | AI agent 工作指引 |
| P1-project | [docs/project-board-guide.md](docs/project-board-guide.md) | GitHub Projects 看板用法、Views 說明、自動化流程（各角色）|
| P1-project | [docs/workflow_guide.md](docs/workflow_guide.md) | 設計理念、整體流程、關鍵機制 |
| P1-project | [docs/issue-body-spec.md](docs/issue-body-spec.md) | 各階段 Issue body 格式（SA/SD/PG） |
| P1-project | [docs/auto-file-format.md](docs/auto-file-format.md) | 自動產生 md 文件格式（business-logic、TDD、TestReport、SpecDiff） |
| P1-project | [docs/repo-design.md](docs/repo-design.md) | Repo 結構、Issue 格式、命名規範 |
| P1-code | [SETUP.md](https://github.com/MPinfo-Co/P1-code/blob/main/SETUP.md) | 開發環境準備，clone 後第一步 |
| P1-design | [TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) | 技術選型與各層選擇原因 |
| P1-design | [FunctionList.md](https://github.com/MPinfo-Co/P1-design/blob/main/FunctionList.md) | 系統功能清單與完成狀態 |

---

## AI 文件審查

定期執行可確保四個 Repo 的文件與實際狀態一致。

| 文件 | 用途 |
|------|------|
| [docs/ai-review/AI-review-prompt.md](docs/ai-review/AI-review-prompt.md) | 文件審查任務 Prompt |
| [docs/ai-review/AI-review-doclist.md](docs/ai-review/AI-review-doclist.md) | 審查範圍清單 |
| [docs/ai-review/AI-review-report.md](docs/ai-review/AI-review-report.md) | 文件審查報告（自動產出） |

對 Claude 說：「請執行 [docs/ai-review/AI-review-prompt.md](docs/ai-review/AI-review-prompt.md)」
→ 產出 `docs/ai-review/AI-review-report.md`
