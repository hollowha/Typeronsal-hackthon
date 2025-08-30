# typersonal FastAPI 服务器最终启动脚本
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "typersonal FastAPI 服务器启动脚本" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 激活 typersonal 环境
Write-Host "正在激活 typersonal 环境..." -ForegroundColor Yellow
& "C:\Users\HackathonUser\miniconda3\Scripts\activate.bat" typersonal

# 检查环境
Write-Host ""
Write-Host "正在检查环境配置..." -ForegroundColor Yellow
& "C:\Users\HackathonUser\miniconda3\envs\typersonal\python.exe" check_environment.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "环境检查完成，启动 FastAPI 服务器..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 启动 FastAPI 服务器
Write-Host "启动服务器: http://localhost:8000" -ForegroundColor Green
Write-Host "API 文档: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host ""

# 切换到 fastapi 目录
Set-Location $PSScriptRoot

# 启动服务器
& "C:\Users\HackathonUser\miniconda3\envs\typersonal\Scripts\uvicorn.exe" main:app --host 0.0.0.0 --port 8000 --reload




