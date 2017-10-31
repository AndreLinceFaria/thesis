from sklearn.neural_network import MLPClassifier
from mining.algorithms.mlearning.classifiers.Classifier import Classifier

class NNet(Classifier):
    def __init__(self, fname=None):
        super(NNet, self).__init__(name='Multi-Layer Perceptron')
        if fname!=None:
            super(NNet,self).load(fname)
        else:
            self.create()

    def create(self):
        self.clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5,2), random_state=0)
