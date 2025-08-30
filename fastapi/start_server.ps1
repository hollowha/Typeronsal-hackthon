# typersonal FastAPI 服务器启动脚本
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "启动 typersonal FastAPI 服务器" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 激活 typersonal 环境
Write-Host "正在激活 typersonal 环境..." -ForegroundColor Yellow
& "C:\Users\HackathonUser\miniconda3\Scripts\activate.bat" typersonal

# 检查环境是否正确激活
Write-Host ""
Write-Host "检查环境状态..." -ForegroundColor Yellow
& "C:\Users\HackathonUser\miniconda3\envs\typersonal\python.exe" --version
& "C:\Users\HackathonUser\miniconda3\envs\typersonal\python.exe" -c "import torch; print('PyTorch:', torch.__version__)"
& "C:\Users\HackathonUser\miniconda3\envs\typersonal\python.exe" -c "import torch; print('CUDA 可用:', torch.cuda.is_available())"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "环境检查完成，启动 FastAPI 服务器..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 启动 FastAPI 服务器
Write-Host "启动服务器: http://localhost:8000" -ForegroundColor Green
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host ""

# 使用环境中的 uvicorn
& "C:\Users\HackathonUser\miniconda3\envs\typersonal\Scripts\uvicorn.exe" main:app --host 0.0.0.0 --port 8000 --reload




