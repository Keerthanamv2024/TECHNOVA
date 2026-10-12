@echo off
title TechNova IT Company Profile Website
color 0B
echo =========================================================
echo       TechNova - IT Company Profile Website
echo       College Web Programming Project
echo =========================================================
echo.
echo [1/3] Checking Python environment...

set PYTHON_CMD=python
where python >nul 2>nul
if %errorlevel% neq 0 (
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
        set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    ) else (
        echo [ERROR] Python is not found. Please install Python 3.
        pause
        exit /b 1
    )
)

echo [2/3] Opening website in your default web browser...
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000"

echo [3/3] Starting TechNova Flask Backend Server...
echo.
echo * Server is running at: http://127.0.0.1:5000
echo * Admin Login: http://127.0.0.1:5000/admin/login
echo * Admin Credentials: admin / admin123
echo.
echo Press Ctrl+C in this window anytime to stop the server.
echo =========================================================
echo.

%PYTHON_CMD% app.py

pause
