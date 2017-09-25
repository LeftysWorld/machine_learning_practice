import numpy as np


def test_run():
    a = np.array([(20,25,10,23,26,32,10,5,0),(0,2,50,20,0,1,28,5,0)])
    b = np.array([(20, 25, 10, 23, 26, 32, 10, 5, 0), (0, 2, 50, 20, 0, 1, 28, 5, 0)])
    print a

    # Calculate mean
    meana = a.mean()
    print meana

    # Calculate mean
    meanb = b.mean()
    print meanb

    # Masking 1
    print a[a<meana]
    
    # Masking 2
    b[b<meanb]= meanb
    print b


if __name__ == "__main__":
    test_run()
