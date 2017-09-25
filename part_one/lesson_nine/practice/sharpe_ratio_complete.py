# coding=utf-8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import util


def normalize_data(df):
    return df / df.ix[0, :]


def allocated_start(df, allocs):
    return df * allocs


def position_values(df, start_val):
    return df * start_val


def compute_daily_returns(df):
    daily_returns = (df / df.shift(1)) - 1
    return daily_returns[1:]


def test_run():
    # Set up
    start_date = dt.datetime(2009, 01, 01)
    end_date = dt.datetime(2011, 01, 01)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    # New Function, call this function here
    dates = pd.date_range(start_date, end_date)
    prices_all = util.get_data(symbols, dates)

    prices = prices_all[symbols] # only portfolio symbols
    prices_SPY = prices_all["SPY"] # Only SPY, for comparison later

    # Get Daily Portfolio Value
    prices_SPY = prices_SPY / prices_SPY.ix[0, :] # Normalizes prices_SPY

    normed_prices = prices / prices.ix[0, :]
    alloced = normed_prices * allocations
    port_vals = alloced.sum(axis=1)
    daily_returns = compute_daily_returns(port_vals)

    # Get Portfolio Statistics
    cum_ret = (port_vals[-1] / port_vals[0]) - 1    # Cumulative Returns
    avg_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()

    # Do if statement to be sure this is daily, else yearly / monthly
    # Below is Daily:
    #   avg_daily_risk_free_rate = (1.0 + yearly_risk_free_rate)**(1. / 252) - 1          # ASK ABOUT Daily RISK FREE RATE USED OR NOT
    #   SR = (avg_daily_ret - avg_daily_risk_free_rate) / std_daily_ret
    #   K = np.sqrt(252)
    #   SRannualized = K * SR
    #
    #Below is Weekly:
    #   avg_weekly_risk_free_rate = (1.0 + yearly_risk_free_rate)**(1. / 52) - 1          # ASK ABOUT Weekly RISK FREE RATE USED OR NOT
    #   SR = (avg_weekly_ret - avg_weekly_risk_free_rate) / std_weekly_ret                   # ASK ABOUT AVG_MONTHLY_RETURNS / STD_MONTHLY_RETURNS
    #   K = np.sqrt(12)
    #   SRannualized = K * SR
    #
    #Below is Monthly:
    #   avg_monthly_risk_free_rate = (1.0 + yearly_risk_free_rate)**(1. / 12) - 1          # ASK ABOUT Monthly RISK FREE RATE USED OR NOT ## Question: for monthly do I simply replace 252 with 12? what about the 1.0?
    #   SR = (avg_daily_ret - avg_monthly_risk_free_rate) / std_monthly_ret                   # ASK ABOUT AVG_MONTHLY_RETURNS / STD_MONTHLY_RETURNS
    #   K = np.sqrt(12)
    #   SRannualized = K * SR
    #Below is Yearly:
    #   risk_free_rate = risk_free_rate                                                     # ASK ABOUT Annual RISK FREE RATE USED OR NOT
    #   SR = (avg_yearly_return - risk_free_rate) / std_yearly_return              # ASK ABOUT this being ave yearly?
    #   SRannualized = SR

    rfr_freq_calc = ((1.0 + float(risk_free_rate))**(1. / sample_freq)) - 1
    # SR = (daily_returns - risk_free_rate).mean() / (np.sqrt(sample_freq) * (daily_returns).std())  # 0.00870688461805
    SR = (float(avg_daily_ret) - float(rfr_freq_calc)) / float(std_daily_ret)
    K = np.sqrt(sample_freq)
    SRannualized = K * SR

    end_value = start_val * (cum_ret + 1)

    # Compare daily portfolio value with SPY using a normalized plot
    df_temp = pd.concat([port_vals, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
    # util.plot_data(df_temp, ylabel="Normalized Price")
    # plt.show()

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", SRannualized
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret


if __name__ == "__main__":
    test_run()
