import pandas as pd


def get_mean_volume(symbol):
    df = pd.read_csv("../ml4t/data/{}.csv".format(symbol))
    res = df["Volume"].mean()
    return res


if __name__ == "__main__":
    symbol = ["AAPL", "IBM"]
    for s in symbol:
        print "Mean Volume for {0} is {1}".format(s, get_mean_volume(s))
