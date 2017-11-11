from mining.algorithms.mlearning.feature import get_tweets
import re
import unidecode as ud


tweets = get_tweets(count=100,cbu=True)

i = 0
for tweet in tweets:
    cleanString = re.sub(r"^\\s+[A-Za-z,;'\"\\s]+[.?!]$",' ',str(ud._unidecode(tweet.text)))
    cleanString = re.sub(r"http \S+|https \S+|http\S+", "", cleanString)
    cleanString = re.sub(r"pic.twitter\S+|youtube.com\S+|twitter.com\S+|bit.ly\S+|goo.gl\S+|youtu.be\S+", "", cleanString)


