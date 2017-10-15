import logging

from sqlalchemy.orm.exc import NoResultFound

from data.database import database as database
from data.database.database import Tweet, TwitterUser
from got.manager import TweetManager, TweetCriteria

logger = logging.getLogger(__name__)
session = database.getSession()

class TwitterClient():

    def __init__(self, startDate = '2017-08-20', endDate = '2017-09-30', country = 'portugal', tweetCount = 0, query='geocode:39.673370,-8.283691,306km AND lang:pt'):
        self.startDate = startDate
        self.endDate = endDate
        self.country = country
        self.tweetCount = tweetCount
        self.query = query

    def getTweetsAndSave(self):
        print("Getting tweets from " + str(self.startDate) + " ...")
        logger.debug("TwitterClient is running...")
        tweets = self.getTweets()

        print("Saving fetched tweets to db...")
        tcount = 0
        if len(tweets) > 0:
            for t in tweets:
                logger.debug("Tweet: " + t.id)
                self.saveTweet(t)
                tcount += 1
        else:
            print("No tweets returned.")
        print("Total tweets saved: " + str(tcount))

    def saveTweet(self, t):
        try:
            query = session.query(Tweet).filter(Tweet.tweetId==t.id).one()
        except NoResultFound:
            try:
                query = session.query(TwitterUser).filter(TwitterUser.username == t.username).one()
            except NoResultFound:
                user = TwitterUser(username=t.username)
                session.add(user)

            #session.commit()
            tweet = Tweet(tweetId=t.id,
                            permalink=t.permalink,
                            username=t.username,
                            text=t.text,
                            date=t.date,
                            retweets=t.retweets,
                            favorites=t.favorites,
                            mentions=t.mentions,
                            hashtags=t.hashtags,
                            geo=t.geo)
            session.add(tweet)
            session.commit()

    def getTweets(self):
        tweetCriteria = TweetCriteria().setQuerySearch(
            self.query).setSince(self.startDate).setUntil(
            self.endDate).setMaxTweets(self.tweetCount)
        tweets = TweetManager.getTweets(tweetCriteria)
        print("Number of tweets fetched: " + str(len(tweets)))
        return tweets


    def setStartDate(self, date):
        self.startDate = date

    def setEndDate(self, date):
        self.endDate = date

    def setCountry(self, country):
        self.country = country

    def setTweetCount(self, tweetCount):
        self.tweetCount = tweetCount