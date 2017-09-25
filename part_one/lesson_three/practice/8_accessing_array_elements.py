import numpy as np


def test_run():
    a = np.random.random((5,4))
    print a

    # elem = a[3,2]
    # print elem
    #
    # elem_range = a[0, 1:3]
    # print elem_range
    #
    # corner = a[0:2, 0:2]
    # print corner

    slicing = a[:, 0:3:2]
    print slicing


if __name__ == '__main__':
    test_run()
