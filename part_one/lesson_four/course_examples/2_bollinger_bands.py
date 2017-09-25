import os
import pandas as pd
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir="../../ml4t/data"):
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
    sd, ed = '2010-01-01', '2010-12-31'
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    dates = pd.date_range(sd, ed)
    df = get_data(symbols, dates)
    # plot_selected(df, symbols, sd, ed)

    # Plot SPY data, retain matplotlib axis object
    ax = df['SPY'].plot(title="SPY rolling mean", label="SPY")

    # Compute rolling mean using a 20-day window
    rm_SPY = pd.rolling_mean(df["SPY"], window=20)

    # Add rolling mean to same plot
    rm_SPY.plot(label="Rolling mean", ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    plt.show()


if __name__ == "__main__":
    print test_run()
