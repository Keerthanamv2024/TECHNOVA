@echo off
title Push TechNova to GitHub (Keerthanamv2024/TECHNOVA)
color 0A
echo =================================================================
echo         Pushing TechNova Project to GitHub Repository
echo         Target: https://github.com/Keerthanamv2024/TECHNOVA
echo =================================================================
echo.

set "PATH=%LOCALAPPDATA%\Programs\MinGit\cmd;%PATH%"

echo [1/3] Checking Git Status...
git status
echo.

echo [2/3] Adding all files and committing...
git add .
git commit -m "Complete TechNova IT Company Profile Website project" 2>nul
git branch -M main
git remote remove origin 2>nul
git remote add origin https://github.com/Keerthanamv2024/TECHNOVA.git
echo.

echo [3/3] Pushing to GitHub...
echo (If prompted, please sign in or provide your GitHub credentials/Personal Access Token)
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo =================================================================
    echo SUCCESS! Your project has been pushed to your GitHub repository!
    echo Visit: https://github.com/Keerthanamv2024/TECHNOVA
    echo =================================================================
) else (
    echo.
    echo =================================================================
    echo [NOTE] If git push asked for credentials or failed:
    echo 1. You can enter your GitHub Username and Personal Access Token (PAT).
    echo OR
    echo 2. Use the instant browser upload link at:
    echo    https://github.com/Keerthanamv2024/TECHNOVA/upload/main
    echo =================================================================
)

echo.
pause
