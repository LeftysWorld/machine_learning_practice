import pandas as pd
import numpy as np
from portfolio.util import get_data
import time
from marketsim import compute_portvals


def compute_portfolio_stats(port_val, rfr=0.0, sf=252.0):
    daily_rets = ((port_val / port_val.shift(1)) - 1).ix[1:]
    cr = (port_val.ix[-1] / port_val.ix[0]) - 1
    adr = daily_rets.mean()
    sdr = daily_rets.std()
    sr = np.sqrt(sf) * (daily_rets - rfr).mean() / sdr
    start_date = port_val.index[0]
    end_date = port_val.index[-1]
    return cr, adr, sdr, sr, port_val, start_date, end_date


"""
==ORDERS.CSV==
    Data Range: 2011-01-10 to 2011-12-20
    Sharpe Ratio of Fund: 1.21540888742
    Sharpe Ratio of $SPX: 0.0183389807443
    Cumulative Return of Fund: 0.13386
    Cumulative Return of $SPX: -0.0224059854302
    Standard Deviation of Fund: 0.00720514136323
    Standard Deviation of $SPX: 0.0149716091522
    Average Daily Return of Fund: 0.000551651296638
    Average Daily Return of $SPX: 1.7295909534e-05
    Final Portfolio Value: 1133860.0
==ORDERS2.CSV==
    Data Range: 2011-01-14 to 2011-12-14
    Sharpe Ratio of Fund: 0.788982285751
    Sharpe Ratio of $SPX: -0.177203019906
    Cumulative Return of Fund: 0.0787526
    Cumulative Return of $SPX: -0.0629581516192
    Standard Deviation of Fund: 0.00711102080156
    Standard Deviation of $SPX: 0.0150564855724
    Average Daily Return of Fund: 0.000353426354584
    Average Daily Return of $SPX: -0.000168071648902
    Final Portfolio Value: 1078752.6
==ORDERS3.CSV==
    Data Range: 2011-01-10 to 2011-08-01
    Sharpe Ratio of Fund: 1.03455887842
    Sharpe Ratio of $SPX: 0.247809335326
    Cumulative Return of Fund: 0.05016
    Cumulative Return of $SPX: 0.0135380980508
    Standard Deviation of Fund: 0.00560508094997
    Standard Deviation of $SPX: 0.00840618502785
    Average Daily Return of Fund: 0.000365289198877
    Average Daily Return of $SPX: 0.000131224926273
    Final Portfolio Value: 1050160.0
"""


def test_run():
    of = "./orders/orders2.csv"
    sv = 1000000
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame): portvals = portvals[portvals.columns[0]]
    cr, adr, sdr, sr, port_val, start_dates, end_dates = compute_portfolio_stats(portvals)
    cr_SPY, adr_SPY, sdr_SPY, sr_SPY, spy_value, start_dates, end_dates = compute_portfolio_stats(
        get_data(['SPY'], dates=pd.date_range(start_dates, end_dates)))

    # Compare portfolio against $SPX
    print
    print "Date Range: {} to {}".format(start_dates, end_dates)
    print
    print "Sharpe Ratio of Fund: {}".format(sr)
    print "Sharpe Ratio of SPY : {}".format(sr_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cr)
    print "Cumulative Return of SPY : {}".format(cr_SPY)
    print
    print "Standard Deviation of Fund: {}".format(sdr)
    print "Standard Deviation of SPY : {}".format(sdr_SPY)
    print
    print "Average Daily Return of Fund: {}".format(adr)
    print "Average Daily Return of SPY : {}".format(adr_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

    if of == "./orders/orders.csv":
        print "Portfolio Value of orders: 1133860.0"
    if of == "./orders/orders2.csv":
        print "Portfolio Value of orders2: 1078752.6"
    if of == "./orders/orders3.csv":
        print "Portfolio Value of orders3: 1050160.0"


if __name__ == "__main__":
    start_time = time.clock()
    test_run()
    print
    print time.clock() - start_time, "seconds"
