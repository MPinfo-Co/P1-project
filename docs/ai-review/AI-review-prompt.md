# P1 文件審查任務

> [← 回到總導覽](../../README.md)

## 任務目標
讀取 P1 四個 Repo 的重要文件，依審查原則逐一分析，輸出結構化建議報告。

## 限制
- 不修改受審文件的內容
- 僅更新報告檔（`docs/ai-review/AI-review-report.md`）
- **所有檔案讀取必須使用本機 git repo（Read 工具讀取本機路徑），不得使用 GitHub MCP 工具**

---

## Phase 1 — 環境準備
1. 四個 Repo **平行**執行 git pull（四個 Repo 為同層目錄）：
   - P1-project / P1-analysis / P1-design / P1-code
2. 執行 `date '+%Y-%m-%d %H:%M'` 取得執行時間，供報告 header 使用

---

## Phase 2 — 建立 Ground Truth

依序執行以下步驟（步驟 1–4 可平行，步驟 5 在步驟 1 完成後執行，步驟 6 在步驟 5 完成後執行）：

1. **讀取審查清單**：讀取 `AI-review-doclist.md`，取得目標文件清單
2. **讀取既有報告**：讀取 `docs/ai-review/AI-review-report.md`（若存在），後續 prepend 新報告時保留歷史
3. **取得執行時間**：執行 `date '+%Y-%m-%d %H:%M'`，供報告 header 使用
4. **讀取關鍵設定檔**：讀取以下檔案，確立技術棧的實際狀態：
   - `P1-code/frontend/package.json`（前端語言與框架）
   - `P1-code/backend/requirements.txt`（後端依賴）
5. **路徑存在確認**：對 doclist 中的每個本機路徑（非 GitHub URL），逐一執行：
   ```bash
   test -f <path> && echo "OK: <path>" || echo "MISSING: <path>"
   ```
   將所有 MISSING 路徑記錄為「doclist 完整性缺口」，寫入報告。
6. **平行讀取受審文件**：在主 session 內直接平行 Read 所有步驟 5 確認存在的文件（不啟動 sub-agent）。外部 Repo 文件依本機相對路徑讀取，忽略表格中的 GitHub URL。

---

## Phase 3 — 逐文件分析

**開始前**：先將報告 header 寫入 `docs/ai-review/AI-review-report.md`（prepend，保留既有內容往下推）：

```markdown
## YYYY-MM-DD HH:MM (vN)
```

版本號 N 從既有報告末尾版本 +1 推算。若無既有報告則從 v1 開始。

對審查清單中的所有文件進行分析，每份文件依以下順序處理：

### 3-A 結構性核對（先做）

針對文件中的**具體聲明**，逐項比對 Phase 2 的 ground truth。以下類型必須主動核對，不可依賴「閱讀感受」判斷：

| 聲明類型 | 核對方式 |
|---------|---------|
| 目錄結構描述（樹狀圖） | 比對 Phase 2 路徑確認結果，確認每個列出的路徑實際存在 |
| 技術棧 / 語言聲明 | 比對 package.json、requirements.txt |
| 跨文件引用（「見 X 文件」） | 確認 X 存在於掃描結果中 |
| 格式範例中的副檔名（.tsx / .jsx） | 比對 package.json 或實際檔案副檔名 |
| 特定檔案或目錄是否存在 | 比對 Phase 2 路徑確認結果 |
| 文件內的 Markdown 連結 | 若連結目標與受審文件屬同一 Repo，且使用 GitHub 絕對 URL（`https://github.com/...`），標記為**優化建議**。例外排除：跨 Repo 連結、`git clone` 指令、看板網址、輸出報告連結（如 AI-review-report.md）、連結目標位於 `.github/` 目錄（本機 HTTP 工具不服務隱藏目錄，絕對 URL 為必要）|

發現不符 → 標記為**事實差異**，寫入該文件的分析內容中，並在問題描述前加上 `**[待處理]**` 標記。

### 3-B 邏輯性審查（後做）

結構性核對通過後，再審查以下兩個維度：

- **簡化**（依據「簡潔完整」「互斥」原則）：可刪減或合併的內容
- **優化**（依據「清晰」「易讀」「優先序」「知識遞進」原則）：內容必要但表達可改進之處

僅記錄有發現的維度。同樣在問題描述前加上 `**[待處理]**` 標記。

> **`[待處理]` 使用慣例**：所有尚未解決的問題均以此標記開頭，方便用 Ctrl+F 搜尋跨版本追蹤。問題解決後，下一版報告的對應段落改寫為已解決，不再加標記。

### 審查原則（判斷標準）
- **清晰**：每句話只有一種解讀
- **簡潔完整**：完整表達所需資訊，不重複不冗餘
- **互斥**：各文件職責不重疊，同一資訊只在一處維護；低層文件不重複高層內容
- **易讀**：結構對目標讀者（角色）友善
- **優先序**：章節順序反映重要性，關鍵內容在前
- **知識遞進**：讀者讀到每段時，已透過上文具備足夠背景

### 文件分析寫法

- **有問題的文件**：以 `**檔名**：` 開頭，每個問題獨立一個 `-` 列項，問題描述前加 `**[待處理]**`
- **無問題的文件**：不逐一列出，僅在「未發現問題的文件」清單中統一列名

範例：
```
**FunctionList.md**：
- **[待處理]** 完成狀態欄位全部空白（優化）
- **[待處理]** 第 3 行技術棧聲明與 package.json 不符（事實差異）
```

### 增量寫入規則

每分析完一個 Repo 的所有文件，**立即**將該 Repo 的分析結果 append 到 `docs/ai-review/AI-review-report.md`（依 Repo 順序：P1-project → P1-analysis → P1-design → P1-code）。

不等其他 Repo 分析完成，立即寫入，確保 timeout 發生時已有部分輸出。

---

## Phase 4 — 收尾

（各 Repo 分析內容已在 Phase 3 逐步寫入，Phase 4 只補寫以下 section）

1. **補寫「摘要」**：填入「本次審查 N 份文件，發現 X 份有問題」
2. **補寫「未發現問題的文件」**清單
3. Commit & Push P1-project（直接 push main）
4. 輸出報告連結：[AI-review-report.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/ai-review/AI-review-report.md)

---

## 報告格式
> - 每次執行為獨立區塊，以 `## YYYY-MM-DD HH:MM (vN)` 標題分隔；版本號從既有報告末尾版本 +1 推算
> - 最新一次插入檔案最上方（既有內容往下推）
> - 僅保留最近 3 次，超過的區塊刪除（完整歷史由 git 追溯）

### 摘要
> 本次審查 {N} 份文件，發現 {X} 份有問題。

（摘要寫在背景脈絡之後、問題列表之前）

### 未發現問題的文件
> 以下 {N} 份文件未發現問題：file1.md、file2.md、...

（未發現問題的文件清單寫在問題列表之後）

---

## 下一步（詢問人類成員是否要接續執行）
完成後可接續執行 [AI-review-gap-prompt.md](AI-review-gap-prompt.md)，掃描缺口與孤立文件。
