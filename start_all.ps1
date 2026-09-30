# Nexus 24/7 Ecosystem Supervisor (PowerShell Launcher)
# -----------------------------------------------------
$Host.UI.RawUI.WindowTitle = "Nexus 24/7 Ecosystem Supervisor"
$ScriptDir = $PSScriptRoot
Set-Location $ScriptDir

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "          NEXUS ALL-IN-ONE SYSTEM SUPERVISOR (v4.0)" -ForegroundColor Green
Write-Host "  Starting AI Server, Revenue Daemon, and Cloudflare Public Tunnel..." -ForegroundColor Yellow
Write-Host "=====================================================================" -ForegroundColor Cyan

python start_all.py
