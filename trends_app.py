# TrendTracker.py
""" Main trend tracker file """

import twitter
from datetime import datetime
from common.storage import Storage
from common.master_list import MasterList
from common.keys import Keys
from operator import attrgetter
import pandas as pd
import sys

import logging

logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.FileHandler("trends_app.log"),
                        logging.StreamHandler(sys.stdout)
                    ], format='%(asctime)s - %(message)s')

LOCATION_ID = 1968212


if __name__ == '__main__':
    keys = Keys()
    storage = Storage(keys.mongo_db_connection)
    ms = MasterList(storage)
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        logging.info('Starting to save into MongoDB...')
        try:
            topics = twitter.get_trends(LOCATION_ID, keys)
        except IndexError as e:#Exception as e:
            logging.error(e)
        else:
            tweets = twitter.get_stream([topic.name for topic in topics], keys)
            for topic in topics:
                topic.id = ms.get_id(topic.name)
                topic.tweets = tweets[topic.name.lower()]

            storage.save_time_topics(datetime.now(), topics)
            logging.info('Saved trends to MondoDB')

