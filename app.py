import streamlit as st
import pandas as pd
import yfinance as yf
from smc import find_setups
from options_utils import recommend_options, account_sizing, call_put_bias
from backtest import backtest_signals

st.set_page_config(page_title="SMC/ICT Options App", layout="wide")

st.title("📈 Smart Money Concepts / ICT Options App")

tabs = st.tabs(["Daily Picks", "Account Sizing", "Backtest / Win %"])

# Tab 1: Daily Picks
with tabs[0]:
    st.header("Top 5 Daily Picks")
    default_tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "TSLA",
                       "META", "GOOGL", "NFLX", "JPM", "AMD"]
    tickers = st.text_area("Enter tickers (comma separated):",
                           ",".join(default_tickers)).split(",")
    tickers = [t.strip().upper() for t in tickers if t.strip()]
    data = find_setups(tickers)
    if not data.empty:
        st.dataframe(data)
        for _, row in data.iterrows():
            st.subheader(f"{row['Ticker']} — {row['Bias']}")
            st.write(f"Entry: {row['Entry']} | Stop: {row['Stop']} | Target1: {row['Target1']} | Target2: {row['Target2']}")
            opt = recommend_options(row['Ticker'], row['Bias'])
            if opt:
                st.json(opt)
            # New Call/Put Bias display
            cp_bias = call_put_bias(row['Ticker'])
            st.write(f"Options Market Bias: **{cp_bias}**")

# Tab 2: Account Sizing
with tabs[1]:
    st.header("Account Sizing Tool")
    account_size = st.number_input("Account size ($):", value=10000)
    risk_pct = st.slider("Risk % per trade:", 0.5, 5.0, 1.0)
    stop_distance = st.number_input("Stop distance ($):", value=2.0)
    contract_price = st.number_input("Option contract price ($):", value=200.0)
    contracts = account_sizing(account_size, risk_pct, stop_distance, contract_price)
    st.write(f"Recommended contracts: **{contracts}**")

# Tab 3: Backtest
with tabs[2]:
    st.header("Backtest Win/Loss %")
    lookahead = st.slider("Lookahead days:", 5, 30, 20)
    tickers_bt = st.text_area("Backtest tickers (comma separated):",
                              ",".join(default_tickers)).split(",")
    tickers_bt = [t.strip().upper() for t in tickers_bt if t.strip()]
    results = backtest_signals(tickers_bt, lookahead=lookahead)
    if not results.empty:
        st.dataframe(results)
        win_rate = (results['Result'] == 'Win').mean() * 100
        st.write(f"Win %: **{win_rate:.2f}%**")
