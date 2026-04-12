# AI-review-prompt Timeout Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修改 `docs/AI-review-prompt.md`，消除 schedule agent 的 timeout 問題，確保每次執行都能成功寫入報告。

**Architecture:** 三處改動：(1) Phase 2 移除全樹 `find`，改為對 doclist 路徑逐一 `test -f`；(2) Phase 2 移除 sub-agent 指示，改為主 session 直接平行 Read；(3) Phase 3 改為每個 Repo 分析完立即寫入，Phase 4 只補寫摘要與清單。

**Tech Stack:** Markdown 文件修改，無程式碼變動。

---

### Task 1：重寫 Phase 2

**Files:**
- Modify: `docs/AI-review-prompt.md`（Phase 2 區塊，原第 22–35 行）

- [ ] **Step 1：確認目前 Phase 2 內容**

讀取 `docs/AI-review-prompt.md` 第 22–35 行，確認原文。

- [ ] **Step 2：將 Phase 2 整段替換為以下內容**

```markdown
## Phase 2 — 建立 Ground Truth

依序執行以下步驟（步驟 1–4 可平行，步驟 5 在步驟 1 完成後執行，步驟 6 在步驟 5 完成後執行）：

1. **讀取審查清單**：讀取 `AI-review-doclist.md`，取得目標文件清單
2. **讀取既有報告**：讀取 `docs/AI-review-report.md`（若存在），後續 prepend 新報告時保留歷史
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
```

- [ ] **Step 3：確認替換結果正確，原本的 find 指令與 sub-agent 指示均已移除**

- [ ] **Step 4：Commit**

```bash
git add docs/AI-review-prompt.md
git commit -m "docs: rewrite Phase 2 — remove find scan and sub-agent"
```

---

### Task 2：Phase 3 加入增量寫入

**Files:**
- Modify: `docs/AI-review-prompt.md`（Phase 3 區塊，原第 39–74 行）

- [ ] **Step 1：在 Phase 3 開頭加入「建立報告 header」指示**

在 `## Phase 3 — 逐文件分析` 標題下方、`對審查清單中的所有文件進行分析` 之前，插入：

```markdown
**開始前**：先將報告 header 寫入 `docs/AI-review-report.md`（prepend，保留既有內容往下推）：

```markdown
## YYYY-MM-DD HH:MM (vN)
<!-- 分析進行中 -->
```

版本號 N 從既有報告末尾版本 +1 推算。若無既有報告則從 v1 開始。
```

- [ ] **Step 2：在 Phase 3 結尾加入「逐 Repo 寫入」指示**

在 `### 審查原則` 區塊之後（Phase 4 之前），加入：

```markdown
### 增量寫入規則

每分析完一個 Repo 的所有文件，**立即**將該 Repo 的分析結果 append 到 `docs/AI-review-report.md`（依 Repo 順序：P1-project → P1-analysis → P1-design → P1-code）。

不等其他 Repo 分析完成，立即寫入，確保 timeout 發生時已有部分輸出。
```

- [ ] **Step 3：Commit**

```bash
git add docs/AI-review-prompt.md
git commit -m "docs: add incremental write per-repo in Phase 3"
```

---

### Task 3：縮減 Phase 4

**Files:**
- Modify: `docs/AI-review-prompt.md`（Phase 4 區塊，原第 76–80 行）

- [ ] **Step 1：將 Phase 4 替換為以下內容**

原本：
```markdown
## Phase 4 — 收尾

1. 將報告寫入 `docs/AI-review-report.md`（prepend，保留歷史）
2. Commit & Push P1-project
3. 輸出報告連結：[AI-review-report.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/AI-review-report.md)
```

改為：
```markdown
## Phase 4 — 收尾

（各 Repo 分析內容已在 Phase 3 逐步寫入，Phase 4 只補寫以下兩個 section）

1. **補寫「建議修改清單」**：依報告格式，將本次所有發現的建議修改項目以累積制方式寫入
2. **補寫「摘要」**：填入「本次審查 N 份文件，發現 X 份有問題，共 Y 項建議修改」
3. **補寫「未發現問題的文件」**清單
4. Commit & Push P1-project（直接 push main）
5. 輸出報告連結：[AI-review-report.md](https://github.com/MPinfo-Co/P1-project/blob/main/docs/AI-review-report.md)
```

- [ ] **Step 2：確認 Phase 4 不再包含「將報告寫入」的整批寫入指令**

- [ ] **Step 3：Commit**

```bash
git add docs/AI-review-prompt.md
git commit -m "docs: reduce Phase 4 to summary-only write + push"
```

---

### Task 4：驗證最終結果

**Files:**
- Read: `docs/AI-review-prompt.md`（完整讀取）

- [ ] **Step 1：完整讀取修改後的 `AI-review-prompt.md`**

確認以下四點：
- Phase 2 中無 `find` 指令
- Phase 2 中無「sub-agent」或「平行 sub-agent」字樣
- Phase 3 中有「增量寫入規則」與「開始前建立 header」
- Phase 4 只剩「補寫清單、摘要、未發現問題的文件 + push」

- [ ] **Step 2：push 到 remote**

```bash
cd /Users/rex/Desktop/P1/P1-project && git push origin main
```
