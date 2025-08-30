@echo off
echo ========================================
echo typersonal FastAPI 服务器启动脚本
echo ========================================
echo.

REM 激活 typersonal 环境
echo 正在激活 typersonal 环境...
call C:\Users\HackathonUser\miniconda3\Scripts\activate.bat typersonal

REM 检查环境
echo.
echo 正在检查环境配置...
C:\Users\HackathonUser\miniconda3\envs\typersonal\python.exe check_environment.py

echo.
echo ========================================
echo 环境检查完成，启动 FastAPI 服务器...
echo ========================================
echo.

REM 启动 FastAPI 服务器
echo 启动服务器: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo 按 Ctrl+C 停止服务器
echo.

REM 切换到 fastapi 目录
cd /d "%~dp0"

REM 启动服务器
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause




