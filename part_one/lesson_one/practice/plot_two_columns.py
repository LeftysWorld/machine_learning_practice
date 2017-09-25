import pandas as pd
import matplotlib.pyplot as plt


def test_run(symbol):
    df = pd.read_csv("../../../ml4t/data/{}.csv".format(symbol))
    lst = ["High", "Close", "Adj Close"]
    df[lst].plot()
    plt.show()


if __name__ == "__main__":
    symbol = "IBM"
    test_run(symbol)