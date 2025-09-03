import pandas as pd
import yfinance as yf

def backtest_signals(tickers, lookahead=20):
    records = []
    for t in tickers:
        try:
            df = yf.download(t, period="1y", interval="1d", progress=False)
            if len(df) < 60:
                continue
            for i in range(30, len(df)-lookahead):
                close = df['Close'].iloc[i]
                ma = df['Close'].rolling(20).mean().iloc[i]
                bias = "Long" if close > ma else "Short"
                atr = (df['High'] - df['Low']).rolling(14).mean().iloc[i]
                entry = close
                stop = entry - atr if bias=="Long" else entry + atr
                target = entry + 1.5*atr if bias=="Long" else entry - 1.5*atr
                future = df['Close'].iloc[i+1:i+lookahead]
                hit_target = (future >= target).any() if bias=="Long" else (future <= target).any()
                hit_stop = (future <= stop).any() if bias=="Long" else (future >= stop).any()
                result = "Win" if hit_target and not hit_stop else ("Loss" if hit_stop else "Open")
                records.append({"Ticker": t, "Date": df.index[i], "Bias": bias,
                                "Entry": entry, "Stop": stop, "Target": target,
                                "Result": result})
        except Exception:
            continue
    return pd.DataFrame(records)
