import numpy as np


def test_run():
    np.random.seed(693)
    a = np.random.randint(0,10,size=(5,4))
    print a
    print a.sum()
    print a.sum(axis=0)
    print a.sum(axis=1)
    print a.min()
    print a.mean()


if __name__ == '__main__':
    test_run()
