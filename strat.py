import yfinance as yf
# from sqlalchemy import create_engine
import pandas as pd
import ta
import numpy as np
import matplotlib.pyplot as plt

# symbols = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
# symbols = symbols.Symbol.to_list()

# engine = create_engine('sqlite:///stocks.db')

# for symbol in symbols[:1]:
#     df = yf.download(symbol, start='2016-01-01', end='2022-04-07')
#     df.to_sql(symbol, engine)


def apply_indicators(df):
    df['SMA_200'] = df.Close.rolling(200).mean()
    df['SMA_20'] = df.Close.rolling(20).mean()
    df['stddev'] = df.Close.rolling(20).std()
    df['Upper'] = df.SMA_20 + 2.5 * df.stddev
    df['Lower'] = df.SMA_20 - 2.5 * df.stddev
    df['rsi2'] = ta.momentum.rsi(df.Close, 2)
    df.dropna(inplace=True)


def strat(df):
    for i in range(300):
        if df.iloc[i, :].Close > df.iloc[i, :].SMA_200:
            print(df.iloc[i, :])

    # trades = pd.DataFrame(['Buydate', 'Buyprice', 'Selldate', 'Sellprice'])
    # print(df.)


def conditions(df):
    df['Buy'] = np.where((df.Close > df.SMA_200) &
                         (df.Close < df.Lower) &
                         (0.97 * df.Close >= df.Low.shift(-1)), 1, 0)
    df['Buyprice'] = 0.97 * df.Close
    df['Sell'] = np.where((df.rsi2 > 50), 1, 0)
    df['Sellprice'] = df.Open.shift(-1)


def matched_trades(df):
    buy_sells = df[(df.Buy == 1) | (df.Sell == 1)]
    return buy_sells[(buy_sells.Buy.diff() == 1) | (buy_sells.Sell.diff() == 1)]


def plot_chart(df, indicators):
    plt.plot(df['Close'])
    for i in indicators:
        plt.plot(df[i])
    plt.show()


def run():
    df = yf.download('TSLA', start='2016-01-01', end='2022-04-07')
    df.Close = df['Adj Close']
    apply_indicators(df)
    strat(df)
    # plot_chart(df, ['SMA_20', 'Upper', 'Lower'])
    # conditions(df)
    # trades = matched_trades(df)
    # profit_pct = (trades.Sellprice.shift(-1) - trades.Buyprice) / trades.Buyprice
    # profit_pct = profit_pct[::2]

    # print(profit_pct)

    # df.tail(250)[['Close', 'SMA_20', 'Upper', 'Lower']].plot()


if __name__ == '__main__':
    run()
