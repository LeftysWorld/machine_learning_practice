import pandas as pd
import matplotlib.pyplot as plt


def test_run(symbol):
    df = pd.read_csv("../ml4t/data/{}.csv".format(symbol))
    print df["High"]
    df["High"].plot()
    plt.show()


if __name__ == "__main__":
    symbol = ["IBM"]
    for s in symbol:
        test_run(s)
