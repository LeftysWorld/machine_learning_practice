import numpy as np


def test_run():
    a = np.random.random((5,4))
    print a

    print ""
    a[0, :] = 2
    print a

    print ""
    a[:, 3] = [1,2,3,4,5]
    print a


if __name__ == '__main__':
    test_run()
