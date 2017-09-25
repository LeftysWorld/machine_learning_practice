import pandas as pd


def test_run(symbol):
    df = pd.read_csv("../ml4t/data/{}.csv".format(symbol))
    print df[10:21] #rows between index 10 and 20


if __name__ == "__main__":
    symbol = ["AAPL"]
    for s in symbol:
        test_run(s)
