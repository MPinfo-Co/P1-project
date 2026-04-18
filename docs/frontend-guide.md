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

---

### 3.3 進入主畫面

**這步在做什麼：** 登入成功後，使用者進入主畫面，看到 Sidebar + Header 的佈局框架，子頁面在右側內容區切換。

**路由結構（`App.jsx`）：**
```
/login          → Login（不含 Layout）
/               → Layout（含 Sidebar + Header）
  index         → Home
  /ai-partner   → AiPartner
  /ai-partner/:partnerId/issues        → IssueList
  /ai-partner/:partnerId/issues/:id   → IssueDetail
  /kb           → KnowledgeBase
  /settings/account → Account
  /settings/role    → Role
  /settings/ai-config → AiConfig
```

**Layout 結構（`Layout.jsx`）：**
```jsx
<Box sx={{ display: 'flex', height: '100vh' }}>
  <Sidebar />                          {/* 固定 260px，深色背景 */}
  <Box sx={{ flex: 1, flexDirection: 'column' }}>
    <Header />                         {/* 頂部列，白色背景 */}
    <Box component="main">
      <Outlet />                       {/* 子頁面在這裡渲染 */}
    </Box>
  </Box>
</Box>
```

`<Outlet />` 是 React Router 的概念：父路由定義 Layout，子路由的元件會「插入」到 Outlet 的位置，不需要每個頁面自己重複寫 Sidebar 和 Header。

**Sidebar active 狀態（`Sidebar.jsx`）：**
```jsx
<NavLink to="/ai-partner">
  {({ isActive }) => (
    <ListItemButton sx={isActive ? activeSx : defaultSx}>
      <ListItemText primary="AI夥伴" />
    </ListItemButton>
  )}
</NavLink>
```

React Router 的 `NavLink` 會自動判斷當前路徑是否匹配，提供 `isActive` 讓我們套用不同樣式（左邊紫色 border + 白色文字）。

**Header 動態標題（`Header.jsx`）：**
```js
const PAGE_TITLES = {
  '/ai-partner': 'AI夥伴',
  '/kb': '知識庫',
  '/settings/account': '帳號',
  // ...
}
// 依當前 pathname 找最長匹配的 key
const title = Object.entries(PAGE_TITLES)
  .filter(([path]) => pathname.startsWith(path))
  .sort((a, b) => b[0].length - a[0].length)[0]?.[1] ?? 'MP-Box'
```

標題不是寫死的，而是根據當前 URL 動態對應，新增頁面只需要在 `PAGE_TITLES` 加一行。

**設計原因：**
- Layout 用 `flex` 排列，Sidebar 固定寬度，右側內容區 `flex: 1` 自動填滿剩餘空間。
- `height: '100vh'` 確保佈局永遠填滿整個視窗高度。

---

### 3.4 瀏覽事件清單

**這步在做什麼：** 從後端拉取資安事件列表，顯示成表格，支援狀態/日期/關鍵字篩選，點擊列進入詳情。

**流程：**
```
IssueList.jsx 掛載
  → useEffect 觸發 fetchEvents()
    → GET /api/events?page=1&status=pending,investigating
      → 拿到 { items, total }
        → setRows(items) → 表格重新渲染
```

**篩選的兩階段設計：**

篩選條件分成「輸入中」和「已套用」兩組 state：

```jsx
const [filterStatus, setFilterStatus] = useState('all')   // 使用者正在輸入的值
const [applied, setApplied] = useState({ status: '_default', ... })  // 實際生效的值

function applyFilters() {
  setPage(1)
  setApplied({ status: filterStatus, ... })  // 按下「套用」才生效
}
```

`useCallback` 讓 `fetchEvents` 只在 `applied` 或 `page` 變動時重新建立，避免無限迴圈：

```jsx
const fetchEvents = useCallback(async () => {
  // ... fetch 邏輯
}, [applied, page])  // 只有這兩個值變動才重建

useEffect(() => {
  fetchEvents()
}, [fetchEvents])  // fetchEvents 重建時才觸發
```

**影響範圍 Popover：**

```jsx
<Chip
  label={row.affected_summary}
  onClick={(e) => {
    e.stopPropagation()   // 阻止觸發 row 的點擊事件（避免跳到詳情頁）
    setPopoverAnchor(e.currentTarget)
    setPopoverContent(row.affected_detail)
  }}
/>
<Popover open={Boolean(popoverAnchor)} anchorEl={popoverAnchor} ...>
  {formatDesc(popoverContent)}
</Popover>
```

**設計原因：**
- 篩選不即時觸發 API（不是每次 onChange 就打），而是等使用者按「套用」，避免打太多無效請求。
- `useCallback` + `useEffect` 的組合是 React 中控制非同步請求的標準做法：依賴陣列明確宣告「什麼情況下重跑」。
- 預設只顯示 `pending + investigating`（未結案），讓資安人員看到需要處理的事件，不被已結案的資料淹沒。

---

### 3.5 開啟事件詳情

**這步在做什麼：** 點擊事件後進入詳情頁，顯示事件分析結果、處置建議、原始 log，並可新增處置紀錄。

**流程：**
```
點擊表格列
  → navigate('/ai-partner/:partnerId/issues/:issueId')
    → IssueDetail 掛載
      → GET /api/events/:issueId
        → setEvent(data) → 畫面渲染
```

**取得路由參數：**
```jsx
const { partnerId, issueId } = useParams()  // 從 URL 取出 :partnerId 和 :issueId
```

**三個 Tab 的切換：**
```jsx
const [tabIndex, setTabIndex] = useState(0)

<Tabs value={tabIndex} onChange={(_, v) => setTabIndex(v)}>
  <Tab label="事件詳情" />   {/* tabIndex === 0 */}
  <Tab label="歷史事件" />   {/* tabIndex === 1 */}
  <Tab label="處置紀錄" />   {/* tabIndex === 2 */}
</Tabs>

{tabIndex === 0 && <事件詳情內容 />}
{tabIndex === 1 && <歷史事件內容 />}
{tabIndex === 2 && <處置紀錄內容 />}
```

用 `tabIndex` state 控制顯示，不用 React Router 子路由，因為 Tab 切換不需要改變 URL。

**新增處置紀錄（兩步驟 API）：**
```jsx
async function addHistoryEntry() {
  // Step 1：如果狀態有變，先更新狀態
  if (histStatus !== event.current_status) await updateStatus(histStatus)

  // Step 2：新增歷史紀錄
  await fetch(`/api/events/${issueId}/history`, {
    method: 'POST',
    body: JSON.stringify({ note: histNote }),
  })

  await fetchEvent()  // 重新拉取，畫面自動更新
}
```

**右側聊天面板：**

目前是 placeholder，面板可透過 `chatVisible` state 收合：

```jsx
<Box sx={{ width: chatVisible ? 360 : 40, transition: 'width 0.2s' }}>
  <Collapse in={chatVisible} orientation="horizontal">
    {/* AI 諮詢功能（即將推出）*/}
  </Collapse>
</Box>
```

**設計原因：**
- 詳情頁每次掛載都重新 fetch，確保資料是最新的（不依賴清單頁傳來的快取資料）。
- 送出處置紀錄後呼叫 `fetchEvent()` 重新拉取，讓歷史列表即時更新，不需要手動操作 local state。
- 聊天面板用 `transition: 'width 0.2s'` 做收合動畫，寬度從 360px 收到 40px（只留收合按鈕）。

---

## 4. 狀態管理設計

本章說明這個專案為什麼同時使用兩種狀態管理工具，以及各自的邊界在哪裡。

### 兩種工具的分工

| 狀態 | 工具 | 原因 |
|------|------|------|
| 登入狀態 / JWT token | **Zustand** (`authStore.js`) | 需要跨多個元件共享、且要持久化到 `localStorage` |
| 資安事件資料 | **React Context** (`IssuesContext.jsx`) | 僅在 App 內部共享，Context 就夠用 |
| 篩選條件、loading、tab 狀態 | **Local state** (`useState`) | 只有該元件自己用，不需要往上提 |

### 決策原則

```
資料只有自己用？
  → useState（local state）

需要跨多個元件共享、但不需要持久化？
  → React Context

需要跨元件共享、且需要持久化（localStorage/sessionStorage）？
  → Zustand
```

### Zustand 怎麼用（`authStore.js`）

```jsx
// 建立 store
const useAuthStore = create((set, get) => ({
  token: localStorage.getItem('mp-box-token') || null,
  login: async (email, password) => { /* ... */ },
  logout: async () => { /* ... */ },
}))

// 在任何元件中取用
function Header() {
  const { logout } = useAuth()  // useAuth 是 useAuthStore 的封裝
  return <Button onClick={logout}>登出</Button>
}
```

### React Context 怎麼用（`IssuesContext.jsx`）

```jsx
// 1. 建立 Context
const IssuesContext = createContext(null)

// 2. Provider 包住子樹
export function IssuesProvider({ children }) {
  const [issues, setIssues] = useState(...)
  return <IssuesContext.Provider value={{ issues, updateIssue }}>{children}</IssuesContext.Provider>
}

// 3. 子元件取用
export function useIssues() {
  return useContext(IssuesContext)
}
```

### 注意事項

`IssuesContext` 目前讀取的是 `data/issues.js`（mock 資料），**`IssueList.jsx` 和 `IssueDetail.jsx` 實際上直接呼叫 API，並未使用此 Context**。這是過渡狀態：早期用 mock 資料開發 UI，後來接上真實 API 時直接在元件內 fetch，Context 尚未同步移除。

---

## 5. 技術框架速查表

快速查詢各框架的核心概念與在本專案的用法。

### React
- **核心概念：** 元件（Component）是回傳 JSX 的函式；state 變動時 React 重新渲染元件。
- **本專案用法：** 所有 UI 都是 React 元件（`.jsx` 檔）。
- **常見問題：** `useEffect` 的依賴陣列要列清楚，遺漏依賴會造成資料過時；多餘依賴會造成無限迴圈。

### React Router v6
- **核心概念：** 用 `<Routes>/<Route>` 宣告 URL 對應的元件；`<Outlet>` 讓父路由嵌入子路由；`useParams()` 取 URL 參數；`useNavigate()` 程式化跳頁。
- **本專案用法：** `App.jsx` 定義所有路由，`Layout` 是父路由，子頁面透過 `<Outlet>` 渲染。
- **常見問題：** v6 已移除 `<Switch>`，改用 `<Routes>`；`<Redirect>` 改成 `<Navigate>`。

### MUI (Material UI) v6
- **核心概念：** 提供現成的 React 元件（`Button`、`Table`、`Tabs` 等）；用 `sx` prop 傳入樣式物件做覆寫。
- **本專案用法：** 幾乎所有畫面元素都用 MUI 元件；主色在 `theme.js` 統一設定為 `#2e3f6e`。
- **常見問題：** 樣式覆寫優先使用 `sx` prop，需要全域覆寫才改 `theme.js` 的 `components`。

### Zustand
- **核心概念：** 用 `create()` 建立 store；store 裡可以放 state 和 action；任何元件用 `useXxxStore()` 取用，變動時只有有訂閱的元件重新渲染。
- **本專案用法：** `authStore.js` 管理登入狀態和 JWT token。
- **常見問題：** 不需要 Provider 包住元件，這是 Zustand 比 Context 輕量的地方。

### Vite
- **核心概念：** 開發時用原生 ES Module，不需打包就能執行，HMR 極速；`import.meta.env.VITE_*` 讀環境變數。
- **本專案用法：** `npm run dev` 啟動開發伺服器；API base URL 從 `.env` 的 `VITE_API_URL` 讀取。
- **常見問題：** 環境變數必須以 `VITE_` 開頭才會暴露給前端；`.env` 不要 commit 到 git。
