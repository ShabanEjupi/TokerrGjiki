#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ML TRAINER - Supervised & Unsupervised Learning
================================================================================
SUPERVISED ALGORITHMS:
- Random Forest Classifier
- Gradient Boosting (XGBoost)
- Logistic Regression
- Support Vector Machine (SVM)

UNSUPERVISED ALGORITHMS:
- K-Means Clustering (Market Regimes)
- PCA (Principal Component Analysis)

Trains models on processed features and saves them for prediction
================================================================================
"""

import os
import sys
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime

# Scikit-learn imports
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)

# Supervised Learning Models
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Unsupervised Learning Models
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Handle warnings
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import happybase
    HBASE_AVAILABLE = True
except ImportError:
    print("⚠️  happybase not installed. Using CSV mode.")
    HBASE_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

ASSETS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX',
          'GC=F', 'SI=F', 'CL=F', 'NG=F', '^GSPC', '^IXIC']

# Feature columns for ML
FEATURE_COLUMNS = [
    'return', 'ma_5', 'ma_14', 'ma_20', 'ma_50',
    'volatility_14', 'volatility_20',
    'momentum_7', 'momentum_14',
    'rsi', 'bb_upper', 'bb_middle', 'bb_lower',
    'price_to_ma5', 'price_to_ma20'
]

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Create models directory if it doesn't exist
os.makedirs(MODELS_DIR, exist_ok=True)

# HBase Configuration
HBASE_HOST = "localhost"
HBASE_PORT = 9090
FEATURES_TABLE = "asset_features"

# ============================================================================
# DATA LOADING
# ============================================================================

def load_data_from_csv():
    """Load processed features from CSV"""
    csv_file = os.path.join(DATA_DIR, 'processed_features.csv')
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return None
    
    print(f"📂 Loading data from CSV: {csv_file}")
    df = pd.read_csv(csv_file)
    
    print(f"✅ Loaded {len(df)} records")
    return df

def load_data_from_hbase():
    """Load processed features from HBase"""
    if not HBASE_AVAILABLE:
        return None
    
    try:
        print(f"📂 Loading data from HBase table: {FEATURES_TABLE}")
        connection = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
        table = connection.table(FEATURES_TABLE)
        
        rows = []
        for key, data in table.scan():
            row = {
                'asset': data[b'metadata:asset'].decode('utf-8'),
                'timestamp': data[b'metadata:timestamp'].decode('utf-8'),
                'close': float(data[b'price:close']),
                'high': float(data[b'price:high']),
                'low': float(data[b'price:low']),
                'volume': int(data[b'price:volume']),
            }
            
            # Add features
            for feature in FEATURE_COLUMNS:
                try:
                    row[feature] = float(data[f'features:{feature}'.encode('utf-8')])
                except:
                    row[feature] = 0.0
            
            # Add label
            try:
                row['label'] = int(float(data[b'features:label']))
            except:
                row['label'] = 0
            
            rows.append(row)
        
        connection.close()
        
        df = pd.DataFrame(rows)
        print(f"✅ Loaded {len(df)} records from HBase")
        return df
        
    except Exception as e:
        print(f"❌ Error loading from HBase: {e}")
        return None

def prepare_ml_data(df):
    """Prepare data for ML training"""
    
    print(f"\n{'='*80}")
    print("PREPARING DATA FOR MACHINE LEARNING")
    print(f"{'='*80}\n")
    
    # Remove rows with NaN values
    print(f"Original records: {len(df)}")
    df = df.dropna(subset=FEATURE_COLUMNS + ['label'])
    print(f"After removing NaN: {len(df)}")
    
    # Remove inf values
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    print(f"After removing inf: {len(df)}")
    
    if len(df) < 100:
        print("❌ Not enough data for training (need at least 100 records)")
        return None, None, None, None, None
    
    # Split features and labels
    X = df[FEATURE_COLUMNS].values
    y = df['label'].values
    assets = df['asset'].values
    timestamps = df['timestamp'].values
    prices = df['close'].values
    
    print(f"\n📊 Dataset Statistics:")
    print(f"   Total samples: {len(X)}")
    print(f"   Features: {len(FEATURE_COLUMNS)}")
    print(f"   Positive class (UP): {np.sum(y == 1)} ({100*np.mean(y == 1):.1f}%)")
    print(f"   Negative class (DOWN): {np.sum(y == 0)} ({100*np.mean(y == 0):.1f}%)")
    
    # Feature scaling
    print(f"\n🔄 Applying feature scaling (StandardScaler)...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Save scaler
    scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"   Scaler saved to: {scaler_path}")
    
    return X_scaled, y, assets, timestamps, prices

# ============================================================================
# SUPERVISED LEARNING - CLASSIFICATION
# ============================================================================

def train_random_forest(X_train, X_test, y_train, y_test):
    """Train Random Forest Classifier"""
    
    print(f"\n{'='*80}")
    print("TRAINING: RANDOM FOREST CLASSIFIER")
    print(f"{'='*80}\n")
    
    print("🌲 Initializing Random Forest...")
    
    # Train model
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    print("🔄 Training model...")
    rf.fit(X_train, y_train)
    
    # Predictions
    y_pred = rf.predict(X_test)
    y_pred_proba = rf.predict_proba(X_test)[:, 1]
    
    # Evaluation
    print("\n📊 Model Performance:")
    print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"   Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"   Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"   F1-Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"   ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    # Feature importance
    print("\n🔍 Top 5 Feature Importances:")
    feature_importance = sorted(
        zip(FEATURE_COLUMNS, rf.feature_importances_),
        key=lambda x: x[1],
        reverse=True
    )
    for feature, importance in feature_importance[:5]:
        print(f"   {feature:20s}: {importance:.4f}")
    
    # Save model
    model_path = os.path.join(MODELS_DIR, 'random_forest.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(rf, f)
    print(f"\n✅ Model saved to: {model_path}")
    
    return rf, {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }

def train_gradient_boosting(X_train, X_test, y_train, y_test):
    """Train Gradient Boosting Classifier"""
    
    print(f"\n{'='*80}")
    print("TRAINING: GRADIENT BOOSTING CLASSIFIER")
    print(f"{'='*80}\n")
    
    print("⚡ Initializing Gradient Boosting...")
    
    # Train model
    gb = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        min_samples_split=5,
        min_samples_leaf=2,
        subsample=0.8,
        random_state=42
    )
    
    print("🔄 Training model...")
    gb.fit(X_train, y_train)
    
    # Predictions
    y_pred = gb.predict(X_test)
    y_pred_proba = gb.predict_proba(X_test)[:, 1]
    
    # Evaluation
    print("\n📊 Model Performance:")
    print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"   Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"   Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"   F1-Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"   ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    # Save model
    model_path = os.path.join(MODELS_DIR, 'gradient_boosting.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(gb, f)
    print(f"\n✅ Model saved to: {model_path}")
    
    return gb, {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }

def train_logistic_regression(X_train, X_test, y_train, y_test):
    """Train Logistic Regression"""
    
    print(f"\n{'='*80}")
    print("TRAINING: LOGISTIC REGRESSION")
    print(f"{'='*80}\n")
    
    print("📈 Initializing Logistic Regression...")
    
    # Train model
    lr = LogisticRegression(
        C=1.0,
        max_iter=1000,
        random_state=42,
        n_jobs=-1
    )
    
    print("🔄 Training model...")
    lr.fit(X_train, y_train)
    
    # Predictions
    y_pred = lr.predict(X_test)
    y_pred_proba = lr.predict_proba(X_test)[:, 1]
    
    # Evaluation
    print("\n📊 Model Performance:")
    print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"   Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"   Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"   F1-Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"   ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    # Save model
    model_path = os.path.join(MODELS_DIR, 'logistic_regression.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(lr, f)
    print(f"\n✅ Model saved to: {model_path}")
    
    return lr, {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }

def train_svm(X_train, X_test, y_train, y_test):
    """Train Support Vector Machine"""
    
    print(f"\n{'='*80}")
    print("TRAINING: SUPPORT VECTOR MACHINE (SVM)")
    print(f"{'='*80}\n")
    
    print("🎯 Initializing SVM...")
    
    # Train model (using small sample for speed)
    # In production, use all data or GPU-based SVM
    sample_size = min(5000, len(X_train))
    indices = np.random.choice(len(X_train), sample_size, replace=False)
    X_train_sample = X_train[indices]
    y_train_sample = y_train[indices]
    
    svm = SVC(
        kernel='rbf',
        C=1.0,
        gamma='scale',
        probability=True,
        random_state=42
    )
    
    print(f"🔄 Training model (using {sample_size} samples for speed)...")
    svm.fit(X_train_sample, y_train_sample)
    
    # Predictions
    y_pred = svm.predict(X_test)
    y_pred_proba = svm.predict_proba(X_test)[:, 1]
    
    # Evaluation
    print("\n📊 Model Performance:")
    print(f"   Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"   Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"   Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"   F1-Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"   ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    # Save model
    model_path = os.path.join(MODELS_DIR, 'svm.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(svm, f)
    print(f"\n✅ Model saved to: {model_path}")
    
    return svm, {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_pred_proba)
    }

# ============================================================================
# UNSUPERVISED LEARNING
# ============================================================================

def train_kmeans_clustering(X):
    """Train K-Means for market regime detection"""
    
    print(f"\n{'='*80}")
    print("TRAINING: K-MEANS CLUSTERING (Market Regimes)")
    print(f"{'='*80}\n")
    
    print("🎪 Initializing K-Means...")
    
    # Determine optimal number of clusters using elbow method
    print("🔍 Finding optimal number of clusters...")
    inertias = []
    K_range = range(2, 8)
    
    for k in K_range:
        kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans_temp.fit(X)
        inertias.append(kmeans_temp.inertia_)
    
    # Use 4 clusters for market regimes: Bull, Bear, Volatile, Stable
    optimal_k = 4
    print(f"   Using {optimal_k} clusters (Bull, Bear, Volatile, Stable)")
    
    # Train final model
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    print("🔄 Training model...")
    clusters = kmeans.fit_predict(X)
    
    # Analysis
    print("\n📊 Cluster Distribution:")
    unique, counts = np.unique(clusters, return_counts=True)
    for cluster_id, count in zip(unique, counts):
        print(f"   Cluster {cluster_id}: {count} samples ({100*count/len(clusters):.1f}%)")
    
    print(f"\n📍 Cluster Centers Shape: {kmeans.cluster_centers_.shape}")
    
    # Save model
    model_path = os.path.join(MODELS_DIR, 'kmeans.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(kmeans, f)
    print(f"✅ Model saved to: {model_path}")
    
    return kmeans, clusters

def train_pca(X):
    """Train PCA for dimensionality reduction"""
    
    print(f"\n{'='*80}")
    print("TRAINING: PRINCIPAL COMPONENT ANALYSIS (PCA)")
    print(f"{'='*80}\n")
    
    print("🔬 Initializing PCA...")
    
    # Train PCA to capture 95% of variance
    pca = PCA(n_components=0.95, random_state=42)
    print("🔄 Training model...")
    X_pca = pca.fit_transform(X)
    
    # Analysis
    print("\n📊 PCA Results:")
    print(f"   Original dimensions: {X.shape[1]}")
    print(f"   Reduced dimensions: {X_pca.shape[1]}")
    print(f"   Explained variance: {100*pca.explained_variance_ratio_.sum():.2f}%")
    
    print("\n🔍 Top 5 Principal Components:")
    for i, var in enumerate(pca.explained_variance_ratio_[:5], 1):
        print(f"   PC{i}: {100*var:.2f}% variance")
    
    # Save model
    model_path = os.path.join(MODELS_DIR, 'pca.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(pca, f)
    print(f"✅ Model saved to: {model_path}")
    
    return pca, X_pca

# ============================================================================
# ENSEMBLE & MODEL COMPARISON
# ============================================================================

def compare_models(results):
    """Compare all trained models"""
    
    print(f"\n{'='*80}")
    print("MODEL COMPARISON")
    print(f"{'='*80}\n")
    
    print(f"{'Model':<25s} {'Accuracy':>10s} {'Precision':>10s} {'Recall':>10s} {'F1-Score':>10s} {'ROC-AUC':>10s}")
    print("-" * 80)
    
    for model_name, metrics in results.items():
        print(f"{model_name:<25s} "
              f"{metrics['accuracy']:>10.4f} "
              f"{metrics['precision']:>10.4f} "
              f"{metrics['recall']:>10.4f} "
              f"{metrics['f1_score']:>10.4f} "
              f"{metrics['roc_auc']:>10.4f}")
    
    # Find best model
    best_model = max(results.items(), key=lambda x: x[1]['f1_score'])
    print("\n" + "-" * 80)
    print(f"🏆 Best Model (by F1-Score): {best_model[0]}")
    print(f"   F1-Score: {best_model[1]['f1_score']:.4f}")

# ============================================================================
# SAVE METADATA
# ============================================================================

def save_training_metadata(results, training_time):
    """Save training metadata and results"""
    
    metadata = {
        'training_date': datetime.now().isoformat(),
        'training_time_seconds': training_time,
        'assets': ASSETS,
        'features': FEATURE_COLUMNS,
        'models': results,
        'best_model': max(results.items(), key=lambda x: x[1]['f1_score'])[0]
    }
    
    metadata_path = os.path.join(MODELS_DIR, 'training_metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    print(f"\n💾 Training metadata saved to: {metadata_path}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main training function"""
    
    start_time = datetime.now()
    
    print("="*80)
    print("MACHINE LEARNING TRAINER")
    print("Supervised & Unsupervised Learning for Financial Predictions")
    print("="*80)
    
    # Load data
    print("\n📂 Loading processed features...")
    df = load_data_from_hbase()
    
    if df is None:
        print("   HBase not available, trying CSV...")
        df = load_data_from_csv()
    
    if df is None:
        print("\n❌ No data available for training!")
        print("   Please run spark_streaming_processor.py first.")
        return
    
    # Prepare data
    X, y, assets, timestamps, prices = prepare_ml_data(df)
    
    if X is None:
        return
    
    # Train-test split
    print(f"\n🔪 Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Train all supervised models
    results = {}
    
    # Random Forest
    _, rf_metrics = train_random_forest(X_train, X_test, y_train, y_test)
    results['Random Forest'] = rf_metrics
    
    # Gradient Boosting
    _, gb_metrics = train_gradient_boosting(X_train, X_test, y_train, y_test)
    results['Gradient Boosting'] = gb_metrics
    
    # Logistic Regression
    _, lr_metrics = train_logistic_regression(X_train, X_test, y_train, y_test)
    results['Logistic Regression'] = lr_metrics
    
    # SVM
    _, svm_metrics = train_svm(X_train, X_test, y_train, y_test)
    results['SVM'] = svm_metrics
    
    # Compare models
    compare_models(results)
    
    # Train unsupervised models
    train_kmeans_clustering(X)
    train_pca(X)
    
    # Save metadata
    training_time = (datetime.now() - start_time).total_seconds()
    save_training_metadata(results, training_time)
    
    print(f"\n{'='*80}")
    print(f"✅ TRAINING COMPLETED!")
    print(f"   Total time: {training_time:.2f} seconds")
    print(f"   Models saved in: {MODELS_DIR}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
