import numpy as np
from time import time


# Python
def test_run_python():
    t1 = time()
    print "ML4T"
    t2 = time()
    print "The time taken by print statement is ", t2-t1," seconds"


# Everything Below is Numpy
def how_long(func, *args):
    t0 = time()
    result = func(*args)
    t1 = time()
    return result, t1-t0


def manual_mean(arr):
    """Compute mean (average) of all elements in the given 2D array."""
    sum = 0
    for i in xrange(0, arr.shape[0]):
        for j in xrange(0, arr.shape[1]):
            sum = sum + arr[i, j]
    return sum / arr.size


def numpy_mean(arr):
    """Compute mean (average) using NumPy."""
    return arr.mean()


def test_run_numpy():
    """Function called by Test Run Numpy"""
    nd1 = np.random.random((1000, 1000)) # use a sufficiently large array

    # Time the two functions, retrieving results and execution times
    res_manual, t_manual = how_long(manual_mean, nd1)
    res_numpy, t_numpy = how_long(numpy_mean, nd1)

    #FIX
    print "Manual: {:.6f} ({:.3f} secs.) vs. NumPy: {:.6f} ({:.3f} secs.)".format(res_manual, res_numpy, res_manual, res_manual) # FIX

    # Make sure both give us the same answer (upto some precision)
    assert abs(res_manual - res_numpy) <= 10e-6, "Results aren't equal!"

    # Compute speedup
    speedup = t_manual / t_numpy
    print "NumPy mean is", speedup, "times faster than manual for loops."


if __name__ == "__main__":
    # test_run_python()
    test_run_numpy()
