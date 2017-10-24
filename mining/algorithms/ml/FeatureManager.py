import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from data.database.database import getSession, TweetParty
from data.utils.parserUtil import PartiesTwitterParser
import mining.algorithms.RAKE.rake as rake
import mining.algorithms.RAKE.rake_setup as rs

rk = rake.Rake()
pTwitterParser = PartiesTwitterParser(filename='../../../files/parties-config/parties-twitter.json')
session = getSession(path='../../../database.sqlite')
labels = pTwitterParser.get_labels()

def parse_tweets(limit = 100):
    ptweets = session.query(TweetParty).filter().limit(limit).all()
    tlist = []
    for tweet in ptweets:
        label = pTwitterParser.getLabelFromUsername(str(tweet.username))
        tkw = rake.get_top_scoring_candidates(
            rk.run(
                rs.remove_regex(tweet.text)))
        raked_text = ""
        for tstr in [x[0].encode('utf-8') for x in tkw]:
            raked_text += tstr + " "
        tup = (raked_text, label)
        tlist.append(
            tup
        )
    return tlist

def get_features(tweets,F):
    from collections import Counter
    from copy import deepcopy

    words = []

    for t in tweets:
        words += t[0].split()

    d = Counter(words)

    for word in deepcopy(d):
        if not word.isalpha or len(word) < 2:
            del d[word]

    most_common = d.most_common(F)

    print("Most common ", F," words")
    i = 1
    features = []
    for word in most_common:
        features.append(word[0])
        print(str(i) + ":" + word[0] + "(" + str(word[1]) + "occurrences)")
        i += 1
    return features

def tweets_to_dataset(tweets, features):
    import numpy as np

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
        Y[n] = labels.index(tweet[1])

    return (X, Y)