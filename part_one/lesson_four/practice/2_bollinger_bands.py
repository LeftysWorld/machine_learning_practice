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


def plot_data(df, title="Stock Prices"):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def plot_selected(df, columns, start_index, end_index):
    plot_data(df.ix[start_index:end_index, columns], title="Selected Data")


def test_run():
    symbols = ['SPY', 'XOM', 'GOOG', 'GLD']
    sd, ed = "01-01-2010", "12-31-2010"
    dates = pd.date_range(sd, ed)
    df = get_data(symbols, dates)

    # Plot
    ax = df['SPY'].plot(title="SPY rolling mean", label="SPY")

    # Rolling Mean
    rm_SPY = df["SPY"].rolling(window=20,center=False).mean() # New Version of Rolling
    # rm_SPY = pd.rolling_mean(df["SPY"], window=20)          # Depreciated Version of Rolling
    rm_SPY.plot(label="Rolling Mean", ax=ax)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    plt.show()


if __name__ == '__main__':
    test_run()
