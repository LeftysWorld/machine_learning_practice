import numpy as np


def test_run_empty_array():
    # Empty array
    print np.empty(5)
    print np.empty((5, 4))


def test_run_ones():
    # Array of 1s
    print np.ones((5, 4))


def test_run_specifying_the_datatype():
    # Specifying the datatype
    print np.ones((5, 4), dtype=np.int_)


if __name__ == "__main__":
    # test_run_empty_array()
    # test_run_ones()
    test_run_specifying_the_datatype()