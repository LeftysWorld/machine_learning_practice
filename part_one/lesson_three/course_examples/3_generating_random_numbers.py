import numpy as np


def test_run_simple():
    # Generate an array full of random numbers, uniformly sampled from [0.0, 1.0]
    print np.random.random((5, 4)) # pass in a size tuple


def test_run_arguments():
    # Generate an array full of random numbers, uniformly sampled from [0.0, 1.0]
    print np.random.rand(5, 4) # function arguments (not a tuple)


def test_run_gaussian_distribution():
    # Sample numbers from a Gaussian (normal) distribution
    # print np.random.normal(size=(2, 3)) # "standard normal" (mean = 0, s.d. = 1)
    print np.random.normal(50, 10, size=(2, 3)) # change mean to 50 and s.d. to 10


def test_run_random_integers():
    # Random integers
    print np.random.randint(10) # a single integer in  [0, 10)
    print np.random.randint(0, 10)  # same as above, specifying [low, high) explicitly
    print np.random.randint(0, 10, size=5) # 5 random integers as a 1D array
    print np.random.randint(0, 10, size=(2, 3)) # 2x3 array of random integers


if __name__ == "__main__":
    # test_run_simple()
    # test_run_arguments()
    # test_run_gaussian_distribution()
    test_run_random_integers()