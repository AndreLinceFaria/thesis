from FeatureManager import get_features, parse_tweets, tweets_to_dataset

from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

tweets = parse_tweets(limit=500)
features = get_features(tweets, 30)

X_train, Y_train = tweets_to_dataset(tweets, features)

print(X_train)

model = LinearSVC()

model.fit(X_train, Y_train)

Y_predict = model.predict(X_train)

score = accuracy_score(Y_train, Y_predict)

print ("SCORE: " + str(score))