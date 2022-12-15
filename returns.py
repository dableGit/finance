import pandas_datareader.data as reader
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

end = dt.datetime.now()
start = dt.datetime(end.year-10, end.month, end.day)

Ticker = 'SPY'

prices = reader.get_data_yahoo(Ticker, start, end)['Adj Close']
returns = prices.pct_change().resample('Y').agg(lambda x: (x+1).prod()-1)
ret_df = returns.reset_index()

plt.bar(ret_df.Date.dt.year, ret_df['Adj Close'],
        color=(ret_df['Adj Close'] > 0).map({True: 'green', False: 'red'}),
        edgecolor='black')
plt.title(f'Yearly returns of {Ticker}')
plt.axhline(0, color='grey')
plt.xticks(np.arange(min(ret_df.Date.dt.year), max(ret_df.Date.dt.year+1), 1))
