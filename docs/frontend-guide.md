# MP-Box 前端說明文件

> 本文以「使用者操作主流程」為主線，帶你了解 P1-code 前端各檔案如何串連，以及每個技術框架為什麼在這裡出現。

---

## 目錄

1. [這份文件怎麼讀](#1-這份文件怎麼讀)
2. [技術選型一覽](#2-技術選型一覽)
3. [主流程走讀](#3-主流程走讀)
   - [3.1 程式啟動](#31-程式啟動)
   - [3.2 登入流程](#32-登入流程)
   - [3.3 進入主畫面](#33-進入主畫面)
   - [3.4 瀏覽事件清單](#34-瀏覽事件清單)
   - [3.5 開啟事件詳情](#35-開啟事件詳情)
4. [狀態管理設計](#4-狀態管理設計)
5. [技術框架速查表](#5-技術框架速查表)
6. [目前尚未完成的功能](#6-目前尚未完成的功能)

---

## 1. 這份文件怎麼讀

**目標讀者：** 剛接觸 P1-code 前端的開發者，不論是個人學習或新進同事皆適用。

**建議閱讀順序：**
1. 先看「技術選型一覽」，對齊框架認知（5 分鐘）
2. 從 3.1 開始按順序走讀主流程（核心，30 分鐘）
3. 讀完後再看「狀態管理設計」，理解全局資料流
4. 遇到不熟悉的框架，去「技術框架速查表」補充細節

**搭配對照的原始碼：**

| 本文章節 | 對應檔案 |
|---------|---------|
| 3.1 程式啟動 | `frontend/src/main.jsx`、`frontend/src/theme.js` |
| 3.2 登入流程 | `frontend/src/pages/Login/Login.jsx`、`frontend/src/stores/authStore.js` |
| 3.3 主畫面 | `frontend/src/App.jsx`、`frontend/src/components/Layout/` |
| 3.4 事件清單 | `frontend/src/pages/AiPartner/IssueList.jsx` |
| 3.5 事件詳情 | `frontend/src/pages/AiPartner/IssueDetail.jsx` |
| 4. 狀態管理 | `frontend/src/stores/authStore.js`、`frontend/src/contexts/IssuesContext.jsx` |

> 所有檔案路徑皆相對於 `P1-code/` 根目錄。

---

## 2. 技術選型一覽

在進入流程之前，先認識這個專案用了哪些框架、各自解決什麼問題。

| 框架 | 用途 | 解決的問題 | 主要檔案 |
|------|------|-----------|---------|
| **React 18** | UI 元件化 | 用宣告式寫法描述畫面，資料變動時自動更新 UI | 所有 `.jsx` 檔 |
| **React Router v6** | 前端路由 | 不重新整理頁面就能切換 URL 對應的元件 | `App.jsx` |
| **MUI (Material UI) v6** | UI 元件庫 | 提供現成的 Button、Table、Tabs 等元件，統一視覺風格 | 所有 pages |
| **Zustand** | 全域狀態管理 | 跨元件共享狀態，並能持久化到 localStorage | `stores/authStore.js` |
| **React Context** | 區域狀態管理 | App 內部共享資料，比 Zustand 輕量 | `contexts/IssuesContext.jsx` |
| **Vite** | 開發/打包工具 | 極速的 HMR（熱更新），取代傳統 webpack | `vite.config.js` |

> **為什麼同時有 Zustand 和 Context？** 兩者都能跨元件共享資料，但職責不同。詳見第 4 章。

---

## 3. 主流程走讀

以下按照使用者實際操作順序，逐步說明每個環節涉及哪些檔案、資料怎麼流動、以及為什麼這樣設計。

---

### 3.1 程式啟動

**這步在做什麼：** 瀏覽器載入頁面，React 掛載到 HTML，全域主題套用完成。

**流程：**
```
index.html（#root）
  → main.jsx（createRoot + render）
    → ThemeProvider（套用 theme.js）
      → CssBaseline（重置瀏覽器預設樣式）
        → App（路由入口）
```

**關鍵程式碼（`main.jsx`）：**
```jsx
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </StrictMode>
)
```

**`theme.js` 做了什麼：**
```js
const theme = createTheme({
  palette: { primary: { main: '#2e3f6e' } },  // 深藍色為主色
  typography: {
    fontFamily: "-apple-system, ..., 'Microsoft JhengHei', sans-serif",  // 支援中文字型
  },
  components: {
    MuiButton: { styleOverrides: { root: { textTransform: 'none' } } },  // 按鈕不強制大寫
  },
})
```

**設計原因：**
- `ThemeProvider` 包住整個 App，讓所有 MUI 元件自動套用相同的主色與字型，不需要每個元件重複設定。
- `CssBaseline` 消除瀏覽器預設的 margin/padding 差異，確保跨瀏覽器一致。
- `StrictMode` 在開發環境下幫助找出潛在問題（例如 effect 執行兩次是正常的）。

---

### 3.2 登入流程

**這步在做什麼：** 使用者輸入帳密，前端呼叫後端取得 JWT，登入狀態存入瀏覽器，後續所有 API 請求帶著這個 token。

**流程：**
```
Login.jsx（使用者填表單）
  → authStore.login()（Zustand）
    → POST /api/auth/login
      → 拿到 access_token
        → 存入 localStorage
          → 頁面跳轉到 /
```

**關鍵程式碼（`authStore.js`）：**
```js
login: async (email, password) => {
  const res = await fetch(`${BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  if (res.status === 401) throw new Error('帳號或密碼錯誤')
  const { access_token } = await res.json()
  localStorage.setItem('mp-box-token', access_token)   // 持久化
  set({ token: access_token, user: { email } })         // 更新 Zustand state
},
```

**守門機制（`App.jsx`）：**
```jsx
function ProtectedRoute({ children }) {
  const { token } = useAuth()
  return token ? children : <Navigate to="/login" replace />
}
```

只要 `token` 不存在（未登入或 token 清空），`ProtectedRoute` 就把使用者踢回 `/login`。

**設計原因：**
- token 存在 `localStorage` 而非只放在 state，是因為頁面重新整理後 state 會清空，但 `localStorage` 不會。`authStore` 初始化時會從 `localStorage` 讀取：`token: localStorage.getItem('mp-box-token') || null`。
- 登出時同時清空 `localStorage` 和 Zustand state，確保兩邊同步。
