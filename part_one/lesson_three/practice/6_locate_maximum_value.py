import numpy as np


def test_run():
    a = np.array([50,6,2,3,12,14,7,10], dtype=np.int32)
    print a
    print a.size
    print a.max()
    print a.shape

    print a.argmax()


if __name__ == '__main__':
    test_run()
