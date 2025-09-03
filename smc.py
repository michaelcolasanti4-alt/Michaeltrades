import pandas as pd
import yfinance as yf
import numpy as np

def find_setups(tickers):
    records = []
    for t in tickers:
        try:
            df = yf.download(t, period="6mo", interval="1d", progress=False)
            if len(df) < 30:
                continue
            # Very simplified example confluences
            last = df.iloc[-1]
            bias = "Long" if last['Close'] > df['Close'].rolling(20).mean().iloc[-1] else "Short"
            atr = (df['High'] - df['Low']).rolling(14).mean().iloc[-1]
            entry = last['Close']
            stop = entry - atr if bias == "Long" else entry + atr
            target1 = entry + 1.5*atr if bias == "Long" else entry - 1.5*atr
            target2 = entry + 2.5*atr if bias == "Long" else entry - 2.5*atr
            records.append({
                "Ticker": t,
                "Bias": bias,
                "Entry": round(entry,2),
                "Stop": round(stop,2),
                "Target1": round(target1,2),
                "Target2": round(target2,2),
                "Confluences": 3
            })
        except Exception:
            continue
    df_out = pd.DataFrame(records)
    return df_out.head(5)
