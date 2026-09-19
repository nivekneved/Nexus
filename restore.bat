@echo off
TITLE Nexus Workforce — 1-Click Disaster Recovery & Restore
chcp 65001 >nul
cls

echo =====================================================================
echo  NEXUS WORKFORCE ENGINE — 1-CLICK RESTORE & DISASTER RECOVERY
echo  Principal: Deven Pawaray (devenpawaray@gmail.com)
echo =====================================================================
echo.

python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not found in your PATH. Please install Python 3.10+
    pause
    exit /b 1
)

python restore.py

echo.
echo =====================================================================
echo  Restore session finished.
echo =====================================================================
pause
