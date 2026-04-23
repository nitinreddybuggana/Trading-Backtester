import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
 
# ── 1. CONFIGURATION ──────────────────────────────────────────────────────────
TICKER = "AAPL"
START  = "2018-01-01"
END    = "2024-01-01"
 
# ── 2. FETCH & PREPARE DATA ───────────────────────────────────────────────────
print(f"Fetching data for {TICKER}...")
df = yf.download(TICKER, start=START, end=END)
df.dropna(inplace=True)
 
# Flatten the multi-level columns from yfinance
df.columns = df.columns.get_level_values(0)
 
# ── 3. CALCULATE MOVING AVERAGES ──────────────────────────────────────────────
df["SMA50"]  = df["Close"].rolling(window=50).mean()   # 50-day average
df["SMA200"] = df["Close"].rolling(window=200).mean()  # 200-day average
 
print("\n── Moving Averages (last 5 rows) ───────")
print(df[["Close", "SMA50", "SMA200"]].tail())
 
# ── 4. GENERATE BUY/SELL SIGNALS ──────────────────────────────────────────────
# Signal = 1 when SMA50 is above SMA200 (uptrend), 0 when below (downtrend)
df["Signal"] = 0
df.loc[df["SMA50"] > df["SMA200"], "Signal"] = 1
 
# A trade happens on the day the signal CHANGES (crossover point)
df["Position"] = df["Signal"].diff()
 
# Position =  1.0 → BUY signal  (50-day just crossed above 200-day)
# Position = -1.0 → SELL signal (50-day just crossed below 200-day)
 
buy_signals  = df[df["Position"] == 1.0]
sell_signals = df[df["Position"] == -1.0]
 
print("\n── Buy signals ─────────────────────────")
print(buy_signals[["Close", "SMA50", "SMA200"]])
 
print("\n── Sell signals ────────────────────────")
print(sell_signals[["Close", "SMA50", "SMA200"]])
 
# ── 5. PLOT ───────────────────────────────────────────────────────────────────
plt.figure(figsize=(14, 7))
plt.plot(df["Close"],  label="AAPL Close Price", alpha=0.5, linewidth=1)
plt.plot(df["SMA50"],  label="50-Day SMA",  linewidth=1.5)
plt.plot(df["SMA200"], label="200-Day SMA", linewidth=1.5)
 
# Mark buy signals with green triangles
plt.scatter(buy_signals.index, buy_signals["Close"],
            marker="^", color="green", s=150, label="Buy Signal",  zorder=5)
 
# Mark sell signals with red triangles
plt.scatter(sell_signals.index, sell_signals["Close"],
            marker="v", color="red",   s=150, label="Sell Signal", zorder=5)
 
plt.title(f"{TICKER} — Golden Cross / Death Cross Strategy")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("phase2_signals.png", dpi=150)
plt.show()
print("\nChart saved to phase2_signals.png")
