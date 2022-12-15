# import yfinance as yf
import pandas as pd
from pandas.tseries.frequencies import to_offset


def get_dow_tickers():
    tickers = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')[1]
    return tickers.Symbol.to_list()


def get_Ndq100_tickers():
    tickers = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')[3]
    return tickers.Ticker.to_list()


def get_sp500_tickers(replace=True):
    tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    tickers = tickers.Symbol.to_list()
    if replace:
        return [ticker.replace('.', '-') for ticker in tickers]
    return tickers


def daily2weekly(df):
    logic = {'Open': 'first',
             'High': 'max',
             'Low': 'min',
             'Close': 'last',
             'Volume': 'sum'}
    dfw = df.resample('W').apply(logic)
    dfw.index -= to_offset('6D')
    return dfw

# print(get_Ndq100_tickers())
