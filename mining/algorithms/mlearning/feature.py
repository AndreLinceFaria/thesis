from settings import *
from data.database.database import getSession, TweetParty
from data.utils.parserUtil import PartiesTwitterParser
import mining.algorithms.RAKE.rake as rake
import mining.algorithms.RAKE.rake_setup as rs
import unidecode as ud
import numpy as np
from collections import Counter
from copy import deepcopy
from sklearn.model_selection import train_test_split

rk = rake.Rake()

session = getSession(DB)

def get_tweets(count,table=TweetParty, cbu = True):
    if not count or count==None:
        return session.query(table).all()
    elif cbu: #if count by user (Around 40 distinct users. nr of tweets fetch should be 40 * count.
        users = session.execute("SELECT DISTINCT(username) FROM tweet_party")
        tweets = []
        for user in users:
            [tweets.append(t) for t in session.execute("SELECT tp.* FROM tweet_party tp WHERE tp.username = \"" + ud._unidecode(user.username) + "\" ORDER BY RANDOM() LIMIT " + str(count))]
        print("Fetched " + str(count) + " Random tweets per party which resulted in " + str(len(tweets)) + " tweets in Total")
        return tweets
    else:
        return session.query(table).filter().limit(count).all()

if __name__ == "__main__":
    get_tweets(count=400,cbu=True)

def get_user_tweets(count):
    if not count or count==None:
        return session.execute('SELECT tweet.username as username, GROUP_CONCAT(tweet.text, "' '")as text FROM tweet GROUP BY tweet.username')
    return session.execute('SELECT tweet.username as username, GROUP_CONCAT(tweet.text, "' '")as text FROM tweet GROUP BY tweet.username LIMIT :count',{'count':count})

def get_ptParser():
    return PartiesTwitterParser()

def rakec(content):
    tkw = rake.get_top_scoring_candidates(
        rk.run(
            ud._unidecode(content)))
    raked_text = ""
    for tstr in [x[0] for x in tkw]:
        raked_text += tstr + " "
    raked_text = rs.remove_regex(raked_text)
    return raked_text

def format_tweets(tweets):
    print("Formatting " + str(len(tweets)) + " tweets...")
    tlist = []
    i = 0
    missed_tweets = 0
    for tweet in tweets:
        label = get_ptParser().getLabelFromUsername(str(tweet.username))
        print("Username: " + str(tweet.username) + " Label: " + str(label))
        if label != None:
            try:
                raked_text = rakec(tweet.text)
            except KeyboardInterrupt:
                print("timed out.")
                raked_text = None
            if raked_text != None:
                tup = (raked_text, label)
                print("idx: " + str(i) + " tid: " + str(tweet.tweetId))
                print("original: " + str(ud._unidecode(tweet.text)))
                print("result: " + str(raked_text))
                tlist.append(
                    tup
                )
            i+=1
        else:
            missed_tweets +=1

    print("formated " + str(i) + " correct tweets. Missed: " + str(missed_tweets) + " tweets.")

    return tlist

class FeatureManager():

    def get_features_most_common(self, tweets, nr_features):
        print("Generating features...")
        tweets = format_tweets(tweets=tweets)
        print("TWEETS FORMATED")
        words = []
        for t in tweets:
            words += t[0].split()

        d = Counter(words)

        for word in deepcopy(d):
            if not word.isalpha or len(word) < 2:
                del d[word]

        most_common = d.most_common(nr_features)
        features = []
        for word in most_common:
            features.append(word[0])
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
        elif isinstance(tweets_formated, str) or isinstance(tweets_formated, unicode):
            raked_tweets = rakec(tweets_formated)
            X = np.zeros(F)
            words_in_text = raked_tweets.split()
            for word in words_in_text:
                if word in features:
                    f = features.index(word)
                    X[f] += 1
            return X.reshape(1, -1)
        else:
            raise ValueError("Wrong input to function. Neither string nor list.")


    def get_ds_train_test(self, X, Y, test_size=0.25):
        X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=test_size, random_state=42)
        return X_Train, X_Test, Y_Train, Y_Test