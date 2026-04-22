import yfinance as yf
import pandas as pd
 
# ── 1. CONFIGURATION ──────────────────────────────────────────────────────────
TICKER = "AAPL"          # Change to any stock symbol e.g. "MSFT", "SPY", "TSLA"
START  = "2018-01-01"
END    = "2024-01-01"
 
# ── 2. FETCH DATA ─────────────────────────────────────────────────────────────
print(f"Fetching data for {TICKER}...")
df = yf.download(TICKER, start=START, end=END)
 
# ── 3. CLEAN DATA ─────────────────────────────────────────────────────────────
df.dropna(inplace=True)                  # Remove any rows with missing values
df.index = pd.to_datetime(df.index)      # Ensure index is datetime
 
# ── 4. EXPLORE DATA ───────────────────────────────────────────────────────────
print("\n── Shape ──────────────────────────────")
print(f"{df.shape[0]} rows, {df.shape[1]} columns")
 
print("\n── Columns ────────────────────────────")
print(df.columns.tolist())
# Columns explained:
#   Open   → price at market open
#   High   → highest price that day
#   Low    → lowest price that day
#   Close  → price at market close  ← this is what we'll use for our strategy
#   Volume → number of shares traded
 
print("\n── First 5 rows ────────────────────────")
print(df.head())
 
print("\n── Last 5 rows ─────────────────────────")
print(df.tail())
 
print("\n── Basic statistics ────────────────────")
print(df["Close"].describe())
 
print("\n── Date range ──────────────────────────")
print(f"From : {df.index[0].date()}")
print(f"To   : {df.index[-1].date()}")
print(f"Days : {len(df)}")
 
# ── 5. SAVE TO CSV (optional) ─────────────────────────────────────────────────
df.to_csv(f"{TICKER}_data.csv")
print(f"\nData saved to {TICKER}_data.csv")