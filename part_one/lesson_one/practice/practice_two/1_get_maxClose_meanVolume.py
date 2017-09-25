"""
imports
get symbol
max close
mean volume

implement


"""
from pprint import pprint
import pandas as pd
from os import listdir
from os.path import isfile, join


PATH = "../../../../ml4t/data/"


def get_symbol_name(mypath):
    only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return only_files


def read_csv(symbol):
    return pd.read_csv("{}{}.csv".format(PATH, symbol))


def max_close(symbol):
    df = read_csv(symbol)
    get_max = df["Close"].max()
    return {symbol: float(get_max)}


def mean_volume(symbol):
    df = read_csv(symbol)
    get_mean = df["Volume"].mean()
    return {symbol: float(get_mean)}


if __name__ == '__main__':
    symbol = ["SPY"]
    get_max_close = {"Max Close": [max_close(s) for s in symbol]}
    get_mean_volume = {"Mean Volume": [mean_volume(s) for s in symbol]}
    combination = reduce(lambda x, y: dict(x, **y), (get_max_close, get_mean_volume))
    print combination
