# twitter.py
""" twitter functions """

import tweepy
import sys
from tweet_listener import TweetListener
from common.data_structs import Topic


def get_auth(keys):
    auth = tweepy.OAuthHandler(keys.twitter_consumer_key, keys.twitter_consumer_secret)
    auth.set_access_token(keys.twitter_access_token, keys.twitter_access_token_secret)
    return auth


def get_api(keys):
    return tweepy.API(get_auth(keys), wait_on_rate_limit=True,
                      wait_on_rate_limit_notify=True)


def get_trends(location_id, keys):
    raw = get_api(keys).trends_place(location_id)
    trends = [Topic(id=None, name=trend['name'], volume=trend['tweet_volume']) for trend in raw[0]['trends'] if trend['tweet_volume']]
    return trends


def get_stream(topics, keys, logger=None):
    api = get_api(keys)
    tweets = {i.lower(): [] for i in topics}

    listener = TweetListener(api, topics, tweets, limit=5, logger=logger)
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(track=topics, languages=['en'], is_async=False)
    return tweets
