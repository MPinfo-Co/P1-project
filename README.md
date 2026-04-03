# MP-Box 專案總導覽

> 本文件是 P1 專案的總入口，所有文件的起點從這裡開始。

MP-BOX 是一套面向企業用戶的 AI 應用平台，協助企業解決資安日誌解讀、專家知識管理、ERP 操作自動化、企業營運解讀等作業難題。

---

## 新成員從這裡開始

**[docs/workflow/quick-start.md](docs/workflow/quick-start.md)** — 第一天操作指南，按角色分類的完整步驟

---

## 四個 Repo

| Repo | 層級 | 負責角色 | 連結 |
|------|------|---------|------|
| **P1-project** | 產品管理（Epic、規範文件） | PM | 你在這裡 |
| **P1-analysis** | 需求分析（業務邏輯、Use Case、SD-WBS） | SA | [MPinfo-Co/P1-analysis](https://github.com/MPinfo-Co/P1-analysis) |
| **P1-design** | 系統設計（Prototype、API Spec、Schema、TestPlan） | SD | [MPinfo-Co/P1-design](https://github.com/MPinfo-Co/P1-design) |
| **P1-code** | 系統開發（React/TypeScript + Python/FastAPI） | PG／AI | [MPinfo-Co/P1-code](https://github.com/MPinfo-Co/P1-code) |

```
PM（P1-project）開立 Epic
 └─ p-workflow 自動建立 SA Issue + Branch（P1-analysis）
     └─ SA merge → a-workflow 自動建立 SD Issue + Branch（P1-design）
         └─ SD merge → d-workflow 自動建立 PG Issue + Branch（P1-code）
```

---

## 重要文件索引（AI 文件審查範圍）

| Repo | 文件 | 用途 |
|------|------|------|
| P1-project | [README.md](README.md) | 專案總入口 |
| P1-project | [CLAUDE.md](CLAUDE.md) | AI agent 工作指引 |
| P1-project | [docs/workflow/guide.md](docs/workflow/guide.md) | 設計理念、整體流程、關鍵機制 |
| P1-project | [docs/workflow/quick-start.md](docs/workflow/quick-start.md) | 各角色第一天操作指南 |
| P1-project | [docs/repo-design.md](docs/repo-design.md) | Repo 結構、Issue 格式、命名規範 |
| P1-project | [spec/p-workflow.md](docs/workflow/spec/p-workflow.md) | P-workflow 技術規格 |
| P1-project | [spec/a-workflow.md](docs/workflow/spec/a-workflow.md) | A-workflow 技術規格 |
| P1-project | [spec/d-workflow.md](docs/workflow/spec/d-workflow.md) | D-workflow 技術規格 |
| P1-project | [spec/c-workflow.md](docs/workflow/spec/c-workflow.md) | C-workflow 技術規格 |
| P1-project | [spec/chore-workflow.md](docs/workflow/spec/chore-workflow.md) | Chore-workflow 技術規格 |
| P1-analysis | [README.md](https://github.com/MPinfo-Co/P1-analysis/blob/main/README.md) | SA 工作起點指南 |
| P1-analysis | [CLAUDE.md](https://github.com/MPinfo-Co/P1-analysis/blob/main/CLAUDE.md) | AI agent 工作指引（SA 階段）|
| P1-design | [README.md](https://github.com/MPinfo-Co/P1-design/blob/main/README.md) | SD 工作起點指南 |
| P1-design | [CLAUDE.md](https://github.com/MPinfo-Co/P1-design/blob/main/CLAUDE.md) | AI agent 工作指引（SD 階段）|
| P1-design | [TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) | 技術選型與各層選擇原因 |
| P1-design | [FunctionList.md](https://github.com/MPinfo-Co/P1-design/blob/main/FunctionList.md) | 系統功能清單與完成狀態 |
| P1-code | [README.md](https://github.com/MPinfo-Co/P1-code/blob/main/README.md) | PG 工作起點指南 |
| P1-code | [CLAUDE.md](https://github.com/MPinfo-Co/P1-code/blob/main/CLAUDE.md) | AI agent 工作指引（PG 階段）|
| P1-code | [SETUP.md](https://github.com/MPinfo-Co/P1-code/blob/main/SETUP.md) | 開發環境準備，clone 後第一步 |

