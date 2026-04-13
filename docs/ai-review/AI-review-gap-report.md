# AI 缺口與孤立文件掃描報告

## 2026-04-06（v2）

## 孤立文件清單

| # | 文件路徑 | 備註 |
|---|---------|------|
| 1 | P1-design/issue-24/test.md | 非標準位置，P1-design 不應有 issue-{N}/ 資料夾（僅 P1-analysis 有此結構），建議刪除或搬移 |
| 2 | P1-code/tests/test_workflow_final.md | 未被任何文件索引，疑似過渡期工作流程測試紀錄，建議確認後刪除 |
| 3 | P1-code/tests/test_workflow_v2.md | 同上 |
| 4 | P1-code/backend/README.md | 被 P1-code/README.md 連結引用，但未納入 directory-structure.md 與 AI-review-doclist.md 索引 |
| 5 | P1-code/frontend/README.md | 同上 |

---

## 缺口清單

| # | 風險 | 缺口描述 | 建議處理方式 |
|---|------|---------|------------|
| 1 | 高 | AI-CONTEXT.md 技術資訊過時：記載 React 18 + shadcn/ui + React Router v6，但實際技術棧已遷移至 React 19 + MUI + React Router v7 | 更新 AI-CONTEXT.md 技術決策摘要區段，與 TechStack.md 對齊 |
| 2 | 中 | 缺少部署指南：技術棧提及 Docker + Railway（後端）+ Vercel（前端），但無對應的部署操作文件 | 於 P1-code/docs/ 新增部署指南，或在 SETUP.md 補充部署章節 |
| 3 | 低 | P1-code/backend/README.md 與 frontend/README.md 未納入中央索引 | 於 directory-structure.md 的 P1-code 區段補列，並考慮加入 AI-review-doclist.md |

---

## 2026-04-06

## 孤立文件清單

| # | 文件路徑 | 備註 |
|---|---------|------|
| 1 | P1-analysis/issue-24/test.md | 非標準檔案，issue 資料夾應只含 business-logic.md 與 SD-WBS.md |
| 2 | P1-design/issue-24/test.md | 同上，非標準檔案 |
| 3 | P1-code/backend/README.md | 未被任何文件索引 |
| 4 | P1-code/frontend/README.md | 未被任何文件索引 |
| 5 | P1-code/tests/test_workflow_final.md | 未被任何文件索引，疑似過渡期測試紀錄 |
| 6 | P1-code/tests/test_workflow_v2.md | 同上 |

---

## 缺口清單

| # | 風險 | 缺口描述 | 建議處理方式 |
|---|------|---------|------------|
| （本次掃描未發現重要主題缺口） | | | |
