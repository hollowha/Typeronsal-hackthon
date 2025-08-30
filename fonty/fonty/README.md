# Typersonal - AI 字型生成平台

一個使用 AI 技術創造獨特字型設計的 Nuxt.js 應用程式。

## 最近修復的問題

### 1. 後端服務連接問題
- **問題**: 應用程式嘗試連接到 `http://localhost:3001/convert` 但服務未運行
- **解決方案**: 重新設計了 template 頁面，移除對外部字型轉換服務的依賴，改用前端處理

### 2. useAuth 導入錯誤
- **問題**: `useAuth is not a function` 錯誤
- **解決方案**: 修正了動態導入路徑，使用相對路徑導入

### 3. Vue 組件反應性警告
- **問題**: 組件被意外地變為反應性對象
- **解決方案**: 將 SideMenu 中的圖標組件改為使用 `defineComponent` 包裝

### 4. Manifest 圖標錯誤
- **問題**: 圖標資源大小不正確
- **解決方案**: 簡化了 manifest.json 中的圖標配置

## Template 頁面功能說明

### 新的實現方式
Template 頁面現在使用純前端方式處理字型生成和應用：

1. **字型生成**: 使用現有的 AI API (`https://typersonal.dy6.click/8000`) 生成單字圖片
2. **字型應用**: 直接在前端將生成的圖片作為字體使用，無需轉換為 TTF 文件
3. **即時預覽**: 使用 Canvas API 將生成的圖片字體渲染到模板上
4. **匯出功能**: 將最終結果匯出為高解析度 PNG 圖片

### 工作流程
1. 選擇模板（結婚賀卡、情書、手寫帳）
2. 上傳手寫參考圖片
3. 勾選要生成的文字區塊
4. 批量生成字型圖片
5. 即時預覽效果
6. 匯出最終圖片

### 技術特點
- 無需外部字型轉換服務
- 使用 Canvas API 進行圖片合成
- 支援高解析度輸出
- 即時預覽和編輯

## 安裝與運行

### 前置需求
- Node.js 18+ 
- npm 或 yarn

### 安裝依賴
```bash
npm install
```

### 開發模式運行
```bash
npm run dev
```

應用程式將在 `http://localhost:3000` 運行

### 建置生產版本
```bash
npm run build
npm run preview
```

## 功能特色

- 🎨 AI 字型生成
- 📱 響應式設計
- 🔐 Firebase 身份驗證
- 🖼️ 字型預覽與模板
- 📱 PWA 支援
- 🎯 純前端字型處理

## 技術架構

- **前端**: Nuxt.js 3 + Vue 3
- **樣式**: Tailwind CSS
- **認證**: Firebase Auth
- **字型處理**: 前端 Canvas API + AI 生成服務
- **AI 服務**: 外部 API (`https://typersonal.dy6.click/8000`)

## 注意事項

- 字型生成依賴外部 AI 服務
- 使用 Canvas API 進行圖片合成，支援高解析度輸出
- 確保 Firebase 配置正確設置
- 需要穩定的網路連接來使用 AI 字型生成服務

## 開發者

Typersonal 開發團隊
