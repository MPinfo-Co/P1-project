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

---

## 3.4 瀏覽事件清單

---

## 3.5 開啟事件詳情

---

## 4. 狀態管理設計

---
