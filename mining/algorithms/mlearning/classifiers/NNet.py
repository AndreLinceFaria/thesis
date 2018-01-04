from settings import *
from sklearn.neural_network import MLPClassifier
from mining.algorithms.mlearning.classifiers.Classifier import Classifier

class NNet(Classifier):
    def __init__(self, fname=None):
        super(NNet, self).__init__(name=NN_NAME,initials=NN_INITIALS)
        if fname!=None:
            super(NNet,self).load(fname)
        else:
            self.create()

    def create(self):
        self.clf = MLPClassifier(solver=NN_SOLVER,
                                 alpha=NN_ALPHA,
                                 hidden_layer_sizes=NN_HIDDEN_LAYERS_SIZE,
                                 random_state=NN_RANDOM_STATE,
                                 activation=NN_ACTIVATION)
