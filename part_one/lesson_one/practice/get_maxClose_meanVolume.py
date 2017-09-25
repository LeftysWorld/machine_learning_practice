from pprint import pprint
import pandas as pd
from os import listdir
from os.path import isfile, join

PATH = "../../../ml4t/data/"


def get_symbol_name(mypath):
    only_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return only_files


def get_max_close(symbol):
    df = pd.read_csv("{0}{1}".format(PATH, symbol))
    get_max = df["Close"].max()
    get_max_dict = {symbol: float(get_max)}
    return get_max_dict


def get_mean_volume(symbol):
    df = pd.read_csv("{0}{1}".format(PATH, symbol))
    get_mean = df["Volume"].mean()
    get_mean_dict = {symbol: float(get_mean)}
    return get_mean_dict


if __name__ == "__main__":
    symbols = get_symbol_name(PATH)
    max_close = {"Max Close": [get_max_close(s) for s in symbols[:10]]}
    mean_volume = {"Mean Volume": [get_mean_volume(s) for s in symbols[:10]]}
    combination = reduce(lambda x,y: dict(x, **y), (max_close, mean_volume))
    pprint(combination)