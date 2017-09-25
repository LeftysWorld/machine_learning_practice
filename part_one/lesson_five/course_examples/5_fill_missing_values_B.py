import pandas as pd
import matplotlib.pyplot as plt
import os


def symbol_to_path(symbol, base_dir="../../../ml4t/data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbollist, dates):
    df_final = pd.DataFrame(index=dates)
    if "SPY" not in symbollist:
        symbollist.insert(0, "SPY")

    for symbol in symbollist:
        file_path = symbol_to_path(symbol)
        df_temp = pd.read_csv(file_path, parse_dates=True, index_col="Date",
            usecols=["Date", "Adj Close"], na_values=["nan"])
        df_temp = df_temp.rename(columns={"Adj Close": symbol})
        df_final = df_final.join(df_temp)
        if symbol == "SPY":
            df_final = df_final.dropna(subset=["SPY"])

    return df_final


def plot_data(df_data):
    ax = df_data.plot(title="Stock Data", fontsize=2)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    plt.show()


def fill_missing_values(df_data):
    # front_fill = df_data.fillna(method="ffill", inplace=True)
    back_fill = df_data.fillna(method="bfill", inplace=True)
    return back_fill


def test_run():
    # Read data
    symbollist = ["JAVA", "FAKE1", "FAKE2"]
    sd, ed = "2005-12-31", "2014-12-07"
    dates = pd.date_range(sd, ed)
    df_data = get_data(symbollist, dates)

    # Forward and Backward fill
    fill_missing_values(df_data)

    # Plot
    plot_data(df_data)


if __name__ == "__main__":
    test_run()
