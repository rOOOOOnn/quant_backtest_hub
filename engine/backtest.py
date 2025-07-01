# engine/backtest.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from openpyxl import load_workbook

def backtest(df, initial_capital=100000, fee=0.0, plot=False):
    """
    Generic backtest engine for single asset with buy/sell signals.
    
    Parameters:
    - df: DataFrame with 'Close' and 'signal' columns (+1 buy, -1 sell, 0 hold)
    - initial_capital: starting cash amount
    - fee: fractional cost per trade (e.g. 0.001 = 0.1%)
    - plot: bool, whether to plot equity curve and drawdown
    
    Returns:
    - results: dict including metrics and optionally plots displayed/saved
    """
    capital = initial_capital
    position = 0
    equity = []
    trades = []

    for price, signal in zip(df['Close'], df['signal']):
        # price = float(price)
        if signal == 1 and position == 0:
            position = capital / price
            capital = 0
            entry_price = price * (1 + fee)
            trades.append(('buy', entry_price))
        elif signal == -1 and position > 0:
            exit_price = price * (1 - fee)
            capital = position * exit_price
            position = 0
            trades.append(('sell', exit_price))

        equity.append(capital + position * price)

    equity = pd.Series(equity, index=df.index)
    returns = equity.pct_change().dropna()

    final_value = equity.iloc[-1]
    total_return = final_value / initial_capital - 1
    cum_max = equity.cummax()
    drawdown = (equity - cum_max) / cum_max  # drawdown calculation :contentReference[oaicite:1]{index=1}
    max_dd = drawdown.min()
    sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() else np.nan

    pnl = []
    for i in range(1, len(trades), 2):
        buy = trades[i-1][1]
        sell = trades[i][1]
        pnl.append(sell - buy)

    wins = [p for p in pnl if p > 0]
    losses = [p for p in pnl if p < 0]
    trade_count = len(pnl)
    win_rate = len(wins) / trade_count if trade_count else np.nan
    avg_win = np.mean(wins) if wins else 0
    avg_loss = np.mean(losses) if losses else 0
    profit_factor = -sum(wins) / sum(losses) if losses else np.nan

    results = {
        'equity_curve': equity,
        'final_value': final_value,
        'total_return': total_return,
        'max_drawdown': max_dd,
        'sharpe': sharpe,
        'trade_count': trade_count,
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'profit_factor': profit_factor,
    }

    if plot:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        ax1.plot(equity, label='Equity Curve')
        ax1.set_ylabel('Portfolio Value')
        ax1.legend()
        ax1.grid(True)

        ax2.fill_between(df.index, drawdown, 0, color='red')
        ax2.set_ylabel('Drawdown')
        ax2.set_xlabel('Date')
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

    return results


def save_results_to_excel(results_dict, filename='strategies_results.xlsx'):
    """
    Save strategy results to an Excel file, with each ticker saved to a separate sheet,
    avoiding duplicate saves of the same ticker + strategy combination.

    Parameters:
    - results_dict: dict, format {ticker: DataFrame}
    - filename: str, Excel file name
    """
    
    # Check if the file exists
    if os.path.exists(filename):
        try:
            # Read existing data from all sheets
            existing_sheets = pd.read_excel(filename, sheet_name=None)
        except:
            existing_sheets = {}
    else:
        existing_sheets = {}

    # Prepare data to write
    sheets_to_write = {}
    total_saved = 0
    total_skipped = 0

    for ticker, df in results_dict.items():
        if df.empty:
            continue

        strategy_name = df.iloc[0]['strategy_name'] if 'strategy_name' in df.columns else 'unknown'

        # Check if the sheet for this ticker already exists
        if ticker in existing_sheets:
            existing_df = existing_sheets[ticker]

            # Check if the same strategy already exists
            if 'strategy_name' in existing_df.columns:
                existing_strategies = existing_df['strategy_name'].tolist()
                if strategy_name in existing_strategies:
                    print(f"Skipping {ticker} + {strategy_name}: already exists")
                    total_skipped += 1
                    # Keep existing data unchanged
                    sheets_to_write[ticker] = existing_df
                    continue

            # Merge existing and new data
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            sheets_to_write[ticker] = combined_df
            print(f"Saving {ticker} + {strategy_name}")
            total_saved += 1
        else:
            # New ticker: save directly
            sheets_to_write[ticker] = df
            print(f"Saving {ticker} + {strategy_name} (new ticker)")
            total_saved += 1

    # Keep other sheets that were not updated
    for sheet_name, sheet_df in existing_sheets.items():
        if sheet_name not in sheets_to_write:
            sheets_to_write[sheet_name] = sheet_df

    # Write to the Excel file
    if sheets_to_write:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            for sheet_name, df in sheets_to_write.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"✅ Saved {total_saved} new records to {filename}")
    else:
        print("ℹ️ No data to save")

    if total_skipped > 0:
        print(f"⏭️ Skipped {total_skipped} duplicate records")