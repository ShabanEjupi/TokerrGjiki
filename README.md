# ANALIZA E AVANCUAR FINANCIARE - PROJEKTI DOKTORATURË

**Universiteti i Prishtinës, Republika e Kosovës 🇽🇰**

---

## 📚 PËRSHKRIMI I PROJEKTIT

Ky është projekt i nivelit **DOKTORAL** që përdor **Apache PySpark** për analizë të sofistikuar financiare. Projekti implementon **TË GJITHA** algoritmet e avancuara që keni mësuar me profesorin tuaj.

### 🎯 Qëllimi
Analiza e thellë e tregut financiar duke përdorur algoritme të Big Data dhe metodologji shkencore të nivelit më të lartë.

---

## 🚀 SI TË FILLONI (3 HAPA TË THJESHTË)

### Opsioni 1: Automatik (MË I LEHTË)
```bash
# Kliko dy herë në këtë file:
EKZEKUTO.bat
```

### Opsioni 2: Terminal i integruar VS Code
1. Shtyp `Ctrl+Shift+B` në VS Code
2. Zgjidh: "🚀 EKZEKUTO PROJEKTIN E PLOTË"
3. Prit derisa të përfundojë

### Opsioni 3: Manual
```powershell
python -m pip install pyspark pandas matplotlib seaborn numpy openpyxl python-pptx Pillow
python gjenerues_dataset_financiar.py
python analiza_financiare_advanced.py
python gjenerues_powerpoint.py
```

---

## 💰 DATASET-I FINANCIAR (NIVEL INSTITUCIONAL)

### Multi-Asset Portfolio me 12 Instrumente:

#### 📈 **Stocks (5)**
- AAPL - Apple Inc.
- GOOGL - Alphabet (Google)
- MSFT - Microsoft
- AMZN - Amazon
- NVDA - NVIDIA

#### ₿ **Cryptocurrency (3)**
- BTC - Bitcoin
- ETH - Ethereum
- SOL - Solana

#### 💱 **Forex Pairs (2)**
- EUR/USD - Euro / US Dollar
- GBP/USD - British Pound / US Dollar

#### 🏆 **Commodities (2)**
- GOLD - Ari
- OIL - Nafta

### Karakteristikat e Dataset-it:
- ✅ **2,470+ ditë tregtare** (2015-2024)
- ✅ **Geometric Brownian Motion** për çmime realiste
- ✅ **Regime Switching** (bull/bear markets)
- ✅ **Market Crashes** të simuluara (2015, 2018, 2020, 2022)
- ✅ **Volume correlation** me volatilitet
- ✅ **OHLC data** të plota (Open, High, Low, Close)

---

## 🎓 TË 10 ALGORITMET E PROFESORIT (TË GJITHA TË IMPLEMENTUARA)

### 1. **PERCENTILE_APPROX**
Llogaritja e kuantileve të përafërta për analiza statistikore.
```
P25 (Quartile 1), P50 (Median), P75 (Quartile 3), P95, P99
```

### 2. **STDDEV_SAMP**
Devijimi standard i mostrave për matjen e shpërndarjes.
```python
σ = √(Σ(x - μ)² / (n-1))
```

### 3. **LAG**
Operacione të serive kohore për krahasime temporale.
```
lag(1)  → çmimi i djeshëm
lag(5)  → çmimi 1 javë më parë
lag(10) → çmimi 2 javë më parë
lag(20) → çmimi 1 muaj më parë
```

### 4. **MOVING AVERAGE**
Mesataret lëvizëse për identifikimin e trendeve.
```
MA_7d  → Mesatarja 7-ditore (1 javë)
MA_30d → Mesatarja 30-ditore (1 muaj)
MA_90d → Mesatarja 90-ditore (3 muaj)
```

### 5. **GROUPBY AGGREGATION**
Agregimet në stil MapReduce për analizë të distribuuar.
```
Mujore:  avg, min, max, stddev, count
Vjetore: total volume, avg returns, volatility
```

### 6. **WINDOW FUNCTIONS**
Funksione analitike të dritareve për ranking dhe analiza.
```
rank()         → Renditja standard
dense_rank()   → Renditja pa zbrazëtira
percent_rank() → Renditja përqindsore
ntile(4)       → Ndarja në quartiles
```

### 7. **NULL COUNTING**
Analiza e plotësisë së të dhënave.
```
Null Count per kolonë
Completeness % = 100 - (nulls / total) * 100
```

### 8. **DATA PROFILING**
Vlerësimi gjithëpërfshirës i të dhënave.
```
Mean, Min, Max, Variance, StdDev
Skewness (asimetria), Kurtosis (kuroziteti)
```

### 9. **RETURNS CALCULATION**
Llogaritja e rendimenteve financiare.
```
Daily Return   = (Price_t - Price_t-1) / Price_t-1 * 100
Weekly Return  = rendimenti 7-ditor
Monthly Return = rendimenti 30-ditor
```

### 10. **VOLATILITY COMPUTATION**
Matja e rrezikut të investimit.
```
Historical Vol = stddev(Daily_Returns)
Annual Vol     = Daily_Vol × √252
Rolling Vol    = 30-day rolling standard deviation
```

---

## 📊 VIZUALIZIMET (12+ FIGURA PROFESIONALE)

### 1. **Time Series Comprehensive**
Çmimet, Moving Averages (7d, 30d, 90d), Returns, Volume

### 2. **Returns Distribution (3D)**
Shpërndarja 3D e rendimenteve + Correlation Matrix

### 3. **Volatility Analysis**
Rolling Volatility, Volatility vs Returns, Distribution

### 4. **Correlation Heatmap**
Matrica e korrelacionit për të gjitha features

### 5. **Portfolio Performance**
Cumulative Returns, Drawdown, Monthly Returns Heatmap

### 6. **Volume Analysis**
Trading Volume, Volume vs Price Change, Distribution

### 7. **Candlestick Charts**
OHLC Candlesticks + Line Charts (100 ditët e fundit)

### 8. **Statistical Distributions**
Box Plots dhe Violin Plots për distribucionestatistikore

### 9. **3D Surface Plot**
Çmimi vs Volume vs Koha (3D scatter)

### 10. **Risk-Return Scatter**
Risk-Return Analysis + Sharpe Ratio vjetore

### 11. **Cumulative Returns**
Long-term performance, YoY returns, Rolling 1-year returns

### 12. **Drawdown Analysis**
Maximum Drawdown, Underwater Chart, Risk Assessment

---

## 📁 STRUKTURA E PROJEKTIT

```
TokerrGjiki/
│
├── 📄 EKZEKUTO.bat                        ← KLIKO KËTU (launcher automatik)
├── 📄 EKZEKUTO.ps1                        ← PowerShell launcher
│
├── 🐍 gjenerues_dataset_financiar.py     ← Gjeneron 12 assets
├── 🐍 analiza_financiare_advanced.py     ← Kodi kryesor (650+ rreshta)
├── 🐍 vizualizime_moduli.py              ← Moduli i vizualizimeve (12+ figura)
├── 🐍 gjenerues_powerpoint.py            ← PowerPoint automatik
│
├── 📘 README_SHQIP.md                     ← Dokumentimi i plotë në SHQIP
├── 📘 UDHEZIME_EKZEKUTIM.md              ← Udhëzime hap-pas-hapi
├── 📘 PROJECT_SUMMARY.txt                 ← Përmbledhja e projektit
├── 📘 RUN_THIS.txt                        ← Quick start guide
├── 📘 NDRYSHIMET.txt                      ← Çfarë u ndryshua
│
├── 📁 .vscode/
│   ├── tasks.json                         ← Task të integruara (Ctrl+Shift+B)
│   └── settings.json                      ← Settings me GitHub sync
│
├── 📁 data_kaggle/
│   ├── financial_data.csv                 ← Dataset kryesor
│   ├── AAPL_historical_data.csv          ← Apple
│   ├── GOOGL_historical_data.csv         ← Google
│   ├── BTC_historical_data.csv           ← Bitcoin
│   └── ... (12 files gjithsej)
│
├── 📁 rezultatet_doktorature/             ← (krijohet automatikisht)
│   ├── 01_null_counting.csv
│   ├── 02_data_profiling.csv
│   ├── 03_monthly_aggregation.csv
│   ├── 04_yearly_aggregation.csv
│   └── 05_dataset_final_i_plote.csv
│
├── 📁 vizualizime_doktorature/            ← (krijohet automatikisht)
│   ├── 01_time_series_comprehensive.png
│   ├── 02_returns_distribution.png
│   ├── ... (12 PNG files)
│   └── 12_drawdown_analysis.png
│
└── 📁 prezantimi_powerpoint/              ← (krijohet automatikisht)
    ├── Prezantimi_Doktoral_Analiza_Financiare.pptx
    └── CustomizePowerPoint.vba
```

---

## 🔬 KONCEPTET SHKENCORE

### Big Data dhe MapReduce
Projekti përdor paradigmën MapReduce përmes PySpark për përpunimin e distribuuar të të dhënave në shkallë të madhe.

### Time Series Analysis
- **Lag Operations**: Autocorrelation analysis
- **Moving Averages**: Trend detection
- **Volatility Clustering**: Risk patterns

### Financial Mathematics
- **Return Formula**: `R_t = (P_t - P_{t-1}) / P_{t-1}`
- **Volatility Formula**: `σ = √(Σ(R_i - μ)² / (n-1))`
- **Sharpe Ratio**: `SR = (E[R] - R_f) / σ`
- **Annualization**: `σ_annual = σ_daily × √252`

### Statistical Computing
- Descriptive Statistics (mean, variance, stddev)
- Inferential Statistics (percentiles, quantiles)
- Distribution Analysis (skewness, kurtosis)

---

## 💻 EKZEKUTIMI NGA VS CODE TERMINAL

### Mënyra 1: Tasks (Më e shpejta)
1. Shtyp `Ctrl+Shift+P`
2. Shkruaj: "Tasks: Run Task"
3. Zgjidh një nga këto:
   - 🚀 EKZEKUTO PROJEKTIN E PLOTË
   - 📊 Gjenero Dataset-in Financiar
   - 🔬 Ekzekuto Analizën PySpark
   - 📽️ Gjenero PowerPoint Prezantimin
   - 📦 Instalo të gjitha librariitet

### Mënyra 2: Keyboard Shortcut
- Shtyp `Ctrl+Shift+B` → Ekzekuton projektin e plotë automatikisht

### Mënyra 3: Terminal Manual
```powershell
# Hap terminal të integruar: Ctrl + `
python gjenerues_dataset_financiar.py
python analiza_financiare_advanced.py
python gjenerues_powerpoint.py
```

---

## 📽️ POWERPOINT PREZANTIMI (AUTOMATIK)

Projekti gjeneron automatikisht një prezantim profesional PowerPoint me:

✅ **15+ Slides**:
- Titull dhe Hyrje
- Agjenda
- 10 Algoritmet e implementuara
- 12 Figura profesionale (të gjitha të integruara)
- Konkluzioni

✅ **VBA Macros** për customization:
- Apply professional theme
- Add animations
- Format text
- Add university logo
- Custom colors

✅ **Gati për Prezantim**:
- Format profesional
- Ngjyrat e universitetit
- Footer me numra faqesh
- Transition smooth

---

## 🏆 DALLIMET NGA PROJEKTI I VJETËR

| Aspekti | Para (❌) | Tani (✅) |
|---------|-----------|----------|
| **Niveli** | Shkolla fillore | Doktoraturë (PhD) |
| **Dataset** | Retail (i mërzitshëm) | Multi-Asset Financial (12 assets) |
| **Rreshta** | ~500K | 2,470 × 12 = 29,640+ |
| **Algoritme** | 0 nga profesori | TË GJITHA 10 algoritmet |
| **Kod** | ~150 rreshta bazike | 650+ rreshta PySpark |
| **Vizualizime** | 0 | 12+ figura profesionale |
| **PowerPoint** | ❌ Asnjë | ✅ Automatik me VBA |
| **Dokumentimi** | Minimal | Gjithëpërfshirës në SHQIP |
| **Terminal** | ❌ Jo | ✅ Integruar në VS Code |
| **GitHub** | ❌ Jo | ✅ Settings të sinkronizuara |

---

## ⚠️ ZGJIDHJA E PROBLEMEVE

### Problem: Python nuk gjendet
**Zgjidhja**:
1. Shkarkoni Python: https://www.python.org/downloads/
2. Gjatë instalimit: ✅ "Add Python to PATH"
3. Restart terminal

### Problem: Librariite mungojnë
**Zgjidhja**:
```powershell
python -m pip install pyspark pandas matplotlib seaborn numpy openpyxl python-pptx Pillow
```

### Problem: Java nuk është instaluar
**Zgjidhja**:
PySpark kërkon Java. Shkarkoni: https://www.java.com/download/

### Problem: Git needs configuration
**Zgjidhja**:
```bash
git config --global user.email "emri.juaj@email.com"
git config --global user.name "Emri Juaj"
```

---

## 📈 REZULTATET E PRITSHME

Pas ekzekutimit të suksesshëm:

```
================================================================================
✓✓✓ ANALIZA U PËRFUNDUA ME SUKSES ✓✓✓
================================================================================

Rezultatet:
  - rezultatet_doktorature/     5 CSV files
  - vizualizime_doktorature/    12 PNG figura
  - prezantimi_powerpoint/      1 PPTX file

Algoritmet e aplikuara:
  ✓ 1. Null Counting
  ✓ 2. Data Profiling
  ✓ 3. Percentile Approx
  ✓ 4. Returns Calculation
  ✓ 5. Moving Average
  ✓ 6. Volatility Computation
  ✓ 7. Lag Time Series
  ✓ 8. Window Functions
  ✓ 9. GroupBy Aggregation
  ✓ 10. STDDEV_SAMP

Vizualizime:
  ✓ 12 figura profesionale (300 DPI)
  ✓ PowerPoint prezantimi (15+ slides)

Total kohë ekzekutimi: ~5-10 minuta
================================================================================
```

---

## 🎓 NIVELI AKADEMIK

**Shkalla**: Doktoraturë (PhD)
**Fusha**: Computer Science - Big Data Analytics dhe Financial Computing
**Institucioni**: Universiteti i Prishtinës, Republika e Kosovës

### Teknologjitë:
- Apache Spark 3.x (Distributed Computing)
- PySpark SQL & DataFrame API
- Python 3.8+ (Scientific Computing)
- Pandas, NumPy (Data Science)
- Matplotlib, Seaborn (Advanced Visualization)
- PowerPoint Automation (python-pptx)

### Metodologjitë:
- MapReduce Programming
- Time Series Analysis
- Statistical Inference
- Financial Risk Management
- Portfolio Optimization

---

## ✅ LISTA E KONTROLLIT - A ËSHTË GJITHÇKA GATI?

- [x] Dataset Multi-Asset (12 instrumente financiare)
- [x] 2,470+ ditë tregtare (2015-2024)
- [x] Geometric Brownian Motion për çmime realiste
- [x] 10 Algoritme të profesorit (të gjitha)
- [x] 12+ Vizualizime profesionale (300 DPI)
- [x] PowerPoint automatik me VBA
- [x] Dokumentim i plotë në SHQIP
- [x] VS Code terminal integration
- [x] GitHub settings sync
- [x] Batch/PowerShell launchers
- [x] Error handling profesional
- [x] Logging i detajuar

---

## 🚀 FILLONI TANI

```bash
# Mënyra më e shpejtë:
1. Kliko dy herë: EKZEKUTO.bat

# Ose në VS Code:
2. Shtyp: Ctrl+Shift+B

# Ose manual:
3. python gjenerues_dataset_financiar.py
4. python analiza_financiare_advanced.py
5. python gjenerues_powerpoint.py
```

---

## 📞 MBËSHTETJE

Për pyetje:
1. Lexoni `UDHEZIME_EKZEKUTIM.md`
2. Kontrolloni `PROJECT_SUMMARY.txt`
3. Shikoni `NDRYSHIMET.txt` për ndryshimet

---

## 📜 LICENSA

**Përdorimi Akademik** - Për qëllime edukative dhe kërkimore.

---

<div align="center">

**FAKULTETI I SHKENCAVE KOMPJUTERIKE**

**UNIVERSITETI I PRISHTINËS**

**REPUBLIKA E KOSOVËS 🇽🇰**

---

### ✨ PROJEKTI I NIVELIT DOKTORAL ✨

*Excellence in Big Data and Financial Analytics*

---

**© 2024 | Të gjitha të drejtat e rezervuara për përdorim akademik**

</div>
