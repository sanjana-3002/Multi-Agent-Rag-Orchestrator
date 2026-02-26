import yfinance as yf

print("Testing yfinance...")
stock = yf.Ticker('AAPL')
price = stock.info.get('currentPrice', 'No data')
print(f"Apple current price: ${price}")
