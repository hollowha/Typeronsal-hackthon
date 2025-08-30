@echo off
echo ========================================
echo SLM NPU 字型生成器測試
echo ========================================
echo.

echo 正在檢查Python環境...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安裝或不在PATH中
    pause
    exit /b 1
)

echo.
echo 正在檢查依賴包...
pip list | findstr "onnxruntime"
if %errorlevel% neq 0 (
    echo ⚠️ 缺少onnxruntime，正在安裝...
    pip install -r requirements.txt
)

echo.
echo 正在運行SLM測試...
python test_slm.py

echo.
echo 測試完成！按任意鍵退出...
pause


