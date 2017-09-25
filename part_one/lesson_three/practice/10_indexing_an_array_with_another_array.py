import numpy as np


def test_run():
    a = np.random.random(5)
    print a

    print ""
    indices = np.array([1,2,3,4,4])
    print indices

    print a[indices]



if __name__ == '__main__':
    test_run()
