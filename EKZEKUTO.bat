@echo off
REM ================================================================================
REM EKZEKUTUES AUTOMATIK I PROJEKTIT DOKTORAL
REM Gjen Python automatikisht dhe ekzekuton projektin
REM ================================================================================

echo ================================================================================
echo PROJEKTI DOKTORATURE - ANALIZA FINANCIARE E AVANCUAR
echo Universiteti i Prishtines, Republika e Kosoves
echo ================================================================================
echo.

REM Provo te gjesh Python
echo [1/4] Duke kerkuar Python...

REM Provo py launcher
py --version >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Python u gjet: py launcher
    set PYTHON_CMD=py
    goto :run_project
)

REM Provo python
python --version >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Python u gjet: python
    set PYTHON_CMD=python
    goto :run_project
)

REM Provo python3
python3 --version >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Python u gjet: python3
    set PYTHON_CMD=python3
    goto :run_project
)

REM Provo ne Program Files
if exist "C:\Program Files\Python312\python.exe" (
    echo [OK] Python u gjet: C:\Program Files\Python312
    set PYTHON_CMD="C:\Program Files\Python312\python.exe"
    goto :run_project
)

if exist "C:\Program Files\Python311\python.exe" (
    echo [OK] Python u gjet: C:\Program Files\Python311
    set PYTHON_CMD="C:\Program Files\Python311\python.exe"
    goto :run_project
)

if exist "C:\Program Files\Python310\python.exe" (
    echo [OK] Python u gjet: C:\Program Files\Python310
    set PYTHON_CMD="C:\Program Files\Python310\python.exe"
    goto :run_project
)

REM Provo ne C:\Python
if exist "C:\Python312\python.exe" (
    echo [OK] Python u gjet: C:\Python312
    set PYTHON_CMD="C:\Python312\python.exe"
    goto :run_project
)

if exist "C:\Python311\python.exe" (
    echo [OK] Python u gjet: C:\Python311
    set PYTHON_CMD="C:\Python311\python.exe"
    goto :run_project
)

REM Provo ne LocalAppData
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    echo [OK] Python u gjet: LocalAppData\Python312
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :run_project
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    echo [OK] Python u gjet: LocalAppData\Python311
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :run_project
)

REM Python nuk u gjet
echo.
echo [GABIM] Python nuk u gjet ne sistem!
echo.
echo Ju lutem shkarkoni dhe instaloni Python nga:
echo https://www.python.org/downloads/
echo.
echo RENDESISHME: Gjate instalimit zgjidhni "Add Python to PATH"
echo.
pause
exit /b 1

:run_project
echo.
echo [2/4] Duke kontrolluar librariite...
%PYTHON_CMD% -m pip install --quiet pyspark pandas matplotlib seaborn numpy openpyxl python-pptx Pillow 2>nul
if %errorlevel%==0 (
    echo [OK] Librariite jane gati
) else (
    echo [INFO] Duke instaluar librariite...
    %PYTHON_CMD% -m pip install pyspark pandas matplotlib seaborn numpy openpyxl python-pptx Pillow
)

echo.
echo [3/4] Duke gjeneruar dataset-in financiar...
%PYTHON_CMD% gjenerues_dataset_financiar.py
if %errorlevel% neq 0 (
    echo [GABIM] Gjenerimi i dataset-it deshtoi
    pause
    exit /b 1
)

echo.
echo [4/4] Duke ekzekutuar analizen e avancuar...
%PYTHON_CMD% analiza_financiare_advanced.py
if %errorlevel% neq 0 (
    echo [GABIM] Analiza deshtoi
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo PROJEKTI U EKZEKUTUA ME SUKSES!
echo ================================================================================
echo.
echo Rezultatet:
echo   - rezultatet_doktorature/     CSV files
echo   - vizualizime_doktorature/    10+ figura profesionale
echo   - prezantimi_powerpoint/      Prezantimi PowerPoint
echo.
pause
