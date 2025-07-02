import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.stats import norm


def plot_long_call(S0, K, premium, T, sigma, days_to_exp):
    S_range = np.linspace(S0 * 0.5, S0 * 1.5, 100)
    payoff = np.maximum(S_range - K, 0) - premium
    breakeven = K + premium

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(S_range, payoff, label='Long Call P&L', color='green')
    ax.axhline(0, color='black', linestyle='--')
    ax.axvline(K, color='red', linestyle='--', label='Strike Price')
    ax.axvline(S0, color='blue', linestyle=':', label=f'Current Price (${S0:.2f})')
    ax.axvline(breakeven, color='purple', linestyle='-.', label=f'Breakeven (${breakeven:.2f})')

    tick_values = np.linspace(S0 * 0.5, S0 * 1.5, 11)
    tick_labels = [f"${x:.2f}\n({((x - S0) / S0 * 100):+.0f}%)" for x in tick_values]
    ax.set_xticks(tick_values)
    ax.set_xticklabels(tick_labels)

    ax.set_title(f"Payoff Diagram – Long Call Option\n(Time to Expiration: {int(days_to_exp)} days)")
    ax.set_xlabel("Stock Price at Expiration ($)")
    ax.set_ylabel("Profit / Loss ($)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()

def plot_long_put(S0, K, premium, T, sigma, days_to_exp):
    S_range = np.linspace(S0 * 0.5, S0 * 1.5, 100)
    payoff = np.maximum(K - S_range, 0) - premium
    breakeven = K - premium

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(S_range, payoff, label='Long Put P&L', color='darkred')
    ax.axhline(0, color='black', linestyle='--')
    ax.axvline(K, color='red', linestyle='--', label=f'Strike Price (${K:.2f})')
    ax.axvline(S0, color='blue', linestyle=':', label=f'Current Price (${S0:.2f})')
    ax.axvline(breakeven, color='purple', linestyle='-.', label=f'Breakeven (${breakeven:.2f})')

    tick_values = np.linspace(S0 * 0.5, S0 * 1.5, 11)
    tick_labels = [f"${x:.2f}\n({((x - S0) / S0 * 100):+.0f}%)" for x in tick_values]
    ax.set_xticks(tick_values)
    ax.set_xticklabels(tick_labels)

    ax.set_title(f"Payoff Diagram – Long Put Option\n(Time to Expiration: {int(days_to_exp)} days)")
    ax.set_xlabel("Stock Price at Expiration ($)")
    ax.set_ylabel("Profit / Loss ($)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()

def print_greeks_and_prob(S0, K, premium, T, sigma, option_type='call'):
    d1 = (np.log(S0 / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        delta = norm.cdf(d1)
        prob_itm = norm.cdf(d2)
    else:
        delta = -norm.cdf(-d1)
        prob_itm = norm.cdf(-d2)

    gamma = norm.pdf(d1) / (S0 * sigma * np.sqrt(T))
    theta = -(S0 * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
    vega = S0 * norm.pdf(d1) * np.sqrt(T) / 100
    rho = (K * T * np.exp(-0.05 * T) * norm.cdf(d2)) / 100 if option_type == 'call' else -(K * T * np.exp(-0.05 * T) * norm.cdf(-d2)) / 100

    print("\n📐 Option Greeks:")
    print(f"Δ Delta: {delta:.4f}")
    print(f"Γ Gamma: {gamma:.4f}")
    print(f"Θ Theta: {theta:.4f}")
    print(f"ν Vega: {vega:.4f}")
    print(f"ρ Rho: {rho:.4f}")
    print(f"📊 Estimated Probability of Expiring ITM: {prob_itm:.2%}\n")


def show_analysis_menu():
    print("\n🧰 Available Actions:")
    print("1. Show Greeks & Probability ITM")
    print("2. Calculate Black-Scholes Price")
    print("3. Plot Payoff Diagram")
    print("4. Try Another Option")
    print("5. Exit")
    return int(input("Choose an action [1–5]: "))
