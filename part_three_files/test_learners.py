
import time
import numpy as np
import math
import LinRegLearner as lrl
import RTLearner as rtl
import BagLearner as bgl
import KNNLearner as knn
import sys


if __name__=="__main__":
    now = time.time()
    try:
        inf = open('Data/Istanbul.csv')
        data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
    except ValueError:
        inf = open('Data/Istanbul.csv')
        data = np.array([map(float,s.strip().split(',')[1:]) for s in inf.readlines()[1:]])

    # compute how much of the data is training and testing
    train_rows = math.floor(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]

    print testX.shape
    print testY.shape

    # create a learner and train it
    #
    #
    #
    #
    #
    #
    # EDIT HERE
    learner = rtl.RTLearner(1)
    # learner = bgl.BagLearner(learner=rtl.RTLearner, kwargs={'leaf_size': 1}, bags=50, verbose=False)
    # learner = bgl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=10, boost=False, verbose=False)
    learner.addEvidence(trainX, trainY)
    # EDIT HERE
    #
    #
    #
    #
    #
    # evaluate in sample
    predY = learner.query(trainX) # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    # evaluate out of sample

    predY = learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]
    later = time.time()
    print "DURATION IN FLOATS", float(later - now)
