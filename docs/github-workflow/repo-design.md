# GitHub Repo 設計規範

## Repo 總覽

```
P1-project    產品管理（Epic、技術研究、規範文件）← PM 大本營
P1-analysis   需求分析（A-Repo）
P1-design     系統設計（D-Repo）
P1-code       系統開發（C-Repo）
```

---

## 各 Repo 目錄結構

### P1-project（PM 大本營）

```
P1-project/
├── README.md
├── issue#1/               ← Epic Issue，選擇性建立資料夾
│   └── 背景說明.md
├── issue#2/
│   └── ...
└── docs/
    └── github-workflow/   ← 本規範文件所在位置
```

**Epic Issue body 格式：**

```markdown
## 功能說明
<!-- 這個功能要解決什麼問題？ -->

## 驗收條件
<!-- 完成的定義是什麼？ -->

## 關聯 Issue
<!-- 由系統自動填入，勿手動編輯 -->
- SA Issue：P1-analysis #
- SD Issue：P1-design #
- PG Issue：P1-code #
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
- 每個 Issue 對應一個資料夾，資料夾本身就是這個 Issue 的完整 delta record
- 資料夾內文件格式不限，以清楚說明商業邏輯為目標

**SA Issue body 格式（結構化，供 AI 讀取）：**

```markdown
## 功能說明

## 關聯項目
- Epic：P1-project #1
- SA Issue：P1-analysis #4（本 Issue）
- SD Issue：P1-design #（merge 後自動填入）
- 階段：SA
```

---

### P1-design（D-Repo）

```
P1-design/
├── README.md
├── TechStacks.md          ← 技術棧選型文件
├── Schema.md              ← 資料庫 Schema 全覽（User、Company...）
├── FunctionList.md        ← 系統功能清單
│
├── Prototype/             ← 畫面原型（HTML，活文件）
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
├── TestPlan/              ← 測試計劃（以 Issue 為單位的 delta record）
│   ├── issue#5.md
│   ├── issue#6.md
│   └── ...
│
└── SD測試報告/
    └── issue#5.md
```

**活文件 vs Delta Record：**

| 類型 | 位置 | 說明 |
|------|------|------|
| 活文件 | `Spec/`、`Prototype/`、`Schema.md` | 永遠反映最新狀態 |
| Delta Record | `TestPlan/issue#N.md` | 記錄「這個 Issue 改了什麼」+ 測試案例 |

**SD Issue body 格式（結構化，供 AI 讀取）：**

```markdown
## 設計範圍

## 關聯項目
- Epic：P1-project #1
- SA Issue：P1-analysis #4
- SD Issue：P1-design #5（本 Issue）
- PG Issue：P1-code #（merge 後自動填入）
- 階段：SD

## 若為拆分 Issue
- 父 Epic：P1-project #1
- 原始 SD Issue：P1-design #5
- 本拆分標記：[1b]
```

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
- Epic：P1-project #1
- SA Issue：P1-analysis #4
- SD Issue：P1-design #5（本 Issue）
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
│   ├── issue#7_Rex_20260326.md
│   └── ...
│
└── PG測試報告/
    └── issue#7.md
```

**PG Issue body 格式（結構化，供 AI 讀取）：**

```markdown
## 實作範圍
<!-- 由系統自動填入 SD 異動的 Spec/Prototype 清單 -->

## 關聯項目
- Epic：P1-project #1
- SA Issue：P1-analysis #4
- SD Issue：P1-design #5
- PG Issue：P1-code #7（本 Issue）
- 階段：PG
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
- Epic：P1-project #1
- SA Issue：P1-analysis #4
- SD Issue：P1-design #5
- PG Issue：P1-code #7（本 Issue）
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
