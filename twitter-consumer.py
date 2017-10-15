from data.api.twitter.TwitterClient import TwitterClient
from data.utils.parserUtil import PartiesTwitterParser

twitterClient = TwitterClient()
partiesTP = PartiesTwitterParser(filename='files/parties-config/parties-twitter.json')

def fetch_timeline_tweets():
    twitterClient.getTweetsAndSave()

def fetch_party_tweets():
    for party in partiesTP.parties:
        print("\nGetting tweets from Party: " + party.pname + ", Username: " + party.pusername)
        twitterClient.setUsername(party.pusername)
        twitterClient.getTweetsAndSave()
        for user in party.pusers:
            print("\nGetting tweets from User: " + user.name)
            twitterClient.setUsername(user.username)
            twitterClient.setStartDate(None)
            twitterClient.getTweetsAndSave()

def fetch_tweets():
    #Get timeline tweets
    #fetch_timeline_tweets()

    #Get party tweets
    fetch_party_tweets()


fetch_tweets()