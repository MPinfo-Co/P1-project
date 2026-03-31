# P1 專案總導覽

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

## PM 工作起點

1. Issues → New Issue → 選 **Epic** template，填寫功能說明與驗收條件
2. 送出後系統自動在 P1-analysis 建立 SA Issue、A-Branch 與 Draft PR
3. 在 Epic Issue 追蹤各階段進度（系統自動回填 SA / SD / PG Issue 連結）
4. 所有 PG Issue merge 後，PM 驗收並手動關閉 Epic

---

## 重要文件索引

### P1-project（本 Repo）

| 文件 | 用途 |
|------|------|
| [docs/workflow/quick-start.md](docs/workflow/quick-start.md) | 各角色第一天操作指南 |
| [docs/repo-design.md](docs/repo-design.md) | Repo 結構、Issue 格式、命名規範 |
| [docs/workflow/guide.md](docs/workflow/guide.md) | 設計理念、整體流程、關鍵機制 |

### P1-design

| 文件 | 用途 |
|------|------|
| [TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md) | 技術選型與各層選擇原因 |
| [FunctionList.md](https://github.com/MPinfo-Co/P1-design/blob/main/FunctionList.md) | 系統功能清單與完成狀態 |

### P1-code

| 文件 | 用途 |
|------|------|
| [SETUP.md](https://github.com/MPinfo-Co/P1-code/blob/main/SETUP.md) | 開發環境準備，clone 後第一步 |

