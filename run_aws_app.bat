@echo off
title Full-Stack Floci Cloud Deployment Automation
cls

echo =====================================================================
echo          LAUNCHING LOCAL CLOUD ENGINE AND FASTAPI APPS
echo =====================================================================
echo.
set CLOUD_PROVIDER=local-aws
docker compose up --build

:: 1. Initialize and launch Floci Emulator
echo [1/4] Starting Floci AWS Emulator Container...
call floci start
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to boot Floci. Ensure Docker Desktop is active!
    pause
    exit /b %ERRORLEVEL%
)
echo.

:: 2. Wait to make sure the Floci internal port 4566 is listening completely
echo [2/4] Waiting for Floci core network layers to initialize...
timeout /t 5 /nobreak >nul

:: 3. Provision S3 buckets and sync Frontend UI assets
echo [3/4] Uploading frontend app dashboard straight into Floci S3...
call aws s3 mb s3://employee-dashboard --endpoint-url=http://localhost:4566 --region us-east-1 2>nul
call aws s3 cp app.html s3://employee-dashboard/index.html --endpoint-url=http://localhost:4566
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to push static file down to Floci S3. Check AWS CLI setup.
    pause
    exit /b %ERRORLEVEL%
)
echo.

:: 4. Launch your Python FastAPI server inside a separate background command window
echo [4/4] Launching FastAPI backend server in a separate window panel...
start "FastAPI Backend Server Pipeline" cmd /k "cd /d D:\Python-Learn\PythonPractice && .venv\Scripts\activate && uvicorn app:app --host 0.0.0.0 --port 7000 --reload"

:: 5. Let the systems settle, then launch the browser dashboard portal directly
timeout /t 3 /nobreak >nul
echo.
echo =====================================================================
echo     SUCCESS: All systems running! Opening Local Cloud Dashboard...
echo =====================================================================
echo.

start "" "http://localhost:4566/employee-dashboard/index.html"

exit