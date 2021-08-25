# twitter.py
""" twitter functions """

import tweepy
from geopy.geocoders import Nominatim
from tweet_listener import TweetListener
from common.data_structs import Topic

LOCATOR_USER_AGENT_NAME = "TrendTracker"


def get_auth(keys):
    """
    get authorization token for Twitter api
    @param keys: Keys object that include the 4 access tokens
    @return:
    """
    auth = tweepy.OAuthHandler(keys.twitter_consumer_key, keys.twitter_consumer_secret)
    auth.set_access_token(keys.twitter_access_token, keys.twitter_access_token_secret)
    return auth


def get_api(keys):
    """
    get Twitter api object
    @param keys: Keys object that include the 4 access tokens
    @return: api object
    """
    return tweepy.API(get_auth(keys), wait_on_rate_limit=True,
                      wait_on_rate_limit_notify=True)


def get_location(address, keys):
    """
    get Twitter woied location for a specific city name/address
    @param address: city name or address to get an id
    @param keys: Keys object that include the 4 access tokens
    @return: woeid, name of location
    """
    geolocator = Nominatim(user_agent=LOCATOR_USER_AGENT_NAME)
    loc = geolocator.geocode(address)
    if not loc:
        raise ValueError(f'Coordinates cannot be produced for location "{address}"')
    api = get_api(keys)
    twitters_locs = api.trends_closest(loc.latitude, loc.longitude)
    if len(twitters_locs) == 0:
        raise ValueError(f'No woeid found for coordinates {loc.latitude}, {loc.longitude}')
    return twitters_locs[0]['woeid'], twitters_locs[0]['name']


def get_trends(location_id, keys):
    """
    get Twitter trending topics for a location
    @param location_id: woeid for the location
    @param keys: Keys object that include the 4 access tokens
    @return: list of Topic objects contaiing teh trends
    """
    raw = get_api(keys).trends_place(location_id)
    trends = [Topic(id=None, name=trend['name'], volume=trend['tweet_volume'], tweets=[]) for trend in raw[0]['trends'] if
              trend['tweet_volume']]
    return trends


def get_stream(topics, keys, logger=None):
    """
    listen to upcoming tweets for certain topics and return a list of saple tweets
    @param topics: list of topics to listen to
    @param keys: Keys object that include the 4 access tokens
    @param logger: optional. Logging object to be used for tracking
    @return: List of sample tweets
    """
    api = get_api(keys)
    tweets = {i.lower(): [] for i in topics}

    listener = TweetListener(api, topics, tweets, limit=5, logger=logger)
    stream = tweepy.Stream(auth=api.auth, listener=listener)
    stream.filter(track=topics, languages=['en'], is_async=False)
    return tweets
