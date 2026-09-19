@echo off
title Nexus Autonomous AI Workforce — Production Server
echo =====================================================================
echo           NEXUS AUTONOMOUS AI WORKFORCE (VERSION 2.5.1)
echo      14 AI Employees ^| 44 SubAgents ^| 25 Safeguards ^| Enterprise
echo =====================================================================
echo.

:: Check Python installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python 3 is not installed or not in PATH.
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: Create and activate virtual environment if not present
if not exist ".venv" (
    echo [*] Initializing virtual environment in .venv...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

:: Install dependencies
echo [*] Checking dependencies from requirements.txt...
pip install -r requirements.txt --quiet

:: Check for .env file
if not exist ".env" (
    if exist ".env.example" (
        echo [*] Creating .env from .env.example...
        copy .env.example .env >nul
    )
)

echo.
echo =====================================================================
echo   NEXUS ENGINE ONLINE: http://localhost:8000
echo   Financial Security &amp; Anti-Fraud Shield Active
echo   Press Ctrl+C to stop the workforce
echo =====================================================================
echo.

python server.py
pause
