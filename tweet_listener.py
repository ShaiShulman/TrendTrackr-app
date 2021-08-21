# tweet_listener.py
""" Used for listening and recording new sample tweets for trending topics """

import logging

import tweepy


class TweetListener(tweepy.StreamListener):
    def __init__(self, api, topics, tweet_list, limit=5, logger=None):
        self.tweet_count = {i.lower(): 0 for i in topics}
        self.tweet_list = tweet_list
        self.topics = [topic.lower() for topic in topics]
        self.logger = logger
        self.TWEET_LIMIT = limit
        self.total_count = 0
        super().__init__(api)

    def on_connect(self):
        if self.logger:
            logging.info('TweetListener connected')

    def on_status(self, status):
        if hasattr(status, "retweeted_status"):
            try:
                tweet_text = status.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                tweet_text = status.retweeted_status.text
        else:
            try:
                tweet_text = status.extended_tweet["full_text"]
            except AttributeError:
                tweet_text = status.text
        self.total_count += 1
        if status.lang != 'en':
            return
        if self.logger:
            logging.info(f'Processing tweet "{tweet_text}"')

        for topic in self.topics:
            if topic in tweet_text.lower() and self.tweet_count[topic] < self.TWEET_LIMIT:
                self.tweet_count[topic] += 1
                self.tweet_list[topic].append(tweet_text)
        return sum(self.tweet_count.values()) < (self.TWEET_LIMIT * len(self.topics)) and self.total_count < (
                self.TWEET_LIMIT * len(self.topics)) * 3
