import pandas as pd


def test_run(symbol):
    df = pd.read_csv("../../ml4t/data/{}.csv".format(symbol))
    symbol_name = symbol
    print symbol_name, df


if __name__ == "__main__":
    symbols = ["AAPL"]
    for s in symbols:
        test_run(s)
