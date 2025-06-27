import pandas as pd
import numpy as np

def ema_crossover(df, fast_span=10, slow_span=20):
    """
    EMA Crossover Strategy Signal Generator

    Parameters:
    - df: pandas DataFrame containing at least a 'Close' column, indexed by timestamp
    - fast_span: period for the fast EMA (default=10)
    - slow_span: period for the slow EMA (default=20)

    Returns:
    - ema_crossover_dataframe: DataFrame with columns ['Close', 'ema_fast', 'ema_slow', 'signal']
      - 'ema_fast': fast EMA
      - 'ema_slow': slow EMA
      - 'signal': trading signal:
          * +1 = buy (fast ema crosses above slow ema)
          * -1 = sell (fast ema crosses below slow ema)
          * 0 = hold / no action
    """
    df = df.copy()  # avoid modifying original DataFrame

    # calculate fast and slow EMA
    df['ema_fast'] = df['Close'].ewm(span=fast_span, adjust=False).mean()
    df['ema_slow'] = df['Close'].ewm(span=slow_span, adjust=False).mean()

    # generate raw signal: 1 when fast > slow, otherwise 0
    df['signal'] = np.where(df['ema_fast'] > df['ema_slow'], 1, 0)

    # convert to trading events: +1 = crossover up, -1 = crossover down
    df['signal'] = df['signal'].diff().fillna(0).astype(int)

    # build final result DataFrame
    ema_crossover_dataframe = df[['Close', 'ema_fast', 'ema_slow', 'signal']]
    return ema_crossover_dataframe


# Usage example (if you want to test it):

import yfinance as yf
from engine.backtest import backtest,save_results_to_excel

df_raw = yf.download("AAPL", start="2022-01-01", end="2024-01-01")
ema_crossover_dataframe = ema_crossover(df_raw, fast_span=10, slow_span=20)

results = backtest(ema_crossover_dataframe)
print(results)