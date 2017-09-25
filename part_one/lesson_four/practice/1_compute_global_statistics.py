import os
import pandas as pd
import matplotlib.pyplot as plt


PATH = "../../../ml4t/data"


def symbol_to_path(symbol, base_dir=PATH):
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbollist, dates):
    df = pd.DataFrame(index=dates)
    symbollist = ["SPY"] + symbollist if "SPY" not in symbollist else symbollist

    for symbol in symbollist:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col="Date", parse_dates=True,
                              usecols=["Date", "Adj Close"], na_values=["nan"])
        df_temp = df_temp.rename(columns={"Adj Close": symbol})
        df = df.join(df_temp)
        df = df.dropna(subset=["SPY"]) if symbol == "SPY" else df
    return df


def test_run():
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    sd, ed = "01-01-2010", "12-31-2010"
    dates = pd.date_range(sd, ed)
    df = get_data(symbols, dates)
    df = df[:7]

    print "mean:\n", df.mean()
    print ""
    print "median:\n", df.median()
    print ""
    print "sd:\n", df.std()


if __name__ == '__main__':
    test_run()
