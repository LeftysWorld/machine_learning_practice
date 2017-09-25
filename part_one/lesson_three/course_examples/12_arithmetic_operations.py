import numpy as np


def test_run():
    a = np.array([(1,2,3,4,5), (10,20,30,40,50)])
    print "Original array: ", a

    # # Multiply a by 2
    # print "\nMultiply a by 2: ", 2*a

    # # Divide a by 2
    # print "\nDivide a by 2: ", a / 2

    b = np.array([(100,200,300,400,500), (1,2,3,4,5)])
    print "\nOriginal array b: ", b

    # Add the two arrays
    print "\nAdd a + b:\n ", a + b

if __name__ == "__main__":
    test_run()
