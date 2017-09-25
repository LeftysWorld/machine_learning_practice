import numpy as np


class KNNLearner(object):
    def __init__(self, k):
        self.k = k

    def addEvidence(self,dataX,dataY):
        self.dataX = dataX
        self.dataY = dataY

    def query(self,points):
        def get_distance(instance1, instance2):
            distance = sum((instance1[_] - instance2[_]) ** 2 for _ in range(len(instance1)))
            return np.sqrt(distance)

        def get_neighbors(_dataX, _dataY, the_points, k):
            def sort_item_key(*items):
                res = lambda x: x[items[0]] if len(items) == 1 else lambda xx: tuple(xx(items[0] for _ in items))
                return res

            distances = [(dist, get_distance(the_points, _dataX[dist])) for dist in range(_dataX.shape[0])]
            distances.sort(key=sort_item_key(1))

            neighbors = [_dataY[distances[i][0]] for i in range(k)]
            for i in range(k):
                while distances[i + 1][1] == distances[i][1]:
                    neighbors += [_dataY[distances[i + 1][0]]]
                    i += 1
            return neighbors

        res = np.array([np.mean(get_neighbors(self.dataX, self.dataY, points[i], self.k)) for i in range(points.shape[0])])
        return res
