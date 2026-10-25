@echo off
title DHARA - Flash Flood Intelligence Launcher
echo ========================================================
echo   DHARA - Flash Flood Intelligence Early Warning System
echo   Team NexGen (SIH26192) - Ministry of Home Affairs / NDRF
echo ========================================================
echo.
echo [1/2] Starting FastAPI ML Backend on http://localhost:8000 ...
start "DHARA Backend" cmd /k "cd /d %~dp0backend && C:\Users\OMEN\flashGuard\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Starting React Vite Frontend on http://localhost:5173 ...
start "DHARA Frontend" cmd /k "cd /d %~dp0frontend && npm run dev -- --host --port 5173"

echo.
echo Launching browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo ========================================================
echo   DHARA is now live!
echo ========================================================
