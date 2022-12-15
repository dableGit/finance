from binance import Client
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pypfopt import EfficientFrontier, risk_models, expected_returns, objective_functions, plotting
import datetime as dt

client = Client()


def get_symbols():
    info = client.get_exchange_info()
    all_symbols = [x['symbol'] for x in info['symbols']]
    # return [symbol for symbol in all_symbols if symbol.endswith('USDT')]
    return [symbol for symbol in all_symbols if 'EUR' in symbol]


def getdailydata(symbol):
    frame = pd.DataFrame(client.get_historical_klines(symbol,
                                                      '1d',
                                                      '2 years ago UTC'))
    frame = frame[[0, 4]]
    frame.columns = ['Timestamp', symbol]
    frame = frame.set_index('Timestamp')
    frame = frame.astype(float)
    return frame


def getminuteprice(symbol, date):
    start = str(int(date.timestamp()*1000))
    end = date + dt.timedelta(seconds=1)
    end = str(int(end.timestamp()*1000))
    klines = client.get_historical_klines(
        symbol, Client.KLINE_INTERVAL_1MINUTE, start, end)
    frame = pd.DataFrame(klines)
    return frame.iloc[0, 4]


# print(get_symbols())
# date = dt.datetime(2021, 5, 30, 11, 5)
# getminuteprice('ADAEUR', date)

symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'LUNAUSDT', 'DOTUSDT', 'ATOMUSDT', 'LINKUSDT']
prices = []
for symbol in symbols:
    prices.append(getdailydata(symbol))

df = pd.concat(prices, axis=1)
mu = expected_returns.mean_historical_return(df, frequency=365)
print(mu)
S = risk_models.sample_cov(df, frequency=365)  # Volatility
ef = EfficientFrontier(mu, S)

# fig, ax = plt.subplots()
# plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True)
# for i, txt in enumerate(ef.tickers):
#     ax.annotate(txt, ((np.diag(ef.cov_matrix) ** (1/2))[i], ef.expected_returns[i]))

# ef.add_objective(objective_functions.L2_reg, gamma=0.1)
# weights = ef.max_sharpe()
# print(ef.clean_weights())
# ef.portfolio_performance(verbose=True)

# weights = ef.min_volatility()
# print(weights)
