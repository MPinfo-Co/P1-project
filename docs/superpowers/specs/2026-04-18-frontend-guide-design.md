# Frontend Guide 文件設計規格

**日期：** 2026-04-18
**目標產出：** `P1-project/docs/frontend-guide.md`
**對象：** 個人學習 + 新進同事
**風格：** 教學型（場景導向）

---

## 目標

撰寫一份以「使用者操作主流程」為主線的前端說明文件，幫助讀者理解：
1. 各技術框架在這個專案裡扮演什麼角色
2. 各檔案之間怎麼串連
3. 為什麼這樣設計

---

## 文件位置

`P1-project/docs/frontend-guide.md`

---

## 章節結構

### 第 1 章：這份文件怎麼讀
- 目標讀者說明
- 建議閱讀順序
- 搭配哪些檔案對照

### 第 2 章：技術選型一覽
一張表格，欄位：框架 / 用途 / 解決的問題 / 對應檔案

涵蓋：React、React Router v6、MUI、Zustand、React Context、Vite

### 第 3 章：主流程走讀（核心章節）

每個小節固定格式：
1. 一句話說這步在做什麼
2. 資料流向（文字箭頭）
3. 關鍵程式碼片段（節錄）
4. 設計原因

**3.1 程式啟動**
- `main.jsx` 掛載 React App、套用 MUI ThemeProvider
- `theme.js` 定義全域色彩與元件樣式覆寫

**3.2 登入流程**
- `Login.jsx` 送出表單
- `authStore.js`（Zustand）呼叫後端 `/api/auth/login`，拿到 JWT 存入 localStorage
- `ProtectedRoute`（App.jsx）讀取 token 決定是否放行

**3.3 進入主畫面**
- `App.jsx` 路由結構：`/` 以下共用 `Layout`
- `Layout.jsx` 三欄：Sidebar（260px）+ Header + `<Outlet />`（子頁面）
- `Sidebar.jsx` NavLink active 狀態邏輯
- `Header.jsx` 依路徑動態顯示頁面標題

**3.4 瀏覽事件清單**
- `IssueList.jsx` 使用 `fetch` 直接打 `/api/events`，帶 JWT header
- 篩選條件（狀態、日期、關鍵字）為本地 state，「套用」後才觸發 API
- `useCallback` + `useEffect` 控制 fetch 時機
- MUI Table + Popover 顯示影響範圍詳情

**3.5 開啟事件詳情**
- `IssueDetail.jsx` 從路由 params 取 `issueId`，GET `/api/events/:id`
- 三個 Tab（事件詳情 / 歷史事件 / 處置紀錄）用 `tabIndex` state 控制顯示
- 處置紀錄：POST `/api/events/:id/history`，送出後重新 fetch 刷新畫面
- 右側聊天面板（Collapse 收合）目前為 placeholder

### 第 4 章：狀態管理設計
解釋兩種狀態管理的分工與邊界：

| 狀態 | 工具 | 原因 |
|------|------|------|
| 登入 / JWT token | Zustand | 需跨元件、需持久化 localStorage |
| 資安事件資料 | React Context | 僅限 App 內部，Context 就夠 |

說明決策原則：能用 local state 就用 local state；需要跨元件共享才往上提；需要持久化才用 Zustand。

**特別說明：** `IssuesContext` 目前讀的是 `data/issues.js`（mock 資料），但 `IssueList.jsx` 和 `IssueDetail.jsx` 實際上直接呼叫 API，並未使用此 Context。文件應說明此現狀，避免讀者誤解。

### 第 5 章：技術框架速查表
各框架的核心概念、在本專案的用法、常見問題各一段。

### 第 6 章：目前尚未完成的功能
- AI 聊天面板（右側 placeholder）
- 歷史事件 tab（Epic 2，尚無資料）
- 負責人員顯示（目前只有 User #ID，等 users API）

---

## 格式規範

- 語言：繁體中文（zh-TW）
- 程式碼片段：節錄關鍵部分，不貼整份檔案
- 箭頭格式：`A → B → C`
- 每章開頭一句話說明本章目的

---

## 不在範圍內

- 後端說明
- 知識庫、設定頁面的詳細介紹（僅在目錄說明用途）
- 部署與 CI/CD
