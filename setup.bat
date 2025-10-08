@echo off
REM Quick setup script for Tokerrgjik on Windows

echo ========================================
echo TOKERRGJIK - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python 3.9 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check pip
echo Checking pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available!
    echo Installing pip...
    python -m ensurepip --upgrade
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
echo This may take a few minutes...
echo.
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo.
    echo Try running as Administrator or check your internet connection.
    pause
    exit /b 1
)

REM Create directories
echo.
echo Creating directories...
if not exist "sounds" mkdir sounds
if not exist "assets" mkdir assets

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the game:
echo   python main.py
echo.
echo To build Windows EXE:
echo   build_windows.bat
echo.
echo For Android APK:
echo   Use WSL2 or Linux and run build_android.sh
echo.
echo For more information, see README.md
echo.
pause
