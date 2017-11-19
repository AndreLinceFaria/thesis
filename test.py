from mining.algorithms.mlearning.feature import get_tweets
import re
import unidecode as ud
import itertools, operator

'''
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
'''


scores = [0.249626307922, 0.42600896861, 0.381165919283, 0.334828101644]
data =  ['PSD', 'PSD', 'PCP-PEV', 'PSD']

group = zip(data, scores)

print group

def accumulate(l):
    it = itertools.groupby(sorted(l), operator.itemgetter(0))
    for key, subiter in it:
       yield key, sum(item[1] for item in subiter)

res = list(accumulate(group))

print res

mx = max(res, key=operator.itemgetter(1))

print mx