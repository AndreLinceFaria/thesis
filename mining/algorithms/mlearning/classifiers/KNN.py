from settings import *
from mining.algorithms.mlearning.classifiers.Classifier import Classifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor


class KNN(Classifier):
    def __init__(self, fname=KNN_FNAME, n_neighbours = KNN_NEIGHBOURS_COUNT):
        self.n_neighbours = n_neighbours
        super(KNN, self).__init__(name=KNN_NAME,initials=KNN_INITIALS)
        if fname!=None:
            super(KNN,self).load(fname)
        else:
            self.create()

    def create(self):
        self.clf = KNeighborsClassifier(n_neighbors=self.n_neighbours,weights='distance',algorithm='auto')