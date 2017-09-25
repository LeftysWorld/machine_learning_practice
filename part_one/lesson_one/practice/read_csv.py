import pandas as pd


def test_run(symbol):
    df = pd.read_csv("../../../ml4t/data/{}.csv".format(symbol))
    print symbol, df


if __name__ == "__main__":
    symbol = ["AAPL"]
    for s in symbol:
        test_run(s)
