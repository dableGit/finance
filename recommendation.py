import sqlalchemy
import pandas as pd
import numpy as np
import pandas_datareader.data as dtr
import datetime as dt

engine = sqlalchemy.create_engine('sqlite:///finance.db')
conn = engine.connect()


def get_last_entry_date(ticker):
    query = sqlalchemy.sql.text(f'SELECT Date FROM "{ticker}" ORDER BY Date DESC LIMIT 1')
    date_str = conn.execute(query).fetchone()[0]
    return sqlite_str_2_dt(date_str)


def sqlite_str_2_dt(date_str):
    date, _time = date_str.split(' ')
    year, month, day = date.split('-')
    return dt.datetime(int(year), int(month), int(day))


# start = dt.datetime(year=2022, month=4, day=20)

# df = dtr.get_data_yahoo('AAPL', start=start)
# df.reset_index()
# df.to_sql('AAPL', conn)

# df = pd.read_sql('SELECT Date FROM AAPL ORDER BY Date DESC LIMIT 1', conn)


# df = pd.read_sql('AAPL', conn)
