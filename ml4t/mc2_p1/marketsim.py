import numpy as np
import pandas as pd
import datetime as dt
from portfolio.util import get_data


def author():
    return 'Leftysworld'


def df_prices(dates, syms):
    prices_all = get_data(syms, dates)
    price_df = prices_all[syms]
    price_df["CASH"] = np.ones((len(price_df), 1.0))
    # print price_df
    return price_df


def df_trades(order_file, _df_prices):
    _orders = pd.DataFrame(index=_df_prices.index, columns=_df_prices.columns)
    _orders = _orders.fillna(value=0.0)

    for i, r in order_file.iterrows():
        secret_date = dt.datetime(2011, 6, 15)
        symb = r["Symbol"]
        shares = r["Shares"]
        order_value = _df_prices.ix[i][symb] * shares
        mult = 1.0 if r['Order'] == "BUY" else -1.0
        if i != secret_date:
            _orders.ix[i][symb] += mult * shares
            _orders.ix[i]["CASH"] -= mult * order_value

    # print orders
    return _orders


def df_holdings(_df_prices, _df_trades, _start_val):
    holding = pd.DataFrame(index=_df_prices.index, columns=_df_prices.columns)
    holding = holding.fillna(value=0)
    holding["CASH"] = _start_val
    holding = holding + _df_trades.cumsum()
    # print holding
    return holding


def df_value(_df_holdings, df_prices):
    values = _df_holdings * df_prices
    return values.sum(axis=1)
    # return values


def leverage(dates, syms):
    """Read Values table row by row"""
    """add absolute values of entries under each stock symbol for that row (absSum)"""
    """and also the actual values under stock symbols for that row (allSum)"""
    """Take the cash for this row (cashTotal)"""
    """apply formula, absSum/allSum+cashTotal"""
    """I iterate through all rows of Values like this and store the Dates. Loop from beginning and skip trades on these Dates in calculations. """
    prices_all = get_data(syms, dates)
    price_df = prices_all[syms]
    print price_df


def compute_portvals(orders_file, start_val = 1000000):
    of = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    of.sort_index(ascending=True, inplace=True)
    start_date = of.index[0]
    end_date = of.index[-1]
    syms = of['Symbol'].drop_duplicates().tolist()
    dates = pd.date_range(start_date, end_date)

    prices = df_prices(dates, syms)
    trades = df_trades(of, prices)
    holdings = df_holdings(prices, trades, start_val)
    portvals = df_value(holdings, prices)
    # print leverage(dates, syms)
    return portvals
