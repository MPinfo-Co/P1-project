# Frontend 語法說明文件

> 本文配合 [frontend-guide.md](./frontend-guide.md) 使用。
> 閱讀方式：在 frontend-guide.md 遇到不懂的語法 → 查下方索引 → 跳到對應說明。

**讀者假設：** 熟悉 JavaScript 基礎（變數、函式、async/await），未接觸 React 生態系。

---

## 語法索引表

| 語法 | 出現章節 | 跳到說明 |
|------|----------|----------|
| `createRoot().render()` | 3.1 程式啟動 | [連結](#createrootrender) |
| `StrictMode` | 3.1 程式啟動 | [連結](#strictmode) |
| `ThemeProvider` | 3.1 程式啟動 | [連結](#themeprovider) |
| `CssBaseline` | 3.1 程式啟動 | [連結](#cssbaseline) |
| `createTheme()` | 3.1 程式啟動 | [連結](#createtheme) |
| `styleOverrides` | 3.1 程式啟動 | [連結](#styleoverrides) |
| `async / await` | 3.2 登入流程 | [連結](#async--await) |
| `fetch(url, options)` | 3.2 登入流程 | [連結](#fetchurl-options) |
| `JSON.stringify()` | 3.2 登入流程 | [連結](#jsonstringify) |
| `res.status` / `res.json()` | 3.2 登入流程 | [連結](#resstatus--resjson) |
| `localStorage.setItem()` | 3.2 登入流程 | [連結](#localstoragesetitem) |
| Zustand `set()` | 3.2 登入流程 | [連結](#zustand-set) |
| `ProtectedRoute` 模式 | 3.2 登入流程 | [連結](#protectedroute-模式) |
| 三元運算子 `? :` | 3.2 登入流程 | [連結](#三元運算子--) |
| `<Navigate>` | 3.2 登入流程 | [連結](#navigate) |
| `<Routes>` / `<Route>` | 3.3 主畫面 | [連結](#routes--route) |
| 巢狀路由 | 3.3 主畫面 | [連結](#巢狀路由) |
| `<Box sx={...}>` | 3.3 主畫面 | [連結](#box-sx) |
| `<Outlet />` | 3.3 主畫面 | [連結](#outlet-) |
| `<NavLink>` + `isActive` | 3.3 主畫面 | [連結](#navlink--isactive) |
| `Object.entries().filter().sort()` | 3.3 主畫面 | [連結](#objectentriesfiltersort) |
| 可選鏈 `?.` 與空值合併 `??` | 3.3 主畫面 | [連結](#可選鏈--與空值合併-) |
| `useState` | 3.4 事件清單 | [連結](#usestate) |
| `useCallback` | 3.4 事件清單 | [連結](#usecallback) |
| `useEffect` | 3.4 事件清單 | [連結](#useeffect) |
| `e.stopPropagation()` | 3.4 事件清單 | [連結](#estoppropagation) |
| `<Chip>` | 3.4 事件清單 | [連結](#chip) |
| `<Popover>` | 3.4 事件清單 | [連結](#popover) |
| `useParams()` | 3.5 事件詳情 | [連結](#useparams) |
| `<Tabs>` / `<Tab>` | 3.5 事件詳情 | [連結](#tabs--tab) |
| 條件渲染 `&&` | 3.5 事件詳情 | [連結](#條件渲染-) |
| 兩步驟 async function | 3.5 事件詳情 | [連結](#兩步驟-async-function) |
| `transition` 動畫 | 3.5 事件詳情 | [連結](#transition-動畫) |
| `<Collapse>` | 3.5 事件詳情 | [連結](#collapse) |
| `create((set, get) => {...})` | 4. 狀態管理 | [連結](#createset-get--) |
| `useXxxStore()` | 4. 狀態管理 | [連結](#usexxxstore) |
| `createContext()` | 4. 狀態管理 | [連結](#createcontext) |
| `<Context.Provider>` | 4. 狀態管理 | [連結](#contextprovider) |
| `useContext()` | 4. 狀態管理 | [連結](#usecontext) |
| 自訂 hook 封裝 | 4. 狀態管理 | [連結](#自訂-hook-封裝) |

---

## 3.1 程式啟動

### `createRoot().render()`

**是什麼：** React 的入口點，把整個 React App 掛載到 HTML 的指定 DOM 節點上。

**專案範例：**
```jsx
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </StrictMode>
)
```

**白話解釋：** HTML 裡有個 `<div id="root">`，`createRoot` 找到它，`.render(...)` 把 React 畫面貼進去。就像找到一個空盒子，把整個應用程式放進去。

**常見錯誤：**
- `document.getElementById('root')` 的 `'root'` 要和 `index.html` 裡 `<div id="root">` 的 id 一致，打錯就整個空白
- React 17 以前用 `ReactDOM.render()`，React 18 改成 `createRoot`，舊教學看到這個不用驚慌

---

### `StrictMode`

**是什麼：** 開發環境下的警告模式，幫助找出潛在問題，正式上線不影響行為。

**專案範例：**
```jsx
<StrictMode>
  <App />
</StrictMode>
```

**白話解釋：** 像程式碼的「嚴格檢查員」，只在 `npm run dev` 時作用。它會刻意讓某些東西執行兩次（例如 `useEffect`），用來偵測有沒有寫出不安全的副作用。

**常見錯誤：**
- useEffect 執行了兩次以為是 bug，其實是 StrictMode 刻意為之，正式環境只跑一次

---

### `ThemeProvider`

**是什麼：** MUI 的主題容器元件，包住整個 App 後，所有子元件自動套用同一套主題設定。

**專案範例：**
```jsx
<ThemeProvider theme={theme}>
  <CssBaseline />
  <App />
</ThemeProvider>
```

**白話解釋：** 像全校統一校服規定，`ThemeProvider` 是那個規定本體，包在最外層後，裡面所有 MUI 元件都自動套用主色、字型，不需要每個元件重複設定。

**常見錯誤：**
- 主題設定不生效，通常是因為 `ThemeProvider` 沒有包在最外層，或 MUI 元件跑到 ThemeProvider 外面

---

### `CssBaseline`

**是什麼：** MUI 提供的樣式重置元件，消除不同瀏覽器對 margin、padding 的預設差異。

**專案範例：**
```jsx
<CssBaseline />
```

**白話解釋：** Chrome 和 Firefox 對 `<body>` 的預設間距不同，`CssBaseline` 把這些差異全部歸零，讓畫面在各瀏覽器長得一致。

**常見錯誤：**
- 不加 `CssBaseline` 可能導致某些瀏覽器頁面邊緣有多餘空白

---

### `createTheme()`

**是什麼：** 建立 MUI 主題物件的函式，可自訂主色、字型、元件預設樣式。

**專案範例：**
```js
const theme = createTheme({
  palette: { primary: { main: '#2e3f6e' } },
  typography: {
    fontFamily: "-apple-system, 'Microsoft JhengHei', sans-serif",
  },
})
```

**白話解釋：** 就像設定「品牌設計規範」，之後所有 MUI 元件都自動用這個深藍色（`#2e3f6e`）作為主色，改一個地方全站都換。

**常見錯誤：**
- 寫 `primary: '#2e3f6e'` 而非 `primary: { main: '#2e3f6e' }`，MUI 規定要有 `main` 這一層，少了會報錯

---

### `styleOverrides`

**是什麼：** 在 `createTheme` 裡覆寫特定 MUI 元件的預設樣式，全站生效。

**專案範例：**
```js
components: {
  MuiButton: { styleOverrides: { root: { textTransform: 'none' } } },
}
```

**白話解釋：** MUI 的 Button 預設會把文字強制大寫（CSS `text-transform: uppercase`），這裡用 `styleOverrides` 關掉，讓按鈕文字保持原樣，不需要每個 Button 單獨加 `sx`。

**常見錯誤：**
- 元件名稱是 `MuiButton`（小寫 ui），拼成 `MUIButton` 或 `muiButton` 都不會生效

---

## 3.2 登入流程

### `async / await`

**是什麼：** 處理非同步操作的語法，讓等待回應的程式碼讀起來像同步。

**專案範例：**
```js
login: async (email, password) => {
  const res = await fetch(`${BASE_URL}/api/auth/login`, { ... })
  const { access_token } = await res.json()
}
```

**白話解釋：** `fetch` 打 API 需要時間，`await` 就是「等到拿到結果再繼續執行」。不加 `await` 的話，程式碼不等 API 回應就往下跑，會拿到 Promise 物件而非真正的資料。

**常見錯誤：**
- 忘記在函式前加 `async`，加了 `await` 卻沒有 `async` 的函式宣告會直接報語法錯誤
- `await` 只能用在 `async` 函式內部，不能在一般函式裡使用

---

### `fetch(url, options)`

**是什麼：** 瀏覽器內建的 HTTP 請求函式。

**專案範例：**
```js
const res = await fetch(`${BASE_URL}/api/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password }),
})
```

**白話解釋：** 就像寄信，`url` 是收件地址，`method: 'POST'` 是寄信方式（POST = 新增資料），`headers` 說明信封格式（JSON），`body` 是信的內容。

**常見錯誤：**
- POST 請求忘記加 `'Content-Type': 'application/json'`，後端就讀不到 body 的內容

---

### `JSON.stringify()`

**是什麼：** 把 JavaScript 物件轉成 JSON 字串。

**專案範例：**
```js
body: JSON.stringify({ email, password })
```

**白話解釋：** `{ email, password }` 是 JS 物件，但 HTTP 只能傳字串。`JSON.stringify` 把它轉成 `'{"email":"a@b.com","password":"123"}'` 才能放進 body 傳送。

**常見錯誤：**
- body 直接放物件 `{ email, password }` 不轉字串，後端收到的會是 `[object Object]` 字串，完全讀不到值

---

### `res.status` / `res.json()`

**是什麼：** `res.status` 是 HTTP 回應的狀態碼（數字）；`res.json()` 是把回應 body 解析成 JS 物件的非同步方法。

**專案範例：**
```js
if (res.status === 401) throw new Error('帳號或密碼錯誤')
const { access_token } = await res.json()
```

**白話解釋：** 伺服器的回應像回信，`status` 是信上的戳章（200 = 成功、401 = 未授權、500 = 伺服器錯誤），`res.json()` 是拆開信封讀裡面的內容。

**常見錯誤：**
- `res.json()` 本身是非同步的，忘記加 `await` 會拿到 Promise 物件而非解析後的資料

---

### `localStorage.setItem()`

**是什麼：** 把資料存到瀏覽器本地儲存，關閉頁面或重新整理後仍然保留。

**專案範例：**
```js
localStorage.setItem('mp-box-token', access_token)
```

**白話解釋：** 像在瀏覽器裡放一個小抽屜，key（`'mp-box-token'`）是抽屜標籤，value（`access_token`）是放進去的東西。重新整理頁面後還在，關掉分頁也還在。

**常見錯誤：**
- 只把 token 存在 state（`useState`）沒有存 localStorage，頁面重新整理後 state 清空，登入狀態消失
- 對應的讀取是 `localStorage.getItem('mp-box-token')`，刪除是 `localStorage.removeItem('mp-box-token')`

---

### Zustand `set()`

**是什麼：** Zustand 提供的函式，用來更新 store 裡的 state，觸發有訂閱的元件重新渲染。

**專案範例：**
```js
set({ token: access_token, user: { email } })
```

**白話解釋：** 類似 React 的 `setState`，呼叫後 store 裡的值更新，所有有使用這些值的元件自動重新渲染。`set` 是合併（merge）而非取代，只需要傳要改的欄位。

**常見錯誤：**
- `set({ token: null })` 不會刪掉其他欄位（如 `user`），只會把 `token` 改成 null，其他欄位保持不變

---

### `ProtectedRoute` 模式

**是什麼：** 一個包裝元件，用來攔截未登入的使用者並強制跳轉到登入頁。

**專案範例：**
```jsx
function ProtectedRoute({ children }) {
  const { token } = useAuth()
  return token ? children : <Navigate to="/login" replace />
}
```

**白話解釋：** 像門衛，`children` 是要進去的內容（受保護的頁面），有 token（有憑證）才放行，沒有就推回登入頁。在 `App.jsx` 裡把需要登入才能看的路由用 `<ProtectedRoute>` 包住即可。

**常見錯誤：**
- 忘記用 `<ProtectedRoute>` 包住受保護路由，未登入的人可以直接輸入 URL 進入

---

### 三元運算子 `? :`

**是什麼：** 簡化版的 if/else，根據條件回傳兩個值之一。

**專案範例：**
```jsx
return token ? children : <Navigate to="/login" replace />
```

**白話解釋：** `條件 ? 成立時的值 : 不成立時的值`。上面這行等同於：
```js
if (token) { return children } else { return <Navigate to="/login" replace /> }
```

**常見錯誤：**
- 在 JSX 裡不能直接用 `if/else`，條件渲染通常用三元運算子或 `&&`

---

### `<Navigate>`

**是什麼：** React Router v6 的跳轉元件，渲染時立刻跳轉到指定路徑。

**專案範例：**
```jsx
<Navigate to="/login" replace />
```

**白話解釋：** `replace` 表示取代當前的瀏覽器歷史記錄，使用者按「返回」不會回到被攔截的頁面（而是再往前一頁）。

**常見錯誤：**
- React Router v5 用 `<Redirect to="/login" />`，v6 改成 `<Navigate to="/login" />`，兩者不相容

---

## 3.3 進入主畫面

### `<Routes>` / `<Route>`

**是什麼：** React Router v6 宣告 URL 路徑對應元件的語法。

**專案範例：**
```jsx
<Routes>
  <Route path="/login" element={<Login />} />
  <Route path="/" element={<Layout />}>
    <Route index element={<Home />} />
    <Route path="ai-partner" element={<AiPartner />} />
  </Route>
</Routes>
```

**白話解釋：** `<Routes>` 是路由清單，每個 `<Route>` 是一條規則：「當 URL 是 `/login`，就顯示 `<Login />` 元件」。路由規則列在這裡，符合哪條就渲染哪個元件。

**常見錯誤：**
- React Router v5 用 `<Switch>`，v6 改成 `<Routes>`，不能混用
- v6 的 `<Route>` 必須放在 `<Routes>` 裡，不能獨立存在

---

### 巢狀路由

**是什麼：** `<Route>` 裡面包 `<Route>`，子路由繼承父路由的路徑，畫面嵌套在父路由的 `<Outlet>` 位置。

**專案範例：**
```jsx
<Route path="/" element={<Layout />}>
  <Route path="ai-partner" element={<AiPartner />} />
</Route>
```

**白話解釋：** 父路由 `/` 對應 `<Layout>`（含 Sidebar + Header），子路由 `ai-partner` 的完整路徑是 `/ai-partner`，對應的 `<AiPartner />` 會插入 `<Layout>` 裡的 `<Outlet />` 位置。這樣所有子頁面都共用同一個 Layout，不用每個頁面重寫 Sidebar。

**常見錯誤：**
- 子路由的 `path` 不要加開頭的 `/`，寫 `path="ai-partner"` 而非 `path="/ai-partner"`；加了 `/` 會變成絕對路徑，不繼承父路由

---

### `<Box sx={...}>`

**是什麼：** MUI 的萬用容器元件，`sx` prop 接受 CSS 樣式物件。

**專案範例：**
```jsx
<Box sx={{ display: 'flex', height: '100vh' }}>
  <Sidebar />
  <Box sx={{ flex: 1, flexDirection: 'column' }}>
    <Outlet />
  </Box>
</Box>
```

**白話解釋：** `<Box>` 預設渲染成 `<div>`，`sx` 是 MUI 的 CSS-in-JS 寫法。常用版面語法：
- `display: 'flex'`：子元素橫排（CSS Flexbox）
- `flex: 1`：撐滿父容器剩餘空間
- `height: '100vh'`：高度等於整個視窗高度（vh = viewport height）

**常見錯誤：**
- `sx` 的值是字串，寫 `display: flex`（不加引號）會報錯，要寫 `display: 'flex'`
- 數值如 `flex: 1` 不加引號，字串如 `height: '100vh'` 要加引號

---

### `<Outlet />`

**是什麼：** React Router 的佔位符，子路由的元件會渲染到這個位置。

**專案範例：**
```jsx
// Layout.jsx
<Box component="main">
  <Outlet />
</Box>
```

**白話解釋：** `<Layout>` 定義了外框（Sidebar + Header），`<Outlet />` 是中間的空位。當路由切換到 `/ai-partner` 時，`<AiPartner />` 自動填入這個空位。不需要每個子頁面自己重寫 Sidebar 和 Header。

**常見錯誤：**
- 父路由的元件忘記放 `<Outlet />`，子路由元件就永遠不會出現

---

### `<NavLink>` + `isActive`

**是什麼：** React Router 的連結元件，提供 `isActive` 讓你知道當前 URL 是否匹配此連結。

**專案範例：**
```jsx
<NavLink to="/ai-partner">
  {({ isActive }) => (
    <ListItemButton sx={isActive ? activeSx : defaultSx}>
      <ListItemText primary="AI夥伴" />
    </ListItemButton>
  )}
</NavLink>
```

**白話解釋：** `NavLink` 把 `isActive`（布林值）傳給你的 function，你的 function 回傳 JSX。這個模式叫 render props。`isActive` 是 true 就套用 `activeSx`（左側紫色 border + 白色文字），React Router 自動計算當前路徑是否匹配。

**常見錯誤：**
- `isActive` 是 NavLink 算好傳給你的，不需要自己比對 `pathname`

---

### `Object.entries().filter().sort()`

**是什麼：** 三個陣列/物件方法串接，從物件中篩選並排序。

**專案範例：**
```js
const title = Object.entries(PAGE_TITLES)
  .filter(([path]) => pathname.startsWith(path))
  .sort((a, b) => b[0].length - a[0].length)[0]?.[1] ?? 'MP-Box'
```

**白話解釋：**
1. `Object.entries(PAGE_TITLES)` — 把 `{ '/ai-partner': 'AI夥伴', ... }` 轉成 `[['/ai-partner', 'AI夥伴'], ...]`
2. `.filter(([path]) => pathname.startsWith(path))` — 留下路徑開頭匹配當前 URL 的
3. `.sort((a, b) => b[0].length - a[0].length)` — 路徑長的排前面（越具體的匹配優先）
4. `[0]?.[1]` — 取第一筆的標題文字

**常見錯誤：**
- `.sort()` 不傳比較函式時，會用字串排序而非長度排序，結果不可預期

---

### 可選鏈 `?.` 與空值合併 `??`

**是什麼：** `?.` 是「如果存在才取值，否則回傳 undefined」；`??` 是「左側是 null/undefined 就取右側的值」。

**專案範例：**
```js
[0]?.[1] ?? 'MP-Box'
```

**白話解釋：**
- `[0]?.[1]`：如果 `[0]` 存在才取 `[1]`，不存在就回傳 undefined（不報錯）
- `?? 'MP-Box'`：如果結果是 undefined，就用 `'MP-Box'` 當預設值

**常見錯誤：**
- `??` 和 `||` 的差異：`||` 遇到空字串 `''`、`0`、`false` 也會取右側；`??` 只對 `null` 和 `undefined` 生效，空字串和 0 不受影響

---

## 3.4 瀏覽事件清單

### `useState`

**是什麼：** React Hook，在元件內建立一個可觸發重新渲染的狀態值。

**專案範例：**
```jsx
const [filterStatus, setFilterStatus] = useState('all')
const [applied, setApplied] = useState({ status: '_default' })
```

**白話解釋：** `filterStatus` 是讀取值，`setFilterStatus` 是更新函式，`'all'` 是初始值。呼叫 `setFilterStatus('pending')` 後，React 重新渲染元件，畫面自動更新。

**常見錯誤：**
- 直接修改 state 變數（`filterStatus = 'new'`）不會觸發重新渲染，一定要用 `setFilterStatus('new')` 才有效

---

### `useCallback`

**是什麼：** 快取函式參考，只在依賴陣列的值改變時重新建立函式。

**專案範例：**
```jsx
const fetchEvents = useCallback(async () => {
  // ... fetch 邏輯
}, [applied, page])
```

**白話解釋：** 每次元件重新渲染，函式都會重新建立（記憶體位址不同）。`useCallback` 讓 `fetchEvents` 在 `applied` 和 `page` 沒變時保持同一個參考位址，避免 `useEffect` 以為「函式變了！要重跑！」造成無限迴圈。

**常見錯誤：**
- `useCallback` 的依賴陣列沒有列出函式內用到的 state 或 props，函式內會讀到過時的舊值（stale closure）

---

### `useEffect`

**是什麼：** 元件渲染後執行副作用，依賴陣列裡的值改變時重新執行。

**專案範例：**
```jsx
useEffect(() => {
  fetchEvents()
}, [fetchEvents])
```

**白話解釋：** 元件掛載後、或 `fetchEvents` 這個函式參考改變時，執行 `fetchEvents()`。這裡監聽 `fetchEvents` 而非直接監聽 `applied`/`page`，是因為 `fetchEvents` 已經用 `useCallback` 封裝了這些依賴，邏輯集中在一處。

**常見錯誤：**
- 依賴陣列寫 `[]` 以為只執行一次，但 `fetchEvents` 內部讀到的 `applied` 會永遠是初始值（stale closure）
- 依賴陣列完全省略，每次渲染都執行，可能造成無限迴圈

---

### `e.stopPropagation()`

**是什麼：** 阻止事件向上冒泡（傳遞到父元素的事件處理器）。

**專案範例：**
```jsx
<Chip
  onClick={(e) => {
    e.stopPropagation()
    setPopoverAnchor(e.currentTarget)
  }}
/>
```

**白話解釋：** `<Chip>` 在 `<TableRow>` 裡，點擊 Chip 事件會「冒泡」到 Row，觸發 Row 的 `onClick`（跳到詳情頁）。`stopPropagation()` 告訴瀏覽器「這個點擊到我這裡停，不要往上傳給 Row」。

**常見錯誤：**
- 子元素的點擊意外觸發父元素的事件，通常就是忘記 `stopPropagation`

---

### `<Chip>`

**是什麼：** MUI 的標籤元件，圓角小標籤，適合顯示狀態、分類或可點擊的摘要資訊。

**專案範例：**
```jsx
<Chip
  label={row.affected_summary}
  onClick={(e) => { ... }}
/>
```

**白話解釋：** 外觀是圓角的小膠囊，`label` 是顯示文字，加上 `onClick` 就變成可互動的標籤。

**常見錯誤：**
- `label` 只接受字串或簡單節點，放複雜的 JSX 結構可能造成排版問題

---

### `<Popover>`

**是什麼：** MUI 的浮動層元件，錨定在某個元素旁邊彈出顯示。

**專案範例：**
```jsx
<Popover
  open={Boolean(popoverAnchor)}
  anchorEl={popoverAnchor}
  onClose={() => setPopoverAnchor(null)}
>
  {formatDesc(popoverContent)}
</Popover>
```

**白話解釋：** `anchorEl` 是「錨點元素」，Popover 會出現在這個元素旁邊。`open={Boolean(popoverAnchor)}` 表示 `popoverAnchor` 有值時顯示、為 null 時關閉。`e.currentTarget`（點擊的元素）存到 state 後傳給 `anchorEl`。

**常見錯誤：**
- 關閉 Popover 要把 `popoverAnchor` 設回 `null`，忘記呼叫 `onClose` 或忘記清空 state，Popover 不會消失

---

## 3.5 開啟事件詳情

### `useParams()`

**是什麼：** React Router Hook，從當前 URL 取出動態路由參數。

**專案範例：**
```jsx
const { partnerId, issueId } = useParams()
```

**白話解釋：** 路由定義是 `/ai-partner/:partnerId/issues/:issueId`，當 URL 是 `/ai-partner/3/issues/42` 時，`useParams()` 回傳 `{ partnerId: '3', issueId: '42' }`，不需要自己解析 URL。

**常見錯誤：**
- 取出的值永遠是字串，要傳給 API 的數字欄位記得用 `Number(issueId)` 轉型

---

### `<Tabs>` / `<Tab>`

**是什麼：** MUI 的分頁切換元件，用 state 控制哪個 Tab 被選中。

**專案範例：**
```jsx
const [tabIndex, setTabIndex] = useState(0)

<Tabs value={tabIndex} onChange={(_, v) => setTabIndex(v)}>
  <Tab label="事件詳情" />
  <Tab label="歷史事件" />
  <Tab label="處置紀錄" />
</Tabs>
```

**白話解釋：** `value` 控制哪個 Tab 選中（對應 Tab 的 index，從 0 開始），`onChange` 的第二個參數 `v` 是點擊的 Tab index，呼叫 `setTabIndex(v)` 更新。

**常見錯誤：**
- `onChange={(e, v) => ...}` 裡第一個參數是 event（通常不用），第二個才是 index；常見錯誤是寫 `onChange={(v) => setTabIndex(v)}` 把 event 當成 index

---

### 條件渲染 `&&`

**是什麼：** 用 `&&` 短路運算在 JSX 中有條件地渲染元件。

**專案範例：**
```jsx
{tabIndex === 0 && <事件詳情內容 />}
{tabIndex === 1 && <歷史事件內容 />}
{tabIndex === 2 && <處置紀錄內容 />}
```

**白話解釋：** `A && B`：A 為 true 時才回傳 B；A 為 false 時回傳 false，React 不渲染 false。三行分別只在對應 tabIndex 時顯示內容。

**常見錯誤：**
- `{count && <元件 />}` 當 `count` 是 `0` 時，React 會渲染數字 `0` 而非不渲染（因為 `0` 不是 false）。要寫 `{count > 0 && <元件 />}`

---

### 兩步驟 async function

**是什麼：** 用 `await` 串接多個非同步 API 呼叫，確保依序執行。

**專案範例：**
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

**白話解釋：** `await` 保證第一個 API 完成後才執行下一個。先更新狀態、再新增紀錄、最後重新拉取最新資料，順序不能亂。

**常見錯誤：**
- 兩個 API 沒有先後依賴時，用 `await` 一個一個串接會讓它們變成序列執行（較慢）；若可以同時打，改用 `await Promise.all([api1(), api2()])` 更有效率

---

### `transition` 動畫

**是什麼：** CSS `transition` 讓元素的樣式值變化有平滑的過渡動畫。

**專案範例：**
```jsx
<Box sx={{ width: chatVisible ? 360 : 40, transition: 'width 0.2s' }}>
```

**白話解釋：** `chatVisible` 改變時，`width` 不是瞬間從 360 跳到 40，而是在 0.2 秒內平滑過渡。格式是 `'屬性名 時間'`，可以加緩動函式如 `'width 0.2s ease'`。

**常見錯誤：**
- `transition` 要和變化的屬性放在同一個元素；該屬性要有明確的數值起始/終止點（如 `width: 360` vs `width: 40`），`width: auto` 無法過渡

---

### `<Collapse>`

**是什麼：** MUI 的動畫元件，讓內容以展開/收合動畫顯示或隱藏。

**專案範例：**
```jsx
<Collapse in={chatVisible} orientation="horizontal">
  {/* AI 諮詢功能 */}
</Collapse>
```

**白話解釋：** `in` 是 true 時展開，false 時收合；`orientation="horizontal"` 是水平方向（預設是垂直，從上往下展開）。這裡聊天面板從右側水平收合。

**常見錯誤：**
- 預設 `orientation` 是垂直方向，水平收合要明確加上 `orientation="horizontal"`

---

## 4. 狀態管理設計

### `create((set, get) => {...})`

**是什麼：** Zustand 建立 store 的函式，接受一個 callback 回傳 state 和 action 的物件。

**專案範例：**
```jsx
const useAuthStore = create((set, get) => ({
  token: localStorage.getItem('mp-box-token') || null,
  login: async (email, password) => {
    // ...
    set({ token: access_token, user: { email } })
  },
  logout: async () => {
    localStorage.removeItem('mp-box-token')
    set({ token: null, user: null })
  },
}))
```

**白話解釋：** `set` 用來更新 state，`get` 用來在 action 裡讀取當前 state。所有 state（如 `token`）和操作函式（如 `login`、`logout`）都定義在同一個物件裡，不需要 Redux 那樣分散在多個檔案。

**常見錯誤：**
- 在 action 裡讀其他 state 要用 `get().token`，不能直接用外層的 `token` 變數（閉包問題，會讀到初始值）

---

### `useXxxStore()`

**是什麼：** Zustand store 回傳的 Hook，在元件中取用 state 和 action，不需要 Provider。

**專案範例：**
```jsx
function Header() {
  const { logout } = useAuth()  // useAuth 是 useAuthStore 的封裝
  return <Button onClick={logout}>登出</Button>
}
```

**白話解釋：** 不像 React Context 需要用 Provider 包住元件樹，Zustand 的 store 是全域的，任意元件直接 import 就能用。只有訂閱的值改變時，該元件才重新渲染。

**常見錯誤：**
- `const store = useAuthStore()` 取出整個 store 物件，任何欄位改變都會重新渲染；應該解構只取需要的欄位：`const { token } = useAuthStore()`

---

### `createContext()`

**是什麼：** 建立一個 React Context 物件，作為跨元件共享資料的管道。

**專案範例：**
```jsx
const IssuesContext = createContext(null)
```

**白話解釋：** `createContext(null)` 建立管道，`null` 是預設值（當元件不在任何 Provider 內時使用）。Context 本身不儲存資料，只是一個媒介。

**常見錯誤：**
- 在沒有對應 Provider 的元件樹裡使用 Context，會拿到 `createContext` 的預設值（null）而非期待的資料

---

### `<Context.Provider>`

**是什麼：** Context 的提供者，`value` 裡的資料可以被包住的所有子元件取用。

**專案範例：**
```jsx
export function IssuesProvider({ children }) {
  const [issues, setIssues] = useState([])
  return (
    <IssuesContext.Provider value={{ issues, updateIssue }}>
      {children}
    </IssuesContext.Provider>
  )
}
```

**白話解釋：** Provider 像廣播站，`value` 是廣播內容，包在裡面的所有子元件（任意深度）都能「收聽」。`{children}` 是被包住的子元件。

**常見錯誤：**
- `value={{ issues, updateIssue }}` 每次渲染都建立新物件（記憶體位址不同），會導致所有消費者重新渲染，資料量大時可考慮用 `useMemo` 包住 value

---

### `useContext()`

**是什麼：** 在被 Provider 包住的子元件中讀取 Context 的值。

**專案範例：**
```jsx
export function useIssues() {
  return useContext(IssuesContext)
}
```

**白話解釋：** 在任意深度的子元件裡呼叫 `useContext(IssuesContext)`，就能拿到最近的 `IssuesContext.Provider` 的 `value`，不需要一層一層用 props 傳遞。

**常見錯誤：**
- 元件不在對應的 Provider 範圍內，`useContext` 回傳的是 `createContext` 的預設值（null），容易造成 null reference 錯誤

---

### 自訂 hook 封裝

**是什麼：** 把 `useContext` 包成自訂 hook，讓使用更簡潔，且可集中加入防呆邏輯。

**專案範例：**
```jsx
// IssuesContext.jsx 裡定義
export function useIssues() {
  return useContext(IssuesContext)
}

// 其他元件使用
import { useIssues } from '../contexts/IssuesContext'
const { issues } = useIssues()
```

**白話解釋：** 不用每次都寫 `import IssuesContext; useContext(IssuesContext)` 這兩步，改成 `import { useIssues }; useIssues()` 一步到位。未來想在 hook 裡加防呆（如「如果不在 Provider 內就報錯」），只需要改一個地方。

**常見錯誤：**
- 直接把 `IssuesContext` export 出去讓各元件自己 `useContext`，無法集中管理，防呆邏輯散落各處

---
