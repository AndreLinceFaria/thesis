from mining.algorithms.mlearning.classifiers.Classifier import Classifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB

class NBayes(Classifier):
    def __init__(self, fname=None):
        super(NBayes, self).__init__(name='Naive Bayes')
        if fname!=None:
            super(NBayes,self).load(fname)
        else:
            self.create()

    def create(self):
        self.clf = GaussianNB()
