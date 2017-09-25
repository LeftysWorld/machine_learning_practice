import numpy as np
import KNNLearner as knn
import math
import LinRegLearner as lr

class BagLearner():

    def __init__(self, learner, bags, kwargs=None, boost=False):
        self.learner = learner
        if learner == knn.KNNLearner:
            if kwargs['k'] <= 0:
                raise ValueError('K must be > 0')
            else:
                self.kwargs = kwargs['k']
        else:
            self.kwargs = kwargs
        self.bags = bags
        self.boost = boost

    def addEvidence(self, Xtrain, Ytrain):
        self.Xtrain = Xtrain
        self.Ytrain = Ytrain

    def query(self, Xtest):

        learners = []
        #bag_size = math.floor(self.Xtrain.shape[0] * .6)
        bag_size = self.Xtrain.shape[0]
        Xtrain = np.zeros((bag_size, 2), dtype='float')
        Ytrain = np.zeros((bag_size, ), dtype='float')
        for i in range(self.bags):
            if self.kwargs:
                learner = self.learner(self.kwargs)
            else:
                learner = self.learner()

            rand_indexes = np.random.randint(0, self.Xtrain.shape[0], size=bag_size)

            j = 0
            for i in rand_indexes:
                Xtrain[j] = self.Xtrain[i, :]
                Ytrain[j] = self.Ytrain[i]
                j += 1

            learner.addEvidence(Xtrain, Ytrain)
            learners.append(learner.query(Xtest))
        result = sum(learners)/len(learners)
        return [float(i) for i in result]
