from data.database.database import *
import mining.algorithms.RAKE.rake as rake
import mining.algorithms.RAKE.rake_setup as rs

session = getSession()
rk = rake.Rake()


def rakeTimelineTweets():
    tweets = session.query(Tweet).all()
    print("RAKE-ing timeline Tweets: " + str(len(tweets)))
    for tweet in tweets:
        print("RAKE-Timeline: tweet " + str(tweet.tweetId))
        top_keywords = rake.get_top_scoring_candidates(
            rk.run(
                rs.remove_regex(tweet.text)))
        text_keyword_list = str(top_keywords)
        tweetP = TweetParsed(tweetId=tweet.tweetId,
                             username=tweet.username,
                             text = text_keyword_list)
        session.add(tweetP)
        session.commit()

def rakePartyTweets():
    tweets_party = session.query(TweetParty).all()
    print("RAKE-ing party Tweets: " + str(len(tweets_party)))
    for tweet in tweets_party:
        print("RAKE-Party: tweet " + str(tweet.tweetId))
        top_keywords = rake.get_top_scoring_candidates(
            rk.run(
                rs.remove_regex(tweet.text)))
        text_keyword_list = str(top_keywords)
        tweetPP = TweetPartyParsed(tweetId=tweet.tweetId,
                             username=tweet.username,
                             text = text_keyword_list)
        session.add(tweetPP)
        session.commit()

print(sys.argv[1])
if sys.argv[1] == 'timeline':
    print("[Rake timeline tweets]")
    rakeTimelineTweets()
elif sys.argv[1] == 'party':
    print("[Rake party tweets]")
    rakePartyTweets()
else:
    print("[Fetching all tweets]")
    rakeTimelineTweets()
    rakePartyTweets()


'''
read list string representation

import ast

list_parsed = ast.literal_eval(list_string)

'''

