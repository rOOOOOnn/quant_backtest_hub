# quant_backtest_hub
Team strategy backtesting engine

## 🔁 How to Contribute a New Strategy

1. Fork this repo
2. Add your strategy to `strategies/your_name_strategy.py`
3. Run your strategy, generate `results/your_name_strategy.json`
4. Submit a Pull Request (PR)



## 🧪 Strategy Testing Workflow

1. Write your strategy in `strategies/your_strategy.py`
2. It should return a DataFrame with `Close` and `signal` columns
3. Run it using `engine/backtest.py`
4. Save results to `results/your_strategy.json`
5. Submit it to the repo (or share via Google Sheet)

Example:
```python
from strategies.your_strategy import generate_signal
from engine.backtest import backtest
import yfinance as yf

df = yf.download("AAPL", start="2022-01-01", end="2024-01-01")
signals = generate_signal(df)
results = backtest(signals)
