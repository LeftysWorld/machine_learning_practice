# coding=utf-8
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
Computing Sharpe Ratio:
Rp: Portfolio return
Rf: risk free rate of return
σp: std dev of portfolio return

# [expected value of the return on a portfolio - Rp] / [standard deviation of same difference]
# Called Ex Ante because using expected its a forward looking measure of what the Sharpe Ratio should be.
S = E[Rp - Rf] / std[Rp - Rf]

To calculate in python using historical data:
S = mean(daily_rets - daily_rf) / std(daily_rets - daily_rf)

What is Risk Free Rate and where do we get it?
    - Traditionally there are a few numbers people use for this:
        - LIBOR
        - 3mo T-bill
        - 0% (a good approximation to the risk free rate)
    - Short cut to getting the daily Rf, where 252 = # trading days per year, 1.0 = 1 year, 0.1 = Rf for the year:
        - (252 root of (1.0 + 0.1) - 1
    - I believe in this class we will approximate the risk free rate with 0

USE THIS FOR CALCULATING SHARPE RATIO:
    S = mean(daily_rets - daily_rf) / std(daily_rets)


More Notes:
    The Sharpe Ratio can vary widely depending on how frequently you sample.
    In other words, if you sample the prices every year and compute ratio based on yearly statistics you'll get one number, monthly you'll get another, daily etc
    The original vision for the Sharpe Ratio is that it's an annual number.
        So if we are sampling at frequencies other than annually, we need to add an adjustment factor.
        SR = Sharpe Ratio
        SRannualized = K * SR   #  multiply the SR by an adjustment factor called K to get the annualized version

    What is K?
        K = square_root(#_samples_per_year)
        Daily Measurements: K = square_root(252)
        Weekly Measurements: K = square_root(52)
        Monthly Measurements: K = square_root(12)

    SO, THE NEW SHARPE RATIO CALCULATION (for daily):
        SR = square_root(252) * mean(daily_rets - daily_rf) / std(daily_rets)

"""


def symbol_to_path(symbol, base_dir="../../../ml4t/data"):
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    df = pd.DataFrame(index=dates)
    symbols = ["SPY"] + symbols if "SPY" not in symbols else symbols

    for s in symbols:
        df_temp = pd.read_csv(symbol_to_path(s), index_col='Date',
                              parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={"Adj Close":s})
        df = df.join(df_temp)
        df = df.dropna(subset=["SPY"]) if s == "SPY" else df
    return df


def normalize_data(df):
    return df / df.ix[0, :]


def allocated_start(df, allocs):
    return df * allocs


def position_values(df, start_val):
    return df * start_val


def compute_daily_returns(df):
    daily_returns = (df / df.shift(1)) - 1
    # daily_returns.ix[0, :] = 0
    # daily_returns[0, :] = [0, 0, 0, 0, 0]
    # daily_returns[0, :] = [0]
    return daily_returns[1:]

#
# def compute_daily_returns(df):
#     daily_returns = df.copy()
#     daily_returns[1:] = (df[1:] / df[:-1].values) - 1
#     # daily_returns.ix[0, :] = 0
#     return daily_returns
#
#
# def compute_daily_returns(df):
#     daily_rets = df.copy()
#     daily_rets[1:] = (df[1:] / df[:-1].values) - 1
#
#     return daily_rets[1:]


def test_run():
    start_val = 1000000
    sd, ed = '2009-01-01', '2011-12-31'
    symbols = ['SPY', 'XOM', 'GOOG', "GLD"]
    allocs = [0.4,0.4,0.1,0.1] # np.array([0.4, 0.4, 0.1, 0.1])
    dates = pd.date_range(sd, ed)
    df = get_data(symbols, dates)

    # Daily Portfolio Value
    df_norm = normalize_data(df)
    df_allocated_start = allocated_start(df_norm, allocs)
    df_pos_vals = position_values(df_allocated_start, start_val)
    df_port_value = df_pos_vals.sum(axis=1)
    daily_return = compute_daily_returns(df_port_value)

    # Portfolio Statistics
    cum_return = (df_port_value[-1] / df_port_value[0]) - 1     # cumulative_return
    avg_daily_ret = daily_return.mean() # average_daily_return
    std_daily_return = daily_return.std()   # standard deviation daily return

    # Sharpe Ratio SR = square_root(252) * (mean(daily_rets - daily_rf) / std(daily_rets))
    SR = np.sqrt(1) * (avg_daily_ret / std_daily_return)
    print SR


if __name__ == "__main__":
    test_run()
