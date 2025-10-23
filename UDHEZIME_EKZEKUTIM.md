# UDHËZIME PËR EKZEKUTIM - PROJEKTI DOKTORATURË

## 🚨 TË RËNDËSISHME - LEXONI ME KUJDES

Ky projekt është i nivelit doktoral dhe përdor algoritme të sofistikuara të PySpark.

## HAPAT E EKZEKUTIMIT

### HAPI 1: Instalimi i Python dhe PySpark

Hapni PowerShell si Administrator dhe ekzekutoni:

```powershell
# Kontrollo nëse Python është i instaluar
python --version

# Nëse nuk është, shkarkoni nga: https://www.python.org/downloads/
# Gjatë instalimit, zgjidhni "Add Python to PATH"

# Instaloni libraritë e nevojshme
python -m pip install --upgrade pip
python -m pip install pyspark pandas matplotlib seaborn numpy openpyxl
```

### HAPI 2: Shkarkimi i Dataset-it Financiar

**OPSIONI A - Manual (Rekomandohet)**:

1. Shkoni në: https://www.kaggle.com/datasets
2. Kërkoni: "S&P 500 stock data" ose "stock market data"
3. Shkarkoni një dataset CSV me kolona: Date, Open, High, Low, Close, Volume
4. Vendoseni në: `c:\Users\Administrator\TokerrGjiki\data_kaggle\financial_data.csv`

**OPSIONI B - Yahoo Finance (Kërkon Internet)**:

```powershell
# Instaloni yfinance
python -m pip install yfinance

# Ekzekutoni skriptin e shkarkimit
python download_financial_data.py
```

**OPSIONI C - Përdorni Dataset-in e Gjeneruar**:

Nëse Python nuk punon, unë kam krijuar një dataset shembull. Por për rezultate më të mira, përdorni të dhëna reale.

```powershell
# Krijoni dataset-in e simuluar
python create_financial_dataset.py
```

### HAPI 3: Ekzekutimi i Analizës Kryesore

```powershell
# Sigurohuni që jeni në direktorinë e projektit
cd c:\Users\Administrator\TokerrGjiki

# Ekzekutoni projektin kryesor
python analiza_financiare_advanced.py
```

### HAPI 4: Shikimi i Rezultateve

Pas ekzekutimit të suksesshëm, do të krijohen:

**Rezultatet CSV**:
- `rezultatet_doktorature/01_null_counting.csv`
- `rezultatet_doktorature/02_data_profiling.csv`
- `rezultatet_doktorature/03_monthly_aggregation.csv`
- `rezultatet_doktorature/04_yearly_aggregation.csv`
- `rezultatet_doktorature/05_dataset_final_i_plote.csv`

**Vizualizimet PNG**:
- `vizualizime_doktorature/01_time_series_analysis.png`
- `vizualizime_doktorature/02_volatility_analysis.png`
- `vizualizime_doktorature/03_volume_analysis.png`
- `vizualizime_doktorature/04_statistical_distribution.png`

## 🔧 ZGJIDHJA E PROBLEMEVE

### Problemi: "Python was not found"

**Zgjidhja**:
1. Shkarkoni Python nga: https://www.python.org/downloads/
2. Gjatë instalimit, **patjetër zgjidhni "Add Python to PATH"**
3. Mbyllni dhe rihapni PowerShell
4. Testoni: `python --version`

### Problemi: "pip is not recognized"

**Zgjidhja**:
```powershell
# Përdorni python -m pip në vend të pip
python -m pip install pyspark
```

### Problemi: "No module named 'pyspark'"

**Zgjidhja**:
```powershell
# Instaloni PySpark
python -m pip install pyspark
```

### Problemi: "File not found: financial_data.csv"

**Zgjidhja**:
1. Sigurohuni që file ekziston në: `data_kaggle/financial_data.csv`
2. Ose krijoni direktorinë:
```powershell
mkdir data_kaggle
```
3. Shkarkoni një dataset CSV financiar dhe vendoseni atje

### Problemi: "Java is not installed"

**Zgjidhja**:
PySpark kërkon Java. Shkarkoni nga: https://www.java.com/download/

## 📊 PËRSHKRIMI I ALGORITMEVE

Projekti implementon 10 algoritme të avancuara:

1. **NULL COUNTING** ✓
2. **DATA PROFILING** ✓
3. **PERCENTILE_APPROX** ✓
4. **RETURNS CALCULATION** ✓
5. **LAG TIME SERIES** ✓
6. **MOVING AVERAGE** ✓
7. **VOLATILITY COMPUTATION** ✓
8. **GROUPBY AGGREGATION** ✓
9. **WINDOW FUNCTIONS** ✓
10. **STDDEV_SAMP** ✓

Të gjitha këto algoritme janë ato që keni mësuar me profesorin tuaj!

## 🎯 REZULTATET E PRITSHME

Pas ekzekutimit të suksesshëm, do të shihni:

```
================================================================================
✓✓✓ ANALIZA U PËRFUNDUA ME SUKSES ✓✓✓
================================================================================

Rezultatet:
  - rezultatet_doktorature/: Të gjitha CSV files
  - vizualizime_doktorature/: Të gjitha figurat

Algoritmet e aplikuara me sukses:
  ✓ Null Counting
  ✓ Data Profiling
  ✓ Percentile Approx
  ✓ Returns Calculation
  ✓ Moving Average (7d, 30d, 90d)
  ✓ Volatility Computation
  ✓ Lag Time Series
  ✓ Window Functions
  ✓ GroupBy Aggregation
================================================================================
```

## 💪 KARAKTERISTIKAT E PROJEKTIT

- ✅ **Niveli Doktoral**: Algoritme të sofistikuara dhe analiza e thellë
- ✅ **Big Data**: Përdor PySpark për përpunimin e distribuuar
- ✅ **Financiare**: Analiza reale e tregut financiar
- ✅ **Vizualizime Profesionale**: Figura të gatshme për prezantime
- ✅ **Dokumentim i Plotë**: Gjithçka në gjuhën shqipe
- ✅ **Kod i Pastër**: Best practices të programimit

## 📞 NDIHMË SHTESË

Nëse hasni në probleme:

1. Lexoni me kujdes mesazhet e gabimit
2. Kontrolloni që Python është i instaluar korrekt
3. Sigurohuni që të gjitha libraritë janë të instaluara
4. Verifikoni që dataset-i është në vendin e duhur

## 🏆 SUKSESE!

Ky projekt është i nivelit më të lartë dhe përmban të gjitha algoritmet që profesori juaj ka mësuar. Përdoreni me krenari për studimet tuaja doktorale!

**Fakulteti i Shkencave Kompjuterike**
**Universiteti i Prishtinës**
**Republika e Kosovës 🇽🇰**
