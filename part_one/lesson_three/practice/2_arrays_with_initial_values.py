import numpy as np


def empty_array1():
    return np.empty(5)


def empty_array2():
    return np.empty((5,4))


def ones_array():
    return np.ones((5,4))


def ones_int_array():
    return np.ones((5,4), dtype=np.int_)


if __name__ == '__main__':
    # print empty_array1()
    # print empty_array2()
    print ones_array()
    print ones_int_array()
