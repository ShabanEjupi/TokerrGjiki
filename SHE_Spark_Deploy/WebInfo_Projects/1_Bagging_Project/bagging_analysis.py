import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import BaggingClassifier, BaggingRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("ANALIZA FINANCIARE ME BAGGING - WEB INFORMATION RETRIEVAL")
print("14 ASETE HALAL: AAPL, GOOGL, MSFT, AMZN, NVDA, TSLA, META, NFLX + Commodities & Indices")
print("PERIUDHA: 1 Janar 2022 deri 26 Tetor 2025")
print("=" * 80)

# Define the 14 assets - 8 Stocks + 4 Commodities + 2 Indices
assets = {
    'Stocks': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX'],
    'Commodities': ['GC=F', 'SI=F', 'CL=F', 'NG=F'],  # Gold, Silver, Oil, Natural Gas
    'Indices': ['^GSPC', '^IXIC']  # S&P 500, NASDAQ
}
all_assets = assets['Stocks'] + assets['Commodities'] + assets['Indices']

asset_names = {
    'AAPL': 'Apple', 'GOOGL': 'Google', 'MSFT': 'Microsoft', 'AMZN': 'Amazon',
    'NVDA': 'NVIDIA', 'TSLA': 'Tesla', 'META': 'Meta', 'NFLX': 'Netflix',
    'GC=F': 'Gold', 'SI=F': 'Silver', 'CL=F': 'Crude Oil', 'NG=F': 'Natural Gas',
    '^GSPC': 'S&P 500', '^IXIC': 'NASDAQ'
}

# Download data from Yahoo Finance
start_date = '2022-01-01'
end_date = '2025-10-26'

print(f"\n📊 Downloading historical data from {start_date} to {end_date}...\n")

# Download data for all assets
data = {}
for category, asset_list in assets.items():
    print(f"\n{category}:")
    for asset in asset_list:
        print(f"   Downloading {asset} ({asset_names[asset]})...", end=' ')
        try:
            df = yf.download(asset, start=start_date, end=end_date, progress=False)
            if not df.empty:
                # yfinance returns multi-index columns, extract Close price as Series
                if 'Close' in df.columns.get_level_values(0):
                    close_price = df['Close']
                    if isinstance(close_price, pd.DataFrame):
                        # It's a DataFrame with one column, get the Series
                        data[asset] = close_price.iloc[:, 0]
                    else:
                        data[asset] = close_price
                    print(f"✓ {len(df)} days")
                else:
                    print(f"✗ No Close column found")
            else:
                print(f"✗ No data received")
        except Exception as e:
            print(f"✗ Error: {e}")

# Create DataFrame with all assets
if data:
    # Debug: Check lengths
    print(f"\nAssets downloaded: {len(data)}")
    for asset, series in data.items():
        print(f"  {asset}: {len(series)} days")
    
    # Create DataFrame - pandas will automatically align by index
    try:
        df_prices = pd.DataFrame(data)
    except Exception as e:
        print(f"\n❌ ERROR creating DataFrame: {e}")
        print("Trying alternative method...")
        # Convert dict of series to DataFrame with explicit index alignment
        df_prices = pd.concat(data, axis=1)
        df_prices.columns = list(data.keys())
    
    if df_prices.empty:
        print("\n❌ ERROR: DataFrame is empty after creation!")
        exit(1)
    
    # Drop rows with any missing values to ensure all assets have data
    initial_rows = len(df_prices)
    df_prices.dropna(inplace=True)
    dropped_rows = initial_rows - len(df_prices)
    
    if dropped_rows > 0:
        print(f"\n⚠️  Dropped {dropped_rows} rows with missing data to align all assets")
    
    if df_prices.empty:
        print("\n❌ ERROR: No common trading days across all assets!")
        exit(1)
else:
    print("\n❌ ERROR: No data was downloaded!")
    exit(1)

print(f"\n✅ Data downloaded successfully!")
print(f"   Total trading days: {len(df_prices)}")
print(f"   Date range: {df_prices.index[0].date()} to {df_prices.index[-1].date()}")

# Save the raw prices to CSV
df_prices.to_csv('real_stock_prices_14_assets.csv')
print(f"\n💾 Raw prices saved to 'real_stock_prices_14_assets.csv'")

# Display current prices (latest available)
print(f"\n📈 CURRENT PRICES (as of {df_prices.index[-1].date()}):")
print("=" * 60)
for category, asset_list in assets.items():
    print(f"\n{category}:")
    for asset in asset_list:
        price = df_prices[asset].iloc[-1]
        print(f"   {asset_names[asset]:15s} ({asset:8s}): ${price:10.2f}")

# ============================================================================
# FEATURE ENGINEERING FOR BAGGING
# ============================================================================
print("\n" + "=" * 80)
print("FEATURE ENGINEERING - CREATING TECHNICAL INDICATORS")
print("=" * 80)

def calculate_features(df_prices):
    """Calculate technical indicators for ML features"""
    features_df = pd.DataFrame(index=df_prices.index)
    
    for asset in df_prices.columns:
        prices = df_prices[asset]
        
        # Returns (daily change percentage)
        features_df[f'{asset}_return'] = prices.pct_change()
        
        # Moving Averages
        features_df[f'{asset}_ma5'] = prices.rolling(window=5).mean()
        features_df[f'{asset}_ma20'] = prices.rolling(window=20).mean()
        features_df[f'{asset}_ma50'] = prices.rolling(window=50).mean()
        
        # Volatility (rolling standard deviation)
        features_df[f'{asset}_volatility'] = prices.pct_change().rolling(window=20).std()
        
        # RSI (Relative Strength Index)
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        features_df[f'{asset}_rsi'] = 100 - (100 / (1 + rs))
        
        # Price momentum
        features_df[f'{asset}_momentum'] = prices - prices.shift(10)
    
    return features_df

features_df = calculate_features(df_prices)
features_df.dropna(inplace=True)

print(f"✅ Features created: {features_df.shape[1]} features")
print(f"   Data points after feature engineering: {len(features_df)}")

# ============================================================================
# BAGGING CLASSIFICATION MODEL
# ============================================================================
print("\n" + "=" * 80)
print("MODELI 1: BAGGING CLASSIFICATION - PARASHIKIM I LËVIZJES SË ÇMIMIT")
print("=" * 80)

# Create target variable: 1 if TSLA price goes up tomorrow, 0 if down
target_classification = (df_prices['TSLA'].pct_change().shift(-1) > 0).astype(int)
target_classification = target_classification.loc[features_df.index]

# Select relevant features (use all assets' returns and technical indicators)
X_class = features_df[[col for col in features_df.columns if 'return' in col or 'rsi' in col or 'momentum' in col]]
X_class = X_class[:-1]  # Remove last row (no future target)
y_class = target_classification[:-1]

# Remove any remaining NaN values
mask = ~(X_class.isna().any(axis=1) | y_class.isna())
X_class = X_class[mask]
y_class = y_class[mask]

# Split data
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_class, y_class, test_size=0.2, random_state=42, shuffle=False
)

print(f"\n📊 Dataset Split:")
print(f"   Training set: {len(X_train_c)} samples")
print(f"   Test set: {len(X_test_c)} samples")
print(f"   Features: {X_train_c.shape[1]}")

# Create Bagging Classifier
base_classifier = DecisionTreeClassifier(max_depth=5, random_state=42)
bagging_classifier = BaggingClassifier(
    estimator=base_classifier,
    n_estimators=50,
    max_samples=0.8,
    max_features=0.8,
    random_state=42,
    oob_score=True
)

print(f"\n🤖 Training Bagging Classifier...")
print(f"   Base Estimator: Decision Tree (max_depth=5)")
print(f"   Number of Estimators: 50")
print(f"   Max Samples: 80%")
print(f"   Max Features: 80%")

bagging_classifier.fit(X_train_c, y_train_c)

# Predictions
y_pred_c = bagging_classifier.predict(X_test_c)

# Evaluation
accuracy = accuracy_score(y_test_c, y_pred_c)
oob_score = bagging_classifier.oob_score_

print(f"\n✅ REZULTATET - CLASSIFICATION:")
print(f"   Accuracy on Test Set: {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"   Out-of-Bag Score: {oob_score:.4f} ({oob_score*100:.2f}%)")

print(f"\n📊 Classification Report:")
print(classification_report(y_test_c, y_pred_c, target_names=['Down', 'Up']))

# ============================================================================
# BAGGING REGRESSION MODEL
# ============================================================================
print("\n" + "=" * 80)
print("MODELI 2: BAGGING REGRESSION - PARASHIKIM I ÇMIMIT ACTUAL")
print("=" * 80)

# Create target variable: Tomorrow's NVDA price
target_regression = df_prices['NVDA'].shift(-1)
target_regression = target_regression.loc[features_df.index]

# Use same features
X_reg = X_class.copy()
y_reg = target_regression[:-1][mask]

# Split data
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42, shuffle=False
)

# Create Bagging Regressor
base_regressor = DecisionTreeRegressor(max_depth=5, random_state=42)
bagging_regressor = BaggingRegressor(
    estimator=base_regressor,
    n_estimators=50,
    max_samples=0.8,
    max_features=0.8,
    random_state=42,
    oob_score=True
)

print(f"\n🤖 Training Bagging Regressor...")
print(f"   Base Estimator: Decision Tree (max_depth=5)")
print(f"   Number of Estimators: 50")

bagging_regressor.fit(X_train_r, y_train_r)

# Predictions
y_pred_r = bagging_regressor.predict(X_test_r)

# Evaluation
mse = mean_squared_error(y_test_r, y_pred_r)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_r, y_pred_r)
oob_score_r = bagging_regressor.oob_score_

print(f"\n✅ REZULTATET - REGRESSION:")
print(f"   R² Score: {r2:.4f}")
print(f"   RMSE: ${rmse:.2f}")
print(f"   Out-of-Bag Score: {oob_score_r:.4f}")
print(f"   Mean Actual Price: ${y_test_r.mean():.2f}")
print(f"   Mean Predicted Price: ${y_pred_r.mean():.2f}")

# ============================================================================
# COMPARISON: BAGGING VS SINGLE MODEL
# ============================================================================
print("\n" + "=" * 80)
print("KRAHASIMI: BAGGING VS SINGLE DECISION TREE")
print("=" * 80)

# Train single decision tree for classification
single_tree_c = DecisionTreeClassifier(max_depth=5, random_state=42)
single_tree_c.fit(X_train_c, y_train_c)
single_pred_c = single_tree_c.predict(X_test_c)
single_accuracy = accuracy_score(y_test_c, single_pred_c)

print(f"\n📊 CLASSIFICATION ACCURACY:")
print(f"   Single Decision Tree: {single_accuracy:.4f} ({single_accuracy*100:.2f}%)")
print(f"   Bagging (50 trees):   {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"   Improvement: {((accuracy - single_accuracy) / single_accuracy * 100):.2f}%")

# Train single decision tree for regression
single_tree_r = DecisionTreeRegressor(max_depth=5, random_state=42)
single_tree_r.fit(X_train_r, y_train_r)
single_pred_r = single_tree_r.predict(X_test_r)
single_r2 = r2_score(y_test_r, single_pred_r)
single_rmse = np.sqrt(mean_squared_error(y_test_r, single_pred_r))

print(f"\n📊 REGRESSION R² SCORE:")
print(f"   Single Decision Tree: {single_r2:.4f}")
print(f"   Bagging (50 trees):   {r2:.4f}")
print(f"   Improvement: {((r2 - single_r2) / abs(single_r2) * 100):.2f}%")

# ============================================================================
# FEATURE IMPORTANCE
# ============================================================================
print("\n" + "=" * 80)
print("FEATURE IMPORTANCE - TOP 10 FEATURES")
print("=" * 80)

# Get average feature importance across all trees
importances = np.mean([tree.feature_importances_ for tree in bagging_classifier.estimators_], axis=0)

# Debug: Check lengths
print(f"\nDebug - Features: {len(X_class.columns)}, Importances: {len(importances)}")

# Ensure lengths match
if len(importances) == len(X_class.columns):
    feature_importance = pd.DataFrame({
        'Feature': X_class.columns,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    print("\nTop 10 Most Important Features:")
    for idx, row in feature_importance.head(10).iterrows():
        print(f"   {row['Feature']:30s}: {row['Importance']:.4f}")
else:
    print(f"\n⚠️  Warning: Feature count mismatch. Skipping feature importance details.")
    # Create a generic feature importance without column names
    feature_importance = pd.DataFrame({
        'Feature': [f'Feature_{i}' for i in range(len(importances))],
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    print("\nTop 10 Most Important Features (by index):")
    for idx, row in feature_importance.head(10).iterrows():
        print(f"   {row['Feature']:30s}: {row['Importance']:.4f}")

# ============================================================================
# SAVE RESULTS
# ============================================================================
print("\n" + "=" * 80)
print("RUAJTJA E REZULTATEVE")
print("=" * 80)

# Create results summary
results_summary = {
    'Model': ['Bagging Classification', 'Single Tree Classification', 
              'Bagging Regression', 'Single Tree Regression'],
    'Metric': ['Accuracy', 'Accuracy', 'R² Score', 'R² Score'],
    'Score': [accuracy, single_accuracy, r2, single_r2],
    'OOB_Score': [oob_score, np.nan, oob_score_r, np.nan]
}

results_df = pd.DataFrame(results_summary)
results_df.to_csv('bagging_results_summary.csv', index=False)
print(f"\n💾 Results saved to 'bagging_results_summary.csv'")

# Save feature importance
feature_importance.to_csv('feature_importance.csv', index=False)
print(f"💾 Feature importance saved to 'feature_importance.csv'")

# Create predictions DataFrame
predictions_df = pd.DataFrame({
    'Date': X_test_c.index,
    'TSLA_Actual_Direction': y_test_c.values,
    'TSLA_Predicted_Direction': y_pred_c,
    'NVDA_Actual_Price': y_test_r.values,
    'NVDA_Predicted_Price': y_pred_r
})
predictions_df.to_csv('bagging_predictions.csv', index=False)
print(f"💾 Predictions saved to 'bagging_predictions.csv'")

print("\n" + "=" * 80)
print("PËRFUNDIM")
print("=" * 80)
print(f"\n✅ Analiza u përfundua me sukses!")
print(f"\n📁 Skedarët e krijuar:")
print(f"   1. real_stock_prices_14_assets.csv - Çmimet historike")
print(f"   2. bagging_results_summary.csv - Përmbledhje e rezultateve")
print(f"   3. feature_importance.csv - Rëndësia e features")
print(f"   4. bagging_predictions.csv - Parashikimet")

print(f"\n📤 Për të dërguar në server (krenuser@185.182.158.150:8022):")
print(f"   scp -P 8022 *.csv krenuser@185.182.158.150:~/bagging_project/")
print(f"   scp -P 8022 bagging_analysis.py krenuser@185.182.158.150:~/bagging_project/")

print("\n" + "=" * 80)

# ============================================================================
# PORTFOLIO OPTIMIZATION WITH BAGGING
# ============================================================================
print("\n" + "=" * 80)
print("PORTFOLIO OPTIMIZATION - BAGGING FOR ASSET SELECTION")
print("=" * 80)

# Calculate returns for each asset
returns_df = df_prices.pct_change().dropna()

# Calculate key metrics
metrics_data = []
for asset in all_assets:
    returns = returns_df[asset]
    metrics_data.append({
        'Asset': asset_names[asset],
        'Symbol': asset,
        'Mean_Return_%': returns.mean() * 100,
        'Volatility_%': returns.std() * 100,
        'Sharpe_Ratio': (returns.mean() / returns.std()) * np.sqrt(252),
        'Max_Drawdown_%': ((df_prices[asset] / df_prices[asset].cummax()) - 1).min() * 100,
        'Current_Price': df_prices[asset].iloc[-1]
    })

metrics_df = pd.DataFrame(metrics_data).sort_values('Sharpe_Ratio', ascending=False)
metrics_df.to_csv('asset_performance_metrics.csv', index=False)

print("\n📊 TOP 5 ASSETS BY SHARPE RATIO:")
for idx, row in metrics_df.head(5).iterrows():
    print(f"   {row['Asset']:15s}: Sharpe={row['Sharpe_Ratio']:.3f}, Return={row['Mean_Return_%']:.2f}%, Vol={row['Volatility_%']:.2f}%")

print(f"\n💾 Performance metrics saved to 'asset_performance_metrics.csv'")

# ============================================================================
# ENSEMBLE MODEL COMPARISON
# ============================================================================
print("\n" + "=" * 80)
print("ENSEMBLE COMPARISON: BAGGING VS RANDOM FOREST")
print("=" * 80)

# Train Random Forest for comparison
rf_classifier = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
rf_classifier.fit(X_train_c, y_train_c)
rf_pred_c = rf_classifier.predict(X_test_c)
rf_accuracy = accuracy_score(y_test_c, rf_pred_c)

print(f"\n📊 CLASSIFICATION COMPARISON:")
print(f"   Bagging:        {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"   Random Forest:  {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")
print(f"   Single Tree:    {single_accuracy:.4f} ({single_accuracy*100:.2f}%)")

# Save comprehensive comparison
comparison_df = pd.DataFrame({
    'Model': ['Bagging Classifier', 'Random Forest', 'Single Decision Tree',
              'Bagging Regressor', 'Single Tree Regressor'],
    'Task': ['Classification', 'Classification', 'Classification', 'Regression', 'Regression'],
    'Score': [accuracy, rf_accuracy, single_accuracy, r2, single_r2],
    'Metric': ['Accuracy', 'Accuracy', 'Accuracy', 'R²', 'R²']
})
comparison_df.to_csv('ensemble_model_comparison.csv', index=False)
print(f"\n💾 Model comparison saved to 'ensemble_model_comparison.csv'")

print(f"\n📁 TOTAL FILES CREATED: 6")
print(f"   1. real_stock_prices_14_assets.csv")
print(f"   2. bagging_results_summary.csv")
print(f"   3. feature_importance.csv")
print(f"   4. bagging_predictions.csv")
print(f"   5. asset_performance_metrics.csv")
print(f"   6. ensemble_model_comparison.csv")

print(f"\n📤 DEPLOYMENT TO SERVER:")
print(f"   ssh -p 8022 krenuser@185.182.158.150")
print(f"   mkdir -p ~/bagging_project")
print(f"   exit")
print(f"   scp -P 8022 *.csv krenuser@185.182.158.150:~/bagging_project/")
print(f"   scp -P 8022 *.py krenuser@185.182.158.150:~/bagging_project/")

print("\n" + "=" * 80)
print("✅ ANALIZA E PLOTË E BAGGING PËRFUNDOI!")
print("=" * 80)

