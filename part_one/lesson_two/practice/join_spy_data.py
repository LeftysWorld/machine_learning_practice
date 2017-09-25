import pandas as pd


def test_run_one():
    sd = "01-01-2010"
    ed = "01-31-2012"
    date = pd.date_range(sd, ed)
    data = {"col1": "dates", "col2": "picles"}
    df1 = pd.DataFrame(data, date)
    dfSPY = pd.read_csv("../../ml4t/data/SPY.csv",
                        index_col="Date", parse_dates=True,
                        usecols=["Date", "Adj Close"], na_values=["nan"])
    df1 = df1.join(dfSPY)
    df1 = df1.dropna()
    return df1[:7]


def test_run_two():
    sd = "01-01-2010"
    ed = "01-31-2012"
    date = pd.date_range(sd, ed)
    df1 = pd.DataFrame(None, date)
    dfSPY = pd.read_csv("../../ml4t/data/SPY.csv",
                        index_col="Date", parse_dates=True,
                        usecols=["Date", "Adj Close"], na_values=["nan"])
    df1 = df1.join(dfSPY, how="inner")
    return df1[:7]


def test_run_three():
    date = pd.date_range("01-01-2010", "01-31-2010")
    df1 = pd.DataFrame(data=None, index=date)
    dfSPY = pd.read_csv("../../ml4t/data/SPY.csv", index_col="Date", parse_dates=True,
                        usecols=["Date", "Adj Close"], na_values=["nan"])
    df1 = df1.join(dfSPY, how="inner")
    return df1[:7]


def test_run_four():
    sd, ed = "01-01-2010", "01-31-2010"
    date = pd.date_range(sd, ed)
    df1 = pd.DataFrame(data=None, index=date)
    dfSPY = pd.read_csv("../../ml4t/data/SPY.csv", index_col="Date", parse_dates=True,
                        usecols=["Date", "Adj Close"], na_values=["nan"])
    df1 = df1.join(dfSPY, how="inner")
    return df1[:7]


def test_run_five():
    sd, ed = "01-01-2010", "01-31-2010"
    dates = pd.date_range(sd, ed)
    df1 = pd.DataFrame(None, dates)
    dfSPY = pd.read_csv("../../ml4t/data/SPY.csv", index_col="Date", parse_dates=True,
                        usecols=["Date", "Adj Close"], na_values=["nan"])
    df2 = df1.join(dfSPY, how="inner")
    return df2[:7]


if __name__ == "__main__":
    # print test_run_one()
    # print test_run_two()
    # print test_run_three()
    # print test_run_four()
    print test_run_five()