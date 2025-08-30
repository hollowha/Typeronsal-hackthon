@echo off
echo ========================================
echo 启动 typersonal FastAPI 服务器
echo ========================================
echo.

REM 激活 typersonal 环境
echo 正在激活 typersonal 环境...
call C:\Users\HackathonUser\miniconda3\Scripts\activate.bat typersonal

REM 检查环境是否正确激活
echo.
echo 检查环境状态...
python --version
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import torch; print('CUDA 可用:', torch.cuda.is_available())"

echo.
echo ========================================
echo 环境检查完成，启动 FastAPI 服务器...
echo ========================================
echo.

REM 启动 FastAPI 服务器
echo 启动服务器: http://localhost:8000
echo 按 Ctrl+C 停止服务器
echo.
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause




