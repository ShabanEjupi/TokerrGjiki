================================================================================
SHE SPARK DEPLOYMENT - FINAL CLEAN VERSION
================================================================================
Date: October 23, 2025
Server: krenuser@185.182.158.150:8022
Folder: /home/krenuser/SHE_Spark_Deploy

================================================================================
FILES INCLUDED (ONLY 2 FILES):
================================================================================
1. gjenerues_simple_spark.py (5.0 KB) - MAIN DATA GENERATOR
   - Date range: January 1, 2022 to October 23, 2025
   - Generates ~96,000 rows (23 assets × 3 models × 1,392 days)
   - Fixed to not crash server (1GB memory, process one-by-one)

2. prezantimi_powerpoint_v2.vba (34 KB) - POWERPOINT GENERATOR
   - Creates 25-slide presentation with auto-embedded images
   - FIXED: VBA path error (uses CurDir() & "\vizualizime\")
   - NO MORE Application.PathSeparator error

================================================================================
ALL REDUNDANT FILES DELETED:
================================================================================
✅ Deleted from LOCAL and SERVER:
   - All .md files (README, documentation)
   - All .txt files (URGENT_FIXES, MANUAL_COPY, etc.)
   - All .sh files (post_process_csv.sh, run_spark_server.sh)
   - All .bat files (update_deployment_package.bat, verify_files.bat)
   - analiza_spark_ml.py (not needed for basic run)
   - vizualizime_advanced.py (not needed for basic run)
   - gjenerues_dataset_spark.py (OLD version that crashed)
   - requirements_spark.txt (not needed - use pip install pyspark)

✅ Server folder RENAMED: TokerrGjiki_Spark_Deploy → SHE_Spark_Deploy
✅ Local folder RENAMED: TokerrGjiki_Spark_Deploy → SHE_Spark_Deploy

================================================================================
HOW TO RUN ON SERVER:
================================================================================
1. SSH to server:
   ssh -p 8022 krenuser@185.182.158.150

2. Navigate to folder:
   cd /home/krenuser/SHE_Spark_Deploy

3. Run Spark generator:
   spark-submit --master local[*] --driver-memory 1g --executor-memory 1g gjenerues_simple_spark.py

4. Data will be in: data_kaggle/{ASSET}.csv (23 CSV files)

================================================================================
HOW TO GENERATE POWERPOINT (LOCAL):
================================================================================
1. Download data and visualizations from server:
   scp -P 8022 -r krenuser@185.182.158.150:/home/krenuser/SHE_Spark_Deploy/data_kaggle ./
   scp -P 8022 -r krenuser@185.182.158.150:/home/krenuser/SHE_Spark_Deploy/vizualizime ./

2. Open PowerPoint (blank presentation)

3. Press ALT + F11 (open VBA editor)

4. Insert → Module

5. Copy entire content of prezantimi_powerpoint_v2.vba

6. Paste into module

7. Press F5 to run (or click Run button)

8. Wait 60-90 seconds for 25 slides to generate

================================================================================
VBA FIX EXPLANATION:
================================================================================
❌ WRONG (students had this):
    vizFolder = ThisWorkbook.Path & Application.PathSeparator & "vizualizime"
    
    ERRORS:
    - ThisWorkbook.Path doesn't work in PowerPoint modules
    - Application.PathSeparator doesn't exist in VBA

✅ CORRECT (fixed version):
    vizFolder = CurDir() & "\vizualizime\"
    
    REASONS:
    - CurDir() returns current working directory
    - "\vizualizime\" is simple Windows path (backslash works in VBA)
    - No need for Application.PathSeparator (not a VBA property)

================================================================================
DEPENDENCIES:
================================================================================
Server needs:
- Apache Spark 3.5.0+
- Python 3.8+
- pip install pyspark numpy pandas matplotlib seaborn scipy

Local needs:
- Microsoft PowerPoint
- VBA enabled
- data_kaggle/ and vizualizime/ folders in same directory

================================================================================
CONTACT:
================================================================================
If errors persist, check:
1. VBA file is the FIXED version (line 28: CurDir() & "\vizualizime\")
2. Current directory is correct (where data_kaggle/ and vizualizime/ exist)
3. PowerPoint VBA macros are enabled
4. Server has enough memory (1GB minimum)

================================================================================
