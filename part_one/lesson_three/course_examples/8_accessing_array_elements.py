import numpy as np


def test_run():
    a = np.random.rand(5, 4)
    print a

    # # Accessing element at position (3, 2)
    # element = a[3, 2]
    # print element
    #
    # # Elements in defined range
    # print a[0, 1:3]
    #
    # # Top-Left corner
    # print a[0:2, 0:2]

    # Slicing
    # Note: Slice n:n:t specifies a range that starts at n, and stops before m, in..
    print " "
    print a[1:, 0:3:2] # will select columns 0, 2 for every row


if __name__ == "__main__":
    test_run()
