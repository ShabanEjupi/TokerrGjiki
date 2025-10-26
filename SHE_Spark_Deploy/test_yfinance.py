import yfinance as yf
import pandas as pd

# Test download
print("Testing yfinance download...")
df = yf.download('AAPL', start='2022-01-01', end='2025-10-26', progress=False)

print(f"Type: {type(df)}")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nClose column type: {type(df['Close'])}")
print(f"Close column shape: {df['Close'].shape}")
