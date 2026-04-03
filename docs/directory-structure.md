# 各 Repo 目錄結構說明

> [← 回到總導覽](../README.md)

本文件說明 P1 四個 Repo 的完整目錄結構，包含每個檔案與資料夾的職責、活文件與歷史紀錄的分界，以及常見操作對應哪些檔案應建立或修改。

---

## 總覽

| Repo | 負責角色 | 主要內容 |
|------|---------|---------|
| **P1-project** | PM | Epic Issue、產品需求、規範文件、Workflow 設計 |
| **P1-analysis** | SA | 商業邏輯、Use Case、工作分解（SD-WBS） |
| **P1-design** | SD | API 規格、畫面規格、Schema、Prototype、測試計劃 |
| **P1-code** | PG／AI | 後端（FastAPI）、前端（React）、測試、部署設定 |

---

## P1-project（PM 大本營）

```
P1-project/
├── README.md                      ← 專案總入口，所有文件的起點
├── CLAUDE.md                      ← AI agent 工作指引（本 Repo 的 AI 行為規範）
├── PRD.md                         ← 產品需求文件（功能範圍、目標用戶）
├── AI-CONTEXT.md                  ← AI 背景資訊（系統背景、術語說明）
└── docs/
    ├── repo-design.md             ← Repo 結構規範、Issue 格式、命名規則
    ├── AI-review-prompt.md        ← AI 文件審查任務 Prompt（定期執行）
    └── workflow/
        ├── guide.md               ← 設計理念、整體流程、關鍵機制說明
        ├── quick-start.md         ← 各角色第一天操作指南
        └── spec/                  ← 各 Workflow GitHub Actions 技術規格
            ├── p-workflow.md      ← Epic 開立後的自動化（建立 SA Issue/Branch）
            ├── a-workflow.md      ← SA merge 後的自動化（建立 SD Issue/Branch）
            ├── d-workflow.md      ← SD merge 後的自動化（建立 PG Issue/Branch）
            ├── c-workflow.md      ← PG merge 後的自動化（VersionDiff 產生）
            └── chore-workflow.md  ← Chore Issue 自動建立 Branch 的流程
```

**不應手動建立的檔案：** Epic Issue 由 GitHub UI 開立（非手動建資料夾），Workflow spec 由 PM 維護，其他 Repo 的 Issue 與 Branch 由 GitHub Actions 自動產生。

---

## P1-analysis（A-Repo）

```
P1-analysis/
├── README.md                          ← Issue 索引（每次 SA merge 後手動更新一行）
├── CLAUDE.md                          ← AI agent 工作指引（SA 階段）
│
├── issue-{N}/                         ← 每個 SA Issue 對應一個資料夾，以 Issue 編號命名
│   ├── business-logic.md              ← 商業邏輯（Use Case、流程圖、ER 示意、Class Diagram）
│   └── SD-WBS.md                      ← 工作分解（給 SD 的工作項目清單，含類型與說明）
│
└── references/                        ← 全域參考文件（跨 Issue 共用的背景知識）
    ├── ai-response-scope.md           ← AI 諮詢回覆範圍規則（資安專家功能）
    ├── backend-overview.md            ← 後端架構總覽（FastAPI + Celery + Redis + PG）
    ├── event-naming-rules.md          ← 安全事件命名規則（Gemini Pro Stage 2 適用）
    ├── flash-json-schema.md           ← Flash 中間 JSON Schema 與欄位對應
    ├── gemini-analysis-prompts.md     ← Gemini Flash/Pro 分析 Prompt 說明
    ├── PRD-template.md                ← PRD 撰寫範本
    ├── priority-rating-rules.md       ← 處理優先級評定規則（Gemini Pro Stage 2 適用）
    ├── syslogng-filters.md            ← syslog-ng 過濾規則（預估保留率 ~1%）
    ├── TDD-template.md                ← TDD 撰寫範本
    └── diagrams/                      ← 系統圖表（Mermaid 格式）
        ├── system-architecture.md     ← 系統架構圖
        ├── er-diagram.md              ← 資料庫 ER Diagram
        ├── analysis-pipeline.md       ← 分析 Pipeline 流程圖
        ├── kb-upload-flow.md          ← 知識庫上傳流程圖
        └── log-processing.md          ← LOG 處理流程圖
```

**不應手動建立的檔案：** `issue-{N}/` 資料夾與其中的兩個 md 檔由 **p-workflow 自動 scaffold**，SA 只需填寫內容。SA Issue 本身也由 p-workflow 自動建立，不可手動開立。

---

## P1-design（D-Repo）

```
P1-design/
├── README.md                          ← SD 工作起點指南
├── CLAUDE.md                          ← AI agent 工作指引（SD 階段）
├── TechStack.md                       ← 技術棧選型文件（各層選擇原因）
├── FunctionList.md                    ← 系統功能清單（含完成狀態）
│
├── schema/                            ← 資料庫 Schema（活文件）
│   ├── schema.md                      ← 全覽說明（Table 定義、欄位說明、關聯）← 人工維護
│   └── mpbox_postgresql_v3_drawsql.sql← DrawSQL 匯出的 SQL，供視覺化工具使用
│
├── Prototype/                         ← 畫面原型（HTML，活文件）
│   └── *.html                         ← 各版本 Prototype（命名含版本號）
│
├── Spec/                              ← API 與畫面規格（活文件，永遠反映最新狀態）
│   ├── {N}{功能名}API.md              ← API 規格（Request/Response 格式、錯誤碼）
│   └── {N}{功能名}Page.md             ← 畫面規格（元件、狀態、API 呼叫關係）
│
└── TestPlan/                          ← 測試計劃（以 Issue 為單位的 Delta Record）
    ├── issue-{N}.md                   ← SD 人工填寫（測試案例表格）
    └── issue-{N}-diff.md              ← 系統自動產生（本次修改項目 + 關聯 commit）← 勿手動編輯
```

### 活文件 vs Delta Record

| 類型 | 位置 | 說明 |
|------|------|------|
| **活文件** | `Spec/`、`Prototype/`、`schema/schema.md` | 永遠反映最新狀態，舊版本透過 git history 追溯 |
| **Delta Record** | `TestPlan/issue-N.md`、`TestPlan/issue-N-diff.md` | 記錄「這個 Issue 改了什麼」，不隨後續修改更新 |

**Spec 檔案命名規則：** `{畫面編號}{功能名稱}{類型}.md`，例：`01LoginAPI.md`、`01LoginPage.md`。舊版（無數字前綴，如 `UserAPI.md`）為歷史遺留，新建文件需使用數字前綴格式。

**不應手動建立的檔案：** `TestPlan/issue-{N}-diff.md` 由 d-workflow 自動產生。SD Issue 由 a-workflow 自動建立。`issue-{N}/` 資料夾（若有）由 a-workflow scaffold。

---

## P1-code（C-Repo）

```
P1-code/
├── README.md                          ← PG 工作起點指南
├── CLAUDE.md                          ← AI agent 工作指引（PG 階段）
├── SETUP.md                           ← 開發環境準備（clone 後第一步）
├── SYSTEM.md                          ← 系統架構與資料流說明
├── docker-compose.yml                 ← 本地開發環境（PostgreSQL + Redis）
│
├── backend/                           ← Python 3.12 + FastAPI
│   ├── app/
│   │   ├── main.py                    ← FastAPI app 入口，掛載 Router、設定 CORS
│   │   ├── api/                       ← API 路由（薄層，只做請求解析與回傳）
│   │   │   ├── auth.py                ← 登入、登出、Token 刷新
│   │   │   ├── events.py              ← 安全事件相關 API
│   │   │   └── health.py              ← 健康檢查
│   │   ├── core/                      ← 跨層共用設定
│   │   │   ├── config.py              ← 環境變數讀取（Pydantic Settings）
│   │   │   ├── deps.py                ← FastAPI 依賴注入（取得 DB Session、當前用戶）
│   │   │   └── security.py            ← JWT 產生/驗證、bcrypt 密碼 hash
│   │   ├── db/
│   │   │   └── session.py             ← SQLAlchemy SessionLocal、engine 設定
│   │   ├── models/                    ← SQLAlchemy ORM Models（對應資料庫 Table）
│   │   │   ├── user.py                ← User、Role、UserRole
│   │   │   ├── security_event.py      ← SecurityEvent（安全事件主表）
│   │   │   └── token_blacklist.py     ← TokenBlacklist（登出 Token 黑名單）
│   │   ├── schemas/                   ← Pydantic Schemas（API 輸入輸出驗證）
│   │   │   ├── auth.py                ← 登入請求、Token 回傳格式
│   │   │   └── security_event.py      ← 安全事件查詢與回傳格式
│   │   ├── services/                  ← 業務邏輯層（被 api/ 或 tasks/ 呼叫）
│   │   │   ├── claude_flash.py        ← Claude Flash：LOG 批次摘要（Stage 1）
│   │   │   ├── claude_pro.py          ← Claude Pro：去重彙整分析（Stage 2）
│   │   │   ├── log_preaggregator.py   ← LOG 前處理與預聚合
│   │   │   └── ssb_client.py          ← SSB 外部系統 API 客戶端
│   │   ├── tasks/                     ← 背景任務定義（由 worker.py 執行）
│   │   │   ├── flash_task.py          ← Flash 分析任務
│   │   │   └── pro_task.py            ← Pro 分析任務
│   │   └── worker.py                  ← 任務 Worker 入口（背景佇列處理）
│   ├── alembic/                       ← 資料庫 Migration 管理
│   │   ├── env.py                     ← Alembic 環境設定（載入 models）
│   │   └── versions/                  ← Migration 腳本（依時序累積，勿手動刪除）
│   ├── tests/                         ← pytest 單元測試（CI 執行範圍）
│   ├── scripts/                       ← 手動執行的一次性腳本（不在 CI 範圍）
│   │   ├── run_pipeline.py            ← 手動觸發分析 Pipeline
│   │   └── run_planb_comparison.py    ← Plan B 方案比較測試
│   ├── seed.py                        ← 資料庫初始資料（開發用）
│   ├── requirements.txt               ← Python 依賴清單
│   ├── pyproject.toml                 ← Ruff linter 設定
│   └── .env.example                   ← 環境變數範本（複製為 .env 後填入實際值）
│
├── frontend/                          ← React 19 + Vite（JavaScript）
│   ├── src/
│   │   ├── main.jsx                   ← React 啟動點（掛載 App）
│   │   ├── App.jsx                    ← 路由設定（React Router v7）
│   │   ├── index.css                  ← 全域樣式（Tailwind 基底）
│   │   ├── theme.js                   ← MUI 主題設定（色彩、字型）
│   │   ├── components/                ← 跨頁面共用元件
│   │   │   ├── Layout/                ← 版面框架元件
│   │   │   │   ├── Layout.jsx         ← 整體版面（Sidebar + 主內容區）
│   │   │   │   ├── Header.jsx         ← 頂部導覽列
│   │   │   │   └── Sidebar.jsx        ← 側邊選單
│   │   │   └── ui/                    ← 通用 UI 元件
│   │   │       ├── Badge.jsx          ← 狀態標籤
│   │   │       ├── Modal.jsx          ← 對話框
│   │   │       └── Pagination.jsx     ← 分頁元件
│   │   ├── pages/                     ← 頁面（每個功能一個資料夾）
│   │   │   ├── Login/                 ← 登入頁
│   │   │   ├── Home/                  ← 首頁（儀表板）
│   │   │   ├── AiPartner/             ← AI 夥伴（資安事件分析）
│   │   │   ├── KnowledgeBase/         ← 知識庫（文件、表格、存取設定）
│   │   │   ├── Settings/              ← 設定（帳號、角色、AI 設定）
│   │   │   └── NotFound.jsx           ← 404 頁面
│   │   ├── stores/                    ← Zustand 全域狀態
│   │   │   └── authStore.js           ← 認證狀態（JWT token、用戶資訊）
│   │   ├── contexts/                  ← React Context（較少用，優先考慮 Zustand）
│   │   │   └── IssuesContext.jsx      ← Issues 資料 Context
│   │   ├── data/                      ← Mock 資料（開發階段暫用，正式環境由 API 取代）
│   │   │   ├── aiPartners.js
│   │   │   ├── issues.js
│   │   │   ├── knowledgeBase.js
│   │   │   ├── mockKnowledge.js
│   │   │   └── users.js
│   │   └── assets/                    ← 靜態資源（圖片、SVG）
│   ├── public/                        ← 直接對外公開的靜態檔案
│   ├── index.html                     ← HTML 入口（Vite 注入 main.jsx）
│   ├── vite.config.js                 ← Vite 設定（proxy、alias）
│   ├── tailwind.config.js             ← Tailwind CSS 設定
│   ├── package.json                   ← 依賴清單與 npm scripts
│   └── .env.example                   ← 環境變數範本（VITE_API_URL 等）
│
├── frontend-mui/                      ← MUI 樣式實驗目錄（與主前端獨立，不在 CI 範圍）
│
├── API/                               ← 外部 API 參考文件（PDF，唯讀）
│   ├── REST API Documentation.pdf
│   └── SSB_7.7.0_RPCAPIQuickstartGuide.pdf
│
├── tests/                             ← 根目錄整合測試（CI 不執行，手動驗證用）
│
├── docs/                              ← 補充技術文件
│   ├── 系統入門導覽.md                ← 系統架構導覽（新成員閱讀）
│   └── superpowers/                   ← AI agent 工作紀錄（不影響主線開發）
│       ├── plans/                     ← 實作計畫文件（日期命名）
│       └── specs/                     ← 設計規格文件（日期命名）
│
├── VersionDiff/                       ← 版本異動紀錄（由 c-workflow 自動產生，勿手動建立）
│   └── issue-{N}_{author}_{date}.md
│
└── PG測試報告/                        ← PG 完成實作後手動提交的測試報告
    └── issue-{N}.md
```

**不應手動建立的檔案：** `VersionDiff/issue-{N}_*.md` 由 c-workflow 自動產生於 merge 時。PG Issue 與 Branch 由 d-workflow 自動建立。`alembic/versions/` 下的腳本由 `alembic revision` 指令產生，勿手動新增。

---

## 場景速查

### SA 收到新 Issue，準備開始分析

**應填寫的檔案**（由 p-workflow 已 scaffold，只需填內容）：
- `P1-analysis/issue-{N}/business-logic.md` — Use Case、流程圖、ER 示意
- `P1-analysis/issue-{N}/SD-WBS.md` — 工作項目清單（類型 + 說明）

**merge 後需手動更新**：
- `P1-analysis/README.md` — 在 Issue 索引表新增一行

---

### SD 收到新 Issue，準備開始設計

**應建立或更新的活文件**：
- `P1-design/Spec/{N}{功能名}API.md` — API 規格（新建或更新）
- `P1-design/Spec/{N}{功能名}Page.md` — 畫面規格（新建或更新）
- `P1-design/schema/schema.md` — 如有 Schema 異動
- `P1-design/Prototype/` — 如有畫面異動

**應建立的 Delta Record**：
- `P1-design/TestPlan/issue-{N}.md` — 手動填寫測試案例（SD 負責）

**自動產生（勿手動建立）**：
- `P1-design/TestPlan/issue-{N}-diff.md` — d-workflow 自動產生

---

### PG 收到新 Issue，準備開始實作

**讀取順序**：
1. PG Issue body「實作範圍」（SD 異動的 Spec 清單）
2. `P1-design/Spec/` — API 與畫面規格
3. `P1-design/TestPlan/issue-{SD#}-diff.md` — 本次 delta
4. `P1-analysis/issue-{SA#}/business-logic.md` — 商業邏輯背景
5. `P1-design/TestPlan/issue-{SD#}.md` — 測試標準

**實作後需提交的檔案**：
- `P1-code/PG測試報告/issue-{N}.md` — 測試結果（手動建立）
- 其餘程式碼變更正常 commit 即可

**自動產生（勿手動建立）**：
- `P1-code/VersionDiff/issue-{N}_*.md` — c-workflow 在 merge 時自動產生

---

### 新增或修改 DB Schema

**需同步更新的檔案**：
- `P1-design/schema/schema.md` — 活文件，更新 Table 定義
- `P1-code/backend/alembic/versions/` — 執行 `alembic revision --autogenerate` 產生 migration 腳本
- `P1-code/backend/app/models/` — 更新或新增 SQLAlchemy Model

---

*本文件反映 2026-04-03 的實際 Repo 狀態。結構異動後請同步更新本文件。*
