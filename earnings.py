import yahoo_fin.stock_info as si
import pandas as pd


ticker = "AAPL"
earnings = si.get_earnings(ticker)
frame = pd.DataFrame.from_dict(earnings)
print(frame)

ed = si.get_next_earnings_date(ticker)
print(f'Next Earnings: {ed}')
