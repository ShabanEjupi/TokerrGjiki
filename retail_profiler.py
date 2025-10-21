# ===== PySpark Online Retail Profiler (Windows-safe, Spark 4.x, NO winutils/Hive) =====
# Dataset: Online Retail Dataset (UCI)
# Columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
# Outputs comprehensive analytics:
#   - schema.json
#   - null_counts.csv
#   - column_stats.csv             (overall numeric stats incl. median, Q1/Q3, IQR)
#   - country_stats.csv            (per-country sales stats)
#   - product_stats.csv            (per-product stats)
#   - customer_stats.csv           (per-customer stats)
#   - monthly_stats.csv            (time-based aggregations)
#   - returns_sample.csv           (sample with calculated metrics)
#   - sample_20.csv

from pathlib import Path
from typing import Optional
import os, sys, json
import pandas as pd

# ---------- 1) CONFIG ----------
INPUT_PATH = r"/workspaces/TokerrGjiki/data_kaggle/online_retail.xlsx"
TREAT_EMPTY_STRING_AS_NULL = True
RETURNS_SAMPLE_LIMIT = 50000

BASE = Path.cwd()
OUT  = BASE / "out_retail";  OUT.mkdir(exist_ok=True)
SCHEMA_JSON          = OUT / "schema.json"
NULLS_CSV            = OUT / "null_counts.csv"
COLSTATS_CSV         = OUT / "column_stats.csv"
COUNTRYSTATS_CSV     = OUT / "country_stats.csv"
PRODUCTSTATS_CSV     = OUT / "product_stats.csv"
CUSTOMERSTATS_CSV    = OUT / "customer_stats.csv"
MONTHLYSTATS_CSV     = OUT / "monthly_stats.csv"
METRICS_SAMPLE_CSV   = OUT / "metrics_sample.csv"
SAMPLE_CSV           = OUT / "sample_20.csv"

LOCAL_TMP_DIR = BASE / "spark-tmp"
LOCAL_TMP_DIR.mkdir(exist_ok=True)

# Use THIS Python (avoids 'python3' worker issues on Windows)
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession, functions as F, types as T, Window

spark = (
    SparkSession.builder
    .appName("RetailProfiler_NoWinutils")
    .master("local[*]")
    .config("spark.sql.catalogImplementation", "in-memory")       # no Hive
    .config("spark.local.dir", str(LOCAL_TMP_DIR.resolve()).replace("\\", "/"))
    .config("spark.driver.bindAddress", "127.0.0.1")
    .config("spark.driver.host", "127.0.0.1")
    .getOrCreate()
)

print("=" * 80)
print("PySpark Online Retail Profiler")
print("=" * 80)
print("Spark version:", spark.version)

# ---------- 3) Load dataset on the DRIVER with pandas ----------
path = Path(INPUT_PATH)
ext = path.suffix.lower()

def load_to_pandas(p: Path) -> pd.DataFrame:
    if ext in (".csv", ".txt"):
        return pd.read_csv(p, low_memory=False)
    elif ext == ".json":
        try:
            return pd.read_json(p, lines=True)
        except ValueError:
            return pd.read_json(p)
    elif ext == ".parquet":
        return pd.read_parquet(p)
    elif ext in (".xlsx", ".xls"):
        return pd.read_excel(p, engine='openpyxl')
    else:
        raise ValueError(f"Unsupported file type: {ext}")

print(f"\nLoading data from: {INPUT_PATH}")
pdf = load_to_pandas(path)
print(f"Loaded with pandas -> shape={pdf.shape}")

# ---------- 4) Create Spark DataFrame ----------
df = spark.createDataFrame(pdf)

if TREAT_EMPTY_STRING_AS_NULL:
    for c, t in df.dtypes:
        if t == "string":
            df = df.withColumn(c, F.when(F.trim(F.col(c)) == "", F.lit(None)).otherwise(F.col(c)))

# Parse InvoiceDate -> timestamp/date
df = df.withColumn("ts", F.to_timestamp("InvoiceDate")) \
       .withColumn("d",  F.to_date("ts")) \
       .withColumn("year",  F.year("ts")) \
       .withColumn("month", F.month("ts")) \
       .withColumn("year_month", F.date_format("d", "yyyy-MM"))

# Ensure numeric types
numeric_casts = {
    "Quantity": "int",
    "UnitPrice": "double",
    "CustomerID": "string"  # Keep as string to handle nulls
}
for col, typ in numeric_casts.items():
    if col in df.columns:
        df = df.withColumn(col, F.col(col).cast(typ))

# Add calculated fields
df = df.withColumn("TotalPrice", F.col("Quantity") * F.col("UnitPrice"))
df = df.withColumn("IsReturn", F.when(F.col("Quantity") < 0, 1).otherwise(0))

df = df.cache()
row_count = df.count()
print(f"\nTotal rows: {row_count:,}")
df.printSchema()

# ---------- 5) Save schema ----------
SCHEMA_JSON.write_text(json.dumps(df.schema.jsonValue(), indent=2))
print(f"\n✓ Saved schema -> {SCHEMA_JSON.as_posix()}")

# ---------- 6) Null counts ----------
null_exprs = [F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).cast("long").alias(c) for c in df.columns]
null_counts_row = df.select(*null_exprs).first().asDict()
pd.DataFrame([null_counts_row]).to_csv(NULLS_CSV, index=False)
print(f"✓ Saved null counts -> {NULLS_CSV.as_posix()}")

# ---------- 7) Overall numeric stats (incl. median & quartiles) ----------
dtypes = dict(df.dtypes)

def is_numeric(t: str) -> bool:
    t = t.lower()
    return t in {"byte","short","int","long","float","double","bigint"} or t.startswith("decimal")

num_cols = [c for c, t in dtypes.items() if is_numeric(t)]

def q(col_name: str, p: float, accuracy: int = 10000):
    return F.percentile_approx(F.col(col_name), p, accuracy)

col_rows = []
for c in num_cols:
    agg = df.agg(
        F.count(F.col(c)).alias("non_null_count"),
        F.countDistinct(F.col(c)).alias("distinct_count"),
        F.mean(F.col(c)).alias("mean"),
        F.stddev_samp(F.col(c)).alias("stddev"),
        F.min(F.col(c)).alias("min"),
        q(c, 0.25).alias("q1"),
        q(c, 0.5).alias("median"),
        q(c, 0.75).alias("q3"),
        F.max(F.col(c)).alias("max"),
    ).first().asDict()

    non_null = int(agg["non_null_count"] or 0)
    missing = row_count - non_null
    q1 = agg["q1"]; q3 = agg["q3"]
    iqr = (q3 - q1) if (q1 is not None and q3 is not None) else None

    col_rows.append({
        "column": c,
        "count": row_count,
        "non_null_count": non_null,
        "missing_count": missing,
        "missing_rate": (missing / row_count) if row_count else None,
        "distinct_count": int(agg["distinct_count"]) if agg["distinct_count"] is not None else None,
        "mean": agg["mean"], "stddev": agg["stddev"],
        "min": agg["min"], "q1": q1, "median": agg["median"], "q3": q3, "max": agg["max"], "iqr": iqr
    })

pd.DataFrame(col_rows).to_csv(COLSTATS_CSV, index=False)
print(f"✓ Saved column stats -> {COLSTATS_CSV.as_posix()}")

# ---------- 8) Per-country stats ----------
country_stats = (
    df.groupBy("Country").agg(
        F.count(F.lit(1)).alias("transactions"),
        F.countDistinct(F.col("CustomerID")).alias("unique_customers"),
        F.countDistinct(F.col("InvoiceNo")).alias("unique_invoices"),
        F.countDistinct(F.col("StockCode")).alias("unique_products"),
        F.sum(F.col("Quantity")).alias("total_quantity"),
        F.sum(F.col("TotalPrice")).alias("total_revenue"),
        F.mean(F.col("TotalPrice")).alias("avg_transaction_value"),
        q("TotalPrice", 0.5).alias("median_transaction_value"),
        F.sum(F.col("IsReturn")).alias("returns_count"),
        F.mean(F.col("IsReturn")).alias("return_rate")
    )
    .orderBy(F.desc("total_revenue"))
)

country_stats.toPandas().to_csv(COUNTRYSTATS_CSV, index=False)
print(f"✓ Saved per-country stats -> {COUNTRYSTATS_CSV.as_posix()}")

# ---------- 9) Per-product stats (Top products) ----------
product_stats = (
    df.filter(F.col("Quantity") > 0)  # Exclude returns for product ranking
    .groupBy("StockCode", "Description").agg(
        F.count(F.lit(1)).alias("transactions"),
        F.sum(F.col("Quantity")).alias("total_quantity_sold"),
        F.sum(F.col("TotalPrice")).alias("total_revenue"),
        F.mean(F.col("UnitPrice")).alias("avg_unit_price"),
        F.countDistinct(F.col("CustomerID")).alias("unique_customers"),
        F.countDistinct(F.col("Country")).alias("countries_sold")
    )
    .orderBy(F.desc("total_revenue"))
    .limit(1000)  # Top 1000 products
)

product_stats.toPandas().to_csv(PRODUCTSTATS_CSV, index=False)
print(f"✓ Saved per-product stats (top 1000) -> {PRODUCTSTATS_CSV.as_posix()}")

# ---------- 10) Per-customer stats ----------
customer_stats = (
    df.filter(F.col("CustomerID").isNotNull())
    .groupBy("CustomerID", "Country").agg(
        F.count(F.lit(1)).alias("transactions"),
        F.countDistinct(F.col("InvoiceNo")).alias("unique_invoices"),
        F.countDistinct(F.col("StockCode")).alias("unique_products_purchased"),
        F.sum(F.col("Quantity")).alias("total_quantity"),
        F.sum(F.col("TotalPrice")).alias("total_spent"),
        F.mean(F.col("TotalPrice")).alias("avg_transaction_value"),
        F.min(F.col("d")).alias("first_purchase_date"),
        F.max(F.col("d")).alias("last_purchase_date"),
        F.sum(F.col("IsReturn")).alias("returns_count")
    )
    .orderBy(F.desc("total_spent"))
    .limit(5000)  # Top 5000 customers
)

customer_stats.toPandas().to_csv(CUSTOMERSTATS_CSV, index=False)
print(f"✓ Saved per-customer stats (top 5000) -> {CUSTOMERSTATS_CSV.as_posix()}")

# ---------- 11) Monthly time-series stats ----------
monthly_stats = (
    df.groupBy("year", "month", "year_month").agg(
        F.count(F.lit(1)).alias("transactions"),
        F.countDistinct(F.col("InvoiceNo")).alias("unique_invoices"),
        F.countDistinct(F.col("CustomerID")).alias("unique_customers"),
        F.countDistinct(F.col("StockCode")).alias("unique_products"),
        F.sum(F.col("Quantity")).alias("total_quantity"),
        F.sum(F.col("TotalPrice")).alias("total_revenue"),
        F.mean(F.col("TotalPrice")).alias("avg_transaction_value"),
        F.sum(F.col("IsReturn")).alias("returns_count"),
        F.mean(F.col("IsReturn")).alias("return_rate")
    )
    .orderBy("year", "month")
)

monthly_stats.toPandas().to_csv(MONTHLYSTATS_CSV, index=False)
print(f"✓ Saved monthly stats -> {MONTHLYSTATS_CSV.as_posix()}")

# ---------- 12) Sample with calculated metrics ----------
# Add customer lifetime metrics using window functions
w = Window.partitionBy("CustomerID").orderBy(F.col("ts").asc_nulls_last())

df_metrics = (
    df.filter(F.col("CustomerID").isNotNull())
    .withColumn("customer_transaction_num", F.row_number().over(w))
    .withColumn("cumulative_spent", F.sum(F.col("TotalPrice")).over(w.rowsBetween(Window.unboundedPreceding, 0)))
)

# Export sample
df_metrics.orderBy("CustomerID", "ts").limit(RETURNS_SAMPLE_LIMIT).toPandas().to_csv(METRICS_SAMPLE_CSV, index=False)
print(f"✓ Saved metrics sample -> {METRICS_SAMPLE_CSV.as_posix()}")

# ---------- 13) Tiny sample (first 20 rows) ----------
df.limit(20).toPandas().to_csv(SAMPLE_CSV, index=False)
print(f"✓ Saved sample (20 rows) -> {SAMPLE_CSV.as_posix()}")

# ---------- SUMMARY ----------
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - Outputs generated:")
print("=" * 80)
print(f" - Schema                : {SCHEMA_JSON.as_posix()}")
print(f" - Null counts           : {NULLS_CSV.as_posix()}")
print(f" - Column stats          : {COLSTATS_CSV.as_posix()}")
print(f" - Per-country stats     : {COUNTRYSTATS_CSV.as_posix()}")
print(f" - Per-product stats     : {PRODUCTSTATS_CSV.as_posix()}")
print(f" - Per-customer stats    : {CUSTOMERSTATS_CSV.as_posix()}")
print(f" - Monthly stats         : {MONTHLYSTATS_CSV.as_posix()}")
print(f" - Metrics sample        : {METRICS_SAMPLE_CSV.as_posix()}")
print(f" - Sample (20 rows)      : {SAMPLE_CSV.as_posix()}")
print("=" * 80)

spark.stop()
print("✓ Spark session stopped")
