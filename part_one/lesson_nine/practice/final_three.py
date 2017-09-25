import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import util


def generate_plot(prices_SPY, start_val, alloced):
    # SPY Data
    prices_SPY_normed = normalize_data(prices_SPY)

    # Portfolio Data
    init_port_distribution = start_val * alloced
    portfolio_values = init_port_distribution.sum(axis=1)

    # Create Plot
    df_temp = pd.concat([portfolio_values / start_val, prices_SPY_normed], keys=['Portfolio', 'SPY'], axis=1)
    util.plot_data(df_temp, ylabel="Normalized Price")
    plt.show()


def get_sharpe_ratio(risk_free_rate, sample_freq, avg_returns, std_returns):
    """
    After searching everywhere in the piazza forum I found the risk free rate provided will not need the rfr_req_calc I created.
    The rfr_req_calc that I used and was provided was only food for thought, but will not be necessary for this project

    # rfr_freq_calc = ((1. + float(risk_free_rate)) ** (1. / sample_freq)) - 1.
    """

    rfr_freq_calc = float(risk_free_rate)
    SR = (float(avg_returns) - float(rfr_freq_calc)) / float(std_returns)
    K = np.sqrt(sample_freq)
    SR_annualized = K * SR
    return SR_annualized


def get_mean_std_returns(returns):
    return returns.mean(), returns.std()


def compute_daily_returns(df):
    daily_returns = (df / df.shift(1)) - 1
    res = daily_returns[1:]
    return res


def normalize_data(df):
    res = df / df.ix[0, :]
    return res


def get_allocated_df(normed_prices, allocations):
    res = normed_prices * allocations
    return res


def get_portfolio_value(prices, allocations, sv):
    """Get portfolio value"""
    normed_prices = normalize_data(prices)
    alloced = get_allocated_df(normed_prices, allocations)
    # portfolio_value = alloced.sum(axis=1)

    position_values = sv * alloced
    portfolio_value = position_values.sum(axis=1)

    return alloced, portfolio_value


def get_prices(start_date, end_date, symbollist):
    """
    Read in adjusted closing prices for given symbols, date range. Separates SPY from the rest.
    Returns both SPY data and syms data
    """
    dates = pd.date_range(start_date, end_date)
    prices_all = util.get_data(symbollist, dates)
    return prices_all[symbollist], prices_all["SPY"]


def determine_sample_freq(sample_freq):
    frequency_list = [252.0, 52.0, 12.0, 1.]
    res = float(sample_freq) if float(sample_freq) in frequency_list else 252.
    return res


def assess_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1),
                     syms=['GOOG', 'AAPL', 'GLD', 'XOM'], allocs=[0.1, 0.2, 0.3, 0.4],
                     sv=1000000, rfr=0.0, sf=252.0, gen_plot=True):

    # see how to make sure if syms is none it still works

    # Get inital portfolio data
    freq = determine_sample_freq(sf)
    prices, prices_SPY = get_prices(sd, ed, syms)
    alloced, portfolio_value = get_portfolio_value(prices, allocs, sv)
    portfolio_returns = compute_daily_returns(portfolio_value)

    # Get portfolio statistics
    cumulative_returns = (portfolio_value[-1] / portfolio_value[0]) - 1
    end_value = sv * (cumulative_returns + 1)
    avg_returns, std_returns = get_mean_std_returns(portfolio_returns)
    SR = get_sharpe_ratio(rfr, freq, avg_returns, std_returns)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        generate_plot(prices_SPY, sv, alloced)

    return cumulative_returns, avg_returns, std_returns, SR, end_value


def test_run():
    # Set up
    start_date = '2010-01-01'
    end_date = '2010-12-31'
    symbols = ['AXP', 'HPQ']
    allocations = [0.0, 1.0]
    start_val = 1000000
    risk_free_rate = 0.001
    sample_freq = 252

    """
    could nto test risk free rate if not 0.0
    """

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
    print "End Value:", end_value


if __name__ == "__main__":
    test_run()
