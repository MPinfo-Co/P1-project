# Prototype 撰寫規則

> 本文件規範 `SA/saPrototype/` 與 `SD/sdPrototype/` 的產製方式。
> 文件會被 SA writer、SD writer 及人類成員讀取，以繁體中文撰寫。

---

## 一、共同規則

### 1.1 目錄結構

SA/saPrototype/ 與 SD/sdPrototype/ 結構相同：

```
_shared/          — 共用資源（_style.css / _nav.js / _state.js / _template.html）
fn_xxx/           — 各功能獨立目錄，含 fn_xxx.html + _data.js
```

### 1.2 新建頁面：從 _template.html 出發

新增功能頁面時，複製 `_shared/_template.html` 作為起點。
不直接修改 `_shared/` 下的任何檔案（除非是設計系統本身需要異動）。

### 1.3 CSS 使用原則

1. 優先使用 `_style.css` 既有 class（class 速查在 `_template.html` 尾端）
2. 禁止 inline style，唯一例外是 `_template.html` 中標注「必須保留」的 `style="display:grid;"`
3. 需要新樣式時，依下方 SA / SD 特則各自處理

### 1.4 Script 引入順序（固定）

```html
<script src="./_data.js"></script>
<script src="../_shared/_state.js"></script>
<script src="../_shared/_nav.js"></script>
<script>
  /* inline 邏輯 */
</script>
```

### 1.5 互動程度

基本 CRUD 操作（新增 / 編輯 / 刪除）與篩選查詢需可實際運作。
Modal 開關、表單必填驗證需正常作動。
不需模擬後端 API，資料操作在前端 `allXxx` 陣列上進行即可。

### 1.6 特殊頁面與 Navbar

**系統入口頁（login、404 等）**
以 `fn_login/`、`fn_error/` 命名，與一般功能頁面相同規格處理（含 `_data.js`）。

**Navbar（sidebar + header）**
由 `_shared/_nav.js` 統一注入，不在各功能頁面中重複定義。
預設不修改 `_nav.js`；當 Epic 需求明確異動導覽結構時，可修改 `_nav.js`，
並在 saLogic / TDD 中標注異動原因。
Navbar 畫面規格見 `sdSpec/fn_navbar/`；Navbar prototype 頁面位於 `sdPrototype/fn_navbar/`。

---

## 二、saPrototype 特則

### 2.1 觸發時機

由 `wf_epic_to_sa` 觸發，當 Epic 需求涉及畫面時，SA writer 依需求描述產製或調整對應的 saPrototype 頁面。

### 2.2 設計依據

以 Epic 需求描述為唯一依據，不需對應既有 sdSpec。
設計目的是讓人類成員能直觀討論操作流程與畫面佈局。

### 2.3 設計自由度

- 優先使用 `_shared/_style.css` 既有元素
- 若既有 class 無法表達需求，可在該功能的 `fn_xxx.html` 內用 `<style>` 區塊自訂樣式
- 不修改 `_shared/_style.css`（探索性樣式不納入共用設計系統）

### 2.4 產出範圍

只修改本次 Epic 涉及的功能頁面，不動其他功能的現有頁面。

### 2.5 生命週期

草稿性質。SA 階段 merge 後，由 sdPrototype 接手成為正式參考。
saPrototype 不隨 SD / PG 階段回頭更新。

---

## 三、sdPrototype 特則

### 3.1 觸發時機

由 `wf_sa_to_sd` 中的 SD writer 觸發，依本次 Epic 的 saPrototype 改動與對應的 sdSpec 畫面規格，調整 sdPrototype。

### 3.2 設計依據

以 sdSpec 畫面規格為主，saPrototype 為視覺參考。
兩者有差異時，以 sdSpec 為準。

### 3.3 設計精確度

- 所有欄位、操作入口、狀態顯示必須與 sdSpec 一致
- 只使用 `_shared/_style.css` 既有 class，禁止自訂樣式
- 若畫面需求超出現有 class，應先評估是否更新 `_shared/_style.css`，再動 HTML

### 3.4 產出範圍

只修改本次 Epic 涉及的功能頁面，不動其他功能的現有頁面。

### 3.5 生命週期

活文件，永遠反映最新已確認的設計狀態。直接修改，不保留舊版。
PG 以此為 UI 實作的視覺依據。
