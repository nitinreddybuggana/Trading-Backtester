import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
 
# ── 1. CONFIGURATION ──────────────────────────────────────────────────────────
TICKER       = "MSFT"
START        = "2006-01-01"
END          = "2026-01-01"
STARTING_CAP = 10_000
 
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
cash      = STARTING_CAP
shares    = 0
portfolio = []
 
for date, row in df.iterrows():
    if row["Position"] == 1.0:
        shares = cash / row["Close"]
        cash   = 0
    elif row["Position"] == -1.0 and shares > 0:
        cash   = shares * row["Close"]
        shares = 0
    portfolio.append(cash + shares * row["Close"])
 
df["Portfolio"]    = portfolio
df["Buy_and_Hold"] = (STARTING_CAP / df["Close"].iloc[0]) * df["Close"]
 
# ── 5. DRAWDOWN ───────────────────────────────────────────────────────────────
rolling_max    = df["Portfolio"].cummax()
df["Drawdown"] = (df["Portfolio"] - rolling_max) / rolling_max * 100
 
buy_signals  = df[df["Position"] == 1.0]
sell_signals = df[df["Position"] == -1.0]
 
# ── 6. PLOT ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 10))
gs  = gridspec.GridSpec(3, 1, height_ratios=[2, 1.5, 1], hspace=0.4)
 
# ── Chart 1: Price + SMAs ─────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])
ax1.plot(df["Close"],  label="AAPL Close Price", alpha=0.5, linewidth=1,   color="steelblue")
ax1.plot(df["SMA50"],  label="50-Day SMA",        linewidth=1.5,            color="orange")
ax1.plot(df["SMA200"], label="200-Day SMA",        linewidth=1.5,            color="green")
ax1.scatter(buy_signals.index,  buy_signals["Close"],  marker="^", color="green", s=120, zorder=5, label="Buy")
ax1.scatter(sell_signals.index, sell_signals["Close"], marker="v", color="red",   s=120, zorder=5, label="Sell")
ax1.set_title(f"{TICKER} — Price & Signals")
ax1.set_ylabel("Price (USD)")
ax1.legend(loc="upper left", fontsize=8)
ax1.grid(alpha=0.3)
 
# ── Chart 2: Equity Curve ─────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1])
ax2.plot(df["Portfolio"],    label=f"Strategy  (${df['Portfolio'].iloc[-1]:,.0f})",    linewidth=1.5, color="royalblue")
ax2.plot(df["Buy_and_Hold"], label=f"Buy & Hold (${df['Buy_and_Hold'].iloc[-1]:,.0f})", linewidth=1.5, color="darkorange", linestyle="--")
ax2.axhline(STARTING_CAP, color="grey", linewidth=0.8, linestyle=":")
ax2.set_title("Equity Curve — Strategy vs Buy & Hold")
ax2.set_ylabel("Portfolio Value (USD)")
ax2.legend(loc="upper left", fontsize=8)
ax2.grid(alpha=0.3)
 
# ── Chart 3: Drawdown ─────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
ax3.fill_between(df.index, df["Drawdown"], 0, color="red", alpha=0.4, label="Drawdown")
ax3.set_title("Strategy Drawdown (%)")
ax3.set_ylabel("Drawdown (%)")
ax3.set_xlabel("Date")
ax3.legend(loc="lower left", fontsize=8)
ax3.grid(alpha=0.3)
 
plt.savefig("phase4_visualisation.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart saved to phase4_visualisation.png")