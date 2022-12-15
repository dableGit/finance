import requests
import gspread
import df_base
import pandas as pd


def update_sheet():
    sa = gspread.service_account()
    sh = sa.open('Stocks')

    wks = sh.worksheet('Portfolio')

    # print(wks.acell('A3').value)
    # print(wks.cell(1, 3).value)

    # print(wks.get('A3:I3'))

    for i in range(1, 49):
        ticker = wks.cell(i+1, 3).value
        r = requests.get(f'https://quote-feed.zacks.com/index.php?t={ticker}').json()
        try:
            wks.update(f'J{i+1}', r[ticker]['zacks_rank'])
        except:
            print(ticker)


zacks = []
for ticker in df_base.get_sp500_tickers(replace=False):
    r = requests.get(f'https://quote-feed.zacks.com/index.php?t={ticker}').json()
    inf = r[ticker]
    div_yield = inf['dividend_yield']
    forw_pe = inf['pe_f1']
    zack = inf['zacks_rank']
    zacks.append([ticker, div_yield, forw_pe, zack])

df = pd.DataFrame(zacks, index=None)
df.columns = ['ticker', 'div_yield', 'forw_pe', 'zack']
df.to_csv('zack_SP500.csv')
