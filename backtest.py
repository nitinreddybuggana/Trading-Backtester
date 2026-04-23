import yfinance as yf
import pandas as pd
import numpy as np
 
# ── 1. CONFIGURATION ──────────────────────────────────────────────────────────
TICKER         = "AAPL"
START          = "2018-01-01"
END            = "2024-01-01"
STARTING_CAP   = 10_000        # Starting capital in USD
 
# ── 2. FETCH & PREPARE DATA ───────────────────────────────────────────────────
print(f"Fetching data for {TICKER}...")
df = yf.download(TICKER, start=START, end=END)
df.dropna(inplace=True)
df.columns = df.columns.get_level_values(0)
 
# ── 3. MOVING AVERAGES & SIGNALS ──────────────────────────────────────────────
df["SMA50"]    = df["Close"].rolling(window=50).mean()
df["SMA200"]   = df["Close"].rolling(window=200).mean()
df["Signal"]   = 0
df.loc[df["SMA50"] > df["SMA200"], "Signal"] = 1
df["Position"] = df["Signal"].diff()
 
# ── 4. SIMULATE TRADES ────────────────────────────────────────────────────────
cash        = STARTING_CAP
shares      = 0
portfolio   = []   # tracks total portfolio value each day
trade_log   = []   # records each buy/sell
 
for date, row in df.iterrows():
    if row["Position"] == 1.0:
        # BUY — spend all cash on shares
        shares = cash / row["Close"]
        cash   = 0
        trade_log.append({
            "Date"   : date,
            "Action" : "BUY",
            "Price"  : round(row["Close"], 2),
            "Shares" : round(shares, 4)
        })
 
    elif row["Position"] == -1.0 and shares > 0:
        # SELL — convert all shares back to cash
        cash   = shares * row["Close"]
        shares = 0
        trade_log.append({
            "Date"   : date,
            "Action" : "SELL",
            "Price"  : round(row["Close"], 2),
            "Cash"   : round(cash, 2)
        })
 
    # Daily portfolio value = cash + value of shares held
    total_value = cash + (shares * row["Close"])
    portfolio.append(total_value)
 
df["Portfolio"] = portfolio
 
# If still holding shares at end, calculate final value
final_value = cash if shares == 0 else shares * df["Close"].iloc[-1]
 
# ── 5. BENCHMARK — BUY AND HOLD ───────────────────────────────────────────────
# How would we have done if we just bought on day 1 and never sold?
shares_bh         = STARTING_CAP / df["Close"].iloc[0]
df["Buy_and_Hold"] = shares_bh * df["Close"]
 
# ── 6. PERFORMANCE METRICS ────────────────────────────────────────────────────
total_return    = ((final_value - STARTING_CAP) / STARTING_CAP) * 100
bh_final        = df["Buy_and_Hold"].iloc[-1]
bh_return       = ((bh_final - STARTING_CAP) / STARTING_CAP) * 100
 
# Daily returns for Sharpe ratio
df["Daily_Return"] = df["Portfolio"].pct_change()
sharpe_ratio = (df["Daily_Return"].mean() / df["Daily_Return"].std()) * np.sqrt(252)
 
# Maximum drawdown — largest peak to trough drop
rolling_max  = df["Portfolio"].cummax()
drawdown     = (df["Portfolio"] - rolling_max) / rolling_max
max_drawdown = drawdown.min() * 100
 
# ── 7. PRINT RESULTS ──────────────────────────────────────────────────────────
print("\n── Trade Log ───────────────────────────")
for trade in trade_log:
    print(trade)
 
print("\n── Performance Metrics ─────────────────")
print(f"Starting Capital  : ${STARTING_CAP:,.2f}")
print(f"Final Value       : ${final_value:,.2f}")
print(f"Strategy Return   : {total_return:.2f}%")
print(f"Buy & Hold Return : {bh_return:.2f}%")
print(f"Sharpe Ratio      : {sharpe_ratio:.2f}")
print(f"Max Drawdown      : {max_drawdown:.2f}%")
