import yfinance as yf
import pandas as pd
# import datetime as dt
from calendar import month_abbr
import df_base

tickers = df_base.get__dow_tickers()

divs = []
for ticker in tickers:
    info = yf.Ticker(ticker)
    info.history(period='1y')
    divs.append(info.dividends)

df = pd.DataFrame(divs, index=tickers)
df.columns = df.columns.month
df = df.groupby(df.columns, axis=1).sum()
# df.columns = [dt.date(1900, m, 1).strftime('%b') for m in df.columns]
df.columns = [month_abbr[m] for m in df.columns]
df.sort_values(['Jan', 'Feb', 'Mar', 'Apr'], ascending=False, inplace=True)
print(df)
