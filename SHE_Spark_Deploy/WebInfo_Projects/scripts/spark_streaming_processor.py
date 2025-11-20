#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SPARK STREAMING PROCESSOR
Big Data Processing - Real-Time Feature Engineering
================================================================================
Processes financial data with Apache Spark
Calculates technical indicators (MA, RSI, Volatility, Momentum)
Stores processed features in HBase for ML predictions
================================================================================
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag, mean, stddev, sum as spark_sum, when, lit
from pyspark.sql.window import Window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, TimestampType
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import happybase
    HBASE_AVAILABLE = True
except ImportError:
    print("⚠️  happybase not installed. Will process CSV files.")
    HBASE_AVAILABLE = False

# Try to import cluster configuration
try:
    sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config'))
    from spark_cluster_config import SPARK_CONFIG, SPARK_MASTER_URL, HBASE_CONFIG
    USE_CLUSTER_CONFIG = True
    print("✅ Using distributed cluster configuration")
except ImportError:
    USE_CLUSTER_CONFIG = False
    print("⚠️  Cluster config not found, using local configuration")

# ============================================================================
# CONFIGURATION
# ============================================================================

# Assets
ASSETS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX',
          'GC=F', 'SI=F', 'CL=F', 'NG=F', '^GSPC', '^IXIC']

# Spark Configuration
# Override to use local mode by default (set USE_LOCAL_MODE=False to use cluster)
USE_LOCAL_MODE = True  # Force local mode for testing

if USE_LOCAL_MODE:
    SPARK_MASTER = "local[*]"  # Local mode with all CPU cores
    APP_NAME = "RealTimeFinancialProcessor_Local"
    USE_CLUSTER_CONFIG = False
    print("🔧 FORCED LOCAL MODE - Using local Spark (no cluster connection)")
elif USE_CLUSTER_CONFIG:
    SPARK_MASTER = SPARK_MASTER_URL
    APP_NAME = SPARK_CONFIG.get("spark.app.name", "RealTimeFinancialProcessor")
else:
    SPARK_MASTER = "local[*]"  # Fallback to local mode
    APP_NAME = "RealTimeFinancialProcessor"

# HBase Configuration
if USE_CLUSTER_CONFIG:
    HBASE_HOST = HBASE_CONFIG.get("host", "localhost")
    HBASE_PORT = HBASE_CONFIG.get("port", 9090)
else:
    HBASE_HOST = "localhost"
    HBASE_PORT = 9090

SOURCE_TABLE = "asset_prices"
FEATURES_TABLE = "asset_features"
PREDICTIONS_TABLE = "ml_predictions"

# Processing intervals
BATCH_INTERVAL = 60  # Process every 60 seconds

# ============================================================================
# SPARK SESSION
# ============================================================================

def create_spark_session():
    """Create and configure Spark session"""
    print("🚀 Initializing Apache Spark...")
    
    builder = SparkSession.builder \
        .appName(APP_NAME) \
        .master(SPARK_MASTER)
    
    # Apply cluster configuration if available
    if USE_CLUSTER_CONFIG and not USE_LOCAL_MODE:
        print("📊 Applying distributed cluster configuration...")
        for key, value in SPARK_CONFIG.items():
            if not key.startswith("spark.app.name"):
                builder = builder.config(key, value)
        print(f"   Total configurations applied: {len(SPARK_CONFIG)}")
    else:
        # Local mode configuration (optimized for Windows)
        print("📊 Applying local mode configuration...")
        builder = builder \
            .config("spark.executor.memory", "2g") \
            .config("spark.driver.memory", "1g") \
            .config("spark.executor.cores", "2") \
            .config("spark.sql.shuffle.partitions", "4") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.eventLog.enabled", "false") \
            .config("spark.ui.enabled", "false")  # Disable UI for faster startup
        print(f"   Optimized for local Windows execution")
    
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    
    print(f"✅ Spark Session Created")
    print(f"   Version: {spark.version}")
    print(f"   Master: {spark.sparkContext.master}")
    print(f"   App Name: {spark.sparkContext.appName}")
    
    if USE_CLUSTER_CONFIG and not USE_LOCAL_MODE:
        print(f"   Mode: DISTRIBUTED CLUSTER")
        print(f"   Executors: {SPARK_CONFIG.get('spark.executor.instances', 'auto')}")
        print(f"   Memory per Executor: {SPARK_CONFIG.get('spark.executor.memory', 'N/A')}")
        print(f"   Cores per Executor: {SPARK_CONFIG.get('spark.executor.cores', 'N/A')}")
        print(f"   Parallelism: {SPARK_CONFIG.get('spark.default.parallelism', 'N/A')}")
    else:
        print(f"   Mode: LOCAL (Windows)")
        print(f"   Using all available CPU cores")
    
    return spark

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data_from_csv(spark, data_dir):
    """Load data from CSV files (fallback mode)"""
    csv_file = os.path.join(data_dir, 'realtime_prices.csv')
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return None
    
    print(f"📂 Loading data from CSV: {csv_file}")
    
    df = spark.read.csv(csv_file, header=True, inferSchema=True)
    
    print(f"✅ Loaded {df.count()} records")
    return df

def load_data_from_hbase(spark, connection):
    """Load data from HBase"""
    if connection is None:
        return None
    
    try:
        print(f"📂 Loading data from HBase table: {SOURCE_TABLE}")
        
        table = connection.table(SOURCE_TABLE)
        
        # Scan all data (in production, you'd scan recent data only)
        rows = []
        for key, data in table.scan(limit=10000):  # Limit for demo
            row = {
                'row_key': key.decode('utf-8'),
                'asset': data[b'metadata:asset'].decode('utf-8'),
                'name': data[b'metadata:name'].decode('utf-8'),
                'timestamp': data[b'metadata:timestamp'].decode('utf-8'),
                'close': float(data[b'price:close']),
                'high': float(data[b'price:high']),
                'low': float(data[b'price:low']),
                'volume': int(data[b'price:volume'])
            }
            rows.append(row)
        
        if not rows:
            print("⚠️  No data found in HBase")
            return None
        
        # Create DataFrame
        df = spark.createDataFrame(rows)
        
        print(f"✅ Loaded {df.count()} records from HBase")
        return df
        
    except Exception as e:
        print(f"❌ Error loading from HBase: {e}")
        return None

# ============================================================================
# FEATURE ENGINEERING
# ============================================================================

def calculate_technical_indicators(df, asset):
    """Calculate technical indicators for a specific asset"""
    
    # Filter for specific asset
    asset_df = df.filter(col('asset') == asset).orderBy('timestamp')
    
    if asset_df.count() < 50:
        print(f"  ⚠️  Not enough data for {asset} (need at least 50 records)")
        return None
    
    # Window specification
    window_spec = Window.orderBy('timestamp')
    
    # 1. RETURNS (daily % change) - safe division to avoid divide by zero
    prev_close = lag('close', 1).over(window_spec)
    asset_df = asset_df.withColumn('return', 
        when(prev_close == 0, 0).otherwise((col('close') - prev_close) / prev_close))
    
    # 2. MOVING AVERAGES
    window_5 = Window.orderBy('timestamp').rowsBetween(-4, 0)
    window_14 = Window.orderBy('timestamp').rowsBetween(-13, 0)
    window_20 = Window.orderBy('timestamp').rowsBetween(-19, 0)
    window_50 = Window.orderBy('timestamp').rowsBetween(-49, 0)
    
    asset_df = asset_df.withColumn('ma_5', mean('close').over(window_5))
    asset_df = asset_df.withColumn('ma_14', mean('close').over(window_14))
    asset_df = asset_df.withColumn('ma_20', mean('close').over(window_20))
    asset_df = asset_df.withColumn('ma_50', mean('close').over(window_50))
    
    # 3. VOLATILITY (rolling standard deviation)
    asset_df = asset_df.withColumn('volatility_14', stddev('return').over(window_14))
    asset_df = asset_df.withColumn('volatility_20', stddev('return').over(window_20))
    
    # 4. MOMENTUM
    asset_df = asset_df.withColumn('momentum_7', 
        col('close') - lag('close', 7).over(window_spec))
    asset_df = asset_df.withColumn('momentum_14', 
        col('close') - lag('close', 14).over(window_spec))
    
    # 5. RSI (Relative Strength Index) - Simplified
    # Calculate gains and losses
    asset_df = asset_df.withColumn('price_change', col('close') - lag('close', 1).over(window_spec))
    asset_df = asset_df.withColumn('gain', when(col('price_change') > 0, col('price_change')).otherwise(0))
    asset_df = asset_df.withColumn('loss', when(col('price_change') < 0, -col('price_change')).otherwise(0))
    
    # Average gain and loss over 14 periods
    asset_df = asset_df.withColumn('avg_gain', mean('gain').over(window_14))
    asset_df = asset_df.withColumn('avg_loss', mean('loss').over(window_14))
    
    # RSI calculation - safe division to avoid divide by zero
    asset_df = asset_df.withColumn('rs', 
        when(col('avg_loss') == 0, 100).otherwise(col('avg_gain') / col('avg_loss')))
    asset_df = asset_df.withColumn('rsi', 100 - (100 / (1 + col('rs'))))
    
    # 6. BOLLINGER BANDS
    asset_df = asset_df.withColumn('bb_middle', col('ma_20'))
    asset_df = asset_df.withColumn('bb_std', stddev('close').over(window_20))
    asset_df = asset_df.withColumn('bb_upper', col('bb_middle') + (2 * col('bb_std')))
    asset_df = asset_df.withColumn('bb_lower', col('bb_middle') - (2 * col('bb_std')))
    
    # 7. PRICE POSITION (% from MA) - safe division to avoid divide by zero
    asset_df = asset_df.withColumn('price_to_ma5', 
        when(col('ma_5') == 0, 0).otherwise((col('close') - col('ma_5')) / col('ma_5') * 100))
    asset_df = asset_df.withColumn('price_to_ma20', 
        when(col('ma_20') == 0, 0).otherwise((col('close') - col('ma_20')) / col('ma_20') * 100))
    
    # 8. CLASSIFICATION LABEL (for ML)
    # 1 if price goes up next period, 0 if down
    asset_df = asset_df.withColumn('next_return', 
        lag('return', -1).over(window_spec))
    asset_df = asset_df.withColumn('label', 
        when(col('next_return') > 0, 1).otherwise(0))
    
    # Drop intermediate columns
    asset_df = asset_df.drop('price_change', 'gain', 'loss', 'avg_gain', 'avg_loss', 
                              'rs', 'bb_std')
    
    return asset_df

def process_all_assets(df):
    """Process all assets and calculate features"""
    
    print(f"\n{'='*80}")
    print("CALCULATING TECHNICAL INDICATORS")
    print(f"{'='*80}\n")
    
    processed_dfs = []
    
    for asset in ASSETS:
        print(f"Processing {asset}...", end=' ')
        
        asset_features = calculate_technical_indicators(df, asset)
        
        if asset_features is not None:
            processed_dfs.append(asset_features)
            print(f"✓ {asset_features.count()} records")
        else:
            print(f"✗ Skipped")
    
    if not processed_dfs:
        print("\n❌ No data processed!")
        return None
    
    # Union all asset DataFrames
    print(f"\nCombining all assets...")
    result_df = processed_dfs[0]
    for df in processed_dfs[1:]:
        result_df = result_df.union(df)
    
    print(f"✅ Total processed records: {result_df.count()}")
    
    return result_df

# ============================================================================
# SAVE RESULTS
# ============================================================================

def save_to_hbase(df, connection, table_name):
    """Save processed features to HBase"""
    if connection is None:
        return False
    
    try:
        # Create table if it doesn't exist
        tables = [t.decode('utf-8') for t in connection.tables()]
        if table_name not in tables:
            print(f"Creating HBase table: {table_name}")
            connection.create_table(
                table_name,
                {
                    'features': dict(),   # All calculated features
                    'price': dict(),      # Original price data
                    'metadata': dict()    # Asset info
                }
            )
        
        table = connection.table(table_name)
        
        # Convert to list and save
        data_rows = df.collect()
        
        print(f"💾 Saving {len(data_rows)} records to HBase table '{table_name}'...")
        
        for row in data_rows:
            row_key = f"{row['asset']}_{row['timestamp']}".encode('utf-8')
            
            hbase_data = {
                # Price data
                b'price:close': str(row['close']).encode('utf-8'),
                b'price:high': str(row['high']).encode('utf-8'),
                b'price:low': str(row['low']).encode('utf-8'),
                b'price:volume': str(row['volume']).encode('utf-8'),
                
                # Metadata
                b'metadata:asset': row['asset'].encode('utf-8'),
                b'metadata:timestamp': row['timestamp'].encode('utf-8'),
                
                # Features
                b'features:return': str(row['return'] if row['return'] else 0).encode('utf-8'),
                b'features:ma_5': str(row['ma_5'] if row['ma_5'] else 0).encode('utf-8'),
                b'features:ma_14': str(row['ma_14'] if row['ma_14'] else 0).encode('utf-8'),
                b'features:ma_20': str(row['ma_20'] if row['ma_20'] else 0).encode('utf-8'),
                b'features:ma_50': str(row['ma_50'] if row['ma_50'] else 0).encode('utf-8'),
                b'features:volatility_14': str(row['volatility_14'] if row['volatility_14'] else 0).encode('utf-8'),
                b'features:volatility_20': str(row['volatility_20'] if row['volatility_20'] else 0).encode('utf-8'),
                b'features:momentum_7': str(row['momentum_7'] if row['momentum_7'] else 0).encode('utf-8'),
                b'features:momentum_14': str(row['momentum_14'] if row['momentum_14'] else 0).encode('utf-8'),
                b'features:rsi': str(row['rsi'] if row['rsi'] else 0).encode('utf-8'),
                b'features:bb_upper': str(row['bb_upper'] if row['bb_upper'] else 0).encode('utf-8'),
                b'features:bb_middle': str(row['bb_middle'] if row['bb_middle'] else 0).encode('utf-8'),
                b'features:bb_lower': str(row['bb_lower'] if row['bb_lower'] else 0).encode('utf-8'),
                b'features:price_to_ma5': str(row['price_to_ma5'] if row['price_to_ma5'] else 0).encode('utf-8'),
                b'features:price_to_ma20': str(row['price_to_ma20'] if row['price_to_ma20'] else 0).encode('utf-8'),
                b'features:label': str(row['label'] if row['label'] else 0).encode('utf-8'),
            }
            
            table.put(row_key, hbase_data)
        
        print(f"✅ Data saved to HBase successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error saving to HBase: {e}")
        return False

def save_to_csv(df, output_dir):
    """Save processed features to CSV (fallback)"""
    try:
        output_file = os.path.join(output_dir, 'processed_features.csv')
        
        print(f"💾 Saving to CSV: {output_file}")
        
        # Convert to Pandas and save
        df.toPandas().to_csv(output_file, index=False)
        
        print(f"✅ Data saved to CSV successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")
        return False

# ============================================================================
# STATISTICS & SUMMARY
# ============================================================================

def print_statistics(df):
    """Print statistics about processed data"""
    
    print(f"\n{'='*80}")
    print("PROCESSING STATISTICS")
    print(f"{'='*80}\n")
    
    # Total records
    total_records = df.count()
    print(f"📊 Total Records: {total_records}")
    
    # Records per asset
    print(f"\n📈 Records per Asset:")
    asset_counts = df.groupBy('asset').count().orderBy('count', ascending=False)
    for row in asset_counts.collect():
        print(f"   {row['asset']:8s}: {row['count']:,} records")
    
    # Sample of latest data
    print(f"\n🔍 Latest Data Sample (first asset):")
    latest = df.filter(col('asset') == ASSETS[0]) \
               .orderBy(col('timestamp').desc()) \
               .limit(1)
    
    if latest.count() > 0:
        row = latest.collect()[0]
        print(f"   Asset: {row['asset']}")
        print(f"   Price: ${row['close']:.2f}")
        print(f"   MA(5): ${row['ma_5']:.2f}" if row['ma_5'] else "   MA(5): N/A")
        print(f"   MA(20): ${row['ma_20']:.2f}" if row['ma_20'] else "   MA(20): N/A")
        print(f"   RSI: {row['rsi']:.2f}" if row['rsi'] else "   RSI: N/A")
        print(f"   Volatility: {row['volatility_14']:.4f}" if row['volatility_14'] else "   Volatility: N/A")
    
    print(f"\n{'='*80}\n")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main processing function"""
    
    print("="*80)
    print("SPARK STREAMING PROCESSOR")
    print("Real-Time Feature Engineering for 14 Financial Assets")
    print("="*80)
    
    # Create Spark session
    spark = create_spark_session()
    
    # Data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    
    # Connect to HBase
    hbase_conn = None
    if HBASE_AVAILABLE:
        try:
            print(f"\n🔌 Connecting to HBase at {HBASE_HOST}:{HBASE_PORT}...")
            hbase_conn = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
            print(f"✅ HBase connection established!")
        except Exception as e:
            print(f"⚠️  HBase connection failed: {e}")
            print(f"   Will use CSV mode.")
    
    # Load data
    if hbase_conn:
        df = load_data_from_hbase(spark, hbase_conn)
        if df is None:
            print("Falling back to CSV...")
            df = load_data_from_csv(spark, data_dir)
    else:
        df = load_data_from_csv(spark, data_dir)
    
    if df is None:
        print("\n❌ No data to process!")
        spark.stop()
        return
    
    # Process data and calculate features
    processed_df = process_all_assets(df)
    
    if processed_df is None:
        print("\n❌ Processing failed!")
        spark.stop()
        return
    
    # Show statistics
    print_statistics(processed_df)
    
    # Save results
    if hbase_conn:
        save_to_hbase(processed_df, hbase_conn, FEATURES_TABLE)
    else:
        save_to_csv(processed_df, data_dir)
    
    # Cleanup
    if hbase_conn:
        hbase_conn.close()
    
    spark.stop()
    
    print("\n✅ Processing completed successfully!\n")

if __name__ == "__main__":
    main()
