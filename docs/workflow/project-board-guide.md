# GitHub Projects 看板使用指南

> [← 回到總導覽](../../README.md)

[MP-BOX Project Board](https://github.com/orgs/MPinfo-Co/projects/4)

---

## 欄位說明

| 欄位 | 用途 |
|------|------|
| **Status** | 工作階段 |
| **Scope** | 分類標記（MP-Box / 資安專家 / Learn / Other）|
| **週期** | 所屬工作週（5 天一個週期，PM 分配）|
| **Start / Target date** | 工作者填入實際開始與完成日 |
| **Estimate** | 預估工時（單位：天，導入中）|
| **References** | Learn 項目的學習筆記連結（純網址或 `[標題](網址)`）|
| **Parent issue** | 上層 Epic |
| **Sub-issues progress** | 子 issue 完成比例（自動計算）|

---

## Status 流程

```
idea → Next → Todo → In progress → Done
```

| 狀態 | 說明 |
|------|------|
| idea | 剛進來的想法，未評估 |
| Next | 評估可行，下版本候補 |
| Todo | 本版本（本季）確認要做 |
| In progress | 進行中（上限 2 個）|
| Done | 完成 |
| **Done(留存)** | Learn 專用，永久保留在 Learn View |

> 版本週期：一季一個版本（Q1/Q2/Q3/Q4）。

---

## Views 說明

| View | 使用者 | 用途 |
|------|--------|------|
| 工作管理(Member) | 全員 | 查詢管理自己的工作（預設 `assignee:@me`）|
| 工作規劃(Member) | 全員 | 填入個人實際 Start / Target date |
| 近期工作(PM) | PM | 調整項目欄位內容 |
| 專案週報(PM) | PM | 向上報告 |
| 工作管理(PM) | PM | 無篩選全覽，分派週期給所有工作 |
| Learn | 全員 | 學習資源庫（`status:Done(留存)`）|

---

## 自動化流程

PM 建立 Epic 後，系統自動串接各階段，**不需手動建 Issue 或分支**：

```
Epic（P1-project）加上 epic label
 └─ 自動建立 SA Issue + A-Branch + Draft PR（P1-analysis）
     └─ SA merge → 自動建立 SD Issue + D-Branch + Draft PR（P1-design）
         └─ SD merge → 自動建立 PG Issue + C-Branch + Draft PR（P1-code）
```

每個階段 merge 後，上游 Issue 自動關閉，Epic 關聯欄位自動更新。

---

## 各角色工作流程

三個角色的流程結構相同，差異如下：

| | SA | SD | PG |
|--|----|----|-----|
| **Repo** | P1-analysis | P1-design | P1-code |
| **分支前綴** | `issue-{N}-` | `issue-{N}-` | `issue-{N}-` |
| **主要產出** | business-logic.md、SD-WBS.md | TestPlan、API Spec、Prototype | 程式碼 + pytest |
| **觸發下游** | Merge → 建 SD Issue | Merge → 建 PG Issue | Merge → 關閉 Epic |

**通用工作步驟：**
1. 在**工作管理(Member)** 頁籤中，確認 Todo 項目之工作細節，例如：Issue 留言內有分支與 Draft PR 連結
2. 改 Status 為 **In progress**，Pull 對應的分支到Local，開始作業
3. 完成工作後將 Draft PR 改為 **Ready for review** → 等待Approve及Merge
4. 在**工作規劃(Member)** 填入(或點擊) Start / Target date

> WIP 原則：**同時 In progress 不超過 2 個**。

---

## Chore 工作

1. 在**對應的 Repo** 建立 Issue，github workflow會，自動建立分支（`chore-{N}-{slug}`）。
2. 改 Status 為 **In progress**，Pull 對應的分支到Local，開始作業
3. 工作完成後，等待Approve及Merge。

---

## Learn 資源庫

- Learn 工作完成後 Status 改為 **Done(留存)**（不用 Done）
- 自動出現在 Learn View，不受週期篩選影響
- References 欄位填入筆記連結供全員查閱
