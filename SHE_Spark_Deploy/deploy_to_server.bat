@echo off
REM ================================================================================
REM DEPLOYMENT SCRIPT - KOPJO SKEDARET NE SERVER
REM Server: krenuser@185.182.158.150:8022
REM Folder: /home/krenuser/SHE_Spark_Deploy
REM ================================================================================

echo.
echo ================================================================================
echo DEPLOYMENT NE SERVER - REPUBLIKA E KOSOVES (XK)
echo ================================================================================
echo.
echo Server: krenuser@185.182.158.150:8022
echo Folder: /home/krenuser/SHE_Spark_Deploy
echo.
echo Duke kopjuar skedaret...
echo.

REM Kopjo gjeneruesin kryesor
echo [1/3] Duke kopjuar gjenerues_simple_spark.py...
scp -P 8022 gjenerues_simple_spark.py krenuser@185.182.158.150:/home/krenuser/SHE_Spark_Deploy/
if %errorlevel% neq 0 (
    echo GABIM: Kopjimi deshtoi!
    pause
    exit /b 1
)
echo   OK - gjenerues_simple_spark.py u kopjua me sukses!
echo.

REM Kopjo README ne shqip
echo [2/3] Duke kopjuar README_SHQIP.txt...
scp -P 8022 README_SHQIP.txt krenuser@185.182.158.150:/home/krenuser/SHE_Spark_Deploy/
if %errorlevel% neq 0 (
    echo GABIM: Kopjimi deshtoi!
    pause
    exit /b 1
)
echo   OK - README_SHQIP.txt u kopjua me sukses!
echo.

REM Kopjo gjeneruesin e vizualizimeve
echo [3/3] Duke kopjuar gjenerues_vizualizime.py...
scp -P 8022 gjenerues_vizualizime.py krenuser@185.182.158.150:/home/krenuser/SHE_Spark_Deploy/
if %errorlevel% neq 0 (
    echo GABIM: Kopjimi deshtoi!
    pause
    exit /b 1
)
echo   OK - gjenerues_vizualizime.py u kopjua me sukses!
echo.

echo ================================================================================
echo SUKSES! Te gjitha skedaret u kopjuan ne server!
echo ================================================================================
echo.
echo Hapat e radhes:
echo.
echo 1. Lidhuni me serverin:
echo    ssh -p 8022 krenuser@185.182.158.150
echo.
echo 2. Shkoni te folderi:
echo    cd /home/krenuser/SHE_Spark_Deploy
echo.
echo 3. Ekzekutoni Spark:
echo    spark-submit --master local[*] --driver-memory 1g --executor-memory 1g gjenerues_simple_spark.py
echo.
echo 4. Gjeneroni prezantimin ne kompjuterin tuaj:
echo    - Hap PowerPoint
echo    - ALT + F11
echo    - Kopjo kodin nga prezantimi_shqip_full.vba
echo    - Shtyp F5
echo.
echo ================================================================================
echo.
pause
