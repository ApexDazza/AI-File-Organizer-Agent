@echo off
title Ultimate AI File Organizer
color 0A
echo.
echo ========================================
echo    Ultimate AI File Organizer
echo ========================================
echo.
echo 🚀 Starting your file organization wizard...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo 📥 Download from: https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is available
npx --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js/npx not found! Please install Node.js first.
    echo 📥 Download from: https://nodejs.org
    pause
    exit /b 1
)

REM Run the file organizer
echo ✅ All dependencies found!
echo.
python ultimate_file_organizer.py

echo.
echo 📝 Organization session complete!
pause