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

rk = rake.Rake()
session = getSession(path=os.path.abspath('../../../database.sqlite'))

class FeatureManager():
    def __init__(self, parties_json):
        self.parties_json = parties_json
        self.ptParser = PartiesTwitterParser(filename=os.path.abspath('../../../files/parties-config/' + str(self.parties_json)))
        self.labels = self.ptParser.get_labels()
        self.features = None #initialized and changed in get_features before return

    def get_parsed_tweets(self, data_size = 100):
        ptweets = session.query(TweetParty).filter().limit(data_size).all()
        tlist = []
        for tweet in ptweets:
            label = self.ptParser.getLabelFromUsername(str(tweet.username))
            tkw = rake.get_top_scoring_candidates(
                rk.run(
                    rs.remove_regex(ud._unidecode(tweet.text))))
            raked_text = ""
            for tstr in [x[0] for x in tkw]:
                raked_text += tstr + " "
            tup = (raked_text, label)
            tlist.append(
                tup
            )
        return tlist

    def get_features(self, tweets, nr_features):
        words = []

        for t in tweets:
            words += t[0].split()

        d = Counter(words)

        for word in deepcopy(d):
            if not word.isalpha or len(word) < 2:
                del d[word]

        most_common = d.most_common(nr_features)

        #print("Most common ", nr_features, " words")
        i = 1
        features = []
        for word in most_common:
            features.append(word[0])
            #print(str(i) + ":" + word[0] + "(" + str(word[1]) + "occurrences)")
            i += 1
        self.features = features
        return features

    def tweets_to_dataset(self, tweets, features):
        N = len(tweets)
        F = len(features)

        X = np.zeros((N,F))
        Y = np.zeros(N)

        for tweet in tweets:
            n = tweets.index(tweet)
            words_in_tweet = tweet[0].split()
            for word in words_in_tweet:
                if word in features:
                    f = features.index(word)
                    X[n][f] += 1
            # Build output labels (Y)
            Y[n] = self.labels.index(tweet[1])

        return (X, Y)

    def tweets_to_input_vector(self, tweets, features):
        N = len(tweets)
        F = len(features)

        X = np.zeros((N,F))

        for tweet in tweets:
            n = tweets.index(tweet)
            words_in_tweet = tweet[0].split()
            for word in words_in_tweet:
                if word in features:
                    f = features.index(word)
                    X[n][f] += 1
            # Build output labels (Y)

        return X

    def get_text_as_input_vector(self, text):
        F = len(self.features)
        X = np.zeros(F)
        words_in_text = text.split()
        for word in words_in_text:
            if word in self.features:
                f = self.features.index(word)
                X[f] += 1
        return X.reshape(1,-1)

    def get_dataset(self, data_size = 10000, nr_features = None):
        if nr_features == None and nr_features <=0:
            nr_features = int(math.floor(math.sqrt(data_size)))
        tweet_list = self.get_parsed_tweets(data_size=data_size)
        features = self.get_features(tweets=tweet_list, nr_features=nr_features)
        return self.tweets_to_dataset(tweets=tweet_list, features=features)

    def get_dataset_test_train(self, data_size=10000, nr_features = None, test_size=0.25):
        X, Y = self.get_dataset(data_size=data_size, nr_features=nr_features)
        return self.split_dataset(X, Y, test_size=test_size)

    def split_dataset(self, X, Y, test_size=0.25):
        from sklearn.model_selection import train_test_split
        X_Train, X_Test, Y_Train, Y_Test = train_test_split(X,Y,test_size=test_size, random_state=42)
        return X_Train, X_Test, Y_Train, Y_Test