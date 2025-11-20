#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
FLASK WEB APPLICATION
Real-Time Financial Dashboard Backend
================================================================================
REST API for real-time financial data visualization
Endpoints: live prices, charts, predictions, portfolio recommendations
================================================================================
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import json
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import happybase
    HBASE_AVAILABLE = True
except ImportError:
    print("⚠️  happybase not installed. Using CSV mode.")
    HBASE_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Assets
ASSETS = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX',
          'GC=F', 'SI=F', 'CL=F', 'NG=F', '^GSPC', '^IXIC']

ASSET_NAMES = {
    'AAPL': 'Apple', 'GOOGL': 'Google', 'MSFT': 'Microsoft', 'AMZN': 'Amazon',
    'NVDA': 'NVIDIA', 'TSLA': 'Tesla', 'META': 'Meta', 'NFLX': 'Netflix',
    'GC=F': 'Gold', 'SI=F': 'Silver', 'CL=F': 'Crude Oil', 'NG=F': 'Natural Gas',
    '^GSPC': 'S&P 500', '^IXIC': 'NASDAQ'
}

# HBase Configuration
HBASE_HOST = 'localhost'
HBASE_PORT = 9090

# Data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Portfolio recommendation (from your analysis)
RECOMMENDED_PORTFOLIO = {
    'allocation': {
        'GC=F': {'weight': 0.40, 'name': 'Gold', 'reason': 'Stability & Safety'},
        'NVDA': {'weight': 0.25, 'name': 'NVIDIA', 'reason': 'High Growth'},
        'SI=F': {'weight': 0.15, 'name': 'Silver', 'reason': 'Diversification'},
        'META': {'weight': 0.10, 'name': 'Meta', 'reason': 'Tech Exposure'},
        'MSFT': {'weight': 0.10, 'name': 'Microsoft', 'reason': 'Stable Tech'}
    },
    'metrics': {
        'expected_return': 0.38,  # 38% annual
        'sharpe_ratio': 0.95,
        'volatility': 0.12  # 12%
    }
}

# ============================================================================
# HBASE CONNECTION
# ============================================================================

def get_hbase_connection():
    """Get HBase connection"""
    if not HBASE_AVAILABLE:
        return None
    
    try:
        connection = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
        return connection
    except Exception as e:
        print(f"HBase connection error: {e}")
        return None

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_latest_prices_from_csv():
    """Load latest prices from CSV (fallback mode)"""
    csv_file = os.path.join(DATA_DIR, 'realtime_prices.csv')
    
    if not os.path.exists(csv_file):
        return {}
    
    try:
        df = pd.read_csv(csv_file)
        
        # Get latest price for each asset
        latest_prices = {}
        for asset in ASSETS:
            asset_data = df[df['asset'] == asset]
            if not asset_data.empty:
                latest = asset_data.iloc[-1]
                latest_prices[asset] = {
                    'price': float(latest['close']),
                    'timestamp': latest['timestamp'],
                    'name': ASSET_NAMES.get(asset, asset),
                    'high': float(latest['high']),
                    'low': float(latest['low']),
                    'volume': int(latest['volume'])
                }
        
        return latest_prices
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return {}

def load_latest_prices_from_hbase(connection):
    """Load latest prices from HBase"""
    if connection is None:
        return {}
    
    try:
        table = connection.table('asset_prices')
        latest_prices = {}
        
        for asset in ASSETS:
            # Get latest record for this asset
            rows = []
            for key, data in table.scan(row_prefix=asset.encode('utf-8'), limit=1, reversed=True):
                rows.append((key, data))
            
            if rows:
                key, data = rows[0]
                latest_prices[asset] = {
                    'price': float(data[b'price:close']),
                    'timestamp': data[b'metadata:timestamp'].decode('utf-8'),
                    'name': data[b'metadata:name'].decode('utf-8'),
                    'high': float(data[b'price:high']),
                    'low': float(data[b'price:low']),
                    'volume': int(data[b'price:volume'])
                }
        
        return latest_prices
    except Exception as e:
        print(f"Error loading from HBase: {e}")
        return {}

def load_historical_data(asset, hours=24):
    """Load historical data for charts"""
    # Try HBase first
    connection = get_hbase_connection()
    
    if connection:
        try:
            table = connection.table('asset_prices')
            
            # Calculate number of records needed (one per 5 minutes)
            limit = hours * 12  # 12 records per hour
            
            data = []
            for key, values in table.scan(row_prefix=asset.encode('utf-8'), limit=limit, reversed=True):
                data.append({
                    'timestamp': values[b'metadata:timestamp'].decode('utf-8'),
                    'price': float(values[b'price:close']),
                    'high': float(values[b'price:high']),
                    'low': float(values[b'price:low']),
                    'volume': int(values[b'price:volume'])
                })
            
            connection.close()
            return data[::-1]  # Reverse to chronological order
            
        except Exception as e:
            print(f"Error loading historical data from HBase: {e}")
    
    # Fallback to CSV
    csv_file = os.path.join(DATA_DIR, 'realtime_prices.csv')
    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
            asset_data = df[df['asset'] == asset].tail(hours * 12)
            
            return asset_data[['timestamp', 'close', 'high', 'low', 'volume']].rename(
                columns={'close': 'price'}
            ).to_dict('records')
        except Exception as e:
            print(f"Error loading from CSV: {e}")
    
    return []

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/')
def index():
    """Homepage - Dashboard"""
    return render_template('dashboard.html', assets=ASSETS, asset_names=ASSET_NAMES)

@app.route('/api/live-prices')
def get_live_prices():
    """Get current prices for all assets"""
    connection = get_hbase_connection()
    
    if connection:
        prices = load_latest_prices_from_hbase(connection)
        connection.close()
    else:
        prices = load_latest_prices_from_csv()
    
    return jsonify(prices)

@app.route('/api/asset/<asset>')
def get_asset_details(asset):
    """Get detailed information for a specific asset"""
    if asset not in ASSETS:
        return jsonify({'error': 'Asset not found'}), 404
    
    connection = get_hbase_connection()
    
    if connection:
        prices = load_latest_prices_from_hbase(connection)
        connection.close()
    else:
        prices = load_latest_prices_from_csv()
    
    if asset in prices:
        return jsonify(prices[asset])
    else:
        return jsonify({'error': 'No data available'}), 404

@app.route('/api/chart/<asset>')
def get_chart_data(asset):
    """Get historical data for charts"""
    if asset not in ASSETS:
        return jsonify({'error': 'Asset not found'}), 404
    
    # Get hours parameter (default 24)
    hours = request.args.get('hours', default=24, type=int)
    
    # Load historical data
    data = load_historical_data(asset, hours)
    
    if not data:
        return jsonify({'error': 'No historical data available'}), 404
    
    # Format for Plotly
    chart_data = {
        'x': [d['timestamp'] for d in data],
        'y': [d['price'] for d in data],
        'type': 'scatter',
        'mode': 'lines',
        'name': ASSET_NAMES.get(asset, asset),
        'line': {'color': '#00ff88', 'width': 2}
    }
    
    layout = {
        'title': f'{ASSET_NAMES.get(asset, asset)} - Last {hours} Hours',
        'xaxis': {'title': 'Time'},
        'yaxis': {'title': 'Price ($)'},
        'template': 'plotly_dark',
        'height': 400
    }
    
    return jsonify({'data': [chart_data], 'layout': layout})

@app.route('/api/portfolio')
def get_portfolio():
    """Get recommended portfolio"""
    return jsonify(RECOMMENDED_PORTFOLIO)

@app.route('/api/predictions')
def get_predictions():
    """Get ML predictions from trained models"""
    
    # Try to load from JSON file (generated by ml_predictor.py)
    predictions_file = os.path.join(DATA_DIR, 'latest_predictions.json')
    
    if os.path.exists(predictions_file):
        try:
            with open(predictions_file, 'r') as f:
                predictions_list = json.load(f)
            
            # Convert list to dict keyed by asset
            predictions = {}
            for pred in predictions_list:
                asset = pred['asset']
                predictions[asset] = {
                    'direction': pred['direction'],
                    'confidence': pred['confidence'],
                    'market_regime': pred.get('market_regime', 'Unknown'),
                    'models': pred.get('individual_probabilities', {}),
                    'timestamp': pred.get('timestamp', None)
                }
            
            return jsonify(predictions)
            
        except Exception as e:
            print(f"Error loading predictions: {e}")
    
    # Fallback: Try HBase
    if HBASE_AVAILABLE:
        try:
            connection = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
            table = connection.table('ml_predictions')
            
            predictions = {}
            for asset in ASSETS:
                # Get latest prediction for this asset
                for key, data in table.scan(row_prefix=asset.encode('utf-8'), limit=1, reversed=True):
                    predictions[asset] = {
                        'direction': data[b'prediction:direction'].decode('utf-8'),
                        'confidence': float(data[b'prediction:confidence']),
                        'market_regime': data[b'prediction:market_regime'].decode('utf-8'),
                        'timestamp': data[b'metadata:timestamp'].decode('utf-8')
                    }
                    break
            
            connection.close()
            
            if predictions:
                return jsonify(predictions)
                
        except Exception as e:
            print(f"Error loading from HBase: {e}")
    
    # Final fallback: Return default predictions
    predictions = {}
    for asset in ASSETS:
        predictions[asset] = {
            'direction': 'NEUTRAL',
            'confidence': 0.50,
            'market_regime': 'Unknown',
            'note': 'No predictions available. Run ml_predictor.py to generate predictions.'
        }
    
    return jsonify(predictions)

@app.route('/api/statistics')
def get_statistics():
    """Get overall statistics"""
    
    # Load all prices
    connection = get_hbase_connection()
    
    if connection:
        prices = load_latest_prices_from_hbase(connection)
        connection.close()
    else:
        prices = load_latest_prices_from_csv()
    
    if not prices:
        return jsonify({'error': 'No data available'}), 404
    
    # Calculate statistics
    stats = {
        'total_assets': len(prices),
        'last_update': max([p['timestamp'] for p in prices.values()]) if prices else None,
        'categories': {
            'stocks': 8,
            'commodities': 4,
            'indices': 2
        },
        'total_market_value': sum([p['price'] for p in prices.values()]),
        'highest_price': max(prices.items(), key=lambda x: x[1]['price'])[0] if prices else None,
        'lowest_price': min(prices.items(), key=lambda x: x[1]['price'])[0] if prices else None
    }
    
    return jsonify(stats)

@app.route('/api/alerts')
def get_alerts():
    """Get price alerts (mock data)"""
    alerts = [
        {
            'asset': 'NVDA',
            'type': 'PRICE_HIGH',
            'message': 'NVIDIA reached new high: $186.26',
            'severity': 'info',
            'timestamp': datetime.now().isoformat()
        },
        {
            'asset': 'GC=F',
            'type': 'RECOMMENDATION',
            'message': 'Gold shows strong buy signal',
            'severity': 'success',
            'timestamp': datetime.now().isoformat()
        }
    ]
    
    return jsonify(alerts)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    connection = get_hbase_connection()
    hbase_status = 'connected' if connection else 'disconnected'
    
    if connection:
        connection.close()
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'hbase': hbase_status,
        'version': '1.0.0'
    })

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("="*80)
    print("FLASK WEB APPLICATION")
    print("Real-Time Financial Dashboard Backend")
    print("="*80)
    print(f"\n📊 Monitoring {len(ASSETS)} assets")
    print(f"💾 Data directory: {DATA_DIR}")
    print(f"🔌 HBase: {'Available' if HBASE_AVAILABLE else 'Not available (CSV mode)'}")
    print(f"\n🚀 Starting Flask server...")
    print(f"📍 Access dashboard at: http://localhost:5000")
    print(f"📍 API documentation: http://localhost:5000/api/health")
    print(f"\nPress Ctrl+C to stop\n")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=5000,
        debug=True,
        threaded=True
    )
