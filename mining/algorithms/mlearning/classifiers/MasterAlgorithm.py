from time import time, strftime
import datetime
from mining.algorithms.mlearning.classifiers.NBayes import NBayes
from mining.algorithms.mlearning.classifiers.NNet import NNet
from mining.algorithms.mlearning.classifiers.KNN import KNN
from mining.algorithms.mlearning.classifiers.SVM import SVM
from sklearn.model_selection import StratifiedKFold
import mining.algorithms.mlearning.feature as f
import mining.algorithms.mlearning.persist as p
import logging
from beautifultable import BeautifulTable

fm = f.FeatureManager()
dm = f.DatasetManager()

class MasterAlgorithm:
    def __init__(self):
        self.features = None
        self.labels = None
        self.algorithms = None
        self.cv = None

    def setup(self, fntg=500, fnf=50, algs = None):
        self.features = fm.get_features_most_common(tweets=f.get_tweets(count=fntg,cbu=True), nr_features=fnf)
        self.labels = f.get_ptParser().get_labels()
        #print("AFTER FEATURES AND LABELS")
        if algs==None or not isinstance(algs, list):
            self.algorithms = [NNet(), NBayes(), KNN(), SVM()]
        else:
            self.algorithms = algs

    def train(self, tweets_train=None, save = False):
        dt = time()
        log = logging.getLogger('train-log')
        log.addHandler(logging.FileHandler('logs/train-log['+datetime.datetime.today().strftime('%Y-%m-%d')+'].log'))
        log.setLevel(logging.DEBUG)

        log.debug("\n[MASTER ALGORITHM] Training: " + str(datetime.datetime.now()) + "\n")

        if self.labels == None or self.features == None:
            self.setup()

        self.cv = StratifiedKFold(n_splits=len(self.labels), shuffle=True)
        X, Y = dm.get_ds_XY(tweets=f.get_tweets(tweets_train), features=self.features, labels_list=self.labels)

        table = BeautifulTable()
        table.column_headers = ["Iteration"] + [alg.name for alg in self.algorithms]

        i = 0
        #CROSS VALIDATION TRAIN-TEST
        for train_indices, test_indices in self.cv.split(X, Y):
            X_train, X_test = X[train_indices], X[test_indices]
            Y_train, Y_test = Y[train_indices], Y[test_indices]

            scores = [-1] * len(self.algorithms)

            for alg in self.algorithms:
                alg.train(X_train, Y_train)
                score = alg.test(X_test, Y_test)

                scores[self.algorithms.index(alg)] = str(score)

            table.append_row([str(i)] + scores)
            i+=1

        log.debug(str(table))

        log.debug("Training time: " + str(round(time()-dt, 2)) + " seconds.")

        if save:
            for alg in self.algorithms:
                p.save_model(alg.clf,'models/' + alg.name)

    def predict(self,tweets_predict=None, load=False):
        dt = time()
        if self.labels == None or self.features == None:
            self.setup()

        log = logging.getLogger('predict-log')
        log.addHandler(
            logging.FileHandler('logs/predict-log[' + datetime.datetime.today().strftime('%Y-%m-%d') + '].log'))
        log.setLevel(logging.DEBUG)

        log.debug("\n[MASTER ALGORITHM] Predict: " + str(datetime.datetime.now()) + "\n")

        if load:
            for alg in self.algorithms:
                alg.clf = p.load_model('models/' + alg.name)

        tweets = f.get_user_tweets(tweets_predict)
        table = BeautifulTable()
        table.column_headers = ["Index","Username"] + [alg.name for alg in self.algorithms] + ["Final (Average)"]

        i = 0
        for tweet in tweets:
            tmp_list = [''] * len(self.algorithms)
            for alg in self.algorithms:
                idx = self.algorithms.index(alg)
                x = dm.get_ds_X(tweet.text, self.features)
                pred, label = alg.predict_with_label(x, self.labels)
                tmp_list[idx] = label
            table.append_row([i,tweet.username] + tmp_list + [max(set(tmp_list), key=tmp_list.count)])
            i+=1
        log.debug(table)

        results_final = [0] * len(self.labels)
        for party in list(table['Final (Average)']):
            results_final[int(self.labels.index(party))] += 1

        table_final = BeautifulTable()
        table_final.column_headers = self.labels
        table_final.append_row(results_final)

        log.debug("\n [Prediction Count] \n")

        log.debug(table_final)
        log.debug("Predict time: " + str(round(time() - dt, 2)) + " seconds.")


if __name__ == "__main__":
    alg = MasterAlgorithm()
    alg.setup(fntg=500, fnf=50)
    #alg.train(tweets_train=10000,save=True)
    #alg.predict(tweets_predict=30,load=True)
    print("END")