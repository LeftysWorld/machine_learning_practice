import numpy as np
import random


class RTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        if verbose:
            verbose = False
        self.verbose = verbose
        self.tree = None
        self.leaf = -1000

    def addEvidence(self, Xdata, Ydata):
        def get_split_val(X, feature):
            return np.mean(np.random.choice(X[:, feature], size=2, replace=False))

        def get_random_feature(X):
            return random.sample(xrange(0, X.shape[1]), X.shape[1])

        def get_indices(data, feature, split_value):
            left_index = data[:, feature] <= split_value
            right_index = data[:, feature] > split_value
            return left_index, right_index

        def build_tree(_Xdata, dataY):
            if _Xdata.shape[0] <= self.leaf_size:
                self.tree = np.asarray([[self.leaf, np.mean(dataY), np.nan, np.nan]])
                return self.tree
            if len(set(dataY)) == 1:
                self.tree = np.array([[self.leaf, np.mean(dataY), np.nan, np.nan]])
                return self.tree

            random_feature = get_random_feature(_Xdata)
            feature = random_feature[0]
            counter = 1

            while len(set(_Xdata[:, feature])) == 1 and counter <= _Xdata.shape[1]:
                random_feature = get_random_feature(_Xdata)
                feature = random_feature[counter]
                counter += 1

            if len(set(_Xdata[:, feature])) == 1:
                self.tree = [[self.leaf, np.mean(dataY), np.nan, np.nan]]
                return self.tree
            else:
                split_val = get_split_val(_Xdata, feature)
                while split_val == np.amax(_Xdata[:, feature]):
                    split_val = get_split_val(_Xdata, feature)

                left_index, right_index = get_indices(_Xdata, feature, split_val)
                left_tree = build_tree(_Xdata[left_index], dataY[left_index])
                right_tree = build_tree(_Xdata[right_index], dataY[right_index])
                root = [feature, split_val, 1, len(left_tree) + 1]
                self.tree = np.concatenate(([root], left_tree, right_tree), axis=0)
                return self.tree

        return build_tree(Xdata, Ydata)

    def query(self, points):
        counter = 0
        results = np.empty(len(points))
        branch = np.zeros(points.shape[0])
        while counter < len(self.tree):
            if self.tree[counter, 0] != self.leaf:
                val = np.array(np.where(branch == counter))
                split = np.array(points[val, int(self.tree[counter, 0])] <= self.tree[counter, 1])
                branch[val[np.where(split == True)]] = 1 + counter
                branch[val[np.where(split == False)]] = self.tree[counter, 3] + counter
            else:
                results[np.where(branch == counter)] = self.tree[counter, 1]
            counter += 1
        return results
