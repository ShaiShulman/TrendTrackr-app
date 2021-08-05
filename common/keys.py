import json
from os.path import dirname, abspath, join

DEFAULT_FILE_NAME = 'keys.json'


class Keys:
    def __init__(self, file_name=DEFAULT_FILE_NAME):
        f = open(join(dirname(dirname(abspath(__file__))), file_name), )
        data = json.load(f)
        self.twitter_consumer_key = data['twitter_consumer_key']
        self.twitter_consumer_secret = data['twitter_consumer_secret']
        self.twitter_access_token = data['twitter_access_token']
        self.twitter_access_token_secret = data['twitter_access_token_secret']
        self.mongo_db_connection = data['mongo_db_connection']
        f.close()
