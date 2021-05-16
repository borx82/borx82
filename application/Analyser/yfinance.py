import yfinance as yf

def yfinance_data(stock_name , num_days):
  diff_list = []
  diff_avg = 0
  stock = yf.Ticker(stock_name)
  stock_df = stock.history(period="max").tail(num_days)
  for i in range(len(stock_df)):
    diff = stock_df["Close"][i] - stock_df["Open"][i]
    diff_avg += diff
    diff_list.append(diff)
  if len(diff_list) == 0:
    diff_avg = None
  else:
    diff_avg = diff_avg / len(diff_list)
  return diff_avg