import os
from data.database.database import getSession, TweetParty
from data.utils.parserUtil import PartiesTwitterParser
import mining.algorithms.RAKE.rake as rake
import mining.algorithms.RAKE.rake_setup as rs
import unidecode as ud
import math
import numpy as np
from collections import Counter
from copy import deepcopy
from sklearn.model_selection import train_test_split

rk = rake.Rake()
session = getSession(path=os.path.abspath('../../../../database.sqlite'))

def get_tweets(count):
    if not count or count==None:
        return session.query(TweetParty).all()
    return session.query(TweetParty).filter().limit(count).all()


def get_ptParser(filename = None):
    if filename == None:
        filename = 'parties-twitter.json'
    fname = os.path.abspath('../../../../files/parties-config/' + str(filename))
    return PartiesTwitterParser(fname)

def rakec(content):
    tkw = rake.get_top_scoring_candidates(
        rk.run(
            rs.remove_regex(ud._unidecode(content))))
    raked_text = ""
    for tstr in [x[0] for x in tkw]:
        raked_text += tstr + " "
    return raked_text

def format_tweets(tweets, pfname = None):
    tlist = []
    for tweet in tweets:
        label = get_ptParser(pfname).getLabelFromUsername(str(tweet.username))
        raked_text = rakec(tweet.text)
        tup = (raked_text, label)
        tlist.append(
            tup
        )
    return tlist

class FeatureManager():

    def get_features_most_common(self, tweets, nr_features, pfname=None):
        tweets = format_tweets(tweets=tweets, pfname=pfname)
        words = []
        for t in tweets:
            words += t[0].split()

        d = Counter(words)

        for word in deepcopy(d):
            if not word.isalpha or len(word) < 2:
                del d[word]

        most_common = d.most_common(nr_features)
        # print("Most common ", nr_features, " words")
        features = []
        for word in most_common:
            features.append(word[0])
            # print(word[0] + "(" + str(word[1]) + "occurrences)")
        self.features = features
        return features

class DatasetManager():

    def get_ds_XY(self, tweets, features, labels_list):

        tweets_formated = format_tweets(tweets)

        N = len(tweets_formated)
        F = len(features)

        X = np.zeros((N,F))
        Y = np.zeros(N)

        for tweet in tweets_formated:
            n = tweets_formated.index(tweet)
            words_in_tweet = tweet[0].split()
            for word in words_in_tweet:
                if word in features:
                    f = features.index(word)
                    X[n][f] += 1
            # Build output labels (Y)
            Y[n] = labels_list.index(tweet[1])

        return (X, Y)

    def get_ds_X(self, tweets, features):
        tweets_formated = tweets
        if isinstance(tweets, list):
            tweets_formated = format_tweets(tweets)

        F = len(features)

        if isinstance(tweets_formated, list):
            N = len(tweets_formated)
            X = np.zeros((N, F))
            for tweet in tweets_formated:
                n = tweets_formated.index(tweet)
                words_in_tweet = tweet[0].split()
                for word in words_in_tweet:
                    if word in features:
                        f = features.index(word)
                        X[n][f] += 1
            return X
        elif isinstance(tweets, str):
            X = np.zeros(F)
            words_in_text = tweets.split()
            for word in words_in_text:
                if word in features:
                    f = features.index(word)
                    #print("word in features: " + word + " Index: " + str(f))
                    X[f] += 1
            return X.reshape(1, -1)
        else:
            raise ValueError("Wrong input to function. Neither string nor list.")


    def get_ds_train_test(self, X, Y, test_size=0.25):
        X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=test_size, random_state=42)
        return X_Train, X_Test, Y_Train, Y_Test


if __name__ == '__main__':
    fm = FeatureManager()
    features = fm.get_features_most_common(tweets=get_tweets(100),nr_features=30)
    labels = get_ptParser().get_labels()
    print(features)
    print(labels)
    dm = DatasetManager()
    X, Y = dm.get_ds_XY(tweets=get_tweets(200), features=features, labels_list=labels)
    print(X)
    print(Y)
    X = dm.get_ds_X("O jose silva pede saude", features)
    print (X)
    X = dm.get_ds_X(tweets=get_tweets(1), features=features)
    print (X)

