# 📈 SMC/ICT Options Web App

This app scans tickers for Smart Money Concepts (SMC) / ICT-style setups, suggests entry/stop/targets, 
recommends options contracts, provides account sizing, and shows backtested win/loss %.

## 🚀 Deployment on Render
1. Create a new GitHub repository and upload these files.
2. Go to [Render](https://render.com) → create new **Web Service**.
3. Connect your repo.
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Deploy → you'll get a live URL.

## Features
- Top 5 daily trade setups (SMC/ICT-inspired, ≥3 confluences).
- Options contract suggestions (near ATM, nearest expiry).
- Account sizing tool (risk-based contracts).
- Backtest tab with Win %.

⚠️ Disclaimer: Educational prototype only. Not financial advice.
