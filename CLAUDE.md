# CLAUDE.md

## 專案簡介

MP-BOX 是一套面向企業用戶的 AI 應用平台，協助企業解決各類作業難題。
核心功能包含：資安日誌解讀與風險處置、專家知識管理、企業技能管理（如 ERP 操作自動化）、
以及企業營運狀況解讀（財務、營運、工作執行）。

## 專案架構

P1 由四個 Repo 組成，對應四個開發階段：

| Repo | 層級 | 負責角色 |
|------|------|---------|
| **P1-project** | 產品管理（Epic、規範文件） | PM |
| **P1-analysis** | 需求分析（業務邏輯、Use Case、SD-WBS） | SA |
| **P1-design** | 系統設計（Prototype、API Spec、Schema、TestPlan） | SD |
| **P1-code** | 系統開發（React/JavaScript + Python/FastAPI） | PG／AI |

## 目錄結構

### P1-project（產品管理）
```
P1-project/
├── README.md                     # 專案總導覽與文件索引
├── CLAUDE.md                     # AI agent 工作指引（本文件）
├── PRD.md                        # 產品需求文件
├── AI-CONTEXT.md                 # AI 背景資訊
└── docs/
    ├── repo-design.md            # Repo 結構與格式規範
    ├── directory-structure.md    # 各 Repo 目錄結構速查
    ├── AI-review-prompt.md       # AI 文件審查任務 Prompt
    ├── AI-review-gap-prompt.md   # AI 缺口與孤立文件掃描 Prompt
    ├── AI-review-doclist.md      # AI 文件審查範圍清單
    └── workflow/
        ├── guide.md              # 設計理念與整體流程
        ├── quick-start.md        # 各角色操作指南
        └── spec/                 # 各 workflow 技術規格
```

### P1-analysis（需求分析）
```
P1-analysis/
├── issue-{N}/
│   ├── business-logic.md         # 商業邏輯說明
│   └── SD-WBS.md                 # 工作分解結構
└── references/                   # 全域參考文件（架構圖、命名規則等）
```

### P1-design（系統設計）
```
P1-design/
├── Spec/                         # API 規格
├── TestPlan/
│   ├── issue-{N}.md              # 完整測試計畫
│   └── issue-{N}-diff.md         # 本次 delta
├── schema/                       # DB Schema
└── Prototype/                    # UI Prototype（HTML）
```

### P1-code（系統開發）
```
P1-code/
├── backend/
│   ├── app/
│   │   ├── api/                  # API 路由
│   │   ├── core/                 # 設定、依賴、安全
│   │   ├── db/                   # DB Session
│   │   ├── models/               # SQLAlchemy Models
│   │   ├── schemas/              # Pydantic Schemas
│   │   ├── services/             # 業務邏輯層
│   │   └── tasks/                # 背景任務
│   ├── tests/                    # 後端單元測試（CI 執行範圍）
│   └── alembic/                  # Migration
├── frontend/src/                 # 前端主目錄（JavaScript）
│   ├── components/               # 共用元件
│   └── pages/                    # 頁面（依功能分資料夾）
├── tests/                        # 根目錄整合測試（CI 不執行）
└── VersionDiff/                  # 版本異動紀錄
```

## 開發流程

Epic（P1-project）→ SA Issue（P1-analysis）→ SD Issue（P1-design）→ PG Issue（P1-code）
每個階段由上游 merge 後 GitHub Actions 自動建立下游 Issue 與 Branch。

## AI 實作指引（PG 階段）

收到 PG Issue 後，沿關聯鏈讀取：
1. PG Issue body「實作範圍」（系統自動填入 SD 異動的 Spec 清單）
2. `P1-design/Spec/` — API 與畫面規格
3. `P1-design/TestPlan/issue-{SD#}-diff.md` — 本次 delta
4. `P1-analysis/issue-{SA#}/business-logic.md` — 商業邏輯背景
5. `P1-design/TestPlan/issue-{SD#}.md` — 測試標準（pytest 數量 ≥ TestPlan 案例數）

## Branch 與 Commit 規範

- Branch：`issue-{N}-{slug}`，由 GitHub Actions 自動建立，**不手動建立**
- 跨 Repo 溝通加前綴：`A-issue-N`（analysis）、`D-issue-N`（design）、`C-issue-N`（code）
- Commit：`{type}({scope}): 說明`，由 commitlint 強制執行
  - 常用 type：`feat` / `fix` / `docs` / `refactor` / `test` / `chore`

## 技術棧

| 層 | 選型 |
|----|------|
| **前端** | JavaScript + React 19 + React Router v7 + Vite |
| **後端** | Python 3.12 + FastAPI |

完整技術棧（UI 元件、State、ORM、部署等）見 [P1-design/TechStack.md](https://github.com/MPinfo-Co/P1-design/blob/main/TechStack.md)。

## 任務規模判斷

任務涉及以下情況時，主動建議使用 Subagent 平行處理：
- 需要跨多個 Repo 操作
- 有多個可獨立進行的步驟（無相依關係）
- 預計需要 5 個以上工具呼叫

## 語言

所有文件與 Issue template 使用繁體中文（zh-TW）。
