@echo off
REM Script to start API Backend Server

cd /d "%~dp0BACKEND"

echo ========================================
echo Starting CVDTT Lab API Server
echo ========================================
echo.
echo Server will run on http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level info

pause
