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

---

## 3.3 進入主畫面

---

## 3.4 瀏覽事件清單

---

## 3.5 開啟事件詳情

---

## 4. 狀態管理設計

---
