# AI-review-prompt.md Timeout 修復設計

**日期：** 2026-04-12
**問題：** Schedule agent 每次在 Phase 4 寫報告前 timeout，導致無任何輸出
**方案：** 方案 B — 修三點 + 重構 Phase 2 指令順序

---

## 根本原因

1. **Phase 2 Step 3**：`find` 掃描 4 個 Repo 完整目錄樹，產生大量輸出，耗時且佔用 context
2. **Phase 2 Step 5**：「盡量平行」措辭導致 agent 自行啟動 4 個 sub-agent，每個 sub-agent 有啟動開銷
3. **Phase 4 是唯一寫入點**：timeout 前沒有任何輸出被儲存

---

## 設計決定

### Phase 2 — 三項改動

| 步驟 | 原本 | 改後 |
|------|------|------|
| Step 3 | `find` 掃全樹 | 對 doclist 22 個路徑逐一 `test -f` 確認存在 |
| Step 5 | 分 4 組啟動 sub-agent | 主 session 內直接平行 Read 22 個檔案 |
| 開頭措辭 | 「盡量平行完成以下工作」 | 明確列出每步執行方式，移除籠統指示 |

**Phase 2 新執行順序：**
1. 讀 `AI-review-doclist.md` 取得清單
2. 讀 `AI-review-report.md`（若存在）保留歷史
3. 執行 `date` 取得時間戳
4. 讀 `package.json` + `requirements.txt`
5. 對 22 個路徑逐一 `test -f` 確認存在，記錄缺口
6. 直接平行 Read 所有存在的文件（不啟動 sub-agent）

### Phase 3 — 增量寫入

每分析完一個 Repo，立即寫入該 Repo 的分析結果：

```
Phase 3 開始 → 建立報告 header（prepend）
→ 分析 P1-project 完成 → 立即寫入
→ 分析 P1-analysis 完成 → 立即寫入
→ 分析 P1-design 完成 → 立即寫入
→ 分析 P1-code 完成 → 立即寫入
```

### Phase 4 — 縮小範圍

Phase 4 只負責補寫「摘要」與「建議修改清單」兩個 section，然後 commit & push。

**最壞情況（Phase 4 前 timeout）：** 各 Repo 分析內容已存在報告中，僅缺摘要與清單。

---

## 不在此次範圍內

- Timeout 防護（讓 agent 判斷執行時間）— 可靠性低，不值得增加複雜度
- 修改報告格式
- 修改審查原則或 doclist
