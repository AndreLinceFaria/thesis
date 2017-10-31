from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from mining.algorithms.mlearning.classifiers.Classifier import Classifier

class SVM(Classifier):
    def __init__(self, fname=None, n_neighbours = 30):
        self.n_neighbours = n_neighbours
        super(SVM, self).__init__(name='Support Vector Machine')
        if fname!=None:
            super(SVM,self).load(fname)
        else:
            self.create()

    def create(self):
        self.clf = OneVsRestClassifier(SVC(random_state=0, kernel='rbf'))