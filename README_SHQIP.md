# ANALIZA E AVANCUAR FINANCIARE - PROJEKTI DOKTORATURË

**Universiteti i Prishtinës, Republika e Kosovës**

## 📚 PËRSHKRIMI I PROJEKTIT

Ky është një projekt i nivelit doktoral që përdor **Apache PySpark** për analizë të sofistikuar financiare. Projekti implementon të gjitha algoritmet e avancuara që keni mësuar me profesorin tuaj.

## 🎓 ALGORITMET E IMPLEMENTUARA

### 1. **NULL COUNTING** - Analiza e Plotësisë së Të Dhënave
Identifikon dhe numëron vlerat që mungojnë në dataset për çdo kolonë. Llogarit përqindjen e plotësisë së të dhënave.

**Aplikimi**: Siguron cilësinë e të dhënave para analizës së mëtejshme.

### 2. **DATA PROFILING** - Vlerësimi Gjithëpërfshirës
Statistika të detajuara për çdo kolonë numerike:
- Minimum, Maximum, Mean (Mesatarja)
- Standard Deviation (Devijimi Standard)
- Variance (Varianca)
- Skewness (Asimetria)
- Kurtosis (Kuroziteti)

**Aplikimi**: Kuptimi i shpërndarjes dhe karakteristikave të të dhënave.

### 3. **PERCENTILE_APPROX** - Llogaritja e Kuantileve
Llogarit kuantilet e përafërta (P25, P50/Median, P75, P95, P99).

**Aplikimi**: Identifikimi i vlerave ekstreme dhe shpërndarjes së të dhënave.

### 4. **RETURNS CALCULATION** - Llogaritja e Rendimenteve
Llogarit rendimentet financiare:
- **Daily Return**: Rendimenti ditor `((Price_today - Price_yesterday) / Price_yesterday) * 100`
- **Weekly Return**: Rendimenti 7-ditor
- **Monthly Return**: Rendimenti 30-ditor

**Aplikimi**: Matja e performancës financiare dhe fitimeve/humbjeve.

### 5. **LAG** - Operacione të Serive Kohore
Përdor funksionin `lag()` për të krahasuar vlerat aktuale me vlerat e periudhave të mëparshme (1 ditë, 5 ditë, 10 ditë, 20 ditë më parë).

**Aplikimi**: Analiza e trendeve dhe modeleve temporale.

### 6. **MOVING AVERAGE** - Mesataret Lëvizëse
Llogarit mesataret lëvizëse duke përdorur window functions:
- **MA 7-ditore**: Mesatarja e 7 ditëve të fundit
- **MA 30-ditore**: Mesatarja e 30 ditëve të fundit
- **MA 90-ditore**: Mesatarja e 90 ditëve të fundit

**Aplikimi**: Smoothing i të dhënave, identifikimi i trendeve afatgjata.

### 7. **GROUPBY AGGREGATION** - Agregimet MapReduce
Agregime komplekse sipas kohës (mujore, vjetore):
- Mesatarja, Min, Max e çmimeve
- Totali i volumit të tregtimit
- Numri i ditëve të tregtimit
- Volatiliteti mujor/vjetor

**Aplikimi**: Analizë e performancës në periudha të ndryshme kohore.

### 8. **WINDOW FUNCTIONS** - Funksione Analitike të Dritareve
Implementon funksione të avancuara të dritareve:
- `rank()`: Renditja e vlerave
- `dense_rank()`: Renditja pa zbrazëtira
- `percent_rank()`: Renditja përqindsore
- `ntile()`: Ndarja në kuantile

**Aplikimi**: Identifikimi i pozitave relative të vlerave në dataset.

### 9. **STDDEV_SAMP** - Devijimi Standard i Mostrave
Llogarit devijimin standard të mostrave për të matur shpërndarjen e të dhënave.

**Aplikimi**: Pjesë integrale e analizës së volatilitetit.

### 10. **VOLATILITY COMPUTATION** - Matja e Rrezikut
Llogarit volatilitetin financiar:
- **Historical Volatility**: Volatiliteti historik (stddev e rendimenteve ditore)
- **Annualized Volatility**: Volatiliteti vjetor = Daily_Vol × √252
- **Rolling Volatility**: Volatiliteti lëvizës 30-ditor

**Aplikimi**: Matja e rrezikut të investimit, planifikimi i strategjive.

## 📊 DATASET-I

**Emri**: Financial Market Data (S&P 500 / Tech Stocks)
**Periudha**: 2015-01-01 deri 2024-10-22
**Format**: CSV me kolona: Date, Open, High, Low, Close, Volume

## 🚀 SI TË EKZEKUTONI PROJEKTIN

### Hapi 1: Instalimi i Dependency-ve

```powershell
pip install pyspark pandas matplotlib seaborn numpy
```

### Hapi 2: Shkarkimi i Dataset-it

Shkarkoni të dhënat financiare nga:
- **Yahoo Finance**: https://finance.yahoo.com/
- **Kaggle**: https://www.kaggle.com/datasets (S&P 500, Stock Market Data)
- **Alpha Vantage**: https://www.alphavantage.co/

Vendosni file CSV në: `data_kaggle/financial_data.csv`

**Formati i Kërkuar**:
```
Date,Open,High,Low,Close,Volume
2015-01-02,2058.90,2072.36,2046.04,2058.20,3539500000
...
```

### Hapi 3: Ekzekutimi i Skriptit

```powershell
python analiza_financiare_advanced.py
```

## 📂 OUTPUTET

### Rezultatet (CSV Files):
- `rezultatet_doktorature/01_null_counting.csv` - Analiza e vlerave NULL
- `rezultatet_doktorature/02_data_profiling.csv` - Profilimi i plotë i të dhënave
- `rezultatet_doktorature/03_monthly_aggregation.csv` - Agregimi mujor
- `rezultatet_doktorature/04_yearly_aggregation.csv` - Agregimi vjetor
- `rezultatet_doktorature/05_dataset_final_i_plote.csv` - Dataset-i final me të gjitha kolonat

### Vizualizimet (PNG Files):
- `vizualizime_doktorature/01_time_series_analysis.png` - Analiza e serive kohore
- `vizualizime_doktorature/02_volatility_analysis.png` - Analiza e volatilitetit
- `vizualizime_doktorature/03_volume_analysis.png` - Analiza e volumit
- `vizualizime_doktorature/04_statistical_distribution.png` - Shpërndarja statistikore

## 🔬 KONCEPTET TEORIKE

### MapReduce dhe Big Data
Projekti përdor paradigmën MapReduce përmes `groupBy()` dhe funksioneve të agregimit, duke mundësuar përpunimin e distribuuar të të dhënave në shkallë të madhe.

### Time Series Analysis
Analizon të dhënat e serive kohore duke përdorur:
- Lag operations për auto-correlation
- Moving averages për trend detection
- Volatility për risk assessment

### Statistical Computing
Implementon algoritme statistikore:
- Descriptive statistics (mean, stddev, variance)
- Inferential statistics (percentiles, quartiles)
- Distribution analysis (skewness, kurtosis)

### Financial Mathematics
Aplikon formula financiare:
- Return calculation: `R = (P_t - P_{t-1}) / P_{t-1}`
- Volatility: `σ = √(Σ(R_i - μ)² / n-1)`
- Annualization: `σ_annual = σ_daily × √252`

## 💡 SHEMBUJ TË KODIT

### Llogaritja e Rendimenteve me LAG:
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import lag, col

window_spec = Window.orderBy('Date')
df = df.withColumn('Previous_Price', lag(col('Close'), 1).over(window_spec))
df = df.withColumn('Daily_Return', 
                   ((col('Close') - col('Previous_Price')) / col('Previous_Price')) * 100)
```

### Mesatarja Lëvizëse me Window Functions:
```python
window_30d = Window.orderBy('Date').rowsBetween(-29, 0)
df = df.withColumn('MA_30d', avg(col('Close')).over(window_30d))
```

### Volatiliteti me STDDEV_SAMP:
```python
volatility = df.select(stddev_samp(col('Daily_Return'))).collect()[0][0]
annual_volatility = volatility * sqrt(252)
```

## 📖 REFERENCAT

1. **Apache Spark Documentation**: https://spark.apache.org/docs/latest/
2. **PySpark SQL Module**: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql.html
3. **Financial Time Series Analysis**: Tsay, R. S. (2010)
4. **Quantitative Finance**: Hull, J. C. (2018) - Options, Futures, and Other Derivatives

## 👨‍🎓 KONTRIBUTI

**Niveli**: Doktoraturë
**Fushë**: Big Data Analytics, Financial Computing, Time Series Analysis
**Teknologjitë**: PySpark, Python, SQL, MapReduce

## 📝 SHËNIME PËR STUDENTËT

1. **Kuptimi i Algoritmeve**: Lexoni kodin me kujdes dhe kuptoni logjikën pas çdo algoritmi.

2. **Dataset Real**: Përdorni të dhëna reale financiare për rezultate më të mira.

3. **Interpretimi**: Analizoni rezultatet dhe nxirrni përfundime të bazuara në statistika.

4. **Saktësia**: Projekti përdor algoritme të sakta dhe eficiente për dataset të mëdhenj.

5. **Vizualizimet**: Figurat janë në nivel profesional dhe mund të përdoren në prezantime.

## ⚠️ KUJDES

- Sigurohuni që PySpark është i instaluar korrekt
- Dataset-i duhet të jetë në formatin e saktë CSV
- Projekti kërkon së paku 4GB RAM për ekzekutim
- Rezultatet ruhen automatikisht në direktoritë e specifikuara

## ✅ LISTA E KONTROLLIT

- [x] Null Counting - Analiza e plotësisë së të dhënave
- [x] Data Profiling - Statistika përshkruese të plota
- [x] Percentile Approx - Kuantilet (P25, P50, P75, P95, P99)
- [x] Returns Calculation - Rendimentet ditore, javore, mujore
- [x] Lag Operations - Time series lag për 1, 5, 10, 20 ditë
- [x] Moving Averages - MA 7d, 30d, 90d
- [x] Volatility Computation - Historical dhe rolling volatility
- [x] GroupBy Aggregation - Agregime mujore dhe vjetore
- [x] Window Functions - Rank, dense_rank, percent_rank, ntile
- [x] Vizualizime të Avancuara - 4 figura profesionale

---

**Përgatiti**: Projekti i analizës financiare të avancuar
**Data**: Tetor 2024
**Qëllimi**: Edukimi doktoral në Big Data dhe Financial Analytics

**Suksese në studimet tuaja doktorale! 🎓**
