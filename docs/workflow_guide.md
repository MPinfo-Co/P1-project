# 一.工作流程

## 開立工作時所填寫的表單 - GitHub Issue Template 設定

| 工作類型   | 動作            | Repo       | yml檔案                                                                                                                                                                                                                                                                                                             | 開立後觸發...                           |
| ------ | ------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 系統功能修改 | 開立 Epic 表單    | P1-project | [epic.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/ISSUE_TEMPLATE/epic.yml)                                                                                                                                                                                                                     | p-workflow.yml<br>**見「Epic自動化流程」** |
| 行政事務   | 行政 Chore 表單   | ALL        | [a-chore](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-chore-workflow.yml)  <br>[d-chore](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-chore-workflow.yml) <br>[c-chore](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/c-chore-workflow.yml) | chore-workflow.yml<br>**開立Branch** |
| 其他工作   | 開立Draft Issue | ALL        |                                                                                                                                                                                                                                                                                                                   |                                    |

> 統一透過專案看板[MP-BOX](https://github.com/orgs/MPinfo-Co/projects/4)開立工作
> 設定禁止開立空白 Issue(設定檔：[config.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/ISSUE_TEMPLATE/config.yml))

##  1.1 Epic自動化流程

WF-P = [p-workflow.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/p-workflow.yml) in P1-project
WF-A = [a-workflow.yml](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-workflow.yml) in P1-analysis
WF-D = [d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml) in P1-design
WF-C = [c-workflow.yml](https://github.com/MPinfo-Co/P1-code/blob/main/.github/workflows/c-workflow.yml) in P1-code

```
PM 開立 Epic（透過填寫範本）
└─ [WF-P 自動建立] SA Issue + SA-Branch + Draft PR
└─ [WF-P 自動產生] P1-analysis:issue-{SA#}/business-logic.md
  └─ SA merge PR
    └─ [WF-A 自動建立] SD Issue + SD-Branch + Draft PR
    └─ [WF-A 自動產生] P1-design:TDD/issue-{SD#}.md
      └─ SD merge PR
        └─ [WF-D 自動產生] P1-design:SpecDiff/issue-{SD#}.md
        └─ [WF-D 自動建立] PG Issue + PG-Branch + Draft PR
        └─ [WF-D 自動產生] P1-code:TestReport/issue-{SD#}.md
          └─ PG merge PR
            └─ [WF-C 自動關閉] Epic、PG Issue
```

> 產生各階段issue時，會自動在issue body產生與該issue相關的所有項目連結
> 如需了解 workflow 細節，直接向AI詢問指定文件內涵即可。

##  1.2 Issue body 
###  Epic Issue body (由[epic.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/ISSUE_TEMPLATE/epic.yml)規範)

```Markdown
## 功能說明
<!-- 這個功能要解決什麼問題？ -->

## 驗收條件
<!-- 完成的定義是什麼？ -->
```

###  SA Issue body(由[p-workflow.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/p-workflow.yml)產生)

```Markdown
## 關聯項目

### SA 工作文件
- business-logic.md：[issue-4/business-logic.md]

### 關聯 Issue
- Epic：MPinfo-Co/P1-project#1
- SA Issue：#4
- SD Issue：P1-design #（merge 後自動填入）

### 相關連結
- 分支：[issue-4-xxx]
- Draft PR：[#3]
```

###  SD Issue body(由[a-workflow.yml](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-workflow.yml) 產生)

```markdown
## 關聯項目

### SD 工作文件
- business-logic.md：[issue-4/business-logic.md]
- TDD：[TDD/issue-5.md]

### 關聯 Issue
- Epic：MPinfo-Co/P1-project#1
- SA Issue：MPinfo-Co/P1-analysis#4
- SD Issue：#5
- PG Issue：P1-code #（merge 後自動填入）

### 相關連結
- 分支：[issue-5-xxx]
- Draft PR：[#6]
```
###  PG Issue body(由[d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml)產生)

```Markdown
## 關聯項目

### PG 工作文件
- business-logic.md：[issue-4/business-logic.md]
- SpecDiff：[SpecDiff/issue-5.md]
- TDD：[TDD/issue-5.md]
- TestReport：[TestReport/issue-5.md]

### 關聯 Issue
- Epic：MPinfo-Co/P1-project#1
- SA Issue：MPinfo-Co/P1-analysis#4
- SD Issue：MPinfo-Co/P1-design#5
- PG Issue：#7

### 相關連結
- 分支：[issue-7-xxx]
- Draft PR：[#8]
```

## 1.3 自動產生的md文件格式

### business-logic.md 格式（由[p-workflow.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/p-workflow.yml)產生）

```markdown
# 業務邏輯分析：{功能標題}

## 需求說明
（PM 填寫的原始需求描述，SA 可補充說明）

## 商業邏輯（選填）
（SA 分析的核心業務規則與流程說明）

## 資料模型示意（選填）
（相關資料欄位與關聯說明）

## SD 注意事項（選填）
（設計階段需特別留意的限制或規則）

## 畫面示意（選填）
（主要畫面或操作流程的文字描述）
```

### TDD/issue-{N}.md 格式（由[a-workflow.yml](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-workflow.yml)產生）：

```markdown
# TDD：[SD] {功能標題}

## 工作項目
| # | 類型 | 說明 |
|---|------|------|
| 1 | API  | POST /api/leaves（建立請假申請） |
| 2 | 畫面 | 請假申請表單 |

## 測試案例
| ID | 類型 | 前置條件 | 操作 | 預期結果 |
|----|------|---------|------|---------|
| T1 | 整合 | 登入 Tenant A | POST /api/leaves | 201，回傳 leave_id |
| T2 | 整合 | 未登入 | POST /api/leaves | 401 Unauthorized |
| T3 | 畫面 | 登入狀態 | 填寫表單，結束日早於開始日 | 顯示日期錯誤提示，禁止送出 |
```


### TestReport/issue-{N}.md 格式（由[d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml)產生）：

```markdown
# TestReport：[SD] {功能標題}

## 工作項目
| # | 類型 | 說明 | PG執行註記 |
|---|------|------|---|
| 1 | API  | POST /api/leaves（建立請假申請） |  |
| 2 | 畫面 | 請假申請表單 |  |

## 測試案例
| ID | 類型 | 前置條件 | 操作 | 預期結果 | PG執行註記 |
|----|------|---------|------|---------|---|
| T1 | 整合 | 登入 Tenant A | POST /api/leaves | 201，回傳 leave_id |  |
| T2 | 整合 | 未登入 | POST /api/leaves | 401 Unauthorized |  |
| T3 | 畫面 | 登入狀態 | 填寫表單，結束日早於開始日 | 顯示日期錯誤提示，禁止送出 |  |
```

> PG執行註記：工作項目填「已執行」或簡短註記；測試案例填「通過」、「失敗」或簡短註記。

### SpecDiff/issue-{N}.md 格式（由[d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml)產生）：

```markdown
# SpecDiff：Issue #N 標題

## 修改項目及內容
- **Spec/02HomeAPI.md**（added，+20 -0）
  {diff 內容}
- **Prototype/03B.html**（modified，+5 -2）
  {diff 內容}

## 關聯項目
- Epic：MPinfo-Co/P1-project#1
- SA Issue：MPinfo-Co/P1-analysis#4
- SD Issue：P1-design #5
- 上一個 commit：{前一個 commit hash}
- 本次 commit：{本次 commit hash}
```



---

# 二.品質把關

## 2.1 程式審查機制(自動＋人工)

### Repo：P1-analysis / P1-design / P1-code
- **PR**：各階段審查人確認品質，需逐行確認細節
### Repo：P1-code
- **Local(commit時)**：pre-commit（ruff）+ husky lint-staged（ESLint、Prettier）+ commitlint
- **Github(push時)**：ruff lint/format、ESLint、Prettier check、pytest

---

## 2.1文件自動審查機制

每天台灣時間 **凌晨 2:00** 自動執行，由 Claude Code Remote Agent 在雲端運作。

| 任務名稱              | 說明                                                     |
| ----------------- | ------------------------------------------------------ |
| Daily Docs Review | 讀取 `docs/ai-review/AI-review-prompt.md`，審查四個 Repo 文件狀況 |

管理介面：https://claude.ai/code/scheduled

---
