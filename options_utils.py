import yfinance as yf

def recommend_options(ticker, bias):
    try:
        tk = yf.Ticker(ticker)
        exps = tk.options
        if not exps:
            return None
        expiry = exps[min(1, len(exps)-1)]  # pick near-term expiry
        chain = tk.option_chain(expiry)
        calls = chain.calls if bias=="Long" else chain.puts
        atm = calls.iloc[(calls['strike'] - tk.history(period="1d")['Close'].iloc[-1]).abs().argsort()[:1]]
        if atm.empty:
            return None
        row = atm.iloc[0]
        return {
            "expiry": expiry,
            "strike": row['strike'],
            "lastPrice": row['lastPrice'],
            "volume": int(row['volume']),
            "openInterest": int(row['openInterest']),
            "type": "CALL" if bias=="Long" else "PUT"
        }
    except Exception:
        return None

def account_sizing(account_size, risk_pct, stop_distance, contract_price):
    risk_dollars = account_size * (risk_pct/100)
    contracts = int(risk_dollars / stop_distance / (contract_price/100))
    return max(1, contracts)

# New function for Call/Put Bias
def call_put_bias(ticker):
    try:
        tk = yf.Ticker(ticker)
        exps = tk.options
        if not exps:
            return "N/A"
        expiry = exps[min(1, len(exps)-1)]
        chain = tk.option_chain(expiry)
        calls_oi = chain.calls['openInterest'].sum()
        puts_oi = chain.puts['openInterest'].sum()
        if calls_oi > puts_oi*1.05:
            return "Call-heavy"
        elif puts_oi > calls_oi*1.05:
            return "Put-heavy"
        else:
            return "Neutral"
    except Exception:
        return "Error"
