import yfinance as yf
import pandas as pd
import ta

import df_base


def apply_indicators(df):
    macd = ta.trend.MACD(df.Close)
    df['MACD'] = macd.macd_diff()
    df['Signal'] = macd.macd_signal()

    # df.dropna(inplace=True)


macd_data = []

tickers = df_base.get_sp500_tickers()
for ticker in tickers:
    df = yf.download(ticker, start='2021-06-01')
    df.Close = df['Adj Close']
    dfw = df_base.daily2weekly(df)
    apply_indicators(dfw)
    macd_data.append([ticker, dfw.MACD[-1], dfw.Signal[-1]])
    print(f'Weekly MACD: {dfw.MACD[-1]}')
    print(f'Weekly Sign: {dfw.Signal[-1]}')

df = pd.DataFrame(macd_data, index=None)
df.columns = ['ticker', 'MACD', 'Signal']
df.to_csv('MACD_SP500.csv')
