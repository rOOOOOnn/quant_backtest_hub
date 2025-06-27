from engine.backtest import backtest, save_results_to_excel
from strategies import ema_crossover

import yfinance as yf

# Load market data
df_raw = yf.download("AAPL", start="2022-01-01", end="2024-01-01")

# Run EMA strategy
ema_df = ema_crossover(df_raw)
ema_metrics = backtest(ema_df)
# Convert to DataFrame for Excel output
ema_results_df = pd.DataFrame([ema_metrics])

# Combine and save
results = {
    'ema_crossover': ema_results_df
}
save_results_to_excel(results)
print("All strategy results written to strategies_results.xlsx")
