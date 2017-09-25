import pandas as pd


def get_max_close_price(symbol):
    """
    Return the maximum closing value for a stock indicated by symbol
    """
    df = pd.read_csv("../ml4t/data/{}.csv".format(symbol))
    return df["Close"].max()


if __name__ == "__main__":
    symbol = ["AAPL", "IBM"]
    for s in symbol:
        print "Max Close for: {0} = {1}".format(s, get_max_close_price(s))
