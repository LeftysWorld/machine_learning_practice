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


def get_rolling_mean(df, window=20, center=False):
    return df.rolling(window=window, center=center).mean()


def get_rolling_std(df, window=20, center=False):
    return df.rolling(window=window, center=center).std()


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + rstd * 2
    lower_band = rm - rstd * 2
    return upper_band, lower_band


def test_run():
    # Read data
    symbols = ['SPY']
    sd, ed = "2012-01-01", "2012-12-31"
    dates = pd.date_range(sd, ed)
    df = get_data(symbols, dates)

    # Rolling Mean
    rm_SPY = get_rolling_mean(df['SPY'])

    # Rolling standard deviation
    rstd_SPY = get_rolling_std(df['SPY'])

    # Compute Upper and Lower Bollinger Bands
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)

    # Plot
    ax = df['SPY'].plot(title="Bollinger Bands", label='SPY')
    rm_SPY.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)

    # Axis info
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()


if __name__ == '__main__':
    test_run()
