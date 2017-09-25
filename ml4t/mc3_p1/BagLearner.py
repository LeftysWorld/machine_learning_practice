import numpy as np
import random


class BagLearner(object):
    def __init__(self, learner, kwargs=None, bags=2, boost=False, verbose=False):
        self.learners = [learner(**kwargs) for _ in range(bags)]
        self.bags = bags
        self.boost = boost
        self.verbose = verbose

    def author(self):
        return 'Leftysworld'

    def addEvidence(self, dataX, dataY):
        for i in range(self.bags):
            get_rand_row_data = [random.randrange(len(dataX)) for _ in range(len(dataX))]
            data_x, data_y = (lambda x, y: (x[get_rand_row_data], y[get_rand_row_data]))(dataX, dataY)
            self.learners[i].addEvidence(data_x, data_y)

    def query(self, points):
        # res = ["Bagging.{}...".format(i) for i in range(self.bags)]
        # for i in res:
        #     print i

        predict_y = [self.learners[i].query(points) for i in range(self.bags)]
        return np.mean(predict_y, axis=0)
