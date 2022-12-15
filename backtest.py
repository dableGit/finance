import pandas as pd
import ta
import yfinance as yf
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, resample_apply


class SMAcross(Strategy):
    n1 = 50
    n2 = 100
    stop = 0.85

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n1)
        self.sma2 = self.I(ta.trend.sma_indicator, pd.Series(close), self.n2)

    def next(self):
        price = self.data.Close[-1]
        if crossover(self.sma1, self.sma2):
            # self.position.close()
            self.buy(sl=self.stop*price)
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            # self.sell()
        # self.trades.sl


class RSIoscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    window = 14
    stop = 0.85

    def init(self):
        close = self.data.Close
        self.daily_rsi = self.I(ta.momentum.rsi, pd.Series(close), self.window)
        self.weekly_rsi = resample_apply(
            'W-FRI', ta.momentum.rsi, close, self.window)

    def next(self):
        if crossover(self.daily_rsi, self.upper_bound) and (self.weekly_rsi[-1] > self.upper_bound):
            self.position.close()

        elif crossover(self.lower_bound, self.daily_rsi) and (self.weekly_rsi[-1] < self.lower_bound):
            self.buy()


class DualMACD(Strategy):
    window_slow = 26
    window_fast = 12
    window_sign = 9
    windows = [window_slow, window_fast, window_sign]
    stop = 90

    def init(self):
        close = self.data.Close
        self.daily_MACD = self.I(ta.trend.macd_diff, pd.Series(close), *self.windows)
        self.weekly_MACD = resample_apply(
            'W-FRI', ta.trend.macd_diff, close, *self.windows)

    def next(self):
        price = self.data.Close[-1]
        # Long only
        if crossover(self.daily_MACD, 0) and self.weekly_MACD[-1] > 0:
            self.buy(sl=self.stop/100*price)

        elif crossover(0, self.daily_MACD):
            self.position.close()
        # Short Only
        else:
            pass


class MACD(Strategy):
    window_slow = 26
    window_fast = 12
    window_sign = 9
    windows = [window_slow, window_fast, window_sign]
    stop = 85

    def init(self):
        close = self.data.Close
        self.weekly_MACD = resample_apply(
            'W-FRI', ta.trend.macd_diff, close, *self.windows)

    def next(self):
        price = self.data.Close[-1]
        if crossover(self.weekly_MACD, 0):
            self.buy(sl=self.stop/100*price)

        elif crossover(0, self.weekly_MACD):
            self.position.close()


df = yf.download('BTC-USD', start='2017-01-01')
bt = Backtest(df, DualMACD, cash=100000, commission=0.002,
              exclusive_orders=True)
# stats = bt.run()


stats = bt.optimize(stop=range(80, 100, 1),
                    maximize='Return [%]')

print(stats)
# bt.plot(f'backtest/{stats["_strategy"]}.html')
bt.plot()
