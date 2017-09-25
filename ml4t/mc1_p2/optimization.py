import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo
import util

#
# Library Functions
#


def get_prices(start_date, end_date, symbollist, selection=None):
    """
    Read in adjusted closing prices for given symbols, date range. Separates SPY from the rest.
    Returns both SPY data and syms data
    """
    dates = pd.date_range(start_date, end_date)
    prices_all = util.get_data(symbollist, dates)
    prices = prices_all[symbollist] if selection is None else prices_all[selection]
    return prices


def get_best_allocations(syms, prices, rfr, sf):
    # Sets up the minimizer
    initial_guess = np.ones(len(syms)) * (1.0 / len(syms))
    bounds1 = [(0.0, 1.0) for _ in range(len(syms))]
    const = ({'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs)})
    allocs = spo.minimize(f, initial_guess, args=(prices, rfr, sf), bounds=bounds1, method='SLSQP',
                          options={'disp': True}, constraints=const).x
    return allocs


def f(allocs, prices, rfr, sf):
    """Equation used for getting minimal value of SR (which becomes the highest value when using SR * -1"""
    sr = get_sharpe_ratio_data(prices, allocs, rfr, sf)
    return -sr


def get_sharpe_ratio_data(prices, allocs, rfr, sf):
    # Gathers necessary data used in the SR calculation
    daily_returns = get_daily_returns_data(prices, allocs)
    avg_daily_return, std_daily_return = daily_returns.mean(), daily_returns.std()
    SR = get_sharpe_ratio(rfr, sf, avg_daily_return, std_daily_return)
    return SR


def get_sharpe_ratio(risk_free_rate, sample_freq, avg_returns, std_returns):
    # Calculates the SR
    rfr_freq_calc = float(risk_free_rate)
    SR = (float(avg_returns) - float(rfr_freq_calc)) / float(std_returns)
    K = np.sqrt(sample_freq)
    SR_annualized = K * SR
    return SR_annualized


def get_daily_returns_data(prices, allocs):
    # A transducer pipeline for getting the daily returns
    dr = reduce(lambda x, y: y(x), [lambda vals: get_portfolio_value_data(*vals), compute_daily_returns],
                [prices, allocs])
    return dr


def get_portfolio_value_data(prices, allocs):
    # A transducer pipeline for getting the portfolio value
    pv = reduce(lambda x, y: y(x), [lambda vals: get_allocated_df(*vals), get_portfolio_value], [prices, allocs])
    return pv


def compute_daily_returns(df):
    # Gets the daily returns
    daily_returns = (df / df.shift(1)) - 1
    res = daily_returns[1:]
    return res


def get_allocated_df(prices, allocations):
    # Gets DF of allocations where starting value is value of normalized stock * stock allocations
    res = normalize_data(prices) * allocations
    return res


def normalize_data(df):
    # Normalizes portfolio such that day 1 stock prices are set to 1.0
    res = df / df.ix[0, :]
    return res


def get_portfolio_value(alloced):
    # Get portfolio value
    portfolio_value = alloced.sum(axis=1)
    return portfolio_value


def get_cumulative_returns(portfolio_value):
    # Returns the cumulative returns of portfolio
    starting_value = portfolio_value[0]
    ending_value = portfolio_value[-1]
    cumulative_returns = (ending_value / starting_value) - 1
    return cumulative_returns


def plot_normalized_data(df, title, xlabel, ylabel):
    normalized_df = normalize_data(df)
    ax = normalized_df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc="upper left")
    plt.grid(True)
    plt.show()


#
# ML4T API
#

def optimize_portfolio(sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 1, 1), syms=None, gen_plot=False):
    # Initial Set up
    if syms is None:
        syms = ['GOOG', 'AAPL', 'GLD', 'XOM']

    rfr = 0.0
    sf = 252.0

    # Get prices
    prices = get_prices(sd, ed, syms)
    prices_SPY = get_prices(sd, ed, syms, "SPY")

    # Get Allocations
    allocs = get_best_allocations(syms, prices, rfr, sf)

    # Get Portfolio Statistics
    portfolio_value = get_portfolio_value_data(prices, allocs)
    cr = get_cumulative_returns(portfolio_value)
    daily_returns = get_daily_returns_data(prices, allocs)
    adr, sddr = daily_returns.mean(), daily_returns.std()
    sr = get_sharpe_ratio_data(prices, allocs, rfr, sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([portfolio_value, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_normalized_data(df_temp, "Daily portfolio value and SPY", "Date", "Normalized price")
        pass

    return allocs, cr, adr, sddr, sr


def test_run():
    # # PLOT TO TURN IN
    start_date = '2008-06-01'
    end_date = '2009-06-01'
    symbols = ['IBM', 'X', 'GLD']
    theirs = [ 0.00000000e+00, 2.02060590e-14, 1.00000000e+00]

    allocs, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date,
                                                   syms=symbols, gen_plot=False)

    t_or_f = True
    if t_or_f:
        print "Start Date:", start_date
        print "End Date:", end_date
        print "Symbols:", symbols
        print "Allocations:", allocs
        print "Their Allocs:", theirs
        print "Sharpe Ratio:", sr
        print "Volatility (stdev of daily returns):", sddr
        print "Average Daily Return:", adr
        print "Cumulative Return:", cr
    else:
        pass


if __name__ == "__main__":
    test_run()

