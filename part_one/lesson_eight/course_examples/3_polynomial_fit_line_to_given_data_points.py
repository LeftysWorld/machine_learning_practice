import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as spo


# Line is a tuple (C0, C1)
def error_poly(C, data):
    """Compute error between given polynomial and observed data.

    Parameters
    ----------
    C: numpy.poly1d object orequivalent array representing polynomial coefficients
    data: 2D array where each row is a point (x, y)

    Returns error as a single real value.
    """
    # Metric: Sum of squared Y-axis differences
    err = np.sum((data[:, 1] - np.polyval(C, data[:, 0])) ** 2)
    return err


def fit_poly(data, error_func, degree=3):
    """Fit a polynomial to given data, using supplied error function.

    Parameters
    ----------
    data: 2D array where each row is a point (x, y)
    error_func: function that computes the error between a polynomial

    Returns polynomial that minimizes the error function.
    """
    # Generate initial guess for polynomial model (all coeffs = 1)
    Cguess = np.poly1d(np.ones(degree + 1, dtype=np.float32))

    # Plot initial guess (optional)
    x = np.linspace(-5, 5, 21)
    plt.plot(x, np.polyval(Cguess, x), "m--", linewidth=2.0, label="Initial guess")

    # Call optimizer to minimize error function
    result = spo.minimize(error_func, Cguess, args=(data,), method="SLQP", options={"disp": True}).x
    return np.poly1d(result.x) # convert optimal result into a poly1d object


def test_run():
    original = np.float32([4, 2])
    print "Original line: C0 = {}, C1".format(original[0], original[1])
    Xoriginal = np.linspace(0, 10, 40)
    Yoriginal = original[0] * Xoriginal + original[1]
    plt.plot(Xoriginal,Yoriginal, "b--", linewidth=2.0, label="Original Line")

    # add some random noise to the data
    noise_sigma = 4.0
    noise = np.random.normal(0, noise_sigma, Yoriginal.shape)
    data = np.asarray([Xoriginal, Yoriginal + noise]).T
    plt.plot(data[:, 0], data[: ,1], "go", label="Data points")

    l_fit = fit_poly(data, error)
    print "Fitted line: C0 = {}, C1 = {}".format(l_fit[0], l_fit[1])
    plt.plot(data[:,0], l_fit[0] * data[:, 0] + l_fit[1], "r--", linewidth=2.0, label="Fitted line")
    plt.legend(loc="upper right")
    plt.show()


if __name__ == '__main__':
    test_run()
