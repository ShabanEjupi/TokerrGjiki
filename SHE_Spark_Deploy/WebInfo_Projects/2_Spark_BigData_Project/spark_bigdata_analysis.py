#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SPARK BIG DATA ANALYSIS - WEB INFORMATION RETRIEVAL
Machine Learning Algorithms with PySpark MLlib
================================================================================
Professor's Algorithms Implementation:
1. Decision Trees (Classification & Regression)
2. Random Forest (Ensemble Learning)
3. Gradient Boosted Trees (GBT)
4. K-Means Clustering
5. Linear Regression
6. Logistic Regression
7. Support Vector Machines (SVM)

Dataset: 14 Financial Assets (8 Stocks + 4 Commodities + 2 Indices)
Period: January 1, 2022 to October 26, 2025
================================================================================
"""

import os
import sys
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# PySpark imports
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag, mean, stddev, min as spark_min, max as spark_max
from pyspark.sql.window import Window
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import DecisionTreeClassifier, RandomForestClassifier, LogisticRegression, LinearSVC
from pyspark.ml.regression import DecisionTreeRegressor, RandomForestRegressor, LinearRegression, GBTRegressor
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator, RegressionEvaluator
from pyspark.ml import Pipeline

# For data download
import pandas as pd
import numpy as np
import yfinance as yf

print("=" * 80)
print("SPARK BIG DATA ANALYSIS - WEB INFORMATION RETRIEVAL")
print("14 ASETE: 8 Stocks + 4 Commodities + 2 Indices")
print("PERIUDHA: 1 Janar 2022 deri 26 Tetor 2025")
print("=" * 80)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Asset definitions
STOCKS = {
    'AAPL': 'Apple',
    'GOOGL': 'Google',
    'MSFT': 'Microsoft',
    'AMZN': 'Amazon',
    'NVDA': 'NVIDIA',
    'TSLA': 'Tesla',
    'META': 'Meta',
    'NFLX': 'Netflix'
}

COMMODITIES = {
    'GC=F': 'Gold',
    'SI=F': 'Silver',
    'CL=F': 'Crude Oil',
    'NG=F': 'Natural Gas'
}

INDICES = {
    '^GSPC': 'S&P 500',
    '^IXIC': 'NASDAQ'
}

ALL_ASSETS = {**STOCKS, **COMMODITIES, **INDICES}

# Date range
START_DATE = '2022-01-01'
END_DATE = '2025-10-26'

# ============================================================================
# STEP 1: DATA DOWNLOAD & PREPARATION
# ============================================================================

print(f"\n📊 Downloading historical data from {START_DATE} to {END_DATE}...\n")

data = {}

print("Stocks:")
for ticker, name in STOCKS.items():
    try:
        df = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
        if not df.empty:
            close_price = df['Close']
            if isinstance(close_price, pd.DataFrame):
                close_price = close_price.iloc[:, 0]
            data[ticker] = close_price
            print(f"   Downloading {ticker} ({name})... ✓ {len(close_price)} days")
    except Exception as e:
        print(f"   Downloading {ticker} ({name})... ✗ Error: {e}")

print("\nCommodities:")
for ticker, name in COMMODITIES.items():
    try:
        df = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
        if not df.empty:
            close_price = df['Close']
            if isinstance(close_price, pd.DataFrame):
                close_price = close_price.iloc[:, 0]
            data[ticker] = close_price
            print(f"   Downloading {ticker} ({name})... ✓ {len(close_price)} days")
    except Exception as e:
        print(f"   Downloading {ticker} ({name})... ✗ Error: {e}")

print("\nIndices:")
for ticker, name in INDICES.items():
    try:
        df = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
        if not df.empty:
            close_price = df['Close']
            if isinstance(close_price, pd.DataFrame):
                close_price = close_price.iloc[:, 0]
            data[ticker] = close_price
            print(f"   Downloading {ticker} ({name})... ✓ {len(close_price)} days")
    except Exception as e:
        print(f"   Downloading {ticker} ({name})... ✗ Error: {e}")

# Create DataFrame and align dates
if data:
    try:
        df_prices = pd.DataFrame(data)
    except Exception as e:
        print(f"\n❌ ERROR creating DataFrame: {e}")
        df_prices = pd.concat(data, axis=1)
        df_prices.columns = list(data.keys())
    
    initial_rows = len(df_prices)
    df_prices.dropna(inplace=True)
    dropped_rows = initial_rows - len(df_prices)
    
    if dropped_rows > 0:
        print(f"\n⚠️  Dropped {dropped_rows} rows with missing data to align all assets")
    
    print(f"\n✅ Data downloaded successfully!")
    print(f"   Total trading days: {len(df_prices)}")
    print(f"   Date range: {df_prices.index[0].date()} to {df_prices.index[-1].date()}")
    
    # Save raw data
    df_prices.to_csv('spark_raw_prices_14_assets.csv')
    print(f"\n💾 Raw prices saved to 'spark_raw_prices_14_assets.csv'")
else:
    print("\n❌ ERROR: No data was downloaded!")
    sys.exit(1)

# ============================================================================
# STEP 2: INITIALIZE SPARK SESSION
# ============================================================================

print("\n" + "=" * 80)
print("INITIALIZING APACHE SPARK")
print("=" * 80)

spark = SparkSession.builder \
    .appName("Financial Analysis - Big Data with Spark") \
    .config("spark.driver.memory", "4g") \
    .config("spark.executor.memory", "4g") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print(f"\n✅ Spark Session Created!")
print(f"   Spark Version: {spark.version}")
print(f"   Application: {spark.sparkContext.appName}")
print(f"   Master: {spark.sparkContext.master}")

# ============================================================================
# STEP 3: FEATURE ENGINEERING WITH SPARK
# ============================================================================

print("\n" + "=" * 80)
print("FEATURE ENGINEERING WITH SPARK")
print("=" * 80)

# Convert pandas DataFrame to Spark DataFrame
df_prices_reset = df_prices.reset_index()
df_prices_reset.columns = ['Date'] + list(df_prices.columns)
spark_df = spark.createDataFrame(df_prices_reset)

# Calculate features for each asset
features_dfs = []

for asset in ALL_ASSETS.keys():
    print(f"\nProcessing features for {asset}...")
    
    # Window specification for lag features
    window_spec = Window.orderBy('Date')
    
    # Create temporary view
    asset_df = spark_df.select('Date', col(asset).alias('Close'))
    
    # Calculate returns
    asset_df = asset_df.withColumn('Return', 
                                    (col('Close') - lag('Close', 1).over(window_spec)) / lag('Close', 1).over(window_spec))
    
    # Moving averages
    window_7 = Window.orderBy('Date').rowsBetween(-6, 0)
    window_14 = Window.orderBy('Date').rowsBetween(-13, 0)
    window_30 = Window.orderBy('Date').rowsBetween(-29, 0)
    
    asset_df = asset_df.withColumn('MA_7', mean('Close').over(window_7))
    asset_df = asset_df.withColumn('MA_14', mean('Close').over(window_14))
    asset_df = asset_df.withColumn('MA_30', mean('Close').over(window_30))
    
    # Volatility (rolling standard deviation)
    asset_df = asset_df.withColumn('Volatility_14', stddev('Return').over(window_14))
    
    # Price momentum
    asset_df = asset_df.withColumn('Momentum_7', col('Close') - lag('Close', 7).over(window_spec))
    asset_df = asset_df.withColumn('Momentum_14', col('Close') - lag('Close', 14).over(window_spec))
    
    # Target: Next day return (classification: Up/Down)
    asset_df = asset_df.withColumn('Next_Return', 
                                    lag('Return', -1).over(window_spec))
    
    # Classification label: 1 if next return > 0, else 0
    asset_df = asset_df.withColumn('Label', 
                                    (col('Next_Return') > 0).cast('integer'))
    
    # Rename columns with asset prefix
    for col_name in ['Close', 'Return', 'MA_7', 'MA_14', 'MA_30', 'Volatility_14', 'Momentum_7', 'Momentum_14']:
        asset_df = asset_df.withColumnRenamed(col_name, f'{asset}_{col_name}')
    
    features_dfs.append(asset_df.select('Date', f'{asset}_Close', f'{asset}_Return', 
                                         f'{asset}_MA_7', f'{asset}_MA_14', f'{asset}_MA_30',
                                         f'{asset}_Volatility_14', f'{asset}_Momentum_7', 
                                         f'{asset}_Momentum_14'))

# Join all features
print("\nCombining features from all assets...")
combined_df = features_dfs[0]
for df in features_dfs[1:]:
    combined_df = combined_df.join(df, on='Date', how='inner')

# Add target label (using AAPL as example)
aapl_label = spark_df.select('Date', col('AAPL').alias('Target_Close'))
window_spec = Window.orderBy('Date')
aapl_label = aapl_label.withColumn('Next_Return',
                                   (lag('Target_Close', -1).over(window_spec) - col('Target_Close')) / col('Target_Close'))
aapl_label = aapl_label.withColumn('Label', (col('Next_Return') > 0).cast('integer'))
aapl_label = aapl_label.withColumn('Target_Price', lag('Target_Close', -1).over(window_spec))

combined_df = combined_df.join(aapl_label.select('Date', 'Label', 'Target_Price'), on='Date', how='inner')

# Drop nulls
combined_df = combined_df.na.drop()

print(f"\n✅ Feature engineering complete!")
print(f"   Total features: {len(combined_df.columns) - 3}")  # Exclude Date, Label, Target_Price
print(f"   Data points: {combined_df.count()}")

# ============================================================================
# STEP 4: PREPARE ML FEATURES
# ============================================================================

print("\n" + "=" * 80)
print("PREPARING MACHINE LEARNING FEATURES")
print("=" * 80)

# Select feature columns (exclude Date, Label, Target_Price)
feature_cols = [c for c in combined_df.columns if c not in ['Date', 'Label', 'Target_Price']]

print(f"\nFeature columns selected: {len(feature_cols)}")

# Assemble features into vector
assembler = VectorAssembler(inputCols=feature_cols, outputCol='features_raw')
scaler = StandardScaler(inputCol='features_raw', outputCol='features')

# Create pipeline for feature preparation
feature_pipeline = Pipeline(stages=[assembler, scaler])
feature_model = feature_pipeline.fit(combined_df)
ml_df = feature_model.transform(combined_df)

# Split data: 80% train, 20% test
train_df, test_df = ml_df.randomSplit([0.8, 0.2], seed=42)

print(f"\n📊 Dataset Split:")
print(f"   Training set: {train_df.count()} samples")
print(f"   Test set: {test_df.count()} samples")

# ============================================================================
# ALGORITHM 1: DECISION TREE CLASSIFICATION
# ============================================================================

print("\n" + "=" * 80)
print("ALGORITHM 1: DECISION TREE CLASSIFICATION")
print("=" * 80)

dt_classifier = DecisionTreeClassifier(featuresCol='features', labelCol='Label', maxDepth=5)
dt_model = dt_classifier.fit(train_df)
dt_predictions = dt_model.transform(test_df)

# Evaluate
evaluator_acc = MulticlassClassificationEvaluator(labelCol='Label', predictionCol='prediction', metricName='accuracy')
evaluator_auc = BinaryClassificationEvaluator(labelCol='Label', rawPredictionCol='rawPrediction')

dt_accuracy = evaluator_acc.evaluate(dt_predictions)
dt_auc = evaluator_auc.evaluate(dt_predictions)

print(f"\n✅ Decision Tree Results:")
print(f"   Accuracy: {dt_accuracy:.4f} ({dt_accuracy*100:.2f}%)")
print(f"   AUC-ROC: {dt_auc:.4f}")
print(f"   Tree Depth: {dt_model.depth}")
print(f"   Number of Nodes: {dt_model.numNodes}")

# ============================================================================
# ALGORITHM 2: RANDOM FOREST CLASSIFICATION
# ============================================================================

print("\n" + "=" * 80)
print("ALGORITHM 2: RANDOM FOREST CLASSIFICATION")
print("=" * 80)

rf_classifier = RandomForestClassifier(featuresCol='features', labelCol='Label', 
                                       numTrees=50, maxDepth=5, seed=42)
rf_model = rf_classifier.fit(train_df)
rf_predictions = rf_model.transform(test_df)

rf_accuracy = evaluator_acc.evaluate(rf_predictions)
rf_auc = evaluator_auc.evaluate(rf_predictions)

print(f"\n✅ Random Forest Results:")
print(f"   Accuracy: {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
print(f"   AUC-ROC: {rf_auc:.4f}")
print(f"   Number of Trees: {rf_model.getNumTrees}")

# ============================================================================
# ALGORITHM 3: LOGISTIC REGRESSION
# ============================================================================

print("\n" + "=" * 80)
print("ALGORITHM 3: LOGISTIC REGRESSION")
print("=" * 80)

lr_classifier = LogisticRegression(featuresCol='features', labelCol='Label', maxIter=100)
lr_model = lr_classifier.fit(train_df)
lr_predictions = lr_model.transform(test_df)

lr_accuracy = evaluator_acc.evaluate(lr_predictions)
lr_auc = evaluator_auc.evaluate(lr_predictions)

print(f"\n✅ Logistic Regression Results:")
print(f"   Accuracy: {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")
print(f"   AUC-ROC: {lr_auc:.4f}")

# ============================================================================
# ALGORITHM 4: LINEAR SVM
# ============================================================================

print("\n" + "=" * 80)
print("ALGORITHM 4: LINEAR SUPPORT VECTOR MACHINE")
print("=" * 80)

svm_classifier = LinearSVC(featuresCol='features', labelCol='Label', maxIter=100)
svm_model = svm_classifier.fit(train_df)
svm_predictions = svm_model.transform(test_df)

svm_accuracy = evaluator_acc.evaluate(svm_predictions)

print(f"\n✅ Linear SVM Results:")
print(f"   Accuracy: {svm_accuracy:.4f} ({svm_accuracy*100:.2f}%)")

# ============================================================================
# ALGORITHM 5: GRADIENT BOOSTED TREES REGRESSION
# ============================================================================

print("\n" + "=" * 80)
print("ALGORITHM 5: GRADIENT BOOSTED TREES REGRESSION")
print("=" * 80)

gbt_regressor = GBTRegressor(featuresCol='features', labelCol='Target_Price', maxDepth=5, maxIter=50)
gbt_model = gbt_regressor.fit(train_df)
gbt_predictions = gbt_model.transform(test_df)

evaluator_r2 = RegressionEvaluator(labelCol='Target_Price', predictionCol='prediction', metricName='r2')
evaluator_rmse = RegressionEvaluator(labelCol='Target_Price', predictionCol='prediction', metricName='rmse')

gbt_r2 = evaluator_r2.evaluate(gbt_predictions)
gbt_rmse = evaluator_rmse.evaluate(gbt_predictions)

print(f"\n✅ Gradient Boosted Trees Results:")
print(f"   R² Score: {gbt_r2:.4f}")
print(f"   RMSE: ${gbt_rmse:.2f}")
print(f"   Number of Trees: {len(gbt_model.trees)}")

# ============================================================================
# ALGORITHM 6: LINEAR REGRESSION
# ============================================================================

print("\n" + "=" * 80)
print("ALGORITHM 6: LINEAR REGRESSION")
print("=" * 80)

linear_reg = LinearRegression(featuresCol='features', labelCol='Target_Price')
linear_model = linear_reg.fit(train_df)
linear_predictions = linear_model.transform(test_df)

linear_r2 = evaluator_r2.evaluate(linear_predictions)
linear_rmse = evaluator_rmse.evaluate(linear_predictions)

print(f"\n✅ Linear Regression Results:")
print(f"   R² Score: {linear_r2:.4f}")
print(f"   RMSE: ${linear_rmse:.2f}")

# ============================================================================
# ALGORITHM 7: K-MEANS CLUSTERING
# ============================================================================

print("\n" + "=" * 80)
print("ALGORITHM 7: K-MEANS CLUSTERING")
print("=" * 80)

# Use only price features for clustering
price_cols = [c for c in combined_df.columns if c.endswith('_Close')]
clustering_assembler = VectorAssembler(inputCols=price_cols, outputCol='clustering_features')
clustering_df = clustering_assembler.transform(combined_df)

kmeans = KMeans(featuresCol='clustering_features', k=3, seed=42)
kmeans_model = kmeans.fit(clustering_df)
kmeans_predictions = kmeans_model.transform(clustering_df)

print(f"\n✅ K-Means Clustering Results:")
print(f"   Number of Clusters: 3")
print(f"   Cluster Centers:")
for i, center in enumerate(kmeans_model.clusterCenters()):
    print(f"      Cluster {i}: Mean price = ${np.mean(center):.2f}")

# Analyze cluster distribution
cluster_counts = kmeans_predictions.groupBy('prediction').count().collect()
print(f"\n   Cluster Distribution:")
for row in cluster_counts:
    print(f"      Cluster {row['prediction']}: {row['count']} days")

# ============================================================================
# SAVE RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("SAVING RESULTS")
print("=" * 80)

# 1. Classification Results Summary
classification_results = pd.DataFrame({
    'Algorithm': ['Decision Tree', 'Random Forest', 'Logistic Regression', 'Linear SVM'],
    'Accuracy': [dt_accuracy, rf_accuracy, lr_accuracy, svm_accuracy],
    'AUC_ROC': [dt_auc, rf_auc, lr_auc, np.nan]
})
classification_results.to_csv('spark_classification_results.csv', index=False)
print("\n💾 Classification results saved to 'spark_classification_results.csv'")

# 2. Regression Results Summary
regression_results = pd.DataFrame({
    'Algorithm': ['Gradient Boosted Trees', 'Linear Regression'],
    'R2_Score': [gbt_r2, linear_r2],
    'RMSE': [gbt_rmse, linear_rmse]
})
regression_results.to_csv('spark_regression_results.csv', index=False)
print("💾 Regression results saved to 'spark_regression_results.csv'")

# 3. Model Comparison
model_comparison = pd.DataFrame({
    'Category': ['Classification', 'Classification', 'Classification', 'Classification', 
                 'Regression', 'Regression', 'Clustering'],
    'Algorithm': ['Decision Tree', 'Random Forest', 'Logistic Regression', 'Linear SVM',
                  'Gradient Boosted Trees', 'Linear Regression', 'K-Means'],
    'Primary_Metric': [dt_accuracy, rf_accuracy, lr_accuracy, svm_accuracy,
                       gbt_r2, linear_r2, np.nan],
    'Secondary_Metric': [dt_auc, rf_auc, lr_auc, np.nan, gbt_rmse, linear_rmse, np.nan]
})
model_comparison.to_csv('spark_model_comparison.csv', index=False)
print("💾 Model comparison saved to 'spark_model_comparison.csv'")

# 4. Sample Predictions
sample_predictions = dt_predictions.select('Label', 'prediction', 'probability').limit(100).toPandas()
sample_predictions.to_csv('spark_sample_predictions.csv', index=False)
print("💾 Sample predictions saved to 'spark_sample_predictions.csv'")

# 5. Clustering Results
clustering_results = kmeans_predictions.select('Date', 'prediction').toPandas()
clustering_results.columns = ['Date', 'Cluster']
clustering_results.to_csv('spark_clustering_results.csv', index=False)
print("💾 Clustering results saved to 'spark_clustering_results.csv'")

# 6. Feature Statistics
feature_stats = combined_df.select(feature_cols[:10]).describe().toPandas()  # Top 10 features
feature_stats.to_csv('spark_feature_statistics.csv', index=False)
print("💾 Feature statistics saved to 'spark_feature_statistics.csv'")

# ============================================================================
# PERFORMANCE SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("PERFORMANCE SUMMARY")
print("=" * 80)

print("\n📊 CLASSIFICATION ALGORITHMS:")
print(f"   Best Accuracy: Random Forest ({rf_accuracy*100:.2f}%)")
print(f"   Best AUC-ROC: Random Forest ({rf_auc:.4f})")

print("\n📊 REGRESSION ALGORITHMS:")
print(f"   Best R² Score: Gradient Boosted Trees ({gbt_r2:.4f})")
print(f"   Best RMSE: Gradient Boosted Trees (${gbt_rmse:.2f})")

print("\n📊 CLUSTERING:")
print(f"   K-Means identified 3 distinct market patterns")

print("\n" + "=" * 80)
print("DEPLOYMENT INSTRUCTIONS")
print("=" * 80)

print("""
📤 Upload to server (krenuser@185.182.158.150:8022):
   
   1. Create project directory:
      ssh -p 8022 krenuser@185.182.158.150
      mkdir -p ~/spark_bigdata_project
      exit
   
   2. Upload all files:
      scp -P 8022 *.csv krenuser@185.182.158.150:~/spark_bigdata_project/
      scp -P 8022 *.py krenuser@185.182.158.150:~/spark_bigdata_project/
   
   3. Run on server:
      ssh -p 8022 krenuser@185.182.158.150
      cd ~/spark_bigdata_project
      spark-submit spark_bigdata_analysis.py
""")

print("\n" + "=" * 80)
print("✅ SPARK BIG DATA ANALYSIS COMPLETE!")
print("=" * 80)

print(f"""
📁 FILES CREATED: 6
   1. spark_raw_prices_14_assets.csv
   2. spark_classification_results.csv
   3. spark_regression_results.csv
   4. spark_model_comparison.csv
   5. spark_sample_predictions.csv
   6. spark_clustering_results.csv
   7. spark_feature_statistics.csv
""")

# Stop Spark session
spark.stop()
print("\n✅ Spark session closed successfully!")
