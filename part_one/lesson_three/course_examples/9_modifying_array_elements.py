import numpy as np


def test_run():
    a = np.random.rand(5, 4)
    print "Array: ", a

    # # Assigning a single value to an entire row
    # a[0, :] = 2
    # print "\nModified (replaced a row with a single value:\n", a

    # Assigning a list to a column in an array
    a[:, 3] = [1, 2, 3, 4, 5]
    print "\nModified (replaced a column with a list):\n", a


if __name__ == "__main__":
    test_run()
