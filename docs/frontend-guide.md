# MP-Box 前端說明文件

> 本文以「使用者操作主流程」為主線，帶你了解 P1-code 前端各檔案如何串連，以及每個技術框架為什麼在這裡出現。

---

## 目錄

1. [這份文件怎麼讀](#1-這份文件怎麼讀)
2. [技術選型一覽](#2-技術選型一覽)
3. [主流程走讀](#3-主流程走讀)
   - [3.1 程式啟動](#31-程式啟動)
   - [3.2 登入流程](#32-登入流程)
   - [3.3 進入主畫面](#33-進入主畫面)
   - [3.4 瀏覽事件清單](#34-瀏覽事件清單)
   - [3.5 開啟事件詳情](#35-開啟事件詳情)
4. [狀態管理設計](#4-狀態管理設計)
5. [技術框架速查表](#5-技術框架速查表)
6. [目前尚未完成的功能](#6-目前尚未完成的功能)

---

## 1. 這份文件怎麼讀

**目標讀者：** 剛接觸 P1-code 前端的開發者，不論是個人學習或新進同事皆適用。

**建議閱讀順序：**
1. 先看「技術選型一覽」，對齊框架認知（5 分鐘）
2. 從 3.1 開始按順序走讀主流程（核心，30 分鐘）
3. 讀完後再看「狀態管理設計」，理解全局資料流
4. 遇到不熟悉的框架，去「技術框架速查表」補充細節

**搭配對照的原始碼：**

| 本文章節 | 對應檔案 |
|---------|---------|
| 3.1 程式啟動 | `frontend/src/main.jsx`、`frontend/src/theme.js` |
| 3.2 登入流程 | `frontend/src/pages/Login/Login.jsx`、`frontend/src/stores/authStore.js` |
| 3.3 主畫面 | `frontend/src/App.jsx`、`frontend/src/components/Layout/` |
| 3.4 事件清單 | `frontend/src/pages/AiPartner/IssueList.jsx` |
| 3.5 事件詳情 | `frontend/src/pages/AiPartner/IssueDetail.jsx` |
| 4. 狀態管理 | `frontend/src/stores/authStore.js`、`frontend/src/contexts/IssuesContext.jsx` |

> 所有檔案路徑皆相對於 `P1-code/` 根目錄。

---

## 2. 技術選型一覽

在進入流程之前，先認識這個專案用了哪些框架、各自解決什麼問題。

| 框架 | 用途 | 解決的問題 | 主要檔案 |
|------|------|-----------|---------|
| **React 18** | UI 元件化 | 用宣告式寫法描述畫面，資料變動時自動更新 UI | 所有 `.jsx` 檔 |
| **React Router v6** | 前端路由 | 不重新整理頁面就能切換 URL 對應的元件 | `App.jsx` |
| **MUI (Material UI) v6** | UI 元件庫 | 提供現成的 Button、Table、Tabs 等元件，統一視覺風格 | 所有 pages |
| **Zustand** | 全域狀態管理 | 跨元件共享狀態，並能持久化到 localStorage | `stores/authStore.js` |
| **React Context** | 區域狀態管理 | App 內部共享資料，比 Zustand 輕量 | `contexts/IssuesContext.jsx` |
| **Vite** | 開發/打包工具 | 極速的 HMR（熱更新），取代傳統 webpack | `vite.config.js` |

> **為什麼同時有 Zustand 和 Context？** 兩者都能跨元件共享資料，但職責不同。詳見第 4 章。
