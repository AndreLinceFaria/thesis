import logging, sys

from sqlalchemy.orm.exc import NoResultFound

from data.database import database as database
from data.database.database import Tweet, TwitterUser, TweetParty
from got.manager import TweetManager, TweetCriteria

logger = logging.getLogger(__name__)
session = database.getSession()

class TwitterClient():

    def __init__(self, startDate = '2017-08-20', endDate = '2017-09-30', country = 'portugal', tweetCount = 0, query='geocode:39.673370,-8.283691,306km AND lang:pt', username=None):
        self.startDate = startDate
        self.endDate = endDate
        self.country = country
        self.tweetCount = tweetCount
        self.query = query
        self.username = username

    def getTweetsAndSave(self, proxy=None):
        if self.startDate != None:
            print("\nGetting tweets since " + str(self.startDate) + " until " + str(self.endDate) + "...")
        logger.debug("TwitterClient is running...")
        tweets = self.getTweets(proxy)

        print("\nSaving fetched tweets to db...")
        tcount = 0
        if len(tweets) > 0:
            for t in tweets:
                logger.debug("Tweet: " + t.id)
                sys.stdout.write("\rSaving tweets " + str(tcount))
                sys.stdout.flush()
                self.saveTweet(t)
                tcount += 1
        else:
            print("\nNo tweets returned.")
        #print("Total tweets saved: " + str(tcount))

    def saveTweet(self, t):
        try:
            if self.username==None: #timeline
                query = session.query(Tweet).filter(Tweet.tweetId==t.id).one()
            else:
                query = session.query(TweetParty).filter(TweetParty.tweetId == t.id).one()
        except NoResultFound:
            try:
                query = session.query(TwitterUser).filter(TwitterUser.username == t.username).one()
            except NoResultFound:
                user = TwitterUser(username=t.username)
                session.add(user)

            if self.username==None:
                print("Save timeline tweet")
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
            else:
                print("Save username tweet")
                tweet = TweetParty(tweetId=t.id,
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

    def getTweets(self, proxy):
        if self.username==None:
            tweetCriteria = TweetCriteria().setQuerySearch(
                self.query).setSince(self.startDate).setUntil(
                self.endDate).setMaxTweets(self.tweetCount)
        else:
            tweetCriteria = TweetCriteria().setUsername(self.username).setSince(self.startDate).setUntil(
                self.endDate).setMaxTweets(self.tweetCount)


        tweets = TweetManager.getTweets(tweetCriteria=tweetCriteria, proxy=proxy)

        return tweets


    def setStartDate(self, date):
        self.startDate = date

    def setEndDate(self, date):
        self.endDate = date

    def setCountry(self, country):
        self.country = country

    def setTweetCount(self, tweetCount):
        self.tweetCount = tweetCount

    def setUsername(self, username):
        self.username = username