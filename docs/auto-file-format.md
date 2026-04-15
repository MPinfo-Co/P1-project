# 自動產生 md 文件格式規範

> [← 回到 workflow_guide.md](workflow_guide.md)

各階段由 GitHub Actions workflow 自動建立的 md 文件，格式如下。

---

## business-logic.md

由 [p-workflow.yml](https://github.com/MPinfo-Co/P1-project/blob/main/.github/workflows/p-workflow.yml) 產生，SA 人工填寫。

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

---

## TDD/issue-{N}.md

由 [a-workflow.yml](https://github.com/MPinfo-Co/P1-analysis/blob/main/.github/workflows/a-workflow.yml) 產生，SD 人工填寫。

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

---

## TestReport/issue-{N}.md

由 [d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml) 產生，PG 人工填寫。

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

---

## SpecDiff/issue-{N}.md

由 [d-workflow.yml](https://github.com/MPinfo-Co/P1-design/blob/main/.github/workflows/d-workflow.yml) 產生，勿手動編輯。

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
