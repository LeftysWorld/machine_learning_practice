import pandas as pd
import matplotlib.pyplot as plt


def test_run(symbol):
    df = pd.read_csv("../ml4t/data/{}.csv".format(symbol))
    print df['Adj Close']
    df["Adj Close"].plot()
    plt.show()


if __name__ == "__main__":
    symbol = ["AAPL"]
    for s in symbol:
        test_run(s)
