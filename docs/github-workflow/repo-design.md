# GitHub Repo 設計規範

## Repo 總覽

```
P1-project    開發以外的專案工作（技術研究、規範文件）
P1-analysis   需求分析（A-Repo）
P1-design     系統設計（D-Repo）
P1-code       系統開發（C-Repo）
```

---

## 各 Repo 目錄結構

### P1-project

```
P1-project/
├── README.md
├── issue#1/               ← 選擇性，無固定格式
│   └── README.md / .doc / .txt
├── issue#2/
│   └── ...
└── docs/
    └── github-workflow/   ← 本規範文件所在位置
```

---

### P1-analysis（A-Repo）

```
P1-analysis/
├── issue#4/               ← 必須建立，以 Issue 編號命名
│   ├── 商業邏輯說明.md     ← Use Case、Use Case Description、流程圖、Class Diagram、ER 示意
│   └── SD-WBS.md          ← 列出 SD 需完成的工作項目清單
│                              例：1. 修改 User Schema  2. 新增 Leave Table
│                                  3. POST /api/leaves  4. GET /api/leaves
│                                  5. 畫面：請假申請頁
├── issue#5/
│   └── ...
```

**原則：**
- 每個 issue 對應一個資料夾，資料夾本身就是這個 issue 的完整 delta record
- 資料夾內文件格式不限，以清楚說明商業邏輯為目標

---

### P1-design（D-Repo）

```
P1-design/
├── README.md
├── TechStacks.md          ← 技術棧選型文件
├── Schema.md              ← 資料庫 Schema 全覽（User、Company...）
├── FunctionList.md        ← 系統功能清單
│
├── Prototype/             ← 畫面原型（HTML）
│   ├── 01A.html           ← 登入畫面
│   ├── 01B.html           ← 忘記密碼畫面
│   ├── 02A.html           ← 首頁畫面
│   ├── 03A.html           ← 使用者查詢畫面
│   ├── 03B.html           ← 使用者新增畫面
│   └── ...
│
├── Spec/                  ← 規格文件（活文件，永遠反映最新狀態）
│   ├── 01LoginAPI.md
│   ├── 01LoginPage.md     ← 前端規格（畫面邏輯、API 呼叫關係）
│   ├── 02HomeAPI.md
│   ├── 02HomePage.md
│   ├── 03UserAPI.md
│   ├── 03UserPage.md
│   ├── UserAPI.md
│   ├── CompanyAPI.md
│   └── ...
│
├── TestPlan/              ← 測試計劃（以 Issue 為單位）
│   ├── issue#4.md         ← 自動產生「修改項目」+ 人工填寫「測試案例」
│   ├── issue#6.md
│   └── ...
│
└── SD測試報告/
    └── issue#4.md
```

**活文件 vs Delta Record：**

| 類型 | 位置 | 說明 |
|------|------|------|
| 活文件 | `Spec/`、`Prototype/`、`Schema.md` | 永遠反映最新狀態 |
| Delta Record | `TestPlan/issue#N.md` | 記錄「這個 issue 改了什麼」+ 測試案例 |

**TestPlan/issue#N.md 格式：**

```markdown
# TestPlan：Issue #N 標題

## 修改項目及內容
<!-- 由 GitHub Actions 自動產生，勿手動編輯 -->
- 02HomeAPI.md：新增 getHomeInfo() API
- 03B.html：加入備註欄位，姓名欄位由 3 碼改為 8 碼

## 測試案例
<!-- 由 SD 人工填寫 -->
| ID | 類型 | 前置條件 | 操作 | 預期結果 |
|----|------|---------|------|---------|
| T1 | 整合 | 登入 Tenant A | POST /api/leaves | 201，回傳 leave_id |
| T2 | 單元 | 無 | calculate_leave_days(2025-01-06, 2025-01-10) | 5 |

## 關聯項目
- SA Issue：P1-analysis #N
- SD Issue：P1-design #N（本 Issue）
- 上一個 commit：{前一個 commit hash}
- 本次 commit：{本次 commit hash}
```

---

### P1-code（C-Repo）

```
P1-code/
├── frontend/              ← React + TypeScript
├── backend/               ← Python + FastAPI
├── tests/
│   ├── unit/              ← 單元測試
│   └── integration/       ← 整合測試
│
├── VersionDiff/           ← Merge 時自動產生
│   ├── issue#4_Rex_20260326.md
│   └── ...
│
└── PG測試報告/
    └── issue#4.md
```

**VersionDiff/issue#N_作者_日期.md 格式：**

```markdown
# VersionDiff：Issue #N 標題

## 修改項目及內容
<!-- 由 GitHub Actions 自動產生 -->
- backend/routers/leaves.py：新增 POST /api/leaves endpoint
- backend/models/leave.py：新增 Leave model
- frontend/src/pages/LeavePage.tsx：新增請假申請頁面

## 關聯項目
- SA Issue：P1-analysis #N
- SD Issue：P1-design #N
- PG Issue：P1-code #N（本 Issue）
- 上一個 commit：{前一個 commit hash}
- 本次 commit：{本次 commit hash}
```

---

## 命名規則

### Branch 命名
```
issue-{編號}-{簡短說明}
```
範例：`issue-4-leave-request`、`issue-12-user-profile`

由 GitHub Actions 自動建立，**不手動建立分支**。

### Commit Message 格式
```
{type}({scope}): {說明}
```

| Type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修復 bug |
| `docs` | 文件變更 |
| `refactor` | 重構 |
| `test` | 測試相關 |
| `chore` | 建置、設定 |

範例：
```
feat(leaves): 新增請假申請 API
docs(schema): 更新 Leave table 欄位說明
test(leaves): 新增 POST /api/leaves 整合測試
```

格式由 `commitlint + pre-commit` 強制執行，不符合格式的 commit 會被擋下。

### 檔案命名
- Spec 文件：`{畫面編號}{功能名稱}{類型}.md`，例：`03UserAPI.md`、`03UserPage.md`
- Prototype：`{畫面編號}{子頁面}.html`，例：`03A.html`、`03B.html`
- TestPlan：`issue#{編號}.md`
- VersionDiff：`issue#{編號}_{作者}_{日期}.md`
