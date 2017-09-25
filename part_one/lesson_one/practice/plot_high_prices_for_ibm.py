import pandas as pd
import matplotlib.pyplot as plt


def test_run(symbol):
    df = pd.read_csv("../../../ml4t/data/{}.csv".format(symbol))
    high = df["High"]
    print high
    high.plot()
    plt.show()


if __name__ == "__main__":
    symbol = "IBM"
    print test_run(symbol)
