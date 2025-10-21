# PySpark Retail Analytics Project

## 📊 Dataset
**Online Retail Dataset** from UCI Machine Learning Repository
- Source: https://archive.ics.uci.edu/ml/datasets/Online+Retail
- Size: 541,909 transactions
- Format: Excel (.xlsx)
- Columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

## 🎯 Analysis Features

This PySpark script performs comprehensive retail analytics including:

1. **Data Profiling**
   - Schema validation and null counts
   - Column statistics (mean, median, quartiles, IQR)
   
2. **Business Metrics**
   - Per-country sales analysis
   - Top products by revenue
   - Customer lifetime value (CLV)
   - Monthly trends
   
3. **Advanced Analytics**
   - Return rate analysis
   - Customer segmentation
   - Transaction patterns
   - Cumulative customer spending

## 📁 Outputs

All outputs are saved in `out_retail/` directory:

- `schema.json` - Dataset schema
- `null_counts.csv` - Null value analysis
- `column_stats.csv` - Statistical summaries
- `country_stats.csv` - Per-country metrics
- `product_stats.csv` - Top 1000 products
- `customer_stats.csv` - Top 5000 customers
- `monthly_stats.csv` - Time-series analysis
- `metrics_sample.csv` - Sample with calculated metrics
- `sample_20.csv` - First 20 rows

## 🚀 Local Usage

```bash
# Install dependencies
pip install pyspark openpyxl pandas

# Run analysis
python retail_profiler.py
```

## 🌐 Deploy to Server

### Method 1: Automated Deployment
```bash
# Make script executable
chmod +x deploy_to_server.sh

# Run deployment (will prompt for credentials)
./deploy_to_server.sh
```

### Method 2: Manual Deployment
```bash
# Connect to server
chmod +x connect_to_server.sh
./connect_to_server.sh

# After connecting, upload files:
# In a separate terminal:
scp -P 8022 retail_profiler.py username@185.182.158.150:~/
scp -P 8022 data_kaggle/online_retail.xlsx username@185.182.158.150:~/

# On the server:
pip install --user pyspark openpyxl pandas
python retail_profiler.py
```

### Method 3: Direct Commands
```bash
# Test connection
ssh -p 8022 username@185.182.158.150

# Upload script
scp -P 8022 retail_profiler.py username@185.182.158.150:~/

# Upload dataset
scp -P 8022 data_kaggle/online_retail.xlsx username@185.182.158.150:~/

# Connect and run
ssh -p 8022 username@185.182.158.150
pip install --user pyspark openpyxl pandas
python retail_profiler.py
```

### Download Results
```bash
# Download all outputs
scp -P 8022 -r username@185.182.158.150:~/out_retail ./results_from_server/
```

## 🔧 Server Configuration

**Target Server:**
- IP: 185.182.158.150
- Port: 8022
- Internal mapping: 185.182.158.150:443 <-> 10.0.0.4:443

## 📝 Algorithm Implementation

The script implements several PySpark algorithms from your coursework:

1. **Aggregation & Grouping**
   - `groupBy()` with multiple aggregation functions
   - `countDistinct()` for unique value counting
   
2. **Window Functions**
   - `row_number()` for customer transaction sequencing
   - Running totals with `rowsBetween()`
   
3. **Statistical Functions**
   - `percentile_approx()` for quartile calculation
   - `stddev_samp()` for volatility measures
   
4. **Data Transformation**
   - Type casting and null handling
   - Calculated columns (TotalPrice, IsReturn)
   - Date/time parsing and formatting

## 🎓 Key Concepts Demonstrated

- ✅ DataFrame API operations
- ✅ UDF-free statistical computations
- ✅ Window functions for customer analytics
- ✅ Partitioning and ordering
- ✅ Multiple output formats
- ✅ Memory-efficient processing
- ✅ Cross-platform compatibility (Windows/Linux)

## 📊 Sample Insights

Run the script to discover:
- Which countries generate the most revenue?
- What are the best-selling products?
- Who are your most valuable customers?
- What are the monthly sales trends?
- What's the return rate by country?

## 🐛 Troubleshooting

**If you get connection errors:**
- Ensure SSH service is running on server
- Check firewall rules for port 8022
- Verify credentials

**If PySpark fails:**
- Check Java is installed: `java -version`
- Ensure sufficient memory
- Try reducing sample sizes in the script

**For Excel reading errors:**
- Ensure openpyxl is installed
- Check file path is correct

## 👨‍🏫 Professor Notes

This implementation extends the patterns from your course:
- Similar structure to stock profiler (Session 3)
- Uses pandas for initial loading (Session 2 pattern)
- Comprehensive windowing like Session 3
- Production-ready with error handling
- No Hadoop/winutils dependencies
