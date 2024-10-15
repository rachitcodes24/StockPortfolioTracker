import requests

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://www.alphavantage.co/query'

# Function to fetch stock price from Alpha Vantage
def fetch_stock_price(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # Check for valid response
    if 'Time Series (1min)' in data:
        latest_timestamp = list(data['Time Series (1min)'].keys())[0]
        latest_data = data['Time Series (1min)'][latest_timestamp]
        return float(latest_data['4. close'])  # Return the latest close price
    else:
        print(f"Error fetching data for {symbol}: {data.get('Error Message', 'Unknown error')}")
        return None

# Class to manage stock portfolio
class StockPortfolio:
    def __init__(self):
        self.portfolio = {}  # Dictionary to store stocks in format {symbol: (quantity, purchase_price)}

    def add_stock(self, symbol, quantity, purchase_price):
        if symbol in self.portfolio:
            print(f"{symbol} is already in the portfolio. Consider updating its quantity.")
        else:
            self.portfolio[symbol] = (quantity, purchase_price)
            print(f"Added {symbol} with {quantity} shares at purchase price ${purchase_price}.")

    def remove_stock(self, symbol):
        if symbol in self.portfolio:
            del self.portfolio[symbol]
            print(f"Removed {symbol} from portfolio.")
        else:
            print(f"{symbol} is not in the portfolio.")

    def view_portfolio(self):
        print("\nYour Portfolio:")
        for symbol, (quantity, purchase_price) in self.portfolio.items():
            print(f"Stock: {symbol} | Quantity: {quantity} | Purchase Price: ${purchase_price}")

    def track_performance(self):
        print("\nTracking Portfolio Performance:")
        total_value = 0
        total_invested = 0

        for symbol, (quantity, purchase_price) in self.portfolio.items():
            current_price = fetch_stock_price(symbol)
            if current_price is not None:
                current_value = current_price * quantity
                invested_value = purchase_price * quantity
                profit_loss = current_value - invested_value
                profit_loss_percent = (profit_loss / invested_value) * 100

                total_value += current_value
                total_invested += invested_value

                print(f"{symbol}: Current Price: ${current_price:.2f} | Total Value: ${current_value:.2f} "
                      f"| Profit/Loss: ${profit_loss:.2f} ({profit_loss_percent:.2f}%)")

        print(f"\nTotal Portfolio Value: ${total_value:.2f}")
        print(f"Total Invested: ${total_invested:.2f}")
        print(f"Overall Profit/Loss: ${total_value - total_invested:.2f}")

def main():
    portfolio = StockPortfolio()

    while True:
        print("\nMenu:")
        print("1. Add Stock to Portfolio")
        print("2. Remove Stock from Portfolio")
        print("3. View Portfolio")
        print("4. Track Performance")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol (e.g., AAPL): ").upper()
            quantity = int(input("Enter quantity of shares: "))
            purchase_price = float(input("Enter purchase price: "))
            portfolio.add_stock(symbol, quantity, purchase_price)
        
        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ").upper()
            portfolio.remove_stock(symbol)

        elif choice == '3':
            portfolio.view_portfolio()

        elif choice == '4':
            portfolio.track_performance()

        elif choice == '5':
            print("Exiting the portfolio tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()

