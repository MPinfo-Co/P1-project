# Spec：frontend-syntax-guide.md 設計文件

## 目標

為「會基本 JS、但未接觸 React 生態系」的初學者，撰寫一份語法說明文件，讓讀者能看懂 `docs/learn/frontend-guide.md` 中出現的所有程式碼片段。

不求包山包海，以「看懂 frontend-guide.md」為終點。

---

## 文件位置

`docs/learn/frontend-syntax-guide.md`

---

## 文件結構

### 開頭：語法索引表

表格欄位：語法名稱 | 出現章節 | anchor 連結

讓讀者遇到不懂的語法時，查表跳到對應說明。

---

### 本體：章節順序完全對應 frontend-guide.md

#### 3.1 程式啟動
說明對象（引用 frontend-guide 程式碼片段）：
- `createRoot().render()` — React 掛載進 HTML
- `<StrictMode>` — 開發環境除錯模式
- `<ThemeProvider theme={...}>` — MUI 全域主題注入
- `<CssBaseline />` — 重置瀏覽器預設樣式
- `createTheme({ palette, typography, components })` — 建立主題物件
- `styleOverrides` — 覆寫 MUI 元件預設樣式

#### 3.2 登入流程
說明對象：
- `async / await` — 非同步函式語法
- `fetch(url, { method, headers, body })` — 打 API
- `JSON.stringify()` — 物件轉字串
- `res.status` / `res.json()` — 讀取回應狀態與資料
- `localStorage.setItem()` — 瀏覽器本地儲存
- Zustand `set({ ... })` — 更新 store 狀態
- `ProtectedRoute` 模式 — 未登入時強制跳轉
- 三元運算子 `condition ? A : B` — 條件回傳
- `<Navigate to="..." replace />` — 程式化跳頁

#### 3.3 進入主畫面
說明對象：
- `<Routes>` / `<Route path element>` — 宣告路由對應
- 巢狀路由結構 — 父子路由的關係
- `<Box sx={{ display: 'flex', flex: 1, height: '100vh' }}>` — flex 版面語法
- `<Outlet />` — 子路由插入點
- `<NavLink>` + render props `{({ isActive }) => ...}` — 動態 active 樣式
- `Object.entries().filter().sort()` — 鏈式陣列操作
- 可選鏈 `?.` 與空值合併 `??`

#### 3.4 瀏覽事件清單
說明對象：
- `useState(initialValue)` — 元件內部狀態
- `useCallback(fn, [deps])` — 快取函式參考、防無限迴圈
- `useEffect(fn, [deps])` — 副作用（fetch data）
- 依賴陣列的運作邏輯
- `e.stopPropagation()` — 阻止事件冒泡
- `<Chip>` — MUI 標籤元件
- `<Popover anchorEl={...}>` — MUI 浮動層

#### 3.5 開啟事件詳情
說明對象：
- `useParams()` — 從 URL 取出動態參數
- `<Tabs value={tabIndex}>` / `<Tab>` + state 控制顯示
- `{tabIndex === 0 && <內容 />}` — 條件渲染
- 兩步驟 async function（`await` 串接多個 API）
- `sx={{ transition: 'width 0.2s' }}` — CSS transition 動畫
- `<Collapse orientation="horizontal">` — 水平收合動畫

#### 4. 狀態管理設計
說明對象：
- `create((set, get) => ({ state, action }))` — 建立 Zustand store
- `useXxxStore()` — 元件取用 store（不需 Provider）
- `createContext(null)` — 建立 React Context
- `<Context.Provider value={...}>` — 提供資料給子樹
- `useContext(Context)` — 子元件讀取 Context
- 自訂 hook 封裝（`export function useIssues()`）

---

## 每個語法條目的固定格式

```
### `語法名稱`
**是什麼：** 一句話定義
**專案範例：** 引用 frontend-guide.md 的程式碼片段
**白話解釋：** 口語說明（可用比喻）
**常見錯誤：** 初學者最容易踩的坑（1-2 條）
```

---

## 讀者假設

- 懂 JavaScript 基礎：變數、函式、`const`、`async/await`、箭頭函式
- 未接觸過：JSX、React Hooks、React Router、MUI、Zustand
- 閱讀目的：看懂 frontend-guide.md，不是成為 React 專家

---

## 不在範圍內

- 完整 React 教學
- TypeScript 語法說明
- 後端 / Python / FastAPI 相關
- frontend-guide.md 未出現的語法
