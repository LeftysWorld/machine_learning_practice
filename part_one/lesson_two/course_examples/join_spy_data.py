import pandas as pd


def test_run():
    # Define date range
    start_date = "2010-01-22"
    end_date = "2010-01-26"
    dates = pd.date_range(start_date, end_date)

    # Create an empty dataframe
    df1 = pd.DataFrame(index=dates)

    # Read SPY data into temporary dataframe, and uses the date column in SPY to merge
    dfSPY = pd.read_csv("../../ml4t/data/SPY.csv",
                        index_col="Date", parse_dates=True,
                        usecols=["Date", "Adj Close"], na_values=["nan"])

    """
    # Left join the two dataframes using DataFrame.join()
    # if left join a and b, where a = a.join(b), it will retain all rows from a, but only the equivalent rows in b
    df1 = df1.join(dfSPY)

    # Drop NaN Values
    df1 = df1.dropna()
    print df1
    """

    # the above left join and drop NaN Values can be accomplished in one step using "how"
    # We only want dates that are in both sets. if not, we drop them
    df1 = df1.join(dfSPY, how="inner")
    print df1
    # print dfSPY


if __name__ == "__main__":
    test_run()
