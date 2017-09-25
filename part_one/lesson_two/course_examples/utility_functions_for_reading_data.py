import os
import pandas as pd


def symbol_to_path(symbol, base_dir="../../ml4t/data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files"""
    df = pd.DataFrame(index=dates)
    if "SPY" not in symbols:
        symbols.insert(0, "SPY")

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col="Date", parse_dates=True,
                              usecols=["Date", "Adj Close"], na_values=["nan"])
        df_temp = df_temp.rename(columns={"Adj Close": symbol})
        df = df.join(df_temp)
        if symbol == "SPY": # drop dates spy did not trade
            df = df.dropna(subset=["SPY"])
    return df


def test_run():
    # Define date range
    start_date = "2010-01-22"
    end_date = "2010-01-26"
    dates = pd.date_range(start_date, end_date)

    # Choose stock symbols to read
    symbols = ["GOOG", "IBM", "GLD"]

    # Get stock data
    df = get_data(symbols, dates)
    print df


if __name__ == "__main__":
    test_run()
