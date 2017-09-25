import os
import pandas as pd
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir=os.path.join("../../../ml4t", "data")):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates, addSPY=True):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()


########### New INFO #############


def compute_daily_returns(df):
    """Compute and return the daily return values"""
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.ix[0, :] = 0 # set daily returns for row 0
    return daily_returns


def test_run():
    # read data
    sd, ed = "2009-01-01", "2012-12-31"
    dates = pd.date_range(sd, ed)
    symbols = ["SPY"]
    df = get_data(symbols, dates)

    # Compute daily returns
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")

    # Plot a histogram
    daily_returns.hist(bins=20) # changing no. of bins to 20

    # Get mean and standard deviation
    mean = daily_returns["SPY"].mean()
    std = daily_returns["SPY"].std()
    plt.axvline(mean, color="w", linestyle="dashed", linewidth=2)
    plt.axvline(std, color="r", linestyle="dashed", linewidth=2)
    plt.axvline(-std, color="r", linestyle="dashed", linewidth=2)
    plt.show()

    # Compute Kurtosis
    return daily_returns.kurtosis()


if __name__ == '__main__':
    print test_run()
