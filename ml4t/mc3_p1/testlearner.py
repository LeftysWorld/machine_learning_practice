import LinRegLearner as lrl
import KNNLearner as knn
import RTLearner as rtl
import BagLearner as bgl

import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time


def unison_shuffle(a, b):
    p = np.random.permutation(len(a))
    return a[p], b[p]


def run():
    try:
        inf = open('Data/Istanbul.csv')
        data = np.array([map(float, s.strip().split(',')) for s in inf.readlines()])
    except ValueError:
        inf = open('Data/Istanbul.csv')
        data = np.array([map(float, s.strip().split(',')[1:]) for s in inf.readlines()[1:]])

    indexes = []
    df = pd.DataFrame()
    test_cs = []
    train_cs = []

    for i in range(1, 11):
        # Training Setup
        train_rows = math.floor(0.6 * data.shape[0])
        test_rows = data.shape[0] - train_rows
        trainX = data[:train_rows, 0:-1]
        trainY = data[:train_rows, -1]
        TRAINX, TRAINY = unison_shuffle(trainX, trainY)

        # Testing Setup
        testX = data[test_rows:, 0:-1]
        testY = data[test_rows:, -1]
        TESTX, TESTY = unison_shuffle(testX, testY)

        # Add Learner
        # learner = lrl.LinRegLearner()
        # learner = knn.KNNLearner(k=3)
        # learner = rtl.RTLearner(i)
        # learner = bgl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=10, boost=False, verbose=False)
        # learner = bgl.BagLearner(learner=knn.KNNLearner, kwargs={'k': 3}, bags=10, boost=False, verbose=False)
        learner = bgl.BagLearner(learner=rtl.RTLearner, kwargs={'leaf_size': 5}, bags=i, verbose=False)

        learner.addEvidence(TRAINX, TRAINY)

        # evaluate in sample
        predY = learner.query(TRAINX)  # get the predictions
        rmse = math.sqrt(((TRAINY - predY) ** 2).sum() / TRAINY.shape[0])
        print
        print "In sample results"
        print "RMSE: ", rmse
        c = np.corrcoef(predY, y=TRAINY)
        print "corr: ", c[0, 1]
        train_cs.append(rmse)

        predY = learner.query(TESTX)  # get the predictions
        rmse = math.sqrt(((TESTY - predY) ** 2).sum() / TESTY.shape[0])
        print
        print "Out of sample results"
        print "RMSE: ", rmse
        c = np.corrcoef(predY, y=TESTY)
        print "corr: ", c[0, 1]
        indexes.append(i)
        test_cs.append(rmse)

    df['Bags'] = indexes
    df['Out of sample corr'] = test_cs
    df['In sample corr'] = train_cs
    df = df.set_index('Bags')
    plt.clf()
    ax = df.plot(title='RMSE in & out vs. bags for BagLearner(leaf_size=26)')
    ax.set_xlabel('ticks')
    ax.set_ylabel('RMSE')
    # plt.savefig('RMSE in & out vs. bags for BagLearner(leaf_size=15)', format='pdf')
    plt.show()


if __name__=="__main__":
    now = time.time()
    run()
    later = time.time()
    print "DURATION IN FLOATS", float(later - now)