import pandas as pd
import numpy as np


def get_portfolio_value(prices, allocs, start_val=1):
    num = np.divide(allocs,prices.ix[0]) * start_val
    port_val = pd.Series(np.dot(prices, num), index=prices.index)
    return port_val


def get_portfolio_stats(port_val, daily_rf=0, samples_per_year=252):
    cum_ret = port_val.ix[-1]/port_val.ix[0] - 1
    daily_ret = port_val/port_val.shift(1) - 1
    avg_daily_ret = daily_ret.mean()
    std_daily_ret = daily_ret.std()
    sharpe_ratio = np.sqrt(samples_per_year)*(avg_daily_ret-daily_rf)/std_daily_ret
    return cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio
