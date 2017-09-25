import pandas as pd

PATH = "../../../ml4t/data/"


def test_run(symbol):
    df = pd.read_csv("{}{}.csv".format(PATH, symbol))
    return df


if __name__ == "__main__":
    symbol = "IBM"
    print test_run(symbol)
