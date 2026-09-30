@echo off
title Nexus 24/7 Ecosystem Supervisor
color 0A
cls
echo =====================================================================
echo           NEXUS ALL-IN-ONE SYSTEM SUPERVISOR (v4.0)
echo   Starting AI Server, Revenue Daemon, and Cloudflare Public Tunnel...
echo =====================================================================
cd /d "%~dp0"
python start_all.py
pause
