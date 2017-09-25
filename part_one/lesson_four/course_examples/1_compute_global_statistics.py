import os
import pandas as pd
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir="../../../ml4t/data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    df = pd.DataFrame(index=dates)
    if "SPY" not in symbols:
        symbols.insert(0, "SPY")

    for s in symbols:
        df_temp = pd.read_csv(symbol_to_path(s), index_col='Date',
                              parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={"Adj Close":s})
        df = df.join(df_temp)
        if s == "SPY":
            df = df.dropna(subset=["SPY"])
    return df


def plot_data(df, title="Stock Prices"):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def plot_selected(df, columns, start_index, end_index):
    plot_data(df.ix[start_index:end_index, columns], title="Selected Data")


def test_run():
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    dates = pd.date_range('2010-01-01', '2010-12-31')
    df = get_data(symbols, dates)
    plot_selected(df, symbols, '2010-01-01', '2010-12-31')

    # Compute global statistics for each stock
    print df.mean()
    print df.median()
    print df.std()


if __name__ == "__main__":
    print test_run()
