import yfinance as yf
import pandas as pd
import df_base


def get_yf_infos():
    tickers = df_base.get_sp500_tickers()
    infos = []
    for ticker in tickers:
        infos.append(yf.Ticker(ticker).info)
    df = pd.DataFrame(infos)
    df = df.set_index('symbol')
    df.to_csv('fundamentals.csv')
    return df


def get_csv_infos():
    df = pd.read_csv('fundamentals.csv')
    df = df.set_index('symbol')
    return df


df = get_csv_infos()

# print(df.columns.to_list())

fundamentals = ['forwardPE', 'pegRatio', 'beta', 'dividendYield', 'industry', 'shortName']
df = df[df.columns[df.columns.isin(fundamentals)]]

df = df.sort_values(by='forwardPE')

print(df[(df['forwardPE'] < 25) & (df['forwardPE'] > 6) &
         (df['pegRatio'] < 1) & (df['pegRatio'] > 0.3) &
         (df['industry'].str.contains('Insura') == False) &
         (df['industry'].str.contains('Bank') == False)])
