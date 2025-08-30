# Typersonal - AI 字型生成系統

一個基於 AI 的智能字型生成系統，結合了深度學習模型和手寫風格遷移技術，能夠從少量範例生成個性化字型。

## 功能特色

- **AI 字型生成**: 使用深度學習模型生成個性化字型
- **SLM NPU 加速**: 支援 NPU 硬體加速的語言模型推理
- **即時預覽**: 實時預覽生成的字型效果
- **批量處理**: 支援多字元批量生成
- **手寫風格遷移**: 從手寫範例學習並應用風格
- **Web 介面**: 直觀的前端操作界面

## 系統架構

```
Typersonal/
├── fastapi/          # 主要後端服務 (FastAPI)
├── slm_npu/          # SLM NPU 服務
├── fonty/            # 前端應用 (Nuxt.js)
├── typersonal/       # AI 模型核心
├── ttf/              # 字型轉換工具
└── configs/          # 配置文件
```

## 系統需求

- **Python**: 3.10.18
- **Node.js**: 18+ 
- **Conda**: 用於環境管理
- **NPU**: Qualcomm 等 NPU 硬體

## 快速開始

### 1. 環境安裝

首先安裝 Conda 環境：

```bash
conda env create -f typersonal_env.yml
conda activate typersonal
```

### 2. 安裝前端依賴

```bash
# 進入前端目錄
cd fonty/fonty

# 安裝 Node.js 依賴
npm install
```

### 3. 啟動服務

#### 第一步：啟動主要後端服務

```bash
# 進入 fastapi 目錄
cd fastapi

# 啟動 FastAPI 後端
uvicorn main:app --host 0.0.0.0 --port 8000
```

後端服務將在 `http://localhost:8000` 運行
- API 文檔: `http://localhost:8000/docs`
- 健康檢查: `http://localhost:8000/health`

#### 第二步：啟動 SLM NPU 服務

```bash
# 進入 slm_npu 目錄
cd slm_npu

# 啟動 SLM 服務
python slm_server.py
```

SLM 服務將在 `http://localhost:8001` 運行

#### 第三步：啟動前端應用

```bash
# 進入前端目錄
cd fonty/fonty

# 啟動開發服務器
npm run dev
```

前端應用將在 `http://localhost:3000` 運行

### 4. 訪問應用

打開瀏覽器訪問 `http://localhost:3000` 開始使用字型生成功能。

## 配置說明

### 後端配置

- **主後端**: 端口 8000，處理主要業務邏輯
- **SLM 後端**: 端口 8001，專門處理 NPU 加速的語言模型
- **數據庫**: MongoDB (配置在 `fastapi/db/mongo.py`)

### 前端配置

- **框架**: Nuxt.js 3
- **UI**: Tailwind CSS
- **狀態管理**: Vue 3 Composition API
- **認證**: Firebase Authentication

## 使用流程

1. **上傳範例**: 上傳手寫字體範例圖片
2. **輸入文字**: 輸入要生成的字元
3. **調整參數**: 設定生成參數 (採樣步數、風格強度等)
4. **生成字型**: 系統使用 AI 模型生成字型
5. **預覽下載**: 預覽效果並下載生成的字型


---

**提示**: 確保所有服務都正常運行後再使用完整功能。建議按照順序啟動服務：後端 → SLM → 前端。
