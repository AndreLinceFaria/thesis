from settings import *
from mining.algorithms.mlearning.classifiers.Classifier import Classifier
from sklearn.naive_bayes import MultinomialNB

class NBayes(Classifier):
    def __init__(self, fname=NB_FNAME):
        super(NBayes, self).__init__(name=NB_NAME,initials=NB_INITIALS)
        if fname!=None:
            super(NBayes,self).load(fname)
        else:
            self.create()

    def create(self):
        self.clf = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
