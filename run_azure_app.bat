@echo off
title Full-Stack Floci Azure Cloud Deployment Automation
cls

echo =====================================================================
echo          LAUNCHING LOCAL AZURE SIMULATION WORKSPACE
echo =====================================================================
echo.


set CLOUD_PROVIDER=local-azure
docker compose up --build

:: 1. Initialize Azure mock cluster stacks
echo [1/3] Booting Floci Azure Stack Container...
call floci az start
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ensure Docker Desktop is active!
    pause
    exit /b %ERRORLEVEL%
)
echo.

echo [2/3] Waiting for Azure mock infrastructure port bindings to stabilize...
timeout /t 3 /nobreak >nul

:: 2. Spin up Python backend execution engine
echo [3/3] Activating database API connection arrays on port 7000...
start "FastAPI Azure Backend Engine" cmd /k "cd /d D:\Python-Learn\PythonPractice && .venv\Scripts\activate && uvicorn app:app --host 0.0.0.0 --port 7000 --reload"

timeout /t 3 /nobreak >nul
echo.
echo =====================================================================
echo     SUCCESS: Opening Local Azure Unified Dashboard Endpoint...
echo =====================================================================
echo.

:: Launches the user interface directly through the port 7000 pipeline handler
start "" "http://localhost:7000/"

exit