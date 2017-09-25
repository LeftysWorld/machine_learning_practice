import pandas as pd


def test_run():
    start_date = "2010-01-22"
    end_date = "2010-01-26"
    dates = pd.date_range(start_date, end_date)
    df1 = pd.DataFrame(index=dates)
    print df1


def test_run_one():
    start_date = "2010-01-22"
    end_date = "2010-01-26"
    dates = pd.date_range(start_date, end_date)
    print dates[0]


if __name__ == "__main__":
    test_run()
    # test_run_one()
