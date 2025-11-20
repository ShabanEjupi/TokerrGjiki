#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
ML PREDICTOR - Real-Time Predictions
================================================================================
Loads trained ML models and makes real-time predictions
Uses ensemble voting for robust predictions

MODELS LOADED:
- Random Forest
- Gradient Boosting
- Logistic Regression
- SVM
- K-Means (for market regime)
- PCA (for dimensionality reduction)
================================================================================
"""

import os
import sys
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import happybase
    HBASE_AVAILABLE = True
except ImportError:
    HBASE_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

ASSETS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX',
          'GC=F', 'SI=F', 'CL=F', 'NG=F', '^GSPC', '^IXIC']

ASSET_NAMES = {
    'AAPL': 'Apple', 'GOOGL': 'Google', 'MSFT': 'Microsoft', 'AMZN': 'Amazon',
    'NVDA': 'NVIDIA', 'TSLA': 'Tesla', 'META': 'Meta', 'NFLX': 'Netflix',
    'GC=F': 'Gold', 'SI=F': 'Silver', 'CL=F': 'Crude Oil', 'NG=F': 'Natural Gas',
    '^GSPC': 'S&P 500', '^IXIC': 'NASDAQ'
}

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

# HBase
HBASE_HOST = "localhost"
HBASE_PORT = 9090
FEATURES_TABLE = "asset_features"
PREDICTIONS_TABLE = "ml_predictions"

# Cluster names
CLUSTER_NAMES = {
    0: "Bull Market",
    1: "Bear Market", 
    2: "High Volatility",
    3: "Stable Market"
}

# ============================================================================
# MODEL LOADER
# ============================================================================

class MLPredictor:
    """Load and use trained ML models for predictions"""
    
    def __init__(self):
        self.models = {}
        self.scaler = None
        self.metadata = None
        self.load_all_models()
    
    def load_all_models(self):
        """Load all trained models"""
        print("🔄 Loading trained models...")
        
        # Load scaler
        scaler_path = os.path.join(MODELS_DIR, 'scaler.pkl')
        if os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            print("   ✓ Scaler loaded")
        else:
            print("   ✗ Scaler not found")
        
        # Load supervised models
        model_files = {
            'random_forest': 'random_forest.pkl',
            'gradient_boosting': 'gradient_boosting.pkl',
            'logistic_regression': 'logistic_regression.pkl',
            'svm': 'svm.pkl'
        }
        
        for name, filename in model_files.items():
            path = os.path.join(MODELS_DIR, filename)
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    self.models[name] = pickle.load(f)
                print(f"   ✓ {name} loaded")
            else:
                print(f"   ✗ {name} not found")
        
        # Load unsupervised models
        kmeans_path = os.path.join(MODELS_DIR, 'kmeans.pkl')
        if os.path.exists(kmeans_path):
            with open(kmeans_path, 'rb') as f:
                self.models['kmeans'] = pickle.load(f)
            print(f"   ✓ K-Means loaded")
        
        pca_path = os.path.join(MODELS_DIR, 'pca.pkl')
        if os.path.exists(pca_path):
            with open(pca_path, 'rb') as f:
                self.models['pca'] = pickle.load(f)
            print(f"   ✓ PCA loaded")
        
        # Load metadata
        metadata_path = os.path.join(MODELS_DIR, 'training_metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            print(f"   ✓ Training metadata loaded")
            print(f"   Training date: {self.metadata.get('training_date', 'Unknown')}")
            print(f"   Best model: {self.metadata.get('best_model', 'Unknown')}")
        
        print(f"\n✅ Loaded {len(self.models)} models")
    
    def predict_single(self, features):
        """Make prediction for a single sample"""
        
        if self.scaler is None:
            print("❌ Scaler not loaded!")
            return None
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        predictions = {}
        probabilities = {}
        
        # Get predictions from all models
        for name, model in self.models.items():
            if name in ['kmeans', 'pca']:
                continue  # Skip unsupervised for classification
            
            try:
                pred = model.predict(features_scaled)[0]
                prob = model.predict_proba(features_scaled)[0]
                
                predictions[name] = pred
                probabilities[name] = prob[1]  # Probability of UP
            except Exception as e:
                print(f"   Warning: {name} prediction failed: {e}")
        
        # Ensemble voting
        if predictions:
            ensemble_prediction = int(np.mean(list(predictions.values())) > 0.5)
            ensemble_confidence = np.mean(list(probabilities.values()))
        else:
            ensemble_prediction = 0
            ensemble_confidence = 0.5
        
        # Market regime from K-Means
        market_regime = None
        if 'kmeans' in self.models:
            try:
                cluster = self.models['kmeans'].predict(features_scaled)[0]
                market_regime = CLUSTER_NAMES.get(cluster, f"Cluster {cluster}")
            except:
                pass
        
        return {
            'prediction': ensemble_prediction,
            'direction': 'UP' if ensemble_prediction == 1 else 'DOWN',
            'confidence': float(ensemble_confidence),
            'individual_predictions': predictions,
            'individual_probabilities': probabilities,
            'market_regime': market_regime
        }
    
    def predict_batch(self, df):
        """Make predictions for multiple samples"""
        
        predictions = []
        
        for idx, row in df.iterrows():
            features = [row[col] for col in FEATURE_COLUMNS]
            pred = self.predict_single(features)
            
            if pred:
                pred['asset'] = row.get('asset', 'Unknown')
                pred['timestamp'] = row.get('timestamp', datetime.now().isoformat())
                pred['current_price'] = row.get('close', 0.0)
                predictions.append(pred)
        
        return predictions

# ============================================================================
# DATA LOADING
# ============================================================================

def load_latest_features_from_csv(asset=None):
    """Load latest features from CSV"""
    csv_file = os.path.join(DATA_DIR, 'processed_features.csv')
    
    if not os.path.exists(csv_file):
        return None
    
    df = pd.read_csv(csv_file)
    
    # Get latest record for each asset
    if asset:
        df = df[df['asset'] == asset]
    
    latest_records = []
    for asset_name in df['asset'].unique():
        asset_df = df[df['asset'] == asset_name]
        latest = asset_df.iloc[-1]
        latest_records.append(latest)
    
    return pd.DataFrame(latest_records)

def load_latest_features_from_hbase(asset=None):
    """Load latest features from HBase"""
    if not HBASE_AVAILABLE:
        return None
    
    try:
        connection = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
        table = connection.table(FEATURES_TABLE)
        
        assets_to_load = [asset] if asset else ASSETS
        
        rows = []
        for asset_name in assets_to_load:
            # Get latest record for this asset
            latest_rows = []
            for key, data in table.scan(row_prefix=asset_name.encode('utf-8'), limit=1, reversed=True):
                row = {
                    'asset': data[b'metadata:asset'].decode('utf-8'),
                    'timestamp': data[b'metadata:timestamp'].decode('utf-8'),
                    'close': float(data[b'price:close']),
                }
                
                # Add features
                for feature in FEATURE_COLUMNS:
                    try:
                        row[feature] = float(data[f'features:{feature}'.encode('utf-8')])
                    except:
                        row[feature] = 0.0
                
                latest_rows.append(row)
            
            if latest_rows:
                rows.append(latest_rows[0])
        
        connection.close()
        
        return pd.DataFrame(rows) if rows else None
        
    except Exception as e:
        print(f"❌ Error loading from HBase: {e}")
        return None

# ============================================================================
# SAVE PREDICTIONS
# ============================================================================

def save_predictions_to_hbase(predictions):
    """Save predictions to HBase"""
    if not HBASE_AVAILABLE:
        return False
    
    try:
        connection = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
        
        # Create table if doesn't exist
        tables = [t.decode('utf-8') for t in connection.tables()]
        if PREDICTIONS_TABLE not in tables:
            connection.create_table(
                PREDICTIONS_TABLE,
                {
                    'prediction': dict(),
                    'metadata': dict()
                }
            )
        
        table = connection.table(PREDICTIONS_TABLE)
        
        for pred in predictions:
            row_key = f"{pred['asset']}_{pred['timestamp']}".encode('utf-8')
            
            data = {
                b'metadata:asset': pred['asset'].encode('utf-8'),
                b'metadata:timestamp': pred['timestamp'].encode('utf-8'),
                b'prediction:direction': pred['direction'].encode('utf-8'),
                b'prediction:confidence': str(pred['confidence']).encode('utf-8'),
                b'prediction:market_regime': str(pred.get('market_regime', 'Unknown')).encode('utf-8'),
                b'prediction:current_price': str(pred['current_price']).encode('utf-8'),
            }
            
            table.put(row_key, data)
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error saving to HBase: {e}")
        return False

def save_predictions_to_json(predictions):
    """Save predictions to JSON file"""
    output_file = os.path.join(DATA_DIR, 'latest_predictions.json')
    
    # Convert numpy types to native Python types for JSON serialization
    def convert_to_native(obj):
        if isinstance(obj, dict):
            return {k: convert_to_native(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_native(item) for item in obj]
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
    
    predictions_native = convert_to_native(predictions)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(predictions_native, f, indent=4)
    
    return True

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main prediction function"""
    
    print("="*80)
    print("ML PREDICTOR - Real-Time Predictions")
    print("="*80)
    
    # Initialize predictor
    predictor = MLPredictor()
    
    if not predictor.models:
        print("\n❌ No models loaded!")
        print("   Please run ml_trainer.py first to train models.")
        return
    
    # Load latest features
    print(f"\n📂 Loading latest features...")
    df = load_latest_features_from_hbase()
    
    if df is None:
        print("   HBase not available, trying CSV...")
        df = load_latest_features_from_csv()
    
    if df is None or df.empty:
        print("\n❌ No data available for predictions!")
        return
    
    print(f"✅ Loaded features for {len(df)} assets")
    
    # Make predictions
    print(f"\n🔮 Making predictions...\n")
    print(f"{'='*80}")
    
    predictions = predictor.predict_batch(df)
    
    # Display predictions
    for pred in predictions:
        asset = pred['asset']
        name = ASSET_NAMES.get(asset, asset)
        direction = pred['direction']
        confidence = pred['confidence']
        regime = pred.get('market_regime', 'Unknown')
        price = pred['current_price']
        
        # Color coding
        if direction == 'UP':
            direction_symbol = '📈'
            confidence_color = '\033[92m' if confidence > 0.6 else '\033[93m'
        else:
            direction_symbol = '📉'
            confidence_color = '\033[91m' if confidence > 0.6 else '\033[93m'
        
        print(f"{direction_symbol} {name:15s} ({asset:8s})")
        print(f"   Direction: {confidence_color}{direction}\033[0m")
        print(f"   Confidence: {confidence_color}{confidence:.1%}\033[0m")
        print(f"   Current Price: ${price:.2f}")
        print(f"   Market Regime: {regime}")
        
        # Individual model predictions
        print(f"   Individual Models:")
        for model_name, prob in pred['individual_probabilities'].items():
            model_pred = 'UP' if prob > 0.5 else 'DOWN'
            print(f"      {model_name:20s}: {model_pred:4s} ({prob:.1%})")
        
        print()
    
    print(f"{'='*80}")
    
    # Save predictions
    print(f"\n💾 Saving predictions...")
    
    saved_hbase = save_predictions_to_hbase(predictions)
    saved_json = save_predictions_to_json(predictions)
    
    if saved_hbase:
        print(f"   ✓ Saved to HBase table: {PREDICTIONS_TABLE}")
    else:
        print(f"   ✗ HBase save failed")
    
    if saved_json:
        print(f"   ✓ Saved to JSON: {os.path.join(DATA_DIR, 'latest_predictions.json')}")
    
    print(f"\n✅ Prediction completed!\n")

if __name__ == "__main__":
    main()
