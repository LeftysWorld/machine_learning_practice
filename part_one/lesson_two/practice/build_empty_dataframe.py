import pandas as pd


def test_run():
    sd = "01-01-2010"
    ed = "01-31-2013"
    data = {"col1": "dates", "col2": "picles"}
    dates = pd.date_range(sd, ed)
    df1 = pd.DataFrame(data, dates)
    return df1


if __name__ == "__main__":
    print test_run()
