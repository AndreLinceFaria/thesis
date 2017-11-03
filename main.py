from time import time, strftime
from mining.algorithms.mlearning.classifiers.NBayes import NBayes
from mining.algorithms.mlearning.classifiers.NNet import NNet
from mining.algorithms.mlearning.classifiers.KNN import KNN
from mining.algorithms.mlearning.classifiers.SVM import SVM
from sklearn.model_selection import StratifiedKFold
import mining.algorithms.mlearning.feature as f
import logging as log
log.basicConfig(filename='logs/main.log',level=log.DEBUG)

features_number_tweets = 1000
features_number_features = 30
number_tweets= 10000

fm = f.FeatureManager()
dm = f.DatasetManager()

features = fm.get_features_most_common(tweets=f.get_tweets(count=features_number_tweets), nr_features=features_number_features)
labels = f.get_ptParser().get_labels()

X, Y = dm.get_ds_XY(tweets=f.get_tweets(number_tweets), features=features, labels_list=labels)
#x_tr,x_ts, y_tr, y_ts = dm.get_ds_train_test(X, Y)

log.debug(features)
log.debug(labels)

nnet = NNet()
nbay = NBayes()
knn = KNN()
svm = SVM()

lst = [nnet, nbay, knn, svm]

log.debug("Using " + str(len(X)) + " tweets for Stratified KFold")


kf = StratifiedKFold(n_splits=len(labels), shuffle=True)

log.debug("Nr Folds: " +  str(kf.n_splits))

i = 1

for train_indices, test_indices in kf.split(X,Y):
    tFold = time()
    #log.debug("Train: ", train_indices, "Test: ", test_indices)
    X_train,X_test = X[train_indices], X[test_indices]
    Y_train, Y_test = Y[train_indices], Y[test_indices]
    log.debug("Train: " + str(len(X_train)) + "Test: " + str(len(X_test)))
    log.debug("Fold Time: " + str(round(time() - tFold,3)) + " Iteration " + str(i))

    for alg in lst:
        tAlg = time()
        alg.train(X_train, Y_train)
        log.debug("training time: " + str(round(time()-tAlg, 3)))
        score = alg.test(X_test,Y_test)
        log.debug(alg.name + " Score: " + str(score) + " IT: " + str(i))
    i+=1

text = "Antonio costa, um bom partido para os adultos"
x_custom = dm.get_ds_X(text, features)

tweets = f.get_user_tweets(10)

for tweet in tweets:
    print(str(tweet.text.encode('utf-8')))
    x = dm.get_ds_X(tweet.text,features)
    label = nnet.predict_with_label(x,labels)
    print(str(tweet.username.encode('utf-8')) + " orientation: " + str(label))

'''
for alg in lst:
    label = alg.predict_with_label(x_custom, labels)
    log.debug(alg.name)
    log.debug("Text: " + text + "\nLabel: " + str(label))
    alg.save(fname=alg.name + "[" + strftime("%b_%d_%Y") +"]")
'''






