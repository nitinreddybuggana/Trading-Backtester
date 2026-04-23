# Algorithmic Trading Backtester

A Python-based backtesting engine implementing a **Golden Cross / Death Cross** moving average crossover strategy on historical stock data. Configurable for any publicly traded ticker via API integration with Yahoo Finance.

---

## Visualisation

![Backtest Results](visualisation.png)

---

## Strategy

- **Buy signal** — 50-day SMA crosses above 200-day SMA (Golden Cross), indicating an uptrend
- **Sell signal** — 50-day SMA crosses below 200-day SMA (Death Cross), indicating a downtrend
- Configurable for any publicly traded ticker by updating the `TICKER` variable in each file

---

## Results (AAPL 2018–2024)

| Metric | Value |
|---|---|
| Starting Capital | $10,000 |
| Final Value | $22,230 |
| Strategy Return | 122.30% |
| Buy & Hold Return | 372.78% |
| Sharpe Ratio | 0.63 |
| Max Drawdown | -43.33% |

> **Note:** Buy & hold outperformed the strategy on AAPL due to its strong long-term uptrend. The strategy is better suited to more volatile or cyclical assets where trend reversals are more frequent. The two whipsaw trades in late 2022 (rapid crossovers in quick succession) were the primary drag on performance.

---

## How to Run

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Run each phase in order**
```bash
python3 data.py          # Fetch and explore historical stock data
python3 signals.py       # Calculate moving averages and generate buy/sell signals
python3 backtest.py      # Simulate trades and calculate performance metrics
python3 visualisation.py # Plot equity curve, signals, and drawdown
```

---

## Project Structure

```
trading-backtester/
├── data.py              # Phase 1 — data fetching and exploration via yfinance API
├── signals.py           # Phase 2 — SMA calculation and crossover signal generation
├── backtest.py          # Phase 3 — trade simulation and performance metrics
├── visualisation.py     # Phase 4 — 3-panel chart: price, equity curve, drawdown
├── visualisation.png    # Output chart
├── requirements.txt     # Dependencies
└── README.md
```

---

## Tech Stack

- **Python** — pandas, numpy, matplotlib, yfinance

---

## Key Concepts

- Moving average crossover strategy (Golden Cross / Death Cross)
- API integration for live and historical market data
- Portfolio simulation and trade execution logic
- Quantitative risk metrics: Sharpe ratio, maximum drawdown
- Benchmark comparison against buy & hold
- Data visualisation of equity curves and trading signals
