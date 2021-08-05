# twitter.py
""" twitter functions """

import tweepy, keys
import sys
from tweet_listener import TweetListener

sys.path.insert(1, '../trends_web/common')
from common.data_structs import Topic

def get_auth():
    auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    return auth

def get_api():
    return tweepy.API(get_auth(), wait_on_rate_limit=True, 
                      wait_on_rate_limit_notify=True)

def get_trends(location_id):
    raw = get_api().trends_place(location_id)
    trends = [Topic(trend['name'], trend['tweet_volume'])  for trend in raw[0]['trends'] if trend['tweet_volume']]
    #trends.sort(key=itemgetter('tweet_volume'),reverse=True)
    return trends

def get_stream(topics, logger=None):
    api = get_api()
    tweets = {i.lower() : [] for i in topics}

    listener = TweetListener(api, topics, tweets, limit=5, logger=logger)
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(track=topics, languages=['en'], is_async=False)
    return tweets