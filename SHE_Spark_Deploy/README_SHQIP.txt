================================================================================
DEPLOYMENT I PLOTË - REPUBLIKA E KOSOVËS (XK)
================================================================================
Data: 23 Tetor 2025
Server: krenuser@185.182.158.150:8022
Folder: /home/krenuser/SHE_Spark_Deploy

================================================================================
PËRMBAJTJA E PROJEKTIT - 100% NË SHQIP
================================================================================

1. gjenerues_simple_spark.py (5.0 KB) - GJENERUESI KRYESOR I TË DHËNAVE
   - Periudha: 1 Janar 2022 deri 23 Tetor 2025
   - Gjeneron 96,048 rreshta (23 asete × 3 modele × 1,392 ditë)
   - Përdor Apache Spark (1GB memorie)

2. prezantimi_shqip_full.vba (KY ËSHTË I RI!) - GJENERUESI I PREZANTIMIT
   - Krijon 8+ slide me FIGURA, SKEMA DHE DIAGRAME
   - 100% në gjuhën shqipe
   - Përfshin flamurin e Kosovës (XK)
   - NUK ka nevojë për imazhe të jashtme - krijon forma në PowerPoint!

3. gjenerues_vizualizime.py - GJENERUESI I FIGURAVE (opsionale)
   - Krijon 8 figura profesionale me matplotlib
   - Të gjitha në shqip

================================================================================
SI TË EKZEKUTOSH NË SERVER
================================================================================

1. LIDHJA ME SERVERIN:
   ssh -p 8022 krenuser@185.182.158.150

2. SHKO TE FOLDERI:
   cd /home/krenuser/SHE_Spark_Deploy

3. EKZEKUTO SPARK GENERATOR:
   spark-submit --master local[*] --driver-memory 1g --executor-memory 1g gjenerues_simple_spark.py

4. TË DHËNAT DO TË JENË NË:
   data_kaggle/{ASETI}.csv (23 skedarë CSV)

================================================================================
SI TË GJENEROSH PREZANTIMIN (NË KOMPJUTERIN TUAJ)
================================================================================

MËNYRA E RE - ME FORMA TË INTEGRUARA (REKOMANDOHET):
-------------------------------------------------------
1. Hap Microsoft PowerPoint (prezantim bosh)

2. Shtyp ALT + F11 për të hapur VBA Editor

3. Insert → Module

4. Kopjo të gjithë kodin nga skedari: prezantimi_shqip_full.vba

5. Ngjit në module

6. Shtyp F5 për të ekzekutuar

7. Prit 30-60 sekonda

8. GATI! Do të krijohen 8 slide me:
   - Flamurin e Kosovës (XK)
   - Arkitekturën e Big Data
   - Flowchart të 8 modeleve
   - Strategjitë e investimit
   - Diagrame dhe forma të ngjyrosura
   - 100% në shqip!

================================================================================
23 ASETET FINANCIARE (PA KRIPTOVALUTA!)
================================================================================

AKSIONE (8):
  • AAPL - Apple Inc.
  • GOOGL - Alphabet Inc. (Google)
  • MSFT - Microsoft Corporation
  • AMZN - Amazon.com Inc.
  • NVDA - NVIDIA Corporation
  • TSLA - Tesla Inc.
  • META - Meta Platforms Inc. (Facebook)
  • NFLX - Netflix Inc.

FOREX - VALUTAT (9):
  • EUR/USD - Euro / Dollari Amerikan
  • GBP/USD - Paundi Britanik / Dollari
  • USD/JPY - Dollari / Jeni Japonez
  • USD/CHF - Dollari / Frangu Zviceran
  • AUD/USD - Dollari Australian / Dollari
  • USD/CAD - Dollari / Dollari Kanadez
  • NZD/USD - Dollari i Zelandës së Re / Dollari
  • USD/CNY - Dollari / Juani Kinez
  • EUR/GBP - Euro / Paundi Britanik

LËNDË TË PARA (4):
  • Gold - Ari
  • Silver - Argjendi
  • Oil - Nafta
  • NaturalGas - Gazi Natyror

INDEKSE (2):
  • SP500 - Standard & Poor's 500
  • NASDAQ - NASDAQ Composite

================================================================================
8 MODELET STOKASTIKE
================================================================================

1. GBM (Geometric Brownian Motion)
   - Modeli bazë për të gjitha asetet
   - Formula: dS/S = μ*dt + σ*dW

2. HESTON (Stochastic Volatility)
   - Volatilitet i ndryshueshëm
   - Për aksione me volatilitet të lartë

3. JUMP DIFFUSION (Merton 1976)
   - Kap ngjarjet e papritura
   - Për lëndë të para dhe aksione volatile

4. GARCH(1,1) EFFECTS
   - Volatilitet clustering
   - Fat tails & autocorrelation

5. REGIME SWITCHING (Markov Chain)
   - Detekton ciklet e tregut (Bull/Bear/Sideways)
   - Ndikon në trend

6. LEVY PROCESSES (Student-t Distribution)
   - Distribucioni me heavy tails
   - Më i mirë për ngjarje ekstreme

7. MARKET CRASH SIMULATION
   - Simulon krashe historike (2015, 2018, 2020, 2022)
   - Magnitude: -6% deri -12%

8. CORRELATION DYNAMICS (Cholesky Decomposition)
   - Matrica e korrelacionit
   - Për ndërtimin e portfolio-s

================================================================================
STRATEGJITË E INVESTIMIT
================================================================================

AFATSHKURTËR (1-5 DITË):
-------------------------
BLI kur:
  ✓ RSI < 30 (oversold)
  ✓ Çmimi nën Bollinger Band
  ✓ MACD kryqëzon mbi linjën e sinjalit
  ✓ Volume spike (>1.5x mesatarja)

SHIT kur:
  ✗ RSI > 70 (overbought)
  ✗ Çmimi mbi Bollinger Band
  ✗ MACD kryqëzon nën linjën e sinjalit
  ✗ Target: +3-5% fitim OSE Stop-loss: -2%

Asete të rekomanduara: NVDA, TSLA, GBP/USD, Nafta

AFATGJATË (6-18 MUAJ):
-----------------------
Portfolio i rekomanduar:
  • 40% - Aksione të mëdha (AAPL, MSFT, GOOGL)
  • 25% - Indekse (SP500, NASDAQ)
  • 20% - Safe havens (Ari, Argjend)
  • 10% - Forex (EUR/USD, USD/JPY)
  • 5% - Para të gatshme (Cash reserves)

Rebalancimi: Çdo 3 muaj (tremujor)

Target fitimi:
  • AAPL: +25-35% (12 muaj)
  • MSFT: +20-30% (12 muaj)
  • Ari: +15-20% (18 muaj)
  • SP500: +12-18% (12 muaj)

================================================================================
BIG DATA - APACHE SPARK
================================================================================

ARKITEKTURA:
  ┌─────────────┬─────────────┬─────────────┐
  │  PySpark   │  Spark SQL │  Spark MLlib │
  │    API     │            │      ML      │
  └──────┬──────┴──────┬──────┴──────┬──────┘
         │             │             │
         └─────────────┴─────────────┘
                       │
          ┌────────────▼────────────┐
          │     SPARK CORE         │
          │   RDD & DataFrames      │
          └────────────┬────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    ┌────▼───┐    ┌───▼────┐   ┌───▼────┐
    │ Driver │    │Executor│   │Cluster │
    │  1GB   │    │  1GB   │   │Local[*]│
    └────────┘    └────────┘   └────────┘
                       │
              ┌────────▼────────┐
              │   TË DHËNAT     │
              │   96,048 rows   │
              └─────────────────┘

SPECIFIKIMET:
  • Gjithsej rreshta: 96,048
  • Periudha: 1 Janar 2022 - 23 Tetor 2025 (1,392 ditë)
  • Asete: 23 instrumente financiare
  • Modele: 3 modele stokastike (GBM, Heston, GARCH)
  • Madhësia: ~15 MB CSV
  • Koha e gjenerimit: ~120 sekonda

================================================================================
REPUBLIKA E KOSOVËS (XK)
================================================================================

Ky projekt është zhvilluar për Universitetin e Prishtinës
në Republikën e Kosovës (Kod Shteti: XK).

Flamuri i Kosovës:
  • Sfond blu (#244AA5)
  • 6 yje të bardhë (përfaqësojnë 6 grupet etnike)
  • Konturat e Kosovës në ari (#D59F3C)

================================================================================
KONTAKTI
================================================================================

Nëse keni probleme:
1. Verifikoni që Spark është i instaluar: spark-submit --version
2. Verifikoni Python packages: pip install pyspark matplotlib numpy
3. Verifikoni gjenerimin e të dhënave: shiko data_kaggle/
4. Verifikoni VBA: rreshti 28 duhet të ketë CurDir() & "\vizualizime\"

================================================================================
STATUS: ✅ DEPLOYMENT I PLOTË I PËRFUNDUAR
DATA: 23 Tetor 2025
SERVER: ssh -p 8022 krenuser@185.182.158.150
GJUHA: 100% SHQIP
KOD SHTETI: XK (KOSOVË)
================================================================================
