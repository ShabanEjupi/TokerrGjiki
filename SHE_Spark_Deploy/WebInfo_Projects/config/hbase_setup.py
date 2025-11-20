#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
HBASE SETUP AND CONFIGURATION
Database Schema and Initialization
================================================================================
Creates HBase tables for the Real-Time Financial Dashboard
Tables: asset_prices, asset_features, ml_predictions
================================================================================
"""

import happybase
import sys
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

HBASE_HOST = 'localhost'  # Change to KREN server IP
HBASE_PORT = 9090

# Table schemas
TABLES = {
    'asset_prices': {
        'price': dict(max_versions=1000),      # Close, High, Low, Volume
        'metadata': dict(max_versions=1)       # Asset, Name, Timestamp
    },
    'asset_features': {
        'features': dict(max_versions=100),    # MA, RSI, Volatility, etc.
        'price': dict(max_versions=100),       # Original price data
        'metadata': dict(max_versions=1)       # Asset info
    },
    'ml_predictions': {
        'pred': dict(max_versions=50),         # Predictions
        'model': dict(max_versions=1),         # Model info
        'metadata': dict(max_versions=1)       # Timestamp, asset
    }
}

# ============================================================================
# HBASE OPERATIONS
# ============================================================================

def connect_to_hbase():
    """Connect to HBase"""
    try:
        print(f"🔌 Connecting to HBase at {HBASE_HOST}:{HBASE_PORT}...")
        connection = happybase.Connection(HBASE_HOST, port=HBASE_PORT, timeout=10000)
        print(f"✅ Connected successfully!")
        return connection
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if HBase is running:")
        print("   $ jps | grep HMaster")
        print("2. Check if Thrift server is running:")
        print("   $ jps | grep ThriftServer")
        print("3. Start Thrift server if needed:")
        print("   $ hbase thrift start -p 9090")
        return None

def list_tables(connection):
    """List all existing tables"""
    try:
        tables = connection.tables()
        print(f"\n📋 Existing tables:")
        if tables:
            for table in tables:
                print(f"   - {table.decode('utf-8')}")
        else:
            print("   (No tables found)")
        return [t.decode('utf-8') for t in tables]
    except Exception as e:
        print(f"❌ Error listing tables: {e}")
        return []

def create_table(connection, table_name, column_families):
    """Create a table with specified column families"""
    try:
        print(f"\n📝 Creating table: {table_name}")
        
        # Check if table exists
        existing_tables = [t.decode('utf-8') for t in connection.tables()]
        
        if table_name in existing_tables:
            print(f"   ⚠️  Table '{table_name}' already exists")
            return True
        
        # Create table
        connection.create_table(table_name, column_families)
        print(f"   ✅ Table '{table_name}' created successfully!")
        
        # Show column families
        print(f"   Column families:")
        for cf in column_families.keys():
            print(f"      - {cf}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating table: {e}")
        return False

def delete_table(connection, table_name):
    """Delete a table (use with caution!)"""
    try:
        print(f"\n🗑️  Deleting table: {table_name}")
        
        # Check if table exists
        existing_tables = [t.decode('utf-8') for t in connection.tables()]
        
        if table_name not in existing_tables:
            print(f"   ⚠️  Table '{table_name}' does not exist")
            return False
        
        # Disable and delete
        connection.delete_table(table_name, disable=True)
        print(f"   ✅ Table '{table_name}' deleted successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error deleting table: {e}")
        return False

def show_table_info(connection, table_name):
    """Show detailed information about a table"""
    try:
        existing_tables = [t.decode('utf-8') for t in connection.tables()]
        
        if table_name not in existing_tables:
            print(f"   ⚠️  Table '{table_name}' does not exist")
            return
        
        table = connection.table(table_name)
        
        print(f"\n📊 Table: {table_name}")
        print(f"   Families: {table.families()}")
        
        # Count rows (sample)
        count = 0
        for key, data in table.scan(limit=1000):
            count += 1
        
        print(f"   Estimated rows: {count}+ (showing first 1000)")
        
    except Exception as e:
        print(f"   ❌ Error getting table info: {e}")

def insert_sample_data(connection):
    """Insert sample data for testing"""
    try:
        print(f"\n💾 Inserting sample data...")
        
        table = connection.table('asset_prices')
        
        # Sample data for AAPL
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        row_key = f"AAPL_{timestamp}".encode('utf-8')
        
        data = {
            b'price:close': b'262.82',
            b'price:high': b'265.50',
            b'price:low': b'260.00',
            b'price:volume': b'50000000',
            b'metadata:asset': b'AAPL',
            b'metadata:name': b'Apple',
            b'metadata:timestamp': timestamp.encode('utf-8')
        }
        
        table.put(row_key, data)
        print(f"   ✅ Sample data inserted: AAPL @ ${data[b'price:close'].decode('utf-8')}")
        
        # Verify
        row = table.row(row_key)
        if row:
            print(f"   ✅ Verification successful!")
            return True
        else:
            print(f"   ❌ Verification failed!")
            return False
            
    except Exception as e:
        print(f"   ❌ Error inserting sample data: {e}")
        return False

# ============================================================================
# SETUP WIZARD
# ============================================================================

def setup_all_tables(connection):
    """Create all required tables"""
    print("\n" + "="*80)
    print("CREATING ALL TABLES")
    print("="*80)
    
    success_count = 0
    
    for table_name, column_families in TABLES.items():
        if create_table(connection, table_name, column_families):
            success_count += 1
    
    print(f"\n{'='*80}")
    print(f"✅ Created {success_count}/{len(TABLES)} tables successfully!")
    print(f"{'='*80}\n")
    
    return success_count == len(TABLES)

def reset_all_tables(connection):
    """Delete and recreate all tables"""
    print("\n⚠️  WARNING: This will delete all existing data!")
    response = input("Are you sure? Type 'yes' to continue: ")
    
    if response.lower() != 'yes':
        print("❌ Operation cancelled")
        return False
    
    print("\n" + "="*80)
    print("RESETTING ALL TABLES")
    print("="*80)
    
    # Delete tables
    for table_name in TABLES.keys():
        delete_table(connection, table_name)
    
    # Recreate tables
    setup_all_tables(connection)
    
    return True

# ============================================================================
# MAIN MENU
# ============================================================================

def show_menu():
    """Show interactive menu"""
    print("\n" + "="*80)
    print("HBASE SETUP & CONFIGURATION")
    print("="*80)
    print("\n1. Create all tables")
    print("2. List existing tables")
    print("3. Show table info")
    print("4. Insert sample data")
    print("5. Reset all tables (DELETE ALL DATA)")
    print("6. Exit")
    print()

def main():
    """Main function"""
    print("="*80)
    print("HBASE SETUP WIZARD")
    print("Real-Time Financial Dashboard")
    print("="*80)
    
    # Connect to HBase
    connection = connect_to_hbase()
    
    if connection is None:
        print("\n❌ Cannot proceed without HBase connection")
        print("\nPlease ensure:")
        print("1. HBase is installed and running")
        print("2. Thrift server is running on port 9090")
        print("3. happybase Python package is installed: pip install happybase")
        sys.exit(1)
    
    # Interactive menu
    while True:
        show_menu()
        choice = input("Select option (1-6): ").strip()
        
        if choice == '1':
            setup_all_tables(connection)
            
        elif choice == '2':
            list_tables(connection)
            
        elif choice == '3':
            table_name = input("Enter table name: ").strip()
            show_table_info(connection, table_name)
            
        elif choice == '4':
            insert_sample_data(connection)
            
        elif choice == '5':
            reset_all_tables(connection)
            
        elif choice == '6':
            print("\n👋 Exiting...")
            connection.close()
            break
            
        else:
            print("❌ Invalid option")
    
    print("\n✅ Setup completed!\n")

if __name__ == "__main__":
    main()
