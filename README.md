# 🧮 Options Simulator

A Python-based command-line tool that allows you to analyze equity options in real time. It fetches option chains from Yahoo Finance, calculates theoretical prices using the Black-Scholes model, displays key Greeks and estimated probabilities, and visualizes payoff diagrams for long call and put strategies.

## 🚀 Features

- ✅ Live options data using `yfinance`
- 📈 Black-Scholes pricing model
- 🔢 Calculates Delta, Gamma, Theta, Vega, Rho
- 🎯 Estimated probability of expiring in-the-money (ITM)
- 📊 Interactive payoff diagram with breakeven, strike, and current price
- 🔄 Easily analyze multiple option contracts in a single session

## 🛠️ Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
