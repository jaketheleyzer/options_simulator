from black_scholes import black_scholes_price
from plot_strategy import plot_long_call, plot_long_put, print_greeks_and_prob, show_analysis_menu
from datetime import datetime
import yfinance as yf
import requests


def format_expiration_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    day = dt.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return dt.strftime(f"%B {day}{suffix}, %Y")


def get_expiration_options(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    raw_dates = ticker.options
    formatted = [format_expiration_date(d) for d in raw_dates]
    return list(zip(range(1, len(formatted) + 1), formatted, raw_dates))


def get_maturity_code(T):
    if T <= 1/12:
        return "DGS1MO"
    elif T <= 0.25:
        return "DGS3MO"
    elif T <= 0.5:
        return "DGS6MO"
    elif T <= 1:
        return "DGS1"
    else:
        return "DGS2"


def get_fred_yield(api_key, maturity_code):
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': maturity_code,
        'api_key': api_key,
        'file_type': 'json',
        'sort_order': 'desc',
        'limit': 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    try:
        return float(data['observations'][0]['value']) / 100
    except:
        return None


def main():
    print("\n🧮 Options Pricing Tool")
    fred_api_key = "18e03dd1e1ac3dbae3ba9e6f27a7b1d7"

    ticker_input = input("Enter stock ticker (e.g., AAPL, BAC): ").upper()
    try:
        ticker = yf.Ticker(ticker_input)
        options = get_expiration_options(ticker_input)
    except Exception as e:
        print(f"Error fetching data for {ticker_input}: {e}")
        return

    print(f"\nAvailable expiration dates for {ticker_input}:")
    for idx, label, raw in options:
        print(f"[{idx}] {label}")

    try:
        choice = int(input("Choose an expiration date [1–{}]: ".format(len(options))))
        _, formatted_date, selected_date = options[choice - 1]
        print(f"\n✅ You selected: {formatted_date} ({selected_date})")
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    today = datetime.today()
    expiration_date = datetime.strptime(selected_date, "%Y-%m-%d")
    time_to_exp = expiration_date - today
    days_to_exp = time_to_exp.days
    T = days_to_exp / 365
    print(f"🕒 Time to expiration: {days_to_exp} days ({T:.3f} years)")

    maturity_code = get_maturity_code(T)
    r = get_fred_yield(fred_api_key, maturity_code)
    print(f"💵 Risk-free rate (from {maturity_code}): {r:.4f}")

    try:
        option_chain = ticker.option_chain(selected_date)
        calls = option_chain.calls
        puts = option_chain.puts
    except Exception as e:
        print(f"❌ Could not retrieve options: {e}")
        return

    option_type = input("Choose option type [call/put]: ").strip().lower()
    if option_type == 'call':
        selected_df = calls
        title = "📈 Available call options"
    elif option_type == 'put':
        selected_df = puts
        title = "📉 Available put options"
    else:
        print("Invalid option type. Please choose 'call' or 'put'.")
        return

    display_options = selected_df[['strike', 'lastPrice', 'impliedVolatility']].sort_values(by='strike', ascending=False).reset_index(drop=True)
    S = float(ticker.history(period="1d")['Close'].iloc[-1])
    divider_shown = False

    print(f"\n{title} for {selected_date}: (Current price: ${S:.2f})")
    for idx, row in display_options.iterrows():
        strike = row['strike']
        price = row['lastPrice']
        iv = row['impliedVolatility']

        if not divider_shown and strike <= S:
            print("\n───────────────────────────────────────────────────────⬅️   " + ticker_input + " current price:  $" + str(round(S, 2)) + "\n")
            divider_shown = True

        print(f"[{idx + 1}] Strike ${strike:.2f} | Last Market Price ${price:.2f} | IV: {iv:.2%}")

    try:
        pick = int(input(f"Choose a {option_type} option [#]: "))
        selected_row = display_options.iloc[pick - 1]
        market_price = float(selected_row['lastPrice'])
        K = float(selected_row['strike'])
        sigma = float(selected_row['impliedVolatility'])
    except (ValueError, IndexError):
        print("Invalid option selection.")
        return

    while True:
        action = show_analysis_menu()

        if action == 1:
            print_greeks_and_prob(S, K, market_price, T, sigma, option_type)

        elif action == 2:
            calc_price = black_scholes_price(S, K, T, r, sigma, option_type=option_type)
            print(f"\n💰 Calculated Black-Scholes {option_type.title()} Price: ${calc_price:.2f}")
            diff = market_price - calc_price
            percent_diff = abs(diff) / calc_price * 100 if calc_price != 0 else 0

            if diff > 0:
                print(f"📈 This option is **overvalued** by the market by ${diff:.2f} ({percent_diff:.2f}%).")
            elif diff < 0:
                print(f"📉 This option is **undervalued** by the market by ${-diff:.2f} ({percent_diff:.2f}%).")
            else:
                print("⚖️ This option is **fairly valued** according to the Black-Scholes model.")

            print(f"📊 Underlying: ${S:.2f}, Strike: ${K:.2f}, IV: {sigma:.2%}, r: {r:.2%}, T: {T:.3f} years")

        elif action == 3:
            if option_type == 'call':
                plot_long_call(S, K, market_price, T, sigma, days_to_exp)
            else:
                plot_long_put(S, K, market_price, T, sigma, days_to_exp)

        elif action == 4:
            print("🔁 Returning to choose another option.")
            return main()  # Restart from top

        elif action == 5:
            print("👋 Exiting Options Pricing Tool. Goodbye!")
            exit()


if __name__ == "__main__":
    main()
