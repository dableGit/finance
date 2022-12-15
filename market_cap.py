# IMPORT LIBRARIES

import pandas as pd  # For DataFrame Manipulation

# Libraries to download data from Yahoo Finance
import yfinance as yf

# Libraries for System functionss
# import datetime
# import time
import os
# import sys
import shutil
import pickle

# from tqdm.notebook import tqdm  # Library to see progress of loop iterations

# Libraries for Treemap
# from functools import partial
# from d3IpyPlus import *
# d3IpyPlus was found in https://github.com/maclandrol/d3IpyPlus
# One just needs to include the file d3IpyPlus.py in the same path as the Jupyter Notebook's file

# Libraries for Table
# from bokeh.io import show, save, output_file
# from bokeh.models import ColumnDataSource
# from bokeh.models.widgets import DataTable, TableColumn


# INITIAL SETUP

def folder_setup():
    # Create a Data Folder
    Data_folder = os.path.abspath(os.getcwd() + '/Data/')
    if not os.path.exists(Data_folder):
        os.makedirs(Data_folder)

    # Clean older files and folders in the Data Folder
    filelist = [f for f in os.listdir(Data_folder)]
    for f in filelist:
        shutil.rmtree(os.path.join(Data_folder, f), ignore_errors=True)

    filelist = [f for f in os.listdir(Data_folder)]
    for f in filelist:
        os.remove(os.path.join(Data_folder, f))

    # Create New Folder for Stoxx
    stoxx_folder = os.path.join(Data_folder, 'Stoxx')
    if not os.path.exists(stoxx_folder):
        os.makedirs(stoxx_folder)

    # Create New Folder for SP500
    sp500_folder = os.path.join(Data_folder, 'SP500')
    if not os.path.exists(sp500_folder):
        os.makedirs(sp500_folder)

    # Create New Folder for Currencies
    currencies_folder = os.path.join(Data_folder, 'Currencies')
    if not os.path.exists(currencies_folder):
        os.makedirs(currencies_folder)


def converter(variable):
    # Formula to Convert variables to number values
    convert_matrix = {'%': 1, 'K': 1000, 'k': 1000,
                      'M': 1000000, 'B': 1000000000, 'T': 1000000000000}
    if pd.isnull(variable):
        variable = 'nan'
    elif isinstance(variable, float):
        variable = variable
    else:
        variable = variable.replace(',', '')
        units = variable[-1]
        if (units == '%' or units == 'K' or units == 'k' or
                units == 'M' or units == 'B' or units == 'T'):
            variable = round(float(variable[:-1])*convert_matrix[units], 2)
        else:
            variable = round(float(variable), 2)
    return variable


class Currency():
    def __init__(self, ticker):
        self.ticker = ticker
        self._info = yf.Ticker(ticker).info
        self.price = self._info['regularMarketPrice']


class Company():
    def __init__(self, ticker):
        self.ticker = ticker
        self._info = yf.Ticker(ticker).info
        self.shares_out = self._info['sharesOutstanding']
        self.price = self._info['regularMarketPrice']
        self.currency = self._info['currency']
        self.market_cap = self._info['marketCap']
        self.name = self._info['shortName']
        self.sector = self._info['sector']
        self.industry = self._info['industry']

    def __repr__(self):
        if self.currency == 'USD':
            cap = round(self._info['marketCap'] / 1000000000)
        else:
            cap = round(self._info['marketCap'] / 1000000000)
        return f'{cap} B {self.currency} {self.name}'

    def __str__(self):
        cap = round(self._info['marketCap'] / 1000000000)
        return f'{cap} B {self.currency} {self.name}'

    def __lt__(self, other):
        return self.market_cap < other.market_cap


# Define the file name with information (Company name, Stock Ticker and so on)
STOXX600 = 'Stoxx600.csv'
SP500 = 'SP500.csv'

# OBTAINING MARKET DATA


def print_index_cap(index):
    # Define the List of tickers
    Index_data = pd.read_csv(index)
    tickers = Index_data['Yahoo_Ticker'].drop_duplicates().tolist()

    companies = []
    for ticker in tickers:
        try:
            companies.append(Company(ticker))
        except Exception as e:
            print(ticker, e)

    companies.sort(reverse=True)
    for companie in companies:
        print(companie)


def save_index(index, filename):
    # Define the List of tickers
    Index_data = pd.read_csv(index)
    tickers = Index_data['Yahoo_Ticker'].drop_duplicates().tolist()

    companies = []
    for ticker in tickers:
        try:
            companies.append(Company(ticker))
        except Exception as e:
            print(ticker, e)

    companies.sort(reverse=True)
    with open(filename, 'wb') as file_co:
        pickle.dump(companies, file_co, protocol=pickle.HIGHEST_PROTOCOL)


def load_index(filename):
    with open(filename, 'rb') as file_co:
        companies = pickle.load(file_co)
    return companies


# save_index(SP500, 'SP500.obj')
SP500 = load_index('SP500.obj')
# print_index_cap(SP500)


def test():
    for company in SP500:
        print(company['ticker'], company['shortRatio'], company['shortName'])


test()

# baba = Company('9988.HK')
# print(baba)

# tenc = Company('0700.HK')
# print(tenc)

# info = yf.Ticker('BRK-A').info
# print(info)
# info = yf.Ticker('BRK-B').info
# print(info)
