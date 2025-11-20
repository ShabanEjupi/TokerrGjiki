#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SAMPLE DATA GENERATOR
Generate synthetic financial data for local testing
================================================================================
Creates realistic price data with trends, volatility, and patterns
No internet connection required!
================================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# Initial prices (approximate realistic values)
INITIAL_PRICES = {
    'AAPL': 178.50, 'GOOGL': 140.20, 'MSFT': 370.80, 'AMZN': 145.30,
    'NVDA': 186.26, 'TSLA': 235.60, 'META': 325.40, 'NFLX': 485.20,
    'GC=F': 2050.00, 'SI=F': 24.50, 'CL=F': 78.30, 'NG=F': 2.85,
    '^GSPC': 4550.00, '^IXIC': 14200.00
}

# Volatility levels (daily standard deviation %)
VOLATILITY = {
    'AAPL': 0.015, 'GOOGL': 0.018, 'MSFT': 0.014, 'AMZN': 0.020,
    'NVDA': 0.030, 'TSLA': 0.035, 'META': 0.022, 'NFLX': 0.025,
    'GC=F': 0.012, 'SI=F': 0.020, 'CL=F': 0.025, 'NG=F': 0.030,
    '^GSPC': 0.010, '^IXIC': 0.012
}

# Trend direction (daily drift %)
TRENDS = {
    'AAPL': 0.0008, 'GOOGL': 0.0010, 'MSFT': 0.0012, 'AMZN': 0.0009,
    'NVDA': 0.0015, 'TSLA': 0.0005, 'META': 0.0011, 'NFLX': 0.0007,
    'GC=F': 0.0003, 'SI=F': 0.0004, 'CL=F': 0.0002, 'NG=F': 0.0001,
    '^GSPC': 0.0005, '^IXIC': 0.0006
}

# Number of days to generate
DAYS = 180  # 6 months of data
RECORDS_PER_DAY = 12  # One record every 2 hours

# ============================================================================
# PRICE GENERATION
# ============================================================================

def generate_price_series(asset, days=DAYS, records_per_day=RECORDS_PER_DAY):
    """Generate realistic price series using geometric Brownian motion"""
    
    initial_price = INITIAL_PRICES[asset]
    volatility = VOLATILITY[asset]
    trend = TRENDS[asset]
    
    total_records = days * records_per_day
    
    # Generate timestamps
    start_date = datetime.now() - timedelta(days=days)
    timestamps = []
    current_time = start_date
    time_increment = timedelta(hours=24/records_per_day)
    
    for _ in range(total_records):
        timestamps.append(current_time.isoformat())
        current_time += time_increment
    
    # Generate prices using geometric Brownian motion
    np.random.seed(hash(asset) % 2**32)  # Reproducible but different per asset
    
    returns = np.random.normal(trend, volatility, total_records)
    
    # Add some autocorrelation (momentum)
    for i in range(1, len(returns)):
        returns[i] += 0.3 * returns[i-1]  # Momentum effect
    
    # Calculate prices
    prices = [initial_price]
    for r in returns[1:]:
        prices.append(prices[-1] * (1 + r))
    
    # Generate high/low/volume
    data = []
    for i, (timestamp, close) in enumerate(zip(timestamps, prices)):
        # High is close + random amount (0-2%)
        high = close * (1 + np.random.uniform(0, 0.02))
        
        # Low is close - random amount (0-2%)
        low = close * (1 - np.random.uniform(0, 0.02))
        
        # Volume is proportional to price movement
        base_volume = 10000000
        volatility_multiplier = abs(returns[i]) * 100
        volume = int(base_volume * (1 + volatility_multiplier) * np.random.uniform(0.5, 1.5))
        
        data.append({
            'timestamp': timestamp,
            'asset': asset,
            'close': close,
            'high': high,
            'low': low,
            'volume': volume
        })
    
    return data

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Generate sample data for all assets"""
    
    print("="*80)
    print("SAMPLE DATA GENERATOR")
    print("Generating synthetic financial data for local testing")
    print("="*80)
    
    print(f"\n📊 Configuration:")
    print(f"   Assets: {len(ASSETS)}")
    print(f"   Days: {DAYS}")
    print(f"   Records per day: {RECORDS_PER_DAY}")
    print(f"   Total records per asset: {DAYS * RECORDS_PER_DAY}")
    print(f"   Total records: {DAYS * RECORDS_PER_DAY * len(ASSETS):,}")
    
    print(f"\n🔄 Generating data...")
    
    all_data = []
    
    for asset in ASSETS:
        print(f"   Generating {asset}...", end=' ')
        asset_data = generate_price_series(asset)
        all_data.extend(asset_data)
        print(f"✓ {len(asset_data)} records")
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Save to CSV
    output_file = os.path.join(data_dir, 'realtime_prices.csv')
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Data generated successfully!")
    print(f"   Saved to: {output_file}")
    print(f"   Total records: {len(df):,}")
    print(f"   File size: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
    
    # Show sample
    print(f"\n📋 Sample data (first 5 records):")
    print(df.head())
    
    # Show statistics
    print(f"\n📊 Statistics:")
    print(f"   Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"   Assets: {df['asset'].nunique()}")
    print(f"   Records per asset:")
    for asset in ASSETS:
        count = len(df[df['asset'] == asset])
        print(f"      {asset:8s}: {count:,}")
    
    print(f"\n✨ Ready for ML pipeline!")
    print(f"   Run: python scripts\\spark_streaming_processor.py")
    print()

if __name__ == "__main__":
    main()
