from sklearn.neural_network import MLPClassifier
from mining.algorithms.mlearning.classifiers import models_path
from mining.algorithms.mlearning import feature as f, persist as p

class NNet():
    def __init__(self, load = True):
        if load != True:
            self.net = self.create_net()

    def load_net(self, net):
        self.net = net

    def create_net(self):
        return MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5,2), random_state=1)

    def train(self, x_train, y_train):
        self.net.fit(x_train, y_train)

    def test(self, x_test, y_test):
        return self.net.score(x_test,y_test)

    def predict(self,X):
        return self.net.predict(X)

    def predict_with_label(self, X, labels):
        pred = self.predict(X)
        return pred,labels[int(pred)]


def run(fnt = 1000, fnf = 30, nt = 10000):
    fm = f.FeatureManager()
    dm = f.DatasetManager()
    nnet = NNet(load=False)

    features = fm.get_features_most_common(tweets=f.get_tweets(fnt), nr_features=fnf)
    labels = f.get_ptParser().get_labels()

    print(features)
    print(labels)

    X, Y = dm.get_ds_XY(tweets=f.get_tweets(nt), features=features, labels_list=labels)
    x_tr,x_ts, y_tr, y_ts = dm.get_ds_train_test(X, Y)

    nnet.train(x_tr, y_tr)
    score = nnet.test(x_ts,y_ts)
    print("Net accuracy: " + str(score))

    text = "Antonio costa, um bom partido para os adultos"
    x_custom = dm.get_ds_X(text, features)
    label = nnet.predict_with_label(x_custom,labels)
    print("Text: " + text +  "\nLabel: " + str(label))

    p.save_model(nnet.net, filename=models_path + "nnet_example")

if __name__ == '__main__':
    run()

