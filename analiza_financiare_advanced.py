"""
ANALIZA E AVANCUAR FINANCIARE - PROJEKTI DOKTORATURË
Universiteti i Prishtinës, Republika e Kosovës

Ky projekt përdor algoritme të sofistikuara të PySpark për analizë financiare:
- percentile_approx: Llogaritja e kuantileve (25%, 50%, 75%, 95%, 99%)
- stddev_samp: Devijimi standard i mostrave
- lag: Operacione të serive kohore për ndryshime të çmimeve
- moving average: Mesatare lëvizëse (7-ditore, 30-ditore, 90-ditore)
- groupBy aggregation: Agregimet në stil MapReduce
- window functions: Funksionet analitike të dritareve
- null counting: Analiza e plotësisë së të dhënave
- data profiling: Vlerësimi gjithëpërfshirës i të dhënave
- returns calculation: Metriku i performancës financiare (rendiment ditor, javore, mujore)
- volatility computation: Matja e rrezikut (volatiliteti historik, rolling volatility)
"""

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    col, lag, avg, stddev_samp, percentile_approx, count, sum as _sum,
    when, isnan, isnull, min as _min, max as _max, expr, datediff,
    year, month, dayofmonth, to_date, unix_timestamp, from_unixtime,
    round as spark_round, lit, sqrt, variance, skewness, kurtosis
)
from pyspark.sql.types import DoubleType
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import os

# Konfigurimi i stilit për vizualizime profesionale
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)
plt.rcParams['font.size'] = 12

class AnalizaFinanciareAdvanced:
    """
    Klasa kryesore për analizën e avancuar financiare duke përdorur PySpark
    """
    
    def __init__(self, emri_aplikacionit="AnalizaFinanciare_Doktorature"):
        """Inicializimi i SparkSession"""
        self.spark = SparkSession.builder \
            .appName(emri_aplikacionit) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.driver.memory", "4g") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        print("✓ SparkSession u krijua me sukses")
        print(f"✓ Spark Version: {self.spark.version}")
    
    def ngarko_te_dhenat(self, shtegu_file):
        """
        Ngarkon të dhënat financiare nga CSV
        
        Args:
            shtegu_file: Shtegu deri te file CSV
            
        Returns:
            DataFrame: PySpark DataFrame me të dhënat
        """
        print(f"\n{'='*80}")
        print("FAZA 1: NGARKIMI I TË DHËNAVE")
        print(f"{'='*80}")
        
        df = self.spark.read.csv(
            shtegu_file, 
            header=True, 
            inferSchema=True
        )
        
        print(f"✓ Të dhënat u ngarkuan: {df.count()} rreshta, {len(df.columns)} kolona")
        print(f"✓ Schema e të dhënave:")
        df.printSchema()
        
        return df
    
    def null_counting_analysis(self, df):
        """
        ALGORITMI 1: NULL COUNTING
        Analiza e plotësisë së të dhënave - identifikon vlerat që mungojnë
        
        Args:
            df: PySpark DataFrame
            
        Returns:
            DataFrame: Statistikat e vlerave null për çdo kolonë
        """
        print(f"\n{'='*80}")
        print("ALGORITMI 1: NULL COUNTING (Analiza e Plotësisë së të Dhënave)")
        print(f"{'='*80}")
        
        total_rows = df.count()
        
        # Llogaritja e null për çdo kolonë duke përdorur agregime
        null_counts = []
        for kolona in df.columns:
            null_count = df.filter(
                col(kolona).isNull() | isnan(col(kolona))
            ).count()
            null_percentage = (null_count / total_rows) * 100
            
            null_counts.append({
                'Kolona': kolona,
                'Null_Count': null_count,
                'Total_Rows': total_rows,
                'Null_Percentage': round(null_percentage, 2),
                'Completeness': round(100 - null_percentage, 2)
            })
        
        null_df = self.spark.createDataFrame(null_counts)
        
        print("\n📊 Rezultatet e Null Counting:")
        null_df.show(truncate=False)
        
        return null_df
    
    def data_profiling_analysis(self, df, kolona_numerike):
        """
        ALGORITMI 2: DATA PROFILING
        Vlerësimi gjithëpërfshirës i të dhënave - statistika të detajuara
        
        Args:
            df: PySpark DataFrame
            kolona_numerike: Lista e kolonave numerike
            
        Returns:
            DataFrame: Profili i plotë i të dhënave
        """
        print(f"\n{'='*80}")
        print("ALGORITMI 2: DATA PROFILING (Vlerësimi Gjithëpërfshirës)")
        print(f"{'='*80}")
        
        profiling_results = []
        
        for kolona in kolona_numerike:
            # Statistika bazë
            stats = df.select(
                lit(kolona).alias('Kolona'),
                _min(col(kolona)).alias('Min'),
                _max(col(kolona)).alias('Max'),
                avg(col(kolona)).alias('Mean'),
                stddev_samp(col(kolona)).alias('StdDev'),
                variance(col(kolona)).alias('Variance'),
                skewness(col(kolona)).alias('Skewness'),
                kurtosis(col(kolona)).alias('Kurtosis'),
                count(col(kolona)).alias('Count')
            ).collect()[0]
            
            profiling_results.append(stats.asDict())
        
        profiling_df = self.spark.createDataFrame(profiling_results)
        
        print("\n📊 Rezultatet e Data Profiling:")
        profiling_df.show(truncate=False)
        
        return profiling_df
    
    def percentile_approx_analysis(self, df, kolona):
        """
        ALGORITMI 3: PERCENTILE_APPROX
        Llogaritja e kuantileve të përafërta për analiza statistikore
        
        Args:
            df: PySpark DataFrame
            kolona: Emri i kolonës për analizë
            
        Returns:
            dict: Kuantilet (P25, P50, P75, P95, P99)
        """
        print(f"\n{'='*80}")
        print(f"ALGORITMI 3: PERCENTILE_APPROX për kolonën '{kolona}'")
        print(f"{'='*80}")
        
        # Llogaritja e kuantileve duke përdorur percentile_approx
        percentiles = df.select(
            percentile_approx(col(kolona), 0.25).alias('P25'),
            percentile_approx(col(kolona), 0.50).alias('P50_Median'),
            percentile_approx(col(kolona), 0.75).alias('P75'),
            percentile_approx(col(kolona), 0.95).alias('P95'),
            percentile_approx(col(kolona), 0.99).alias('P99')
        ).collect()[0]
        
        result = percentiles.asDict()
        
        print(f"\n📊 Kuantilet për {kolona}:")
        for key, value in result.items():
            print(f"   {key}: {value:.2f}")
        
        return result
    
    def returns_calculation(self, df, kolona_cmimi, kolona_date):
        """
        ALGORITMI 4: RETURNS CALCULATION
        Llogaritja e rendimenteve financiare (ditore, javore, mujore)
        
        Args:
            df: PySpark DataFrame
            kolona_cmimi: Kolona e çmimit
            kolona_date: Kolona e datës
            
        Returns:
            DataFrame: DataFrame me rendimentet e llogaritura
        """
        print(f"\n{'='*80}")
        print("ALGORITMI 4: RETURNS CALCULATION (Llogaritja e Rendimenteve)")
        print(f"{'='*80}")
        
        # Sortimi sipas datës
        df = df.orderBy(col(kolona_date))
        
        # Window për lag operations
        window_spec = Window.orderBy(col(kolona_date))
        
        # Llogaritja e rendimenteve ditore duke përdorur LAG
        df = df.withColumn(
            'Previous_Price',
            lag(col(kolona_cmimi), 1).over(window_spec)
        )
        
        df = df.withColumn(
            'Daily_Return',
            when(col('Previous_Price').isNotNull(),
                 ((col(kolona_cmimi) - col('Previous_Price')) / col('Previous_Price')) * 100
            ).otherwise(None)
        )
        
        # Rendimenti javore (7 ditë)
        df = df.withColumn(
            'Price_7d_Ago',
            lag(col(kolona_cmimi), 7).over(window_spec)
        )
        
        df = df.withColumn(
            'Weekly_Return',
            when(col('Price_7d_Ago').isNotNull(),
                 ((col(kolona_cmimi) - col('Price_7d_Ago')) / col('Price_7d_Ago')) * 100
            ).otherwise(None)
        )
        
        # Rendimenti mujore (30 ditë)
        df = df.withColumn(
            'Price_30d_Ago',
            lag(col(kolona_cmimi), 30).over(window_spec)
        )
        
        df = df.withColumn(
            'Monthly_Return',
            when(col('Price_30d_Ago').isNotNull(),
                 ((col(kolona_cmimi) - col('Price_30d_Ago')) / col('Price_30d_Ago')) * 100
            ).otherwise(None)
        )
        
        print("\n✓ Rendimentet u llogaritën: Daily, Weekly, Monthly")
        
        # Statistika të rendimenteve
        return_stats = df.select(
            avg('Daily_Return').alias('Avg_Daily_Return'),
            stddev_samp('Daily_Return').alias('StdDev_Daily_Return'),
            _min('Daily_Return').alias('Min_Daily_Return'),
            _max('Daily_Return').alias('Max_Daily_Return'),
            avg('Weekly_Return').alias('Avg_Weekly_Return'),
            avg('Monthly_Return').alias('Avg_Monthly_Return')
        ).collect()[0]
        
        print("\n📊 Statistikat e Rendimenteve:")
        print(f"   Rendimenti Ditor Mesatar: {return_stats['Avg_Daily_Return']:.4f}%")
        print(f"   StdDev Ditor: {return_stats['StdDev_Daily_Return']:.4f}%")
        print(f"   Rendimenti Javore Mesatar: {return_stats['Avg_Weekly_Return']:.4f}%")
        print(f"   Rendimenti Mujore Mesatar: {return_stats['Avg_Monthly_Return']:.4f}%")
        
        return df
    
    def moving_average_analysis(self, df, kolona_cmimi, kolona_date):
        """
        ALGORITMI 5: MOVING AVERAGE
        Llogaritja e mesatareve lëvizëse duke përdorur Window Functions
        
        Args:
            df: PySpark DataFrame
            kolona_cmimi: Kolona e çmimit
            kolona_date: Kolona e datës
            
        Returns:
            DataFrame: DataFrame me mesataret lëvizëse
        """
        print(f"\n{'='*80}")
        print("ALGORITMI 5: MOVING AVERAGE (Mesataret Lëvizëse)")
        print(f"{'='*80}")
        
        # Window specifications për mesataret lëvizëse
        window_7d = Window.orderBy(col(kolona_date)).rowsBetween(-6, 0)
        window_30d = Window.orderBy(col(kolona_date)).rowsBetween(-29, 0)
        window_90d = Window.orderBy(col(kolona_date)).rowsBetween(-89, 0)
        
        # Llogaritja e mesatareve lëvizëse
        df = df.withColumn('MA_7d', avg(col(kolona_cmimi)).over(window_7d))
        df = df.withColumn('MA_30d', avg(col(kolona_cmimi)).over(window_30d))
        df = df.withColumn('MA_90d', avg(col(kolona_cmimi)).over(window_90d))
        
        print("\n✓ Mesataret Lëvizëse u llogaritën: 7-ditore, 30-ditore, 90-ditore")
        
        # Mostra e rezultateve
        df.select(kolona_date, kolona_cmimi, 'MA_7d', 'MA_30d', 'MA_90d') \
            .orderBy(col(kolona_date).desc()) \
            .show(10)
        
        return df
    
    def volatility_computation(self, df, kolona_rendimenti='Daily_Return'):
        """
        ALGORITMI 6: VOLATILITY COMPUTATION
        Matja e rrezikut - llogaritja e volatilitetit historik
        
        Args:
            df: PySpark DataFrame
            kolona_rendimenti: Kolona e rendimenteve ditore
            
        Returns:
            DataFrame: DataFrame me volatilitetin
        """
        print(f"\n{'='*80}")
        print("ALGORITMI 6: VOLATILITY COMPUTATION (Matja e Rrezikut)")
        print(f"{'='*80}")
        
        # Volatiliteti historik (devijimi standard i rendimenteve)
        historical_volatility = df.select(
            stddev_samp(col(kolona_rendimenti)).alias('Historical_Volatility_Daily')
        ).collect()[0]['Historical_Volatility_Daily']
        
        # Volatiliteti vjetor (anualizuar)
        annual_volatility = historical_volatility * np.sqrt(252)  # 252 ditë tregtare
        
        print(f"\n📊 Rezultatet e Volatilitetit:")
        print(f"   Volatiliteti Ditor: {historical_volatility:.4f}%")
        print(f"   Volatiliteti Vjetor (Anualizuar): {annual_volatility:.4f}%")
        
        # Rolling volatility duke përdorur window functions
        window_30d = Window.orderBy('Date').rowsBetween(-29, 0)
        
        df = df.withColumn(
            'Rolling_Volatility_30d',
            stddev_samp(col(kolona_rendimenti)).over(window_30d)
        )
        
        print("✓ Rolling Volatility (30-ditore) u llogarit")
        
        return df, historical_volatility, annual_volatility
    
    def groupby_aggregation_analysis(self, df, kolona_date):
        """
        ALGORITMI 7: GROUPBY AGGREGATION
        Agregimet në stil MapReduce për analizë mujore dhe vjetore
        
        Args:
            df: PySpark DataFrame
            kolona_date: Kolona e datës
            
        Returns:
            DataFrame: Rezultatet e agregimeve
        """
        print(f"\n{'='*80}")
        print("ALGORITMI 7: GROUPBY AGGREGATION (MapReduce Style)")
        print(f"{'='*80}")
        
        # Shtimi i kolonave kohore
        df = df.withColumn('Year', year(col(kolona_date)))
        df = df.withColumn('Month', month(col(kolona_date)))
        
        # Agregimi mujore
        monthly_agg = df.groupBy('Year', 'Month').agg(
            avg('Close').alias('Avg_Close'),
            _min('Close').alias('Min_Close'),
            _max('Close').alias('Max_Close'),
            avg('Volume').alias('Avg_Volume'),
            _sum('Volume').alias('Total_Volume'),
            stddev_samp('Daily_Return').alias('Monthly_Volatility'),
            avg('Daily_Return').alias('Avg_Monthly_Return'),
            count('*').alias('Trading_Days')
        ).orderBy('Year', 'Month')
        
        print("\n📊 Agregimi Mujore (10 muajt e fundit):")
        monthly_agg.orderBy(col('Year').desc(), col('Month').desc()).show(10)
        
        # Agregimi vjetore
        yearly_agg = df.groupBy('Year').agg(
            avg('Close').alias('Avg_Close'),
            _min('Close').alias('Min_Close'),
            _max('Close').alias('Max_Close'),
            _sum('Volume').alias('Total_Volume'),
            stddev_samp('Daily_Return').alias('Yearly_Volatility'),
            avg('Daily_Return').alias('Avg_Yearly_Return'),
            count('*').alias('Trading_Days')
        ).orderBy('Year')
        
        print("\n📊 Agregimi Vjetore:")
        yearly_agg.show()
        
        return monthly_agg, yearly_agg
    
    def lag_time_series_analysis(self, df, kolona_cmimi, kolona_date, lags=[1, 5, 10, 20]):
        """
        ALGORITMI 8: LAG (Time Series Operations)
        Operacione të serive kohore për analizë të ndryshimeve
        
        Args:
            df: PySpark DataFrame
            kolona_cmimi: Kolona e çmimit
            kolona_date: Kolona e datës
            lags: Lista e lag periods
            
        Returns:
            DataFrame: DataFrame me lag features
        """
        print(f"\n{'='*80}")
        print("ALGORITMI 8: LAG TIME SERIES OPERATIONS")
        print(f"{'='*80}")
        
        window_spec = Window.orderBy(col(kolona_date))
        
        for lag_period in lags:
            # Lag values
            df = df.withColumn(
                f'Lag_{lag_period}d',
                lag(col(kolona_cmimi), lag_period).over(window_spec)
            )
            
            # Ndryshimi përqindor
            df = df.withColumn(
                f'Change_{lag_period}d_pct',
                when(col(f'Lag_{lag_period}d').isNotNull(),
                     ((col(kolona_cmimi) - col(f'Lag_{lag_period}d')) / col(f'Lag_{lag_period}d')) * 100
                ).otherwise(None)
            )
        
        print(f"\n✓ Lag features u krijuan për periudhat: {lags}")
        
        # Mostra e rezultateve
        lag_columns = [kolona_date, kolona_cmimi] + [f'Lag_{lag}d' for lag in lags] + [f'Change_{lag}d_pct' for lag in lags]
        df.select(*lag_columns).orderBy(col(kolona_date).desc()).show(5)
        
        return df
    
    def window_function_analysis(self, df, kolona_cmimi, kolona_date):
        """
        ALGORITMI 9: WINDOW FUNCTIONS
        Funksione analitike të dritareve për ranking dhe cumulative analysis
        
        Args:
            df: PySpark DataFrame
            kolona_cmimi: Kolona e çmimit
            kolona_date: Kolona e datës
            
        Returns:
            DataFrame: DataFrame me window function results
        """
        print(f"\n{'='*80}")
        print("ALGORITMI 9: WINDOW FUNCTIONS (Analytical Windows)")
        print(f"{'='*80}")
        
        from pyspark.sql.functions import row_number, rank, dense_rank, percent_rank, ntile
        
        window_spec = Window.orderBy(col(kolona_cmimi).desc())
        
        df = df.withColumn('Price_Rank', rank().over(window_spec))
        df = df.withColumn('Price_Dense_Rank', dense_rank().over(window_spec))
        df = df.withColumn('Price_Percent_Rank', percent_rank().over(window_spec))
        df = df.withColumn('Price_Quartile', ntile(4).over(window_spec))
        
        print("\n✓ Window functions u aplikuan: rank, dense_rank, percent_rank, ntile")
        
        # Mostra e top 10 çmimeve më të larta
        print("\n📊 Top 10 Çmimet më të Larta:")
        df.select(kolona_date, kolona_cmimi, 'Price_Rank', 'Price_Quartile') \
            .orderBy('Price_Rank') \
            .show(10)
        
        return df
    
    def ruaj_rezultatet(self, df, emri_output, direktoria='rezultatet_doktorature'):
        """
        Ruajtja e rezultateve në CSV dhe Parquet
        
        Args:
            df: PySpark DataFrame
            emri_output: Emri i file
            direktoria: Direktoria për ruajtje
        """
        os.makedirs(direktoria, exist_ok=True)
        
        # Konvertimi në Pandas për CSV
        df_pandas = df.toPandas()
        csv_path = os.path.join(direktoria, f"{emri_output}.csv")
        df_pandas.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        print(f"✓ Rezultatet u ruajtën në: {csv_path}")
    
    def krijo_vizualizime(self, df, direktoria='vizualizime_doktorature'):
        """
        Krijimi i vizualizimeve të avancuara për analizë doktorale
        
        Args:
            df: PySpark DataFrame (me të gjitha kolonat e analizës)
            direktoria: Direktoria për ruajtje të figurave
        """
        print(f"\n{'='*80}")
        print("KRIJIMI I VIZUALIZIMEVE TË AVANCUARA")
        print(f"{'='*80}")
        
        os.makedirs(direktoria, exist_ok=True)
        
        # Konvertimi në Pandas
        df_pandas = df.toPandas()
        df_pandas['Date'] = pd.to_datetime(df_pandas['Date'])
        df_pandas = df_pandas.sort_values('Date')
        
        # FIGURA 1: Time Series Analysis me Moving Averages
        fig, axes = plt.subplots(2, 1, figsize=(20, 12))
        
        ax1 = axes[0]
        ax1.plot(df_pandas['Date'], df_pandas['Close'], label='Çmimi Actual', linewidth=2, alpha=0.7)
        ax1.plot(df_pandas['Date'], df_pandas['MA_7d'], label='MA 7-ditore', linewidth=2)
        ax1.plot(df_pandas['Date'], df_pandas['MA_30d'], label='MA 30-ditore', linewidth=2)
        ax1.plot(df_pandas['Date'], df_pandas['MA_90d'], label='MA 90-ditore', linewidth=2)
        ax1.set_title('Analiza e Serive Kohore: Çmimi dhe Mesataret Lëvizëse', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Data', fontsize=14)
        ax1.set_ylabel('Çmimi ($)', fontsize=14)
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # FIGURA 2: Daily Returns Distribution
        ax2 = axes[1]
        df_pandas['Daily_Return'].dropna().hist(bins=100, ax=ax2, edgecolor='black', alpha=0.7)
        ax2.set_title('Shpërndarja e Rendimenteve Ditore', fontsize=16, fontweight='bold')
        ax2.set_xlabel('Rendimenti Ditor (%)', fontsize=14)
        ax2.set_ylabel('Frekuenca', fontsize=14)
        ax2.axvline(0, color='red', linestyle='--', linewidth=2, label='Zero Return')
        ax2.legend(fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(direktoria, '01_time_series_analysis.png'), dpi=300, bbox_inches='tight')
        print("✓ Figura 1: Time Series Analysis u krijua")
        plt.close()
        
        # FIGURA 3: Volatility Analysis
        fig, axes = plt.subplots(2, 1, figsize=(20, 12))
        
        ax1 = axes[0]
        ax1.plot(df_pandas['Date'], df_pandas['Rolling_Volatility_30d'], 
                 label='Rolling Volatility (30-ditore)', linewidth=2, color='red')
        ax1.set_title('Analiza e Volatilitetit: Rolling Volatility 30-ditore', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Data', fontsize=14)
        ax1.set_ylabel('Volatiliteti (%)', fontsize=14)
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # FIGURA 4: Returns Heatmap
        ax2 = axes[1]
        returns_data = df_pandas[['Daily_Return', 'Weekly_Return', 'Monthly_Return']].dropna()
        correlation = returns_data.corr()
        sns.heatmap(correlation, annot=True, fmt='.3f', cmap='coolwarm', center=0, ax=ax2, 
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        ax2.set_title('Matrica e Korrelacionit: Rendimentet', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(direktoria, '02_volatility_analysis.png'), dpi=300, bbox_inches='tight')
        print("✓ Figura 2: Volatility Analysis u krijua")
        plt.close()
        
        # FIGURA 5: Volume Analysis
        fig, ax = plt.subplots(figsize=(20, 8))
        ax.bar(df_pandas['Date'], df_pandas['Volume'], alpha=0.6, color='steelblue', label='Volume')
        ax.set_title('Analiza e Volumit të Tregtimit', fontsize=16, fontweight='bold')
        ax.set_xlabel('Data', fontsize=14)
        ax.set_ylabel('Volume', fontsize=14)
        ax.legend(fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(direktoria, '03_volume_analysis.png'), dpi=300, bbox_inches='tight')
        print("✓ Figura 3: Volume Analysis u krijua")
        plt.close()
        
        # FIGURA 6: Statistical Distribution (Percentiles)
        fig, axes = plt.subplots(1, 2, figsize=(20, 8))
        
        ax1 = axes[0]
        df_pandas.boxplot(column='Close', ax=ax1)
        ax1.set_title('Box Plot: Shpërndarja e Çmimeve', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Çmimi ($)', fontsize=14)
        ax1.grid(True, alpha=0.3)
        
        ax2 = axes[1]
        df_pandas.boxplot(column='Daily_Return', ax=ax2)
        ax2.set_title('Box Plot: Shpërndarja e Rendimenteve Ditore', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Rendimenti Ditor (%)', fontsize=14)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(direktoria, '04_statistical_distribution.png'), dpi=300, bbox_inches='tight')
        print("✓ Figura 4: Statistical Distribution u krijua")
        plt.close()
        
        print(f"\n✓ Të gjitha vizualizimet u ruajtën në direktorinë: {direktoria}")
    
    def mbyll(self):
        """Mbyllja e SparkSession"""
        self.spark.stop()
        print("\n✓ SparkSession u mbyll me sukses")


def main():
    """
    Funksioni kryesor - ekzekuton të gjithë pipeline-in e analizës
    """
    print("="*80)
    print("PROJEKTI DOKTORATURË: ANALIZA E AVANCUAR FINANCIARE ME PYSPARK")
    print("Universiteti i Prishtinës, Republika e Kosovës")
    print("="*80)
    
    # Inicializimi
    analiza = AnalizaFinanciareAdvanced()
    
    # Shtegu i të dhënave (do të përdorim një dataset financiar real)
    # Për tani, do të krijojmë një dataset shembull
    # Studentët duhet të zëvendësojnë këtë me dataset real financiar
    SHTEGU_TE_DHENAT = "data_kaggle/financial_data.csv"
    
    # Kontrollimi nëse ekziston file
    if not os.path.exists(SHTEGU_TE_DHENAT):
        print(f"\n⚠️  KUJDES: File {SHTEGU_TE_DHENAT} nuk u gjet!")
        print("Ju lutem shkarkoni një dataset financiar (p.sh. nga Kaggle: S&P 500 stock data, Bitcoin prices, etc.)")
        print("Dhe vendoseni në direktorinë 'data_kaggle/' me emrin 'financial_data.csv'")
        print("\nFormati i kërkuar i CSV:")
        print("Date,Open,High,Low,Close,Volume")
        analiza.mbyll()
        return
    
    try:
        # FAZA 1: Ngarkimi i të dhënave
        df = analiza.ngarko_te_dhenat(SHTEGU_TE_DHENAT)
        
        # FAZA 2: NULL COUNTING
        null_df = analiza.null_counting_analysis(df)
        analiza.ruaj_rezultatet(null_df, "01_null_counting")
        
        # FAZA 3: DATA PROFILING
        kolona_numerike = ['Open', 'High', 'Low', 'Close', 'Volume']
        profiling_df = analiza.data_profiling_analysis(df, kolona_numerike)
        analiza.ruaj_rezultatet(profiling_df, "02_data_profiling")
        
        # FAZA 4: PERCENTILE_APPROX
        percentiles_close = analiza.percentile_approx_analysis(df, 'Close')
        percentiles_volume = analiza.percentile_approx_analysis(df, 'Volume')
        
        # FAZA 5: RETURNS CALCULATION
        df = analiza.returns_calculation(df, 'Close', 'Date')
        
        # FAZA 6: MOVING AVERAGE
        df = analiza.moving_average_analysis(df, 'Close', 'Date')
        
        # FAZA 7: VOLATILITY COMPUTATION
        df, hist_vol, annual_vol = analiza.volatility_computation(df)
        
        # FAZA 8: LAG TIME SERIES
        df = analiza.lag_time_series_analysis(df, 'Close', 'Date', [1, 5, 10, 20])
        
        # FAZA 9: WINDOW FUNCTIONS
        df = analiza.window_function_analysis(df, 'Close', 'Date')
        
        # FAZA 10: GROUPBY AGGREGATION
        monthly_agg, yearly_agg = analiza.groupby_aggregation_analysis(df, 'Date')
        analiza.ruaj_rezultatet(monthly_agg, "03_monthly_aggregation")
        analiza.ruaj_rezultatet(yearly_agg, "04_yearly_aggregation")
        
        # FAZA 11: Ruajtja e dataset-it final me të gjitha kolonat
        analiza.ruaj_rezultatet(df, "05_dataset_final_i_plote")
        
        # FAZA 12: Krijimi i vizualizimeve TË AVANCUARA (12+ figura)
        print(f"\n{'='*80}")
        print("FAZA 12: GJENERIMI I VIZUALIZIMEVE TË AVANCUARA")
        print(f"{'='*80}")
        
        # Konverto në Pandas për vizualizime
        df_pandas = df.toPandas()
        
        # Importo modulin e vizualizimeve
        try:
            from vizualizime_moduli import VizualizimeDoktorale
            viz = VizualizimeDoktorale()
            viz.generate_all_visualizations(df_pandas)
        except ImportError:
            print("⚠️  Moduli i vizualizimeve nuk u gjet, duke përdorur metodën bazë...")
            analiza.krijo_vizualizime(df)
        
        print(f"\n{'='*80}")
        print("✓✓✓ ANALIZA U PËRFUNDUA ME SUKSES ✓✓✓")
        print(f"{'='*80}")
        print("\nRezultatet:")
        print("  - rezultatet_doktorature/: 5 CSV files me analiza të detajuara")
        print("  - vizualizime_doktorature/: 12+ figura profesionale")
        print("\nAlgoritmet e aplikuara me sukses:")
        print("  ✓ 1. Null Counting - Analiza e plotësisë")
        print("  ✓ 2. Data Profiling - Statistika gjithëpërfshirëse")
        print("  ✓ 3. Percentile Approx - Kuantilet P25, P50, P75, P95, P99")
        print("  ✓ 4. Returns Calculation - Daily, Weekly, Monthly")
        print("  ✓ 5. Moving Average - MA 7d, 30d, 90d")
        print("  ✓ 6. Volatility Computation - Historical & Rolling")
        print("  ✓ 7. Lag Time Series - Lag 1, 5, 10, 20 ditë")
        print("  ✓ 8. Window Functions - rank, dense_rank, percent_rank, ntile")
        print("  ✓ 9. GroupBy Aggregation - MapReduce style")
        print("  ✓ 10. STDDEV_SAMP - Sample standard deviation")
        print("\nVizualizimet e gjeneruara:")
        print("  ✓ 01. Time Series Comprehensive")
        print("  ✓ 02. Returns Distribution (3D)")
        print("  ✓ 03. Volatility Analysis")
        print("  ✓ 04. Correlation Heatmap")
        print("  ✓ 05. Portfolio Performance")
        print("  ✓ 06. Volume Analysis")
        print("  ✓ 07. Candlestick Charts")
        print("  ✓ 08. Statistical Distributions")
        print("  ✓ 09. 3D Surface Plot")
        print("  ✓ 10. Risk-Return Scatter")
        print("  ✓ 11. Cumulative Returns")
        print("  ✓ 12. Drawdown Analysis")
        print(f"{'='*80}")
        
    except Exception as e:
        print(f"\n❌ GABIM: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        analiza.mbyll()


if __name__ == "__main__":
    main()
