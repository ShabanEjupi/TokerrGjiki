@echo off
REM Build script for Windows EXE using PyInstaller

echo ========================================
echo Building Tokerrgjik for Windows...
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build EXE
echo Building Windows EXE...
pyinstaller tokerrgjik_windows.spec

REM Check if build was successful
if exist "dist\Tokerrgjik.exe" (
    echo.
    echo ========================================
    echo Build successful!
    echo ========================================
    echo.
    echo EXE location: dist\Tokerrgjik.exe
    echo.
    echo You can now run the game by double-clicking:
    echo   dist\Tokerrgjik.exe
    echo.
) else (
    echo.
    echo ========================================
    echo Build failed! Check errors above.
    echo ========================================
    echo.
    exit /b 1
)

pause
