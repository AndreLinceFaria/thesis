from mining.algorithms.mlearning.feature import get_tweets
import re
import unidecode as ud


tweets = get_tweets(count=10,cbu=True)

i = 0
for tweet in tweets:
    #pattern = re.compile("/^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/")
    pattern = re.compile("https?://.*?\\s+")
    text = ud._unidecode(tweet.text)
    cleanString = re.sub(pattern, '', text)
    print("Original: " + text)
    print("Regex: " + cleanString)
    print("")
