# 前端程式規範（React / TypeScript）

> 適用範圍：`P1-code/frontend/src/`
> 格式由 **ESLint + Prettier** 自動管理，本文件只涵蓋工具管不到的架構、命名、禁用模式。

---

## 一、命名速查表

### 1-1 檔案命名

檔名跟主要 export 的命名一致：React 元件用 PascalCase，其他檔案用 camelCase。

| 類型 | 位置 | 格式 | 範例 |
|------|------|------|------|
| Function 資料夾 | `src/pages/` | `fn_{id}/` | `fn_user/`, `fn_role/` |
| Page 元件 | `src/pages/fn_{id}/` | PascalCase.tsx | `FnUserList.tsx` |
| 共用元件 | `src/components/{Category}/` | PascalCase.tsx | `Pagination.tsx` |
| React Query hook | `src/queries/` | `use{Domain}Query.ts` | `useUsersQuery.ts` |
| Zustand Store | `src/stores/` | `{domain}Store.ts` | `authStore.ts` |
| 新檔案副檔名 | — | `.tsx` | 舊 `.jsx` 漸進遷移，不強制 |

> `fn_{id}` 對應 `functionList.md` 的功能 ID（`fn_user`、`fn_role`…）。
> 功能放在哪個頁面是 UX 決定，不影響資料夾位置。

### 1-2 元件命名

| 情境 | 格式 | 範例 |
|------|------|------|
| Page 元件 | `Fn{Domain}{描述}` | `FnUserList`, `FnUserForm` |
| 共用元件 | 描述用途 | `Pagination`, `Modal` |
| export 方式 | `export default function` | `export default function FnUserList()` |
| Props interface | `Props` | `interface Props { ... }` |

### 1-3 Query 命名（React Query）

| 類型 | 格式 | 範例 |
|------|------|------|
| Hook 檔名 | `use{Domain}Query.ts` | `useUsersQuery.ts` |
| Query key | `['{domain}', params]` | `['users', { roleId: 1 }]` |
| 資料 interface | 描述資料形狀，定義在 query 檔內 | `UserRow`, `RoleOption` |

### 1-4 Store 命名（Zustand，只管 auth / UI 狀態）

| 類型 | 格式 | 範例 |
|------|------|------|
| Store 檔名 | `{domain}Store.ts` | `authStore.ts` |
| Hook 名稱 | `use{Domain}Store` | `useAuthStore` |
| State interface | `{Domain}State` | `AuthState` |

### 1-5 變數 / 函式命名

| 情境 | 格式 | 範例 |
|------|------|------|
| Boolean state | `is{狀態}` | `isLoading`, `isFormOpen`, `isRolesLoaded` |
| 一般 state | camelCase | `filterRole`, `error` |
| Event handler | `handle{動作}` | `handleDelete`, `handleApply` |
| Query mutation | `{動詞}{Domain}` | `createUser`, `deleteUser` |

---

## 二、架構規則

### 2-1 分層結構

```
src/
├── pages/fn_{id}/          ← 元件：render UI、呼叫 query hook 或 store
├── components/{Category}/  ← 共用元件：純 UI，只接 props
├── queries/                ← React Query：API fetch、cache、loading/error
│   └── use{Domain}Query.ts
├── stores/                 ← Zustand：auth token、全域 UI 狀態
│   └── authStore.ts
└── App.tsx                 ← 路由設定
```

### 2-2 各層職責

| 層 | 做什麼 | 不做什麼 |
|----|--------|---------|
| **Page 元件** | render UI、呼叫 query hook 或 store | 直接 `fetch()`、自己管 loading/error |
| **共用元件** | 接 props 渲染 UI | 碰 query、碰 store、碰 API |
| **queries/** | fetch API、管 server data 與 cache | 操作 DOM、管 UI 狀態 |
| **stores/** | 管 auth token、登入身份、全域 UI | 存 API 回傳的 server data |

### 2-3 資料流向

```
使用者操作
  ↓
Page 元件（handle{動作}）
  ↓
queries/use{Domain}Query.ts（mutation 打 API）
  ↓
後端 API
  ↓
React Query 自動更新 cache → 元件自動重新 render
```

### 2-5 UI 元件規範

| 畫面類型 | 元件 |
|---------|------|
| 查詢清單 | MUI DataGrid |
| 新增 / 修改表單 | MUI Dialog（含 DialogTitle / DialogContent / DialogActions）|

### 2-6 QueryClient 設定

`QueryClient` 在 `src/main.jsx` 建立，以 `QueryClientProvider` 包住整個 App，全域共用同一個 client instance。各 query hook 不自行建立 `QueryClient`。

### 2-4 Token 取得方式

query hook 內部統一從 `authStore` 取，不讀 localStorage：

```typescript
// src/queries/useUsersQuery.ts
import useAuthStore from '@/stores/authStore'
const token = useAuthStore.getState().token
```

---

## 三、禁用模式

### ✗ 1 元件直接呼叫 fetch

```typescript
// ✗
export default function FnUserList() {
  useEffect(() => {
    fetch('/api/users').then(...)
  }, [])
}

// ✓
export default function FnUserList() {
  const { data: users, isLoading, error } = useUsersQuery()
}
```

### ✗ 2 手動管 API 的 loading / error

```typescript
// ✗
const [isLoading, setIsLoading] = useState(false)
const [error, setError] = useState<string | null>(null)

// ✓ React Query 內建，不需要自己寫
const { isLoading, error } = useUsersQuery()
```

### ✗ 3 把 API 資料放進 Zustand

```typescript
// ✗ server data 不放 Zustand
const useUserStore = create(() => ({
  users: [],
  fetchUsers: async () => { ... }
}))

// ✓ Zustand 只管 auth / UI 狀態
const useAuthStore = create(() => ({
  token: null,
  user: null,
}))
```

### ✗ 4 元件直接讀 localStorage 取 token

```typescript
// ✗
const token = localStorage.getItem('mp-box-token')

// ✓
import useAuthStore from '@/stores/authStore'
const token = useAuthStore.getState().token
```

### ✗ 5 共用元件碰 query 或 store

```typescript
// ✗
export default function UserBadge() {
  const { data } = useUsersQuery()
}

// ✓ 純 props
export default function UserBadge({ name, email }: Props) { ... }
```

### ✗ 6 新檔案用 .jsx

```
// ✗  FnRoleList.jsx
// ✓  FnRoleList.tsx
```

### ✗ 7 Boolean state 不加 is 前綴

```typescript
// ✗
const [loading, setLoading] = useState(false)
const [formOpen, setFormOpen] = useState(false)

// ✓
const [isLoading, setIsLoading] = useState(false)
const [isFormOpen, setIsFormOpen] = useState(false)
```
