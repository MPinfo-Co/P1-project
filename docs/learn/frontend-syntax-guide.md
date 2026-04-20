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
