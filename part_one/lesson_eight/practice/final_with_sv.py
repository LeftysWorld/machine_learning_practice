import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import util
import scipy.optimize as spo


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


def get_best_allocations(syms, prices, start_val, rfr, sf):
    # Sets up the minimizer
    initial_guess = np.ones(len(syms)) * (1.0 / len(syms))
    bounds1 = [(0.0, 1.0) for _ in range(len(syms))]
    bounds2 = tuple((0.0, 1.0) for _ in range(len(syms)))
    print "bounds1:", bounds1
    print "bounds2:", bounds2

    const = ({'type': 'eq', 'fun': lambda inputs: 1.0 - np.sum(inputs)})
    allocs = spo.minimize(f, initial_guess, args=(prices, start_val, rfr, sf), bounds=bounds1, method='SLSQP',
                          options={'disp': True}, constraints=const).x
    return allocs


def f(allocs, prices, start_val, rfr, sf):
    """Equation used for getting minimal value of SR (which becomes the highest value when using SR * -1"""
    sr = get_sharpe_ratio_data(prices, allocs, start_val, rfr, sf)
    return -sr


def get_sharpe_ratio_data(prices, allocs, start_val, rfr, sf):
    # Gathers necessary data used in the SR calculation
    daily_returns = get_daily_returns_data(prices, allocs, start_val)
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


def get_daily_returns_data(prices, allocs, start_val):
    # A transducer pipeline for getting the daily returns
    daily_returns = reduce(lambda x, y: y(x), [
        lambda vals: get_portfolio_value_data(*vals),
        compute_daily_returns], [prices, allocs, start_val])
    return daily_returns


def get_portfolio_value_data(prices, allocs, start_val):
    # A transducer pipeline for getting the portfolio value
    portfolio_value = reduce(lambda x, y: y(x), [
        lambda vals: get_allocated_df(*vals),
        lambda x: get_portfolio_value(x, start_val)], [prices, allocs])
    return portfolio_value


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


def get_portfolio_value(alloced, sv):
    # Get portfolio value
    position_values = sv * alloced
    portfolio_value = position_values.sum(axis=1)
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
def optimize_portfolio(sd, ed, syms, gen_plot=False):
    # Set Up
    # Hardcoding is encouraged here? I gotta be missing something.
    start_val = 1000000
    rfr = 0.0
    sf = 252.0

    # Get inital portfolio data
    prices = get_prices(sd, ed, syms)
    prices_SPY = get_prices(sd, ed, syms, "SPY")

    # Get Allocations
    allocs = get_best_allocations(syms, prices, start_val, rfr, sf)

    # Get Portfolio Statistics
    portfolio_value = get_portfolio_value_data(prices, allocs, start_val)
    cr = get_cumulative_returns(portfolio_value)

    daily_returns = get_daily_returns_data(prices, allocs, start_val)
    adr, sddr = daily_returns.mean(), daily_returns.std()
    sr = get_sharpe_ratio_data(prices, allocs, start_val, rfr, sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([portfolio_value, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_normalized_data(df_temp, "Daily portfolio value and SPY", "Date", "Normalized price")
        pass

    return allocs, cr, adr, sddr, sr


def test_run():
    # # example 1
    # start_date = '2010-01-01'
    # end_date = '2010-12-31'
    # symbols = ['GOOG', 'AAPL', 'GLD', 'XOM']
    # theirs = [5.38105153e-16, 3.96661695e-01, 6.03338305e-01, -5.42000166e-17]
    # allocs, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, syms=symbols, gen_plot=True)

    # My graph compared to theirs: The Same

    # # example 2
    start_date = '2004-01-01'
    end_date = '2006-01-01'
    symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    theirs = [7.75113042e-01, 2.24886958e-01, -1.18394877e-16, -7.75204553e-17]
    allocs, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, syms=symbols, gen_plot=True)

    # My graph compared to theirs: The Same

    # # example 3
    # start_date = '2004-12-01'
    # end_date = '2006-05-31'
    # symbols = ['YHOO', 'XOM', 'GLD', 'HNZ']
    # theirs = [ -3.84053467e-17,   7.52817663e-02,   5.85249656e-01,   3.39468578e-01]
    # allocs, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, syms=symbols, gen_plot=False)

    # # example 4
    # start_date = '2005-12-01'
    # end_date = '2006-05-31'
    # symbols = ['YHOO', 'HPQ', 'GLD', 'HNZ']
    # theirs = [ -1.67414005e-15,   1.01227499e-01,   2.46926722e-01,   6.51845779e-01]
    # allocs, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, syms=symbols, gen_plot=False)

    # Example from @348 Piazza
    # start_date = '2008-06-01'
    # end_date = '2009-06-01'
    # symbols = ['IBM', 'X', 'GLD']
    # theirs = [0.00000000e+00, 2.50910404e-14, 1.00000000e+00]
    # allocs, cr, adr, sddr, sr = optimize_portfolio(sd=start_date, ed=end_date, syms=symbols, gen_plot=False)

    theirs = np.array(theirs).tolist()
    allocs = np.array(allocs).tolist()


    ###########
    # Testing #
    ###########
    def get_all_allocs(theirs, allocs):
        return {"Masters Example": theirs, "Mine": allocs}

    def test_1_sum(allocs):
        summ = sum(allocs)
        if 1.0 - 0.02 < summ < 1.0 + 0.2:
            # return "Pass:", {"Sum Test Pass": summ}
            return "Sum Test Pass", summ
        elif 1.0 - 0.2 > summ:
            return "Sum Test Fail: Too Small", summ
        else:
            return "Sum Test Fail: Too Large", summ

    def test_2_alloc_range(dict):
        """a = np.array([1, 2]) a.tolist()"""
        them = dict["Masters Example"]
        mine = dict["Mine"]
        range_or_not = []

        for m in mine:
            if 0 - 0.02 < m < 1 + 0.02:
                range_or_not += ["in range"]

        if all(x == range_or_not[0] for x in range_or_not):
            return "Range Test Pass", range_or_not
        else:
            return "Range Test Fail", range_or_not

    def test_3_allocs_match(theirs, allocs):
        match_list = []
        final_list = []
        test_list = []

        for i in range(len(theirs)):  # [0,1,2,3]
            a = theirs[i] * 10 - allocs[i] * 10
            match_list += [a]

        for i in match_list:
            final_list = final_list + ["Pass"] if round(i, 2) == 0 else final_list + ["Fail"]
            test_list += [i]

        if all(x == final_list[0] for x in final_list):
            return "Allocs Test Pass", final_list, "Masters - Mine", test_list
        else:
            return "Allocs Test Fail", final_list, "Masters - Mine", test_list

    print "All Allocs:\n", get_all_allocs(theirs, allocs)
    print "Test 1: Sum \n", test_1_sum(allocs)
    print "Test 2: Allocation between 0 and 1.0 +- 0.02 \n", test_2_alloc_range(get_all_allocs(theirs, allocs))
    print "Test 3: Allocation matches ML4T solution +- 0.10 \n", test_3_allocs_match(theirs, allocs)
    print ""

    # Print statistics
    t_or_f = True
    if t_or_f:
        print "Start Date:", start_date
        print "End Date:", end_date
        print "Symbols:", symbols
        my_allocs = []
        their_allocs = []
        for i in allocs:
            my_allocs += [(float(format(i, '10f')))]
            their_allocs += [(float(format(i, '10f')))]
        print "Converted Allocs:", {"Mine": my_allocs, "Theirs": their_allocs}
        print "My Allocations Original:", allocs
        print "Their Allocs Original:", theirs
        print "Sharpe Ratio:", sr
        print "Volatility (stdev of daily returns):", sddr
        print "Average Daily Return:", adr
        print "Cumulative Return:", cr
    else:
        pass


if __name__ == "__main__":
    test_run()

