# 📊 Quant Backtest Hub

Welcome to the team's quantitative backtesting project! This repository allows every member to upload their own strategy, run unified backtests, and save results to a shared Excel file for easy comparison and analysis.

---

## 📁 Project Structure

```
quant_backtest_hub/
├── strategies/               # Upload your own strategy files here
│   └── your_name_strategy.py
├── engine/                   # Backtest engine and helper functions
│   └── backtest.py
├── run_all_strategies.py     # Main script to select a strategy and run backtests
├── strategies_results.xlsx   # Backtest results will be saved here
├── requirements.txt          # Required Python packages
└── README.md
```

---

## ✅ How to Add Your Strategy

1️⃣ Create a new Python file in the `strategies/` folder.  
Example file names:
```
strategies/alice_ema_crossover.py
strategies/bob_rsi_strategy.py
```

2️⃣ In your strategy file, implement a function, for example:
```python
def ema_crossover(df, fast_span=10, slow_span=20):
    df = df.copy()
    df['ema_fast'] = df['Close'].ewm(span=fast_span, adjust=False).mean()
    df['ema_slow'] = df['Close'].ewm(span=slow_span, adjust=False).mean()
    df['signal'] = 0
    df.loc[df['ema_fast'] > df['ema_slow'], 'signal'] = 1
    df.loc[df['ema_fast'] < df['ema_slow'], 'signal'] = -1
    return df[['Close', 'ema_fast', 'ema_slow', 'signal']]
```

---

## 🔎 Strategy Requirements

- Your strategy function **must**:
  - Accept a pandas DataFrame as input, which includes at least the `Close` column.
  - Return a pandas DataFrame containing:
    - `Close`: closing prices
    - `signal`: your trading signals (1=buy, -1=sell, 0=hold/do nothing)
    - Optionally other columns like `ema_fast`, `ema_slow` if relevant.
- Do not execute backtests or data downloads directly in the strategy file. Only define your strategy function.

Example function signature:
```python
def your_strategy(df: pd.DataFrame) -> pd.DataFrame:
    ...
    return df_with_signals
```

---

## 🚀 How to Run Backtests

1️⃣ Install the required packages:
```bash
pip install -r requirements.txt
```

2️⃣ Run the main script with the strategy you want to backtest (replace `<strategy_file_name>` with your file name **without** the `.py` extension):
```bash
python run_all_strategies.py <strategy_file_name>
```

For example:
```bash
python run_all_strategies.py alice_ema_crossover
```

This will run your strategy on all tickers defined in the script and append results to the shared Excel file.

---

## 📂 Backtest Results

- After running, results will be saved/appended to `strategies_results.xlsx`.
- Each ticker will have:
  - `<ticker>_summary`: key performance metrics.
  - `<ticker>_equity`: equity curve time series.
- Each record will include a `strategy_name` column for clear identification of the model used.
- Running the same strategy multiple times will append new results instead of overwriting existing data.

---

## ✅ Strategy Contribution Guidelines

- Place your strategy file in the `strategies/` directory.
- Name your file with your name or identifier + strategy name (e.g., `bob_rsi_strategy.py`).
- Make sure your strategy function follows the required input/output format.
- When submitting code or PRs, include a brief description of your strategy logic, indicators used, and parameters.

---

## ❗ Need Help?

Contact the project maintainer or ask in the team chat for assistance.

Happy coding and good luck with your strategies! 🚀