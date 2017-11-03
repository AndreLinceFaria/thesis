from mining.algorithms.mlearning.classifiers.MasterAlgorithm import MasterAlgorithm

train = False

if __name__ == "__main__":
    alg = MasterAlgorithm()
    alg.setup(fnt=10000, fnf=50)
    if train:
        alg.train(tweets_train=10000,save=True)
    else:
        alg.predict(tweets_predict=30, load=True)