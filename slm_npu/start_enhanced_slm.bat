@echo off
echo 🚀 啟動增強版 SLM NPU 服務器
echo ======================================
echo.
echo 📍 服務地址: http://localhost:8001
echo 🔧 健康檢查: http://localhost:8001/health
echo 📚 API文檔: http://localhost:8001/docs
echo.
echo 💡 優化內容:
echo    • 回應長度提升 2.5 倍 (80 -> 200 tokens)
echo    • 增強提示詞工程
echo    • 智能模板大幅增強
echo.
echo ⏳ 正在啟動服務器...
echo.

cd /d "%~dp0"
python slm_server.py

pause
