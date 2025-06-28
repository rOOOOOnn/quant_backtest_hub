import os
import sys
import importlib
import yfinance as yf
import pandas as pd
from engine.backtest import backtest, save_results_to_excel

# ─────────────────────────────────────────────────────────────
# CLI usage: python run_all_strategies.py <strategy_module_name>
# Example: python run_all_strategies.py example_ema_crossover
# ─────────────────────────────────────────────────────────────

if len(sys.argv) != 2:
    print("Usage: python run_all_strategies.py <strategy_module_name>")
    sys.exit(1)

strategy_module_name = sys.argv[1]

# Dynamically import the strategy module from strategies folder
try:
    strategy_module = importlib.import_module(f"strategies.{strategy_module_name}")
except ModuleNotFoundError:
    print(f"Error: strategies/{strategy_module_name}.py not found.")
    sys.exit(1)

# Automatically get strategy file path → strategy name
strategy_file = strategy_module.__file__
strategy_name = os.path.splitext(os.path.basename(strategy_file))[0]

print(f"Running strategy: {strategy_name}")

# List of tickers to backtest
tickers = ["AAPL", "MSFT"]

# Download multiple tickers; yfinance returns MultiIndex dataframe
df_raw = yf.download(tickers, start="2022-01-01", end="2024-01-01")

results = {}

for ticker in tickers:
    print(f"Running backtest for {ticker} with strategy {strategy_name}...")

    # Extract data for this ticker from MultiIndex columns
    try:
        df_ticker = df_raw.xs(ticker, level=1, axis=1)
    except KeyError:
        print(f"Warning: No data found for ticker {ticker}, skipping.")
        continue

    if "Close" not in df_ticker.columns:
        print(f"Ticker {ticker} has no 'Close' column, skipping.")
        continue

    # Call strategy function from the imported module
    df_strategy = strategy_module.ema_crossover(df_ticker)

    # Backtest
    strategy_results = backtest(df_strategy, plot=False)

    # Add strategy name dynamically
    strategy_results["strategy_name"] = strategy_name

    # Convert results to DataFrame for saving
    results_df = pd.DataFrame([strategy_results])
    results[ticker] = results_df

# Save all strategy results into one Excel file
save_results_to_excel(results)
print("All strategy results saved to strategies_results.xlsx")