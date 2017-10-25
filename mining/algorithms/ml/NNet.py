import os
from FeatureManager import FeatureManager
from sklearn.neural_network import MLPClassifier
import pickle

net_path = 'models/'

class NNet():
    def __init__(self, fm = FeatureManager(parties_json='parties-twitter.json'),
                 show=False,
                 data_size = 10000,
                 nr_features = None,
                 get_data = True):

                self.fm = fm
                self.show = show
                if get_data:
                    self.x_train, self.x_test, self.y_train, self.y_test = fm.get_dataset_test_train(data_size=data_size, nr_features=nr_features)
                self.net = self.create_net()

    def load_net(self, filename='NNet.pkl'):
        with open(net_path + filename, 'rb') as f:
            self.net = pickle.load(f)

    def save_net(self, filename='NNet.pkl'):
        with open(net_path + filename, 'wb') as f:
            pickle.dump(self.net, f)

    def create_net(self):
        if self.show:
            pass
            #print("Creating NNet classifier")
        return MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5,2), random_state=1)

    def train(self):
        self.net.fit(self.x_train, self.y_train)
        if self.show:
            print("Train Results: Success")

    def test(self):
        score = self.net.score(self.x_test,self.y_test)
        if self.show:
            print("Test Results (Score): " + str(score))
        return score

    def predict(self,X):
        return self.net.predict(X)

    def predict_with_label(self, X):
        res = self.predict(X)
        label = self.fm.labels[int(res)]
        if self.show:
            print("Predict Result: " + str(res) + " = " + str(label))
        return res, label


    # utils
    def p_datasets(self):
        print(
            "X_train: " + str(len(self.x_train)) + "\n" +
            "X_test: " + str(len(self.x_test)) + "\n" +
            "Y_train: " + str(len(self.y_train)) + "\n" +
            "Y_test: " + str(len(self.y_test)) + "\n"
        )


def test_NNet(show = True):

    mlp = NNet(show=show,data_size=10000)
    mlp.p_datasets()
    mlp.train()
    mlp.test()
    vec = mlp.fm.get_text_as_input_vector("Eu sou do BE")
    print (vec)
    mlp.predict_with_label(vec)
    mlp.save_net('NNet-1.pkl')

if __name__ == '__main__':
    test_NNet()