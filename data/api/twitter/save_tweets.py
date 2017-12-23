from datetime import date, datetime, timedelta
from sys import stdout
from data.database.database import Tweet, TwitterUser, TweetParty
import unidecode as ud

from data.api.twitter.TwitterClient import TwitterClient
from data.api.twitter.TweepyClient import TweepyClient
from data.utils.parserUtil import PartiesTwitterParser
from data.database import database as database

twitterClient = TwitterClient()
partiesTP = PartiesTwitterParser()
tweepyClient = TweepyClient()
session = database.getSession()

def fetch_timeline_tweets():
    startdate,enddate = date(2017, 8, 28),date(2017, 10, 1)
    count = 0
    while startdate != datetime.now().date() and startdate != enddate:
        count += 1
        nextdate = startdate + timedelta(days=1)
        twitterClient.setStartDate(str(startdate))
        twitterClient.setEndDate(str(nextdate))
        stdout.write("\nStart date: " + str(startdate) + " -> Next date: " + str(nextdate))
        twitterClient.getTweetsAndSave(proxy=True,table=Tweet)
        startdate = nextdate
    print("Finished saving tweets from " + str(count) + " days")

def fetch_party_tweets():
    for party in partiesTP.parties:
        print("\nGetting tweets from Party: " + party.pname + ", Username: " + party.pusername)
        twitterClient.setUsername(party.pusername)
        twitterClient.setStartDate(str(date(2010,1,1)))
        twitterClient.setEndDate(str(date(2017,9,30)))
        twitterClient.getTweetsAndSave(proxy=True,table=TweetParty)
        for user in party.pusers:
            print("\nGetting tweets from User: " + user.name)
            twitterClient.setUsername(user.username)
            twitterClient.setStartDate(None)
            twitterClient.getTweetsAndSave(proxy=True)

def save_tweepy_for_users(proxy = True, thld = 400):

    if proxy:
        from data.proxy.tor import TorProxy
        tor = TorProxy()
        tor.start_tor()
        tor.proxy_requests()

    user_names_tweepy = tweepyClient.get_user_names()
    users_db = [ud._unidecode(user.username) for user in session.query(TwitterUser).all()]
    usernames = user_names_tweepy + list(set(users_db) - set(user_names_tweepy))
    #Remove party users
    for party in partiesTP.parties:
        usernames = [x for x in usernames if x != ud._unidecode(party.pusername)]
        for user in party.pusers:
            usernames = [x for x in usernames if x != ud._unidecode(user.username)]

    print("Users: " + str(len(usernames)))

    startdate, enddate = date(2017, 8, 28), date(2017, 10, 1)
    for user in usernames:
        print("user => [ " + str(user)+ " ]")
        tweets = tweepyClient.get_user_timeline_tweets(user,startdate,enddate, threshold=thld)
        print("Attempting to save: " + str(len(tweets)) + " tweets.")
        for t in tweets:
            twitterClient.saveTweet(t, table=Tweet)

    if proxy:
        tor.stop_tor()

def fetch_tweets():
    #Get timeline tweets
    fetch_timeline_tweets()
    #Get party tweets
    fetch_party_tweets()


if __name__ == "__main__":
    save_tweepy_for_users(thld=400)