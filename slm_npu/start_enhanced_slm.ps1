#!/usr/bin/env pwsh
# 啟動增強版 SLM NPU 服務器

Write-Host "🚀 啟動增強版 SLM NPU 服務器" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "📍 服務地址: http://localhost:8001" -ForegroundColor Cyan
Write-Host "🔧 健康檢查: http://localhost:8001/health" -ForegroundColor Cyan
Write-Host "📚 API文檔: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 優化內容:" -ForegroundColor Yellow
Write-Host "   • 回應長度提升 2.5 倍 (80 -> 200 tokens)" -ForegroundColor Yellow
Write-Host "   • 增強提示詞工程" -ForegroundColor Yellow
Write-Host "   • 智能模板大幅增強" -ForegroundColor Yellow
Write-Host ""
Write-Host "⏳ 正在啟動服務器..." -ForegroundColor Magenta
Write-Host ""

# 切換到腳本所在目錄
Set-Location $PSScriptRoot

# 啟動服務器
try {
    python slm_server.py
}
catch {
    Write-Host "❌ 啟動失敗: $_" -ForegroundColor Red
    Write-Host "請檢查 Python 環境和依賴庫" -ForegroundColor Red
}

Write-Host ""
Write-Host "按任意鍵退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
