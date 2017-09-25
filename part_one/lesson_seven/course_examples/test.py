import os
import pandas as pd
import util


def normalize_data(df):
    """Normalize stock prices using the first row of the dataframe"""
    res = df / df.ix[0, :]
    return res


def plot_selected(df, columns, start_index, end_index):
    util.plot_data(df.ix[start_index:end_index, columns], title="Selected Data")


def test_run():
    start_val = 1000000
    sd, ed = '2009-01-01', '2011-12-31'
    symbols = ['SPY', 'XOM', 'GOOG', "GLD"]
    allocs = [0.4, 0.4, 0.1, 0.1]

    dates = pd.date_range(sd, ed)
    df = util.get_data(symbols, dates)
    df = normalize_data(df)
    return df, plot_selected(df, symbols, '2010-01-01', '2010-12-31')


if __name__ == "__main__":
    print test_run()
