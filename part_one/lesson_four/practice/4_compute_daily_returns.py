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


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()


def compute_daily_returns(df):
    daily_returns = (df / df.shift(1)) -1
    daily_returns.ix[0, :] = 0
    return daily_returns


def compute_cumulative_returns(df):
    cr = (df / df.ix[0]) - 1
    return cr


def test_run():
    # Read data
    symbols = ['SPY', "XOM"]
    sd, ed = "2012-07-01", "2012-07-31"
    dates = pd.date_range(sd, ed)
    df = get_data(symbols, dates)

    # Compute daily returns
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")
    print daily_returns

    print ""

    # Compute cum returns
    cr = compute_cumulative_returns(df)
    plot_data(cr, title="Cum returns", ylabel="Daily returns")
    print cr


if __name__ == '__main__':
    test_run()
