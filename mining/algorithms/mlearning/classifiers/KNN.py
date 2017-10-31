from mining.algorithms.mlearning.classifiers.Classifier import Classifier
from sklearn.neighbors import KNeighborsClassifier

class KNN(Classifier):
    def __init__(self, fname=None, n_neighbours = 25):
        self.n_neighbours = n_neighbours
        super(KNN, self).__init__(name='K-Nearest Neighbours')
        if fname!=None:
            super(KNN,self).load(fname)
        else:
            self.create()

    def create(self):
        self.clf = KNeighborsClassifier(self.n_neighbours)