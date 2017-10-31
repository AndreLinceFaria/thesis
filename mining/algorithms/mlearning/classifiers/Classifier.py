from mining.algorithms.mlearning import persist as p
from mining.algorithms.mlearning.classifiers import models_path

class Classifier(object):

    def __init__(self, name, desc='Not provided'):
        self.name = name
        self.desc = desc
        self.clf = None

    def load(self, fname):
        self.clf = p.load_model(models_path + fname)

    def create(self):
        pass

    def save(self, fname):
        p.save_model(self.clf, models_path + fname)

    def train(self, x_train, y_train):
        self.clf.fit(x_train, y_train)

    def test(self, x_test, y_test):
        return self.clf.score(x_test,y_test)

    def predict(self,X):
        return self.clf.predict(X)

    def predict_with_label(self, X, labels):
        pred = self.predict(X)
        return pred,labels[int(pred)]