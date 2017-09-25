import numpy as np


def random():
    return np.random.random((5,4))


def random_no_tuple():
    return np.random.rand(5,4)


def gaussian_distribution():
    return np.random.normal(50, 10, size=(2,3))


if __name__ == '__main__':
    # print random()
    # print random_no_tuple()
    print gaussian_distribution()

