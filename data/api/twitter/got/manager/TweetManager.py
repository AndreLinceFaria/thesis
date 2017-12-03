import cookielib
import datetime
import json
import logging
import re

import sys
from pyquery import PyQuery

from .. import models

logger = logging.getLogger(__name__)

class TweetManager:

    def __init__(self):
        pass

    @staticmethod
    def getTweets(tweetCriteria, receiveBuffer=None, bufferLength=100, proxy=None):

        count = 0
        refreshCursor = ''
        results = []
        resultsAux = []
        cookieJar = cookielib.CookieJar()

        if hasattr(tweetCriteria, 'username') and (tweetCriteria.username.startswith("\'") or tweetCriteria.username.startswith("\"")) and (tweetCriteria.username.endswith("\'") or tweetCriteria.username.endswith("\"")):
            tweetCriteria.username = tweetCriteria.username[1:-1]

        active = True

        while active:
            try:
                logger.debug("Getting new json...")
                json = TweetManager.getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy)
            except ValueError as error:
                print("Value Error: " +  str(error))
                break

            if len(json['items_html'].strip()) == 0:
                break
            refreshCursor = json['min_position']
            tweets = PyQuery(json['items_html'])('div.js-stream-tweet')
            if len(tweets) == 0:
                break
            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)
                tweet = models.Tweet()

                usernameTweet = tweetPQ("span:first.username.u-dir b").text();
                txt = re.sub(r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'));
                retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
                favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr("data-tweet-stat-count").replace(",", ""));
                dateSec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"));
                id = tweetPQ.attr("data-tweet-id");
                permalink = tweetPQ.attr("data-permalink-path");
                geo = ''
                geoSpan = tweetPQ('span.Tweet-geo')
                if len(geoSpan) > 0:
                    geo = geoSpan.attr('title')

                tweet.id = id
                tweet.permalink = 'https://twitter.com' + permalink
                tweet.username = usernameTweet
                tweet.text = txt
                tweet.date = datetime.datetime.fromtimestamp(dateSec)
                tweet.retweets = retweets
                tweet.favorites = favorites
                tweet.mentions = " ".join(re.compile('(@\\w*)').findall(tweet.text))
                tweet.hashtags = " ".join(re.compile('(#\\w*)').findall(tweet.text))
                tweet.geo = geo

                results.append(tweet)
                resultsAux.append(tweet)

                sys.stdout.write('\rGetting tweet: ' + str(tweet.id) + ' Fetched tweets: '+str(count))
                sys.stdout.flush()
                count += 1

                logger.debug("Tweet added: " +  str(tweet.id))
                logger.debug("Nr Tweets: " +  str(len(results)))

                if receiveBuffer and len(resultsAux) >= bufferLength:
                    receiveBuffer(resultsAux)
                    resultsAux = []

                if tweetCriteria.maxTweets > 0 and len(results) >= tweetCriteria.maxTweets:
                    active = False
                    break


        if receiveBuffer and len(resultsAux) > 0:
            receiveBuffer(resultsAux)
        #print("Total tweets fetched: " + str(len(results)))
        return results

    @staticmethod
    def getJsonReponse(tweetCriteria, refreshCursor, cookieJar, proxy):

        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&max_position=%s"

        urlGetData = ''

        if hasattr(tweetCriteria, 'username'):
            urlGetData += ' from:' + tweetCriteria.username

        if hasattr(tweetCriteria, 'querySearch'):
            urlGetData += ' ' + tweetCriteria.querySearch

        if hasattr(tweetCriteria, 'near'):
            urlGetData += "&near:" + tweetCriteria.near + " within:" + tweetCriteria.within

        if hasattr(tweetCriteria, 'since'):
            if tweetCriteria.since != None:
                urlGetData += ' since:' + tweetCriteria.since

        if hasattr(tweetCriteria, 'until'):
            if tweetCriteria.until != None:
                urlGetData += ' until:' + tweetCriteria.until


        if hasattr(tweetCriteria, 'topTweets'):
            if tweetCriteria.topTweets:
                url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"


        import socket, socks #pip install pysocks
        if proxy:
            print("############\n Using TOR proxy \n###########")
            # Configuration
            SOCKS5_PROXY_HOST = '127.0.0.1'
            SOCKS5_PROXY_PORT = 9150

            print("==================================\n"
                  "=> Using TOR on "+SOCKS5_PROXY_HOST+":"+str(SOCKS5_PROXY_PORT)+"...\n"
                  "==================================\n ")

            # Remove this if you don't plan to "deactivate" the proxy later
            default_socket = socket.socket

            # Set up a proxy
            socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
            socket.socket = socks.socksocket


        import urllib
        import urllib2

        url = url % (urllib.quote(urlGetData), refreshCursor)

        headers = [
            ('Host', "twitter.com"),
            ('User-Agent', "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"),
            ('Accept', "application/json, text/javascript, */*; q=0.01"),
            ('Accept-Language', "de,en-US;q=0.7,en;q=0.3"),
            ('X-Requested-With', "XMLHttpRequest"),
            ('Referer', url),
            ('Connection', "keep-alive")
        ]

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        opener.addheaders = headers

        try:
            response = opener.open(url)
            jsonResponse = response.read()
        except:
            raise ValueError("\nTwitter weird response. Try to see on proxy: https://twitter.com/search?q=%s&src=typd" % urllib.quote(urlGetData))

        dataJson = json.loads(jsonResponse)

        #return to default socket
        if proxy:
            socket.socket = default_socket

        return dataJson
