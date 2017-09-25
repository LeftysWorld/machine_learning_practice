import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import util


def compute_daily_returns(df):
    daily_returns = (df / df.shift(1)) - 1
    res = daily_returns[1:]
    return res


def get_prices(start_date, end_date, symbollist):
    """
    Read in adjusted closing prices for given symbols, date range. Separates SPY from the rest.
    Returns both SPY data and syms data
    """
    dates = pd.date_range(start_date, end_date)
    prices_all = util.get_data(symbollist, dates)
    return prices_all[symbollist], prices_all["SPY"]


def normalize_data(df):
    res = df / df.ix[0, :]
    return res


def get_allocated_df(normed_prices, allocations):
    res = normed_prices * allocations
    return res


def get_portfolio_value(prices, allocations):
    """Get portfolio value"""
    normed_prices = normalize_data(prices)
    alloced = get_allocated_df(normed_prices, allocations)
    port_val_dist = alloced.sum(axis=1)
    return alloced, port_val_dist


def get_sharpe_ratio(risk_free_rate, sample_freq, avg_daily_ret, std_daily_ret):
    rfr_freq_calc = ((1.0 + float(risk_free_rate)) ** (1. / sample_freq)) - 1
    SR = (float(avg_daily_ret) - float(rfr_freq_calc)) / float(std_daily_ret)
    K = np.sqrt(sample_freq)
    SR_annualized = K * SR
    return SR_annualized


def get_mean_std_returns(returns):
    return returns.mean(), returns.std()


def generate_plot(prices_SPY, sv, alloced):
    prices_SPY_norm = normalize_data(prices_SPY)
    init_port_distrib = sv * alloced
    port_vals = init_port_distrib.sum(axis=1)
    df_temp = pd.concat([port_vals / sv, prices_SPY_norm], keys=['Portfolio', 'SPY'], axis=1)
    util.plot_data(df_temp, ylabel="Normalized Price")
    plt.show()


def assess_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1),
                     syms=['GOOG', 'AAPL', 'GLD', 'XOM'], allocs=[0.1, 0.2, 0.3, 0.4],
                     sv=1000000, rfr=0.0, sf=252.0, gen_plot=False):

    # Get inital portfolio data
    prices, prices_SPY = get_prices(sd, ed, syms)
    alloced, port_val_dist = get_portfolio_value(prices, allocs)
    daily_returns = compute_daily_returns(port_val_dist)

    # Get portfolio statistics
    cum_ret = (port_val_dist[-1] / port_val_dist[0]) - 1
    end_value = sv * (cum_ret + 1)
    avg_daily_ret, std_daily_ret = get_mean_std_returns(daily_returns)
    SR = get_sharpe_ratio(rfr, sf, avg_daily_ret, std_daily_ret)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        generate_plot(prices_SPY, sv, alloced)

    return cum_ret, avg_daily_ret, std_daily_ret, SR, end_value


def test_run():
    # Set up
    start_date = dt.datetime(2009, 01, 01)
    end_date = dt.datetime(2011, 01, 01)
    symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000
    risk_free_rate = 0.0
    sample_freq = 252

    cum_ret, avg_daily_ret, std_daily_ret, SRannualized, end_value = \
        assess_portfolio(sd=start_date, ed=end_date, syms=symbols,
                         allocs=allocations, sv=start_val, rfr=risk_free_rate,
                         sf=sample_freq, gen_plot=True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", SRannualized
    print "Volatility (stdev of daily returns):", std_daily_ret
    print "Average Daily Return:", avg_daily_ret
    print "Cumulative Return:", cum_ret
    print "End Value", end_value


if __name__ == "__main__":
    test_run()
