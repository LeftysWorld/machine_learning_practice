import os
import pandas as pd
import matplotlib.pyplot as plt


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

    df_norm = normalize_data(df)
    df_allocated_start = allocated_start(df_norm, allocs)
    df_pos_vals = position_values(df_allocated_start, start_val)
    df_port_value = df_pos_vals.sum(axis=1)
    daily_return = compute_daily_returns(df_pos_vals)

    print "df_pos_vals[:7]"
    print df_pos_vals[:7]

    print ""
    print "df_port_value[:7]"
    print df_port_value[:7]

    print ""
    print "daily_return[:7]"
    print daily_return[:7]

    print ""
    print "compute_daily_returns(df_port_value)[:7]"
    print compute_daily_returns(df_port_value)[:7]


if __name__ == "__main__":
    test_run()
