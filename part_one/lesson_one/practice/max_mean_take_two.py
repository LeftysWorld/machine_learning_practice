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
    max_close = df["Close"].max()
    return {"Max Close": float(max_close)}


def get_mean_volume(symbol):
    df = pd.read_csv("{0}{1}".format(PATH, symbol))
    mean_volume = df["Volume"].mean()
    return {"Mean Volume": float(mean_volume)}


if __name__ == "__main__":
    symbols = get_symbol_name(PATH)[:10]

    def create_dict(str, *func):
        string_to_replace = str.replace(".csv", "")
        dict = {string_to_replace: [f for f in func]}
        return dict

    all_data = [create_dict(s, get_max_close(s), get_mean_volume(s)) for s in symbols]
    res = reduce(lambda x,y: dict(x, **y), (all_data))
    pprint(res)
