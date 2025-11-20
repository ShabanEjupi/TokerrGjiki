#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
REAL-TIME FINANCIAL DATA COLLECTOR
Web Information Retrieval - Continuous Data Collection
================================================================================
Collects real-time price data for 14 financial assets every 5 minutes
Stores data in HBase for distributed storage and processing
================================================================================
"""

import yfinance as yf
import time
import json
import csv
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import happybase  # HBase Python client
    HBASE_AVAILABLE = True
except ImportError:
    print("⚠️  happybase not installed. Will use CSV fallback.")
    HBASE_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

# 14 Financial Assets (same as your existing projects)
ASSETS = {
    'Stocks': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX'],
    'Commodities': ['GC=F', 'SI=F', 'CL=F', 'NG=F'],
    'Indices': ['^GSPC', '^IXIC']
}

ALL_ASSETS = ASSETS['Stocks'] + ASSETS['Commodities'] + ASSETS['Indices']

ASSET_NAMES = {
    'AAPL': 'Apple', 'GOOGL': 'Google', 'MSFT': 'Microsoft', 'AMZN': 'Amazon',
    'NVDA': 'NVIDIA', 'TSLA': 'Tesla', 'META': 'Meta', 'NFLX': 'Netflix',
    'GC=F': 'Gold', 'SI=F': 'Silver', 'CL=F': 'Crude Oil', 'NG=F': 'Natural Gas',
    '^GSPC': 'S&P 500', '^IXIC': 'NASDAQ'
}

# Collection settings
COLLECTION_INTERVAL = 300  # 5 minutes (300 seconds)
HBASE_HOST = 'localhost'   # Change to KREN server IP
HBASE_PORT = 9090
HBASE_TABLE = 'asset_prices'

# Data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================================
# HBASE CONNECTION
# ============================================================================

def connect_to_hbase():
    """Connect to HBase and create table if it doesn't exist"""
    if not HBASE_AVAILABLE:
        return None
    
    try:
        connection = happybase.Connection(HBASE_HOST, port=HBASE_PORT)
        
        # Create table if it doesn't exist
        tables = [t.decode('utf-8') for t in connection.tables()]
        if HBASE_TABLE not in tables:
            print(f"Creating HBase table: {HBASE_TABLE}")
            connection.create_table(
                HBASE_TABLE,
                {
                    'price': dict(),      # price:close, price:high, price:low, price:volume
                    'metadata': dict(),   # metadata:asset, metadata:timestamp, metadata:name
                }
            )
            print(f"✅ Table '{HBASE_TABLE}' created successfully!")
        
        return connection
    except Exception as e:
        print(f"❌ Error connecting to HBase: {e}")
        print("   Will use CSV fallback mode.")
        return None

# ============================================================================
# DATA COLLECTION
# ============================================================================

def collect_asset_data(asset):
    """Collect current price data for a single asset"""
    try:
        ticker = yf.Ticker(asset)
        
        # Get latest data (1 day with 1-minute interval)
        data = ticker.history(period='1d', interval='1m')
        
        if data.empty:
            print(f"  ⚠️  No data available for {asset}")
            return None
        
        # Get latest price
        latest = data.iloc[-1]
        
        result = {
            'asset': asset,
            'name': ASSET_NAMES.get(asset, asset),
            'timestamp': datetime.now().isoformat(),
            'close': float(latest['Close']),
            'high': float(latest['High']),
            'low': float(latest['Low']),
            'volume': int(latest['Volume']) if 'Volume' in latest else 0,
        }
        
        return result
        
    except Exception as e:
        print(f"  ❌ Error collecting {asset}: {e}")
        return None

def save_to_hbase(connection, data):
    """Save data to HBase"""
    if connection is None or data is None:
        return False
    
    try:
        table = connection.table(HBASE_TABLE)
        
        # Create row key: asset_timestamp
        timestamp_str = datetime.now().strftime('%Y%m%d%H%M%S')
        row_key = f"{data['asset']}_{timestamp_str}".encode('utf-8')
        
        # Prepare data for HBase
        hbase_data = {
            b'price:close': str(data['close']).encode('utf-8'),
            b'price:high': str(data['high']).encode('utf-8'),
            b'price:low': str(data['low']).encode('utf-8'),
            b'price:volume': str(data['volume']).encode('utf-8'),
            b'metadata:asset': data['asset'].encode('utf-8'),
            b'metadata:name': data['name'].encode('utf-8'),
            b'metadata:timestamp': data['timestamp'].encode('utf-8'),
        }
        
        # Insert into HBase
        table.put(row_key, hbase_data)
        return True
        
    except Exception as e:
        print(f"  ❌ Error saving to HBase: {e}")
        return False

def save_to_csv(data):
    """Save data to CSV as fallback"""
    if data is None:
        return False
    
    try:
        csv_file = os.path.join(DATA_DIR, 'realtime_prices.csv')
        
        # Check if file exists to write header
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, 'a', newline='') as f:
            fieldnames = ['timestamp', 'asset', 'name', 'close', 'high', 'low', 'volume']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(data)
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error saving to CSV: {e}")
        return False

# ============================================================================
# MAIN COLLECTION LOOP
# ============================================================================

def collect_all_assets(hbase_conn):
    """Collect data for all 14 assets"""
    print(f"\n{'='*80}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] COLLECTING DATA")
    print(f"{'='*80}")
    
    success_count = 0
    failed_count = 0
    
    for category, asset_list in ASSETS.items():
        print(f"\n{category}:")
        
        for asset in asset_list:
            print(f"  Collecting {asset} ({ASSET_NAMES[asset]})...", end=' ')
            
            # Collect data
            data = collect_asset_data(asset)
            
            if data:
                # Save to HBase (or CSV if HBase unavailable)
                if hbase_conn:
                    if save_to_hbase(hbase_conn, data):
                        print(f"✓ ${data['close']:.2f} → HBase")
                        success_count += 1
                    else:
                        if save_to_csv(data):
                            print(f"✓ ${data['close']:.2f} → CSV (HBase failed)")
                            success_count += 1
                        else:
                            print(f"✗ Failed")
                            failed_count += 1
                else:
                    if save_to_csv(data):
                        print(f"✓ ${data['close']:.2f} → CSV")
                        success_count += 1
                    else:
                        print(f"✗ Failed")
                        failed_count += 1
            else:
                print(f"✗ No data")
                failed_count += 1
    
    print(f"\n{'='*80}")
    print(f"✅ Success: {success_count} | ❌ Failed: {failed_count}")
    print(f"{'='*80}")
    
    return success_count, failed_count

def main():
    """Main function - continuous data collection"""
    print("="*80)
    print("REAL-TIME FINANCIAL DATA COLLECTOR")
    print("14 Assets • Continuous Collection • Every 5 Minutes")
    print("="*80)
    
    print(f"\n📊 Assets to collect:")
    for category, asset_list in ASSETS.items():
        print(f"   {category}: {', '.join(asset_list)}")
    
    print(f"\n⏰ Collection interval: {COLLECTION_INTERVAL} seconds ({COLLECTION_INTERVAL//60} minutes)")
    print(f"💾 Data directory: {DATA_DIR}")
    
    # Connect to HBase
    print(f"\n🔌 Connecting to HBase at {HBASE_HOST}:{HBASE_PORT}...")
    hbase_conn = connect_to_hbase()
    
    if hbase_conn:
        print(f"✅ HBase connection established!")
    else:
        print(f"⚠️  HBase not available. Using CSV fallback mode.")
    
    # Statistics
    total_collections = 0
    total_success = 0
    total_failed = 0
    
    print(f"\n🚀 Starting continuous collection...")
    print(f"   Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Collect data
            success, failed = collect_all_assets(hbase_conn)
            
            # Update statistics
            total_collections += 1
            total_success += success
            total_failed += failed
            
            # Calculate success rate
            success_rate = (total_success / (total_success + total_failed) * 100) if (total_success + total_failed) > 0 else 0
            
            print(f"\n📈 Statistics:")
            print(f"   Collections: {total_collections}")
            print(f"   Total Success: {total_success}")
            print(f"   Total Failed: {total_failed}")
            print(f"   Success Rate: {success_rate:.1f}%")
            
            # Wait for next collection
            next_collection = datetime.now() + timedelta(seconds=COLLECTION_INTERVAL)
            print(f"\n⏳ Waiting until {next_collection.strftime('%H:%M:%S')} for next collection...")
            print(f"   (Sleeping for {COLLECTION_INTERVAL} seconds)\n")
            
            time.sleep(COLLECTION_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Collection stopped by user")
        print(f"\n📊 Final Statistics:")
        print(f"   Total Collections: {total_collections}")
        print(f"   Total Records: {total_success}")
        print(f"   Failed Records: {total_failed}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        if hbase_conn:
            hbase_conn.close()
            print(f"\n✅ HBase connection closed")
        
        print(f"\n💾 Data saved in: {DATA_DIR}")
        print(f"✅ Data collection completed successfully!\n")

if __name__ == "__main__":
    main()
