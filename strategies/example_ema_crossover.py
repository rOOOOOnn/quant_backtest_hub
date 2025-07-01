import pandas as pd
import numpy as np
import yfinance as yf
from engine import backtest

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

    # 更清晰的信号生成
    df['position'] = np.where(df['ema_fast'] > df['ema_slow'], 1, -1)
    df['signal'] = df['position'].diff().fillna(0)
    # 或者更明确的交叉信号
    df['signal'] = 0
    df['signal'] = np.where((df['ema_fast'] > df['ema_slow']) & 
                        (df['ema_fast'].shift(1) <= df['ema_slow'].shift(1)), 1, df['signal'])
    df['signal'] = np.where((df['ema_fast'] < df['ema_slow']) & 
                        (df['ema_fast'].shift(1) >= df['ema_slow'].shift(1)), -1, df['signal'])

    # build final result DataFrame
    ema_crossover_dataframe = df[['Close', 'ema_fast', 'ema_slow', 'signal']]
    return ema_crossover_dataframe

# put your testing code under main guard
if __name__ == "__main__":
    
    df_raw = yf.download("AAPL", start="2022-01-01", end="2024-01-01")
    ema_crossover_dataframe = ema_crossover(df_raw)
    # If columns are MultiIndex (like when yfinance adds Ticker), flatten them
    if isinstance(ema_crossover_dataframe.columns, pd.MultiIndex):
        ema_crossover_dataframe.columns = ['_'.join([str(c) for c in col if c]) for col in ema_crossover_dataframe.columns]

    print(ema_crossover_dataframe)
    # results = backtest(ema_crossover_dataframe)
    # print(results)