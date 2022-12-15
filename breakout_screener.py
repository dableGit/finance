import yfinance as yf
import ta

import df_base

# Load Data & Transform to Weekly Candles
tickers = df_base.get_sp500_tickers()
breakout_tickers = []
for ticker in tickers:
    dfd = yf.download(ticker, period='1y', interval='1d')
    df = df_base.daily2weekly(dfd)
    # df.drop(df.tail(1).index, inplace=True)
    sma = 20
    df['sma'] = ta.trend.sma_indicator(df.Close, sma)
    df['macd'] = ta.trend.macd_diff(df.Close)
    last_close = df.Close[-1]
    last_volume = df.Volume[-1]
    last_sma = df.sma[-1]
    last_macd = df.macd[-1]
    df.drop(df.tail(1).index, inplace=True)

    # Conditions:
    # Consolidation
    min_period = 6
    channel_width = 0.2
    channel = df.tail(min_period)
    max_v = max(channel.Open.max(), channel.Close.max())
    min_v = min(channel.Open.min(), channel.Close.min())
    if max_v/min_v > channel_width+1:
        # print(f'Channel width too big: {round((max/min-1)*100,2)}%')
        continue

    # Price Breakout
    breakout_min = 0.05
    breakout_max = 0.2
    breakout = (last_close / channel.Close[-1]) - 1
    if (breakout < breakout_min) or (breakout > breakout_max):
        # print('Price Breakout not in range')
        continue

    # Volume Breakout
    vol_increase = 1.1
    if last_volume < vol_increase * channel.Volume[-1]:
        # print('Not enough Volume')
        continue

    # Price above SMA
    if last_close < last_sma:
        # print('Price below SMA')
        continue

    # Weekly MACD above 0
    if last_macd < 0:
        # print('Weekly MACD below 0')
        continue
    breakout_tickers.append(ticker)

print(breakout_tickers)
