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


def print_fundamentals():
    df = get_csv_infos()

    # print(df.columns.to_list())

    fundamentals = ['forwardPE', 'pegRatio', 'beta', 'dividendYield', 'industry', 'shortName']
    df = df[df.columns[df.columns.isin(fundamentals)]]

    df = df.sort_values(by='forwardPE')

    print(df[(df['forwardPE'] < 25) & (df['forwardPE'] > 6) &
            (df['pegRatio'] < 1) & (df['pegRatio'] > 0.3) &
            (df['industry'].str.contains('Insura') == False) &
            (df['industry'].str.contains('Bank') == False)])


import fundamentalanalysis as fa
from _keys import fa_api_key
ticker = "TXRH"


def save_fundamentals(ticker):
    # Collect the Balance Sheet statements
    balance_sheet = fa.balance_sheet_statement(ticker, fa_api_key, period="annual")    

    # Collect the Income Statements
    income_statement = fa.income_statement(ticker, fa_api_key, period="annual")    

    # Collect the Cash-Flow Statements
    cashflow_statement = fa.income_statement(ticker, fa_api_key, period="annual")

    # Combine statements into 1 df
    fundamentals = pd.concat([balance_sheet, income_statement, cashflow_statement])    
    fundamentals = fundamentals.transpose()    
    fundamentals.sort_index(inplace=True)
    # fundamentals = fundamentals.rename(columns=fundamentals.iloc[0])#.drop(fundamentals.index[0]).dropna()
    # print(fundamentals)

    # Save    
    fundamentals.to_csv(f'fundamentals/{ticker}.csv')

def get_roic(ticker):
    try:
        df = pd.read_csv(f'fundamentals/{ticker}.csv', index_col=0)
    except:
        save_fundamentals(ticker)
        df = pd.read_csv(f'fundamentals/{ticker}.csv', index_col=0)    

    # Only keep relevant data
    columns = ['totalEquity', 'longTermDebt','incomeBeforeTax', 'incomeTaxExpense']
    df = df[columns]

    # Calculations
    df['ROIC'] = (df.incomeBeforeTax - df.incomeTaxExpense) / (df.totalEquity + df.longTermDebt)    
    df['ROIC_5Y'] = df.ROIC.rolling(5).mean()
    print(df)

# save_fundamentals(ticker)
get_roic(ticker)