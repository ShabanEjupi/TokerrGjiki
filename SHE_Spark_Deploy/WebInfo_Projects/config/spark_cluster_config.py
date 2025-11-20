#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
SPARK CLUSTER CONFIGURATION
10-Node Distributed Computing Setup with 128GB+ RAM
================================================================================
Configuration for distributed Spark cluster across 10 VMs
Optimized for maximum performance and resource utilization
================================================================================
"""

# ============================================================================
# CLUSTER TOPOLOGY
# ============================================================================

# Master Node (port 8022)
MASTER_HOST = "185.182.158.150"
MASTER_PORT = 8022
MASTER_USER = "krenuser"
SPARK_MASTER_URL = f"spark://{MASTER_HOST}:7077"
SPARK_MASTER_WEBUI_PORT = 8080

# Worker Nodes (ports 8023-8031 = 9 workers)
WORKERS = [
    {"host": MASTER_HOST, "port": 8023, "user": "krenuser", "cores": 12, "memory": "120g"},
    {"host": MASTER_HOST, "port": 8024, "user": "krenuser", "cores": 12, "memory": "120g"},
    {"host": MASTER_HOST, "port": 8025, "user": "krenuser", "cores": 12, "memory": "120g"},
    {"host": MASTER_HOST, "port": 8026, "user": "krenuser", "cores": 12, "memory": "120g"},
    {"host": MASTER_HOST, "port": 8027, "user": "krenuser", "cores": 12, "memory": "120g"},
    {"host": MASTER_HOST, "port": 8028, "user": "krenuser", "cores": 12, "memory": "120g"},
    {"host": MASTER_HOST, "port": 8029, "user": "krenuser", "cores": 12, "memory": "120g"},
    {"host": MASTER_HOST, "port": 8030, "user": "krenuser", "cores": 12, "memory": "120g"},
    {"host": MASTER_HOST, "port": 8031, "user": "krenuser", "cores": 12, "memory": "120g"},
]

# Total cluster resources
TOTAL_WORKERS = len(WORKERS)
TOTAL_CORES = sum(w["cores"] for w in WORKERS)
TOTAL_MEMORY_GB = sum(int(w["memory"].replace("g", "")) for w in WORKERS)

# ============================================================================
# SPARK APPLICATION CONFIGURATION
# ============================================================================

# Optimized for 128GB+ RAM per node and 10+ cores
SPARK_CONFIG = {
    # Master configuration
    "spark.master": SPARK_MASTER_URL,
    
    # Driver configuration (runs on master)
    "spark.driver.memory": "16g",
    "spark.driver.cores": "4",
    "spark.driver.maxResultSize": "4g",
    
    # Executor configuration (runs on workers)
    # With 9 workers at 120GB each = 1080GB total
    "spark.executor.memory": "100g",  # Leave 20GB for OS per worker
    "spark.executor.cores": "10",      # Use 10 cores per executor
    "spark.executor.instances": "9",   # One executor per worker
    
    # Memory management
    "spark.memory.fraction": "0.8",           # 80% for execution & storage
    "spark.memory.storageFraction": "0.3",    # 30% of that for caching
    "spark.memory.offHeap.enabled": "true",
    "spark.memory.offHeap.size": "10g",
    
    # Parallelism & Partitions
    # Rule: 2-3x number of total cores for optimal parallelism
    "spark.default.parallelism": str(TOTAL_CORES * 3),  # ~324 partitions
    "spark.sql.shuffle.partitions": str(TOTAL_CORES * 3),
    
    # Dynamic allocation (optional - disable for consistent performance)
    "spark.dynamicAllocation.enabled": "false",
    "spark.shuffle.service.enabled": "false",
    
    # Network & Serialization
    "spark.network.timeout": "800s",
    "spark.executor.heartbeatInterval": "60s",
    "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
    "spark.kryoserializer.buffer.max": "512m",
    
    # Adaptive Query Execution (AQE) - Spark 3.x feature
    "spark.sql.adaptive.enabled": "true",
    "spark.sql.adaptive.coalescePartitions.enabled": "true",
    "spark.sql.adaptive.skewJoin.enabled": "true",
    
    # Broadcast joins (for small tables < 100MB)
    "spark.sql.autoBroadcastJoinThreshold": "100m",
    
    # Compression
    "spark.rdd.compress": "true",
    "spark.io.compression.codec": "snappy",
    
    # Logging
    "spark.eventLog.enabled": "true",
    "spark.eventLog.dir": "file:///tmp/spark-events",
    
    # Application info
    "spark.app.name": "RealTimeFinancialDashboard",
}

# ============================================================================
# OPTIMIZATION PROFILES
# ============================================================================

# For streaming workloads (real-time data processing)
STREAMING_CONFIG = {
    **SPARK_CONFIG,
    "spark.streaming.backpressure.enabled": "true",
    "spark.streaming.kafka.maxRatePerPartition": "10000",
    "spark.streaming.receiver.maxRate": "10000",
    "spark.streaming.blockInterval": "200ms",
}

# For batch processing (historical data analysis)
BATCH_CONFIG = {
    **SPARK_CONFIG,
    "spark.sql.shuffle.partitions": str(TOTAL_CORES * 4),  # More partitions for batch
    "spark.default.parallelism": str(TOTAL_CORES * 4),
}

# For machine learning workloads
ML_CONFIG = {
    **SPARK_CONFIG,
    "spark.executor.memory": "110g",  # More memory for ML
    "spark.driver.memory": "20g",
    "spark.memory.fraction": "0.9",   # More memory for computation
}

# ============================================================================
# HBASE CONFIGURATION
# ============================================================================

HBASE_CONFIG = {
    "host": "localhost",  # Or specific HBase master if different
    "port": 9090,
    "tables": {
        "prices": "asset_prices",
        "features": "asset_features",
        "predictions": "ml_predictions"
    }
}

# ============================================================================
# DEPLOYMENT PATHS
# ============================================================================

# Remote paths on cluster nodes
REMOTE_BASE_DIR = "/home/krenuser/financial_dashboard"
REMOTE_SPARK_HOME = "/opt/spark"  # Adjust based on actual Spark installation
REMOTE_PYTHON = "python3"

# Local paths
LOCAL_BASE_DIR = "c:\\Users\\Administrator\\TokerrGjiki\\SHE_Spark_Deploy\\WebInfo_Projects"

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_spark_submit_command(script_name, config_type="default"):
    """Generate spark-submit command with optimal configuration"""
    
    # Select configuration profile
    if config_type == "streaming":
        config = STREAMING_CONFIG
    elif config_type == "batch":
        config = BATCH_CONFIG
    elif config_type == "ml":
        config = ML_CONFIG
    else:
        config = SPARK_CONFIG
    
    # Build command
    cmd_parts = [
        "spark-submit",
        f"--master {config['spark.master']}",
        f"--driver-memory {config['spark.driver.memory']}",
        f"--driver-cores {config['spark.driver.cores']}",
        f"--executor-memory {config['spark.executor.memory']}",
        f"--executor-cores {config['spark.executor.cores']}",
        f"--num-executors {config['spark.executor.instances']}",
        f"--name {config['spark.app.name']}",
    ]
    
    # Add additional configs
    for key, value in config.items():
        if not key.startswith(("spark.master", "spark.driver.", "spark.executor.", "spark.app.name")):
            cmd_parts.append(f"--conf {key}={value}")
    
    # Add script
    cmd_parts.append(script_name)
    
    return " \\\n  ".join(cmd_parts)

def print_cluster_info():
    """Print cluster configuration summary"""
    print("=" * 80)
    print("SPARK CLUSTER CONFIGURATION")
    print("=" * 80)
    print(f"\n📡 Master Node:")
    print(f"   Host: {MASTER_HOST}:{MASTER_PORT}")
    print(f"   Spark Master: {SPARK_MASTER_URL}")
    print(f"   Web UI: http://{MASTER_HOST}:{SPARK_MASTER_WEBUI_PORT}")
    
    print(f"\n⚡ Worker Nodes: {TOTAL_WORKERS}")
    for i, worker in enumerate(WORKERS, 1):
        print(f"   Worker {i}: {worker['host']}:{worker['port']} - "
              f"{worker['cores']} cores, {worker['memory']} RAM")
    
    print(f"\n💪 Total Resources:")
    print(f"   Total Cores: {TOTAL_CORES}")
    print(f"   Total Memory: {TOTAL_MEMORY_GB} GB")
    print(f"   Parallelism: {SPARK_CONFIG['spark.default.parallelism']}")
    print(f"   Shuffle Partitions: {SPARK_CONFIG['spark.sql.shuffle.partitions']}")
    
    print(f"\n🎯 Executor Configuration:")
    print(f"   Executors: {SPARK_CONFIG['spark.executor.instances']}")
    print(f"   Memory per Executor: {SPARK_CONFIG['spark.executor.memory']}")
    print(f"   Cores per Executor: {SPARK_CONFIG['spark.executor.cores']}")
    
    print(f"\n🚀 Estimated Performance:")
    # Rough estimates
    records_per_second = TOTAL_CORES * 1000  # Conservative estimate
    print(f"   Processing: ~{records_per_second:,} records/second")
    print(f"   Daily Capacity: ~{records_per_second * 86400:,} records/day")
    print(f"   Concurrent Jobs: {TOTAL_CORES // 4} (recommended)")
    
    print("\n" + "=" * 80 + "\n")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print_cluster_info()
    
    print("\n📝 Example Spark Submit Commands:\n")
    
    print("# Streaming workload:")
    print(get_spark_submit_command("scripts/spark_streaming_processor.py", "streaming"))
    print("\n")
    
    print("# Batch processing:")
    print(get_spark_submit_command("scripts/spark_batch_processor.py", "batch"))
    print("\n")
    
    print("# Machine Learning:")
    print(get_spark_submit_command("scripts/spark_ml_training.py", "ml"))
