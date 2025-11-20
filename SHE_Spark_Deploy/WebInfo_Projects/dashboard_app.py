"""
Dashboard Aplikacion për Vizualizim të Të dhënave Financiare
Duke përdorur Flask, Plotly, dhe të dhëna nga CSV/JSON
TË GJITHA NË GJUHËN SHQIPE
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
import numpy as np
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Emrat e aseteve në shqip
ASSET_NAMES = {
    'AAPL': 'Apple Inc.',
    'GOOGL': 'Alphabet (Google)',
    'MSFT': 'Microsoft Corp.',
    'AMZN': 'Amazon.com Inc.',
    'NVDA': 'NVIDIA Corp.',
    'TSLA': 'Tesla Inc.',
    'META': 'Meta Platforms',
    'NFLX': 'Netflix Inc.',
    'GC=F': 'Ari (Gold Futures)',
    'SI=F': 'Argjendi (Silver Futures)',
    'CL=F': 'Nafta (Crude Oil)',
    'NG=F': 'Gazi Natyror (Natural Gas)',
    '^GSPC': 'S&P 500',
    '^IXIC': 'NASDAQ Composite'
}

# Ngarkimi i të dhënave
def load_data():
    """Ngarkon të gjitha të dhënat nga skedarët CSV dhe JSON"""
    try:
        # Të dhënat e përpunuara
        df_labels = pd.read_csv('data/advanced_labels.csv')
        df_features = pd.read_csv('data/processed_features.csv')
        df_prices = pd.read_csv('data/realtime_prices.csv')
        
        # Konvertoni timestamp në datetime
        df_labels['timestamp'] = pd.to_datetime(df_labels['timestamp'])
        df_features['timestamp'] = pd.to_datetime(df_features['timestamp'])
        df_prices['timestamp'] = pd.to_datetime(df_prices['timestamp'])
        
        # Parashikimet
        with open('data/latest_predictions.json', 'r') as f:
            predictions = json.load(f)
        
        return {
            'labels': df_labels,
            'features': df_features,
            'prices': df_prices,
            'predictions': predictions
        }
    except Exception as e:
        print(f"Gabim në ngarkimin e të dhënave: {e}")
        return None

# Ngarkimi i të dhënave në fillim
DATA = load_data()

@app.route('/')
def index():
    """Faqja kryesore e dashboard-it"""
    return render_template('dashboard.html')

@app.route('/api/live-prices')
def get_live_prices():
    """Jep çmimet e fundit për të gjitha asetet"""
    if DATA is None:
        return jsonify({"error": "Të dhënat nuk janë ngarkuar"}), 500
    
    df = DATA['prices']
    assets = df['asset'].unique() if 'asset' in df.columns else ['AAPL']
    
    result = {}
    for asset in assets:
        asset_data = df[df['asset'] == asset].sort_values('timestamp', ascending=False).iloc[0] if 'asset' in df.columns else df.sort_values('timestamp', ascending=False).iloc[0]
        
        result[asset] = {
            'name': ASSET_NAMES.get(asset, asset),
            'price': float(asset_data['close']),
            'high': float(asset_data['high']),
            'low': float(asset_data['low']),
            'volume': int(asset_data['volume']) if 'volume' in asset_data else 0,
            'timestamp': str(asset_data['timestamp'])
        }
    
    return jsonify(result)

@app.route('/api/chart/<asset>')
def get_chart_data(asset):
    """Jep të dhënat për grafikun e një aseti"""
    hours = int(request.args.get('hours', 24))
    
    if DATA is None:
        return jsonify({"error": "Të dhënat nuk janë ngarkuar"}), 500
    
    df = DATA['prices']
    
    # Filtro për asetin e zgjedhur
    if 'asset' in df.columns:
        df_asset = df[df['asset'] == asset].copy()
    else:
        df_asset = df.copy()
    
    # Filtro për kohën
    cutoff_time = datetime.now() - timedelta(hours=hours)
    df_asset = df_asset[df_asset['timestamp'] > cutoff_time]
    
    # Sorto sipas kohës
    df_asset = df_asset.sort_values('timestamp')
    
    # Përgatit të dhënat për Plotly
    data = [
        {
            'x': df_asset['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
            'y': df_asset['close'].tolist(),
            'type': 'scatter',
            'mode': 'lines',
            'name': 'Çmimi Mbyllës',
            'line': {'color': '#00ff88', 'width': 2}
        }
    ]
    
    layout = {
        'title': f'{ASSET_NAMES.get(asset, asset)} - {hours} Orët e Fundit',
        'xaxis': {'title': 'Koha', 'gridcolor': '#2d3561'},
        'yaxis': {'title': 'Çmimi ($)', 'gridcolor': '#2d3561'},
        'plot_bgcolor': '#1e2749',
        'paper_bgcolor': '#1e2749',
        'font': {'color': '#ffffff'}
    }
    
    return jsonify({'data': data, 'layout': layout})

@app.route('/api/technical/<asset>')
def get_technical_data(asset):
    """Jep treguesit teknikë për një aset"""
    if DATA is None:
        return jsonify({"error": "Të dhënat nuk janë ngarkuar"}), 500
    
    df = DATA['labels']
    
    # Filtro për asetin
    if 'asset' in df.columns:
        df_asset = df[df['asset'] == asset].copy()
    else:
        df_asset = df.copy()
    
    df_asset = df_asset.sort_values('timestamp').tail(100)
    
    technical = {
        'rsi': {
            'x': df_asset['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
            'y': df_asset['rsi'].tolist() if 'rsi' in df_asset.columns else []
        },
        'bollinger': {
            'x': df_asset['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
            'upper': df_asset['bb_upper'].tolist() if 'bb_upper' in df_asset.columns else [],
            'middle': df_asset['bb_middle'].tolist() if 'bb_middle' in df_asset.columns else [],
            'lower': df_asset['bb_lower'].tolist() if 'bb_lower' in df_asset.columns else [],
            'price': df_asset['close'].tolist()
        },
        'moving_averages': {
            'x': df_asset['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
            'ma5': df_asset['ma_5'].tolist() if 'ma_5' in df_asset.columns else [],
            'ma14': df_asset['ma_14'].tolist() if 'ma_14' in df_asset.columns else [],
            'ma20': df_asset['ma_20'].tolist() if 'ma_20' in df_asset.columns else [],
            'ma50': df_asset['ma_50'].tolist() if 'ma_50' in df_asset.columns else [],
            'price': df_asset['close'].tolist()
        },
        'momentum': {
            'x': df_asset['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
            'momentum7': df_asset['momentum_7'].tolist() if 'momentum_7' in df_asset.columns else [],
            'momentum14': df_asset['momentum_14'].tolist() if 'momentum_14' in df_asset.columns else []
        },
        'volatility': {
            'x': df_asset['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
            'vol14': df_asset['volatility_14'].tolist() if 'volatility_14' in df_asset.columns else [],
            'vol20': df_asset['volatility_20'].tolist() if 'volatility_20' in df_asset.columns else []
        }
    }
    
    return jsonify(technical)

@app.route('/api/volume/<asset>')
def get_volume_data(asset):
    """Jep të dhënat e volumit për një aset"""
    if DATA is None:
        return jsonify({"error": "Të dhënat nuk janë ngarkuar"}), 500
    
    df = DATA['prices']
    
    # Filtro për asetin
    if 'asset' in df.columns:
        df_asset = df[df['asset'] == asset].copy()
    else:
        df_asset = df.copy()
    
    df_asset = df_asset.sort_values('timestamp').tail(100)
    
    volume_data = {
        'x': df_asset['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
        'volume': df_asset['volume'].tolist() if 'volume' in df_asset.columns else [],
        'price': df_asset['close'].tolist(),
        'avg_volume': float(df_asset['volume'].mean()) if 'volume' in df_asset.columns else 0,
        'max_volume': float(df_asset['volume'].max()) if 'volume' in df_asset.columns else 0,
        'trend': float(df_asset['volume'].iloc[-1] - df_asset['volume'].iloc[0]) if 'volume' in df_asset.columns and len(df_asset) > 0 else 0
    }
    
    return jsonify(volume_data)

@app.route('/api/volume-heatmap')
def get_volume_heatmap():
    """Jep heatmap të volumit për të gjitha asetet"""
    if DATA is None:
        return jsonify({"error": "Të dhënat nuk janë ngarkuar"}), 500
    
    df = DATA['prices']
    
    if 'asset' not in df.columns:
        return jsonify({"error": "Nuk ka të dhëna për shumë asete"}), 400
    
    # Merr volumin mesatar për çdo aset
    volume_by_asset = df.groupby('asset')['volume'].mean().to_dict()
    
    heatmap_data = {
        'assets': list(volume_by_asset.keys()),
        'volumes': list(volume_by_asset.values()),
        'names': [ASSET_NAMES.get(asset, asset) for asset in volume_by_asset.keys()]
    }
    
    return jsonify(heatmap_data)

@app.route('/api/predictions')
def get_predictions():
    """Jep parashikimet e ML"""
    if DATA is None or DATA['predictions'] is None:
        return jsonify({"error": "Parashikimet nuk janë të disponueshme"}), 500
    
    predictions = DATA['predictions']
    
    result = {}
    for pred in predictions:
        asset = pred['asset']
        result[asset] = {
            'direction': pred['direction'],
            'confidence': pred['confidence'],
            'market_regime': pred.get('market_regime', 'I Panjohur'),
            'models': pred.get('individual_probabilities', {})
        }
    
    return jsonify(result)

@app.route('/api/portfolio')
def get_portfolio():
    """Jep rekomandimin e portofolit"""
    # Kjo është një shembull i thjeshtë - ju mund ta personalizoni bazuar në të dhënat tuaja
    
    portfolio = {
        'allocation': {
            'NVDA': {'weight': 0.25, 'name': 'NVIDIA', 'reason': 'Rritje e fortë, treg në ekspansion'},
            'GOOGL': {'weight': 0.20, 'name': 'Google', 'reason': 'Stabilitet dhe diversifikim'},
            'MSFT': {'weight': 0.15, 'name': 'Microsoft', 'reason': 'Teknologji cloud në rritje'},
            'AAPL': {'weight': 0.15, 'name': 'Apple', 'reason': 'Brand i fortë, inovacion'},
            'NG=F': {'weight': 0.10, 'name': 'Gazi Natyror', 'reason': 'Diversifikim në komoditete'},
            '^GSPC': {'weight': 0.08, 'name': 'S&P 500', 'reason': 'Indeks tregu i gjerë'},
            'GC=F': {'weight': 0.07, 'name': 'Ari', 'reason': 'Mbrojtje nga inflacioni'}
        },
        'metrics': {
            'expected_return': 0.38,
            'sharpe_ratio': 0.95,
            'volatility': 0.12
        }
    }
    
    return jsonify(portfolio)

@app.route('/api/assets')
def get_assets():
    """Jep listën e të gjitha aseteve"""
    if DATA is None:
        return jsonify({"error": "Të dhënat nuk janë ngarkuar"}), 500
    
    df = DATA['prices']
    assets = df['asset'].unique().tolist() if 'asset' in df.columns else ['AAPL']
    
    result = []
    for asset in assets:
        result.append({
            'symbol': asset,
            'name': ASSET_NAMES.get(asset, asset)
        })
    
    return jsonify(result)

@app.route('/api/candlestick/<asset>')
def get_candlestick_data(asset):
    """Jep të dhënat për grafiku candlestick"""
    if DATA is None:
        return jsonify({"error": "Të dhënat nuk janë ngarkuar"}), 500
    
    df = DATA['prices']
    
    # Filtro për asetin
    if 'asset' in df.columns:
        df_asset = df[df['asset'] == asset].copy()
    else:
        df_asset = df.copy()
    
    df_asset = df_asset.sort_values('timestamp').tail(50)
    
    candlestick = {
        'x': df_asset['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
        'open': df_asset['close'].tolist(),  # Nuk kemi të dhëna 'open', përdorim 'close'
        'high': df_asset['high'].tolist(),
        'low': df_asset['low'].tolist(),
        'close': df_asset['close'].tolist()
    }
    
    return jsonify(candlestick)

if __name__ == '__main__':
    print("🚀 Duke nisur Dashboard-in Financiar...")
    print("📊 Dashboard-i do të jetë i disponueshëm në: http://localhost:5000")
    print("🌐 Gjuha: Shqip")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
