#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
BIG DATA FUNDAMENTALS
MapReduce Programming Model & Data Pipeline
Based on: "Big Data Fundamentals" by Erl, Buhler, and Khattak (Chapters 3-4)
================================================================================
Topic: MapReduce Paradigm and Distributed Data Processing
Concepts:
- MapReduce Programming Model
- Map Phase and Reduce Phase
- Distributed Data Processing
- Word Count (Classic Example)
- Data Aggregation Patterns
- Hadoop/Spark Implementation
================================================================================
Date: October 27, 2025
Time: 17:00
================================================================================
"""

import pandas as pd
import numpy as np
from collections import defaultdict, Counter
import json
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Konfiguro matplotlib për grafiqe më të mira
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

print("=" * 80)
print("BIG DATA FUNDAMENTALS - PROFESSOR PRESENTATION")
print("TEMA: MapReduce Programming Model & Data Pipeline")
print("LIBRI: 'Big Data Fundamentals' by Erl, Buhler, and Khattak")
print("=" * 80)

# ============================================================================
# PART 1: MAPREDUCE THEORY (Erl/Buhler/Khattak Chapter 3)
# ============================================================================

print("\n" + "=" * 80)
print("PART 1: MAPREDUCE PROGRAMMING MODEL - THEORY")
print("=" * 80)

print("""
MAPREDUCE FUNDAMENTALS (Chapter 3.2, p. 78-85):
==============================================

DEFINITION:
MapReduce is a programming model for processing large datasets in parallel
across a distributed cluster of computers.

CORE CONCEPTS:
1. MAP PHASE: Transform input data into key-value pairs
   - Input: Data records
   - Process: Apply map function to each record
   - Output: Intermediate key-value pairs (k, v)

2. SHUFFLE & SORT: Group by key
   - Collect all values for same key
   - Sort by key
   - Distribute to reducers

3. REDUCE PHASE: Aggregate values for each key
   - Input: Key and list of values
   - Process: Apply reduce function
   - Output: Final aggregated results

MAPREDUCE WORKFLOW (Erl/Buhler/Khattak, Figure 3.4):
===================================================

Input Data → SPLIT → MAP → Shuffle → REDUCE → Output

KEY ADVANTAGES:
✓ Scalability: Process petabytes of data
✓ Fault Tolerance: Automatic recovery from failures
✓ Simplicity: Hide complexity of distributed computing
✓ Flexibility: Works with structured and unstructured data
✓ Cost-Effective: Runs on commodity hardware
""")

# ============================================================================
# PART 2: CLASSIC EXAMPLE - WORD COUNT
# ============================================================================

print("\n" + "=" * 80)
print("PART 2: WORD COUNT - CLASSIC MAPREDUCE EXAMPLE")
print("=" * 80)

# Sample text data (simulating Big Data documents)
documents = [
    "Big Data is revolutionizing the way we process information",
    "MapReduce enables distributed processing of large datasets",
    "Hadoop and Spark are popular Big Data frameworks",
    "Data processing at scale requires distributed computing",
    "Big Data analytics helps organizations make better decisions",
    "Machine learning on Big Data unlocks new insights",
    "Processing massive datasets requires parallel computing frameworks",
    "Distributed systems enable scalable data processing",
    "Big Data technologies transform how we analyze information",
    "MapReduce is fundamental to modern data processing pipelines"
]

print(f"\nInput Data:")
print(f"   Number of documents: {len(documents)}")
print(f"   Sample documents:")
for i, doc in enumerate(documents[:3], 1):
    print(f"   {i}. {doc}")

# MAP PHASE
print("\n" + "=" * 80)
print("MAP PHASE: Transform documents to key-value pairs")
print("=" * 80)

def map_function(document):
    """
    MAP function: Split document into words and emit (word, 1) pairs
    
    Input: document (string)
    Output: list of (key, value) pairs where key=word, value=1
    """
    words = document.lower().replace(',', '').replace('.', '').split()
    return [(word, 1) for word in words]

# Apply map function to all documents
mapped_data = []
for doc_id, document in enumerate(documents):
    pairs = map_function(document)
    mapped_data.extend(pairs)
    if doc_id < 2:  # Show first 2 examples
        print(f"\nDocument {doc_id + 1}: '{document}'")
        print(f"   Mapped to: {pairs[:8]}...")

print(f"\n✅ Total intermediate pairs generated: {len(mapped_data)}")
print(f"   Sample pairs: {mapped_data[:10]}")

# SHUFFLE & SORT PHASE
print("\n" + "=" * 80)
print("SHUFFLE & SORT PHASE: Group values by key")
print("=" * 80)

def shuffle_sort(mapped_pairs):
    """
    SHUFFLE & SORT: Group all values for each unique key
    
    Input: list of (key, value) pairs
    Output: dict of {key: [list of values]}
    """
    shuffled = defaultdict(list)
    for key, value in mapped_pairs:
        shuffled[key].append(value)
    return dict(sorted(shuffled.items()))

shuffled_data = shuffle_sort(mapped_data)

print(f"\nShuffle & Sort results:")
print(f"   Unique keys (words): {len(shuffled_data)}")
print(f"   Sample grouped data:")
for word, values in list(shuffled_data.items())[:5]:
    print(f"      '{word}': {values} (count: {len(values)})")

# REDUCE PHASE
print("\n" + "=" * 80)
print("REDUCE PHASE: Aggregate values for each key")
print("=" * 80)

def reduce_function(key, values):
    """
    REDUCE function: Sum all values for a key
    
    Input: key (word), values (list of 1s)
    Output: (key, sum of values)
    """
    return (key, sum(values))

# Apply reduce function
reduced_data = {}
for key, values in shuffled_data.items():
    word, count = reduce_function(key, values)
    reduced_data[word] = count

# Sort by count (descending)
sorted_words = sorted(reduced_data.items(), key=lambda x: x[1], reverse=True)

print(f"\n✅ WORD COUNT RESULTS:")
print(f"\n{'Word':<20} {'Count':<10} {'Percentage'}")
print("-" * 50)

total_words = sum(reduced_data.values())
for word, count in sorted_words[:15]:
    percentage = (count / total_words) * 100
    print(f"{word:<20} {count:<10} {percentage:>6.2f}%")

# ============================================================================
# PART 3: ADVANCED MAPREDUCE - DATA AGGREGATION
# ============================================================================

print("\n" + "=" * 80)
print("PART 3: ADVANCED EXAMPLE - LOG FILE ANALYSIS")
print("=" * 80)

# Simulate web server log data
log_data = [
    {"timestamp": "2025-10-27 10:15:23", "ip": "192.168.1.100", "status": 200, "bytes": 1024, "url": "/home"},
    {"timestamp": "2025-10-27 10:16:45", "ip": "192.168.1.101", "status": 404, "bytes": 512, "url": "/missing"},
    {"timestamp": "2025-10-27 10:17:12", "ip": "192.168.1.100", "status": 200, "bytes": 2048, "url": "/products"},
    {"timestamp": "2025-10-27 10:18:33", "ip": "192.168.1.102", "status": 200, "bytes": 1536, "url": "/home"},
    {"timestamp": "2025-10-27 10:19:54", "ip": "192.168.1.101", "status": 500, "bytes": 256, "url": "/api"},
    {"timestamp": "2025-10-27 10:20:15", "ip": "192.168.1.103", "status": 200, "bytes": 3072, "url": "/download"},
    {"timestamp": "2025-10-27 10:21:36", "ip": "192.168.1.100", "status": 200, "bytes": 1024, "url": "/about"},
    {"timestamp": "2025-10-27 10:22:57", "ip": "192.168.1.104", "status": 403, "bytes": 0, "url": "/admin"},
    {"timestamp": "2025-10-27 10:23:18", "ip": "192.168.1.102", "status": 200, "bytes": 2560, "url": "/contact"},
    {"timestamp": "2025-10-27 10:24:39", "ip": "192.168.1.101", "status": 200, "bytes": 1792, "url": "/services"},
]

print(f"\nLog Data Sample:")
for i, log in enumerate(log_data[:3], 1):
    print(f"   {i}. {log}")

# MapReduce Job 1: Status Code Distribution
print("\n" + "-" * 80)
print("MAPREDUCE JOB 1: Status Code Distribution")
print("-" * 80)

# Map: Extract status codes
status_mapped = [(log["status"], 1) for log in log_data]
# Reduce: Count each status
status_counts = Counter(status for status, _ in status_mapped)

print(f"\nStatus Code Distribution:")
for status, count in sorted(status_counts.items()):
    print(f"   HTTP {status}: {count} requests")

# MapReduce Job 2: Bandwidth per IP
print("\n" + "-" * 80)
print("MAPREDUCE JOB 2: Bandwidth Usage per IP Address")
print("-" * 80)

# Map: Extract (IP, bytes)
bandwidth_mapped = [(log["ip"], log["bytes"]) for log in log_data]
# Reduce: Sum bytes per IP
bandwidth_by_ip = defaultdict(int)
for ip, bytes_transferred in bandwidth_mapped:
    bandwidth_by_ip[ip] += bytes_transferred

print(f"\nBandwidth Usage:")
for ip, total_bytes in sorted(bandwidth_by_ip.items(), key=lambda x: x[1], reverse=True):
    print(f"   {ip}: {total_bytes:,} bytes ({total_bytes/1024:.2f} KB)")

# MapReduce Job 3: Most Popular URLs
print("\n" + "-" * 80)
print("MAPREDUCE JOB 3: Most Popular URLs")
print("-" * 80)

# Map: Extract URLs
url_mapped = [(log["url"], 1) for log in log_data]
# Reduce: Count each URL
url_counts = Counter(url for url, _ in url_mapped)

print(f"\nTop URLs:")
for url, count in url_counts.most_common():
    print(f"   {url}: {count} visits")

# ============================================================================
# PART 4: MAPREDUCE PATTERNS (Erl/Buhler/Khattak Chapter 4)
# ============================================================================

print("\n" + "=" * 80)
print("PART 4: COMMON MAPREDUCE PATTERNS")
print("=" * 80)

patterns = {
    "Counting & Summarizing": {
        "Description": "Count occurrences or calculate statistics",
        "Examples": ["Word Count", "Log Analysis", "User Activity Tracking"],
        "Map Output": "(key, 1) or (key, value)",
        "Reduce Output": "(key, sum/count/avg)"
    },
    "Filtering & Searching": {
        "Description": "Filter data based on criteria",
        "Examples": ["Error Log Filtering", "Data Validation", "Pattern Matching"],
        "Map Output": "(key, record) if condition",
        "Reduce Output": "(key, [filtered_records])"
    },
    "Sorting & Ranking": {
        "Description": "Order data by specific fields",
        "Examples": ["Top-K Problems", "Leaderboards", "Search Results"],
        "Map Output": "(score, record)",
        "Reduce Output": "Sorted list"
    },
    "Joining & Merging": {
        "Description": "Combine data from multiple sources",
        "Examples": ["Database Joins", "Data Integration", "Entity Resolution"],
        "Map Output": "(join_key, (source, record))",
        "Reduce Output": "(key, merged_records)"
    },
    "Grouping & Aggregation": {
        "Description": "Group data and compute aggregates",
        "Examples": ["GROUP BY operations", "Sales by Region", "Analytics"],
        "Map Output": "(group_key, value)",
        "Reduce Output": "(group_key, aggregate)"
    }
}

print("\nCommon MapReduce Patterns (Chapter 4.3):")
print("=" * 80)
for pattern_name, details in patterns.items():
    print(f"\n{pattern_name}:")
    for key, value in details.items():
        if isinstance(value, list):
            print(f"   {key}: {', '.join(value)}")
        else:
            print(f"   {key}: {value}")

# ============================================================================
# PART 5: HADOOP VS SPARK COMPARISON
# ============================================================================

print("\n" + "=" * 80)
print("PART 5: HADOOP vs SPARK - BIG DATA FRAMEWORKS")
print("=" * 80)

comparison = pd.DataFrame({
    'Feature': [
        'Processing Model',
        'Speed',
        'Data Storage',
        'Fault Tolerance',
        'Ease of Use',
        'Real-Time Processing',
        'Iterative Processing',
        'Language Support'
    ],
    'Hadoop MapReduce': [
        'Batch processing',
        'Slower (disk I/O)',
        'HDFS',
        'Replication',
        'Complex (Java)',
        'Not suitable',
        'Slow',
        'Java, Python (limited)'
    ],
    'Apache Spark': [
        'Batch + Streaming',
        'Faster (in-memory)',
        'HDFS, S3, Cassandra',
        'RDD lineage',
        'Easier (Python, Scala)',
        'Yes (Spark Streaming)',
        'Fast (100x)',
        'Python, Scala, Java, R, SQL'
    ]
})

print("\nFramework Comparison:")
print(comparison.to_string(index=False))

print("\n\nWHEN TO USE:")
print("━" * 80)
print("\nHadoop MapReduce:")
print("   ✓ Very large batch processing jobs")
print("   ✓ Budget constraints (free, open-source)")
print("   ✓ Linear data processing workflows")
print("   ✓ Mature, stable production environment")

print("\nApache Spark:")
print("   ✓ Iterative algorithms (ML, Graph processing)")
print("   ✓ Real-time data processing")
print("   ✓ Interactive data analysis")
print("   ✓ Complex data pipelines with multiple stages")

# ============================================================================
# PART 6: BIG DATA PIPELINE ARCHITECTURE
# ============================================================================

print("\n" + "=" * 80)
print("PART 6: BIG DATA PIPELINE ARCHITECTURE")
print("=" * 80)

print("""
COMPLETE BIG DATA PIPELINE (Erl/Buhler/Khattak, Chapter 4.5):
=============================================================

1. DATA INGESTION
   • Batch: HDFS, S3, databases
   • Streaming: Kafka, Kinesis, Flume
   • APIs: REST, Web scraping

2. DATA STORAGE
   • Distributed File Systems: HDFS, S3
   • NoSQL Databases: HBase, Cassandra, MongoDB
   • Data Lakes: Delta Lake, Iceberg

3. DATA PROCESSING
   • Batch: Hadoop MapReduce, Spark Batch
   • Stream: Spark Streaming, Flink, Storm
   • SQL: Hive, Spark SQL, Presto

4. DATA ANALYSIS
   • Analytics: Spark MLlib, Mahout
   • Visualization: Tableau, PowerBI
   • Querying: Impala, Drill

5. DATA SERVING
   • Applications: APIs, Web services
   • Dashboards: Grafana, Kibana
   • Databases: PostgreSQL, MySQL

CHARACTERISTICS OF BIG DATA (5 Vs):
==================================
✓ VOLUME: Terabytes to Petabytes of data
✓ VELOCITY: High-speed data generation and processing
✓ VARIETY: Structured, semi-structured, unstructured
✓ VERACITY: Data quality and trustworthiness
✓ VALUE: Business insights and decision-making
""")

# ============================================================================
# PART 7: SAVE RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("PART 7: SAVING RESULTS")
print("=" * 80)

# 1. Word Count Results
df_word_count = pd.DataFrame(sorted_words, columns=['Word', 'Count'])
df_word_count['Percentage'] = (df_word_count['Count'] / total_words) * 100
df_word_count.to_csv('mapreduce_word_count.csv', index=False)
print("\n💾 Saved: mapreduce_word_count.csv")

# 2. Log Analysis Results
df_status = pd.DataFrame(list(status_counts.items()), columns=['Status_Code', 'Count'])
df_status.to_csv('mapreduce_status_codes.csv', index=False)
print("💾 Saved: mapreduce_status_codes.csv")

df_bandwidth = pd.DataFrame(list(bandwidth_by_ip.items()), columns=['IP_Address', 'Bytes'])
df_bandwidth['KB'] = df_bandwidth['Bytes'] / 1024
df_bandwidth = df_bandwidth.sort_values('Bytes', ascending=False)
df_bandwidth.to_csv('mapreduce_bandwidth.csv', index=False)
print("💾 Saved: mapreduce_bandwidth.csv")

df_urls = pd.DataFrame(list(url_counts.items()), columns=['URL', 'Visits'])
df_urls = df_urls.sort_values('Visits', ascending=False)
df_urls.to_csv('mapreduce_url_popularity.csv', index=False)
print("💾 Saved: mapreduce_url_popularity.csv")

# 3. MapReduce Patterns
df_patterns = pd.DataFrame([
    {
        'Pattern': name,
        'Description': details['Description'],
        'Examples': ', '.join(details['Examples'])
    }
    for name, details in patterns.items()
])
df_patterns.to_csv('mapreduce_patterns.csv', index=False)
print("💾 Saved: mapreduce_patterns.csv")

# 4. Framework Comparison
comparison.to_csv('hadoop_vs_spark.csv', index=False)
print("💾 Saved: hadoop_vs_spark.csv")

# ============================================================================
# PART 8: KEY CONCEPTS FROM THE BOOK
# ============================================================================

print("\n" + "=" * 80)
print("PART 8: KEY CONCEPTS SUMMARY")
print("=" * 80)

concepts = {
    'MapReduce Model': {
        'Chapter': '3.2',
        'Definition': 'Programming model for processing large datasets in parallel',
        'Components': 'Map function, Shuffle/Sort, Reduce function',
        'Advantage': 'Hides distributed computing complexity'
    },
    'Data Locality': {
        'Chapter': '3.3',
        'Definition': 'Move computation to data, not data to computation',
        'Benefit': 'Reduces network bandwidth usage',
        'Implementation': 'HDFS block placement strategy'
    },
    'Fault Tolerance': {
        'Chapter': '3.4',
        'Definition': 'System continues operating despite failures',
        'Mechanism': 'Task re-execution, data replication',
        'Recovery': 'Automatic restart of failed tasks'
    },
    'Scalability': {
        'Chapter': '4.1',
        'Definition': 'Handle growing amounts of data by adding resources',
        'Types': 'Horizontal (add nodes) vs Vertical (add power)',
        'MapReduce': 'Linearly scalable with cluster size'
    }
}

print("\nKey Concepts from 'Big Data Fundamentals':")
print("=" * 80)
for concept, details in concepts.items():
    print(f"\n{concept} (Chapter {details['Chapter']}):")
    for key, value in details.items():
        if key != 'Chapter':
            print(f"   {key}: {value}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("FINAL SUMMARY - BIG DATA FUNDAMENTALS")
print("=" * 80)

print(f"""
📊 ANALYSIS COMPLETED:
====================
✅ Word Count: {len(reduced_data)} unique words processed
✅ Log Analysis: {len(log_data)} log entries analyzed
✅ Status Codes: {len(status_counts)} different HTTP codes
✅ Bandwidth: {len(bandwidth_by_ip)} unique IP addresses
✅ URL Popularity: {len(url_counts)} URLs tracked

📁 OUTPUT FILES (6 CSV):
======================
1. mapreduce_word_count.csv - Word frequency analysis
2. mapreduce_status_codes.csv - HTTP status distribution
3. mapreduce_bandwidth.csv - Bandwidth usage per IP
4. mapreduce_url_popularity.csv - Most visited URLs
5. mapreduce_patterns.csv - Common MapReduce patterns
6. hadoop_vs_spark.csv - Framework comparison

📚 REFERENCES:
============
- Erl, Buhler & Khattak, "Big Data Fundamentals"
- Chapter 3: MapReduce Programming Model
- Chapter 4: Distributed Data Processing Patterns

🎯 KEY LEARNINGS:
===============
• MapReduce separates WHAT to compute from HOW to distribute
• Map phase: Transform data into key-value pairs
• Reduce phase: Aggregate values for each key
• Fault tolerance through task re-execution
• Scalability through horizontal expansion
• Spark provides 100x faster in-memory processing

🚀 APPLICATIONS:
==============
- Web indexing and search (Google)
- Log analysis and monitoring
- Data warehousing and ETL
- Machine learning at scale
- Scientific data processing
- Financial analytics

✅ READY FOR PROFESSOR PRESENTATION AT 17:00!
""")

print("\n" + "=" * 80)
print("✅ BIG DATA ANALYSIS COMPLETE!")
print("=" * 80)
