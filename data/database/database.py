import os, sys
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TwitterUser(Base):
    __tablename__ = 'twitter_user'
    username = Column(String, primary_key=True)

class Tweet(Base):
    __tablename__ = 'tweet'
    tweetId = Column(Integer, primary_key=True, autoincrement=True)
    permalink = Column(Text)
    username = Column(String, ForeignKey('twitter_user.username'))
    text = Column(Text)
    date = Column(DateTime)
    retweets = Column(Integer)
    favorites = Column(Integer)
    mentions = Column(Text)
    hashtags = Column(Text)
    geo = Column(String)

class TweetParty(Base):
    __tablename__ = 'tweet_party'
    tweetId = Column(Integer, primary_key=True, autoincrement=True)
    permalink = Column(Text)
    username = Column(String, ForeignKey('twitter_user.username'))
    text = Column(Text)
    date = Column(DateTime)
    retweets = Column(Integer)
    favorites = Column(Integer)
    mentions = Column(Text)
    hashtags = Column(Text)
    geo = Column(String)

#create engine
from sqlalchemy import create_engine
engine = create_engine('sqlite:///database.sqlite')
Base.metadata.create_all(engine)

# create session
from sqlalchemy.orm import sessionmaker

def getSession():
    DBSession = sessionmaker()
    DBSession.configure(bind=engine)
    session = DBSession()
    return session
