# TrendTracker.py
"""
Look for Twitter trending topics in certain location (woeid - translated from place name) and save the topics and sample
tweets in a MongoDB database

Module expects a keys.json file in the root folder with the twitter api keys and MongoDB connection string
MongoDB should have a database names TrendTracker with two collections: masterlist and topics

(c) Shai Shulman (shaishulman@gmail.com), 2021
"""

import sys
import logging
import twitter
import argparse
from datetime import datetime
from common.keys import Keys
from common.storage import Storage
from common.master_list import MasterList

_DATE_FORMAT = "%d/%m/%Y"


def init_args():
    parser = argparse.ArgumentParser(description='Collect Twitter trends for specific location')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--save', action='store', dest='location',
                       help='save trending topic for location (specify Twitter woeid or location name (in '
                            'qoutes if longer than one word)')
    group.add_argument('-n', '--name', action='store',
                       help='extract topic history by base name')
    group.add_argument('-d', '--date', action='store', metavar='from_date',
                       help=f'extract trending topic from date (from date in format {_DATE_FORMAT})')
    group.add_argument('-a', '--all', action='store_true',
                       help='extract trending topic for all days collected')
    group.add_argument('-stt', '--stats_topic', action='store', metavar='topic',
                       help='extract statistics for topic')
    group.add_argument('-sta', '--stats_all', action='store_true',
                       help='extract statistics for all')
    parser.add_argument('-nt', '--no_tweets', action='store_true',
                        help='omit sample tweets for each topic')

    return parser.parse_args()


logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.FileHandler("trends_app.log"),
                        logging.StreamHandler(sys.stdout)
                    ], format='%(asctime)s - %(message)s')

keys = Keys()
storage = Storage(keys.mongo_db_connection)

args = init_args()

if args.location:
    woeid, loc_name = twitter.get_location(args.location, keys)
    logging.info(f'Collecting topics for location {loc_name} ({woeid})')
    ms = MasterList(storage)
    try:
        topics = twitter.get_trends(woeid, keys)
    except IndexError as e:  # Exception as e:
        logging.error(e)
    else:
        logging.info(f'Collected {len(topics)} trending topics')
        if not args.no_tweets:
            tweets = twitter.get_stream([topic.name for topic in topics], keys)
        else:
            tweets = []
        for topic in topics:
            logging.info(f'Collecting sample tweets for topic {topic.name}')
            topic.id = ms.get_id(topic.name)
            topic.tweets = tweets[topic.name.lower()]
        logging.info(f'Saving {len(topics)} topics to MongoDB')
        storage.save_time_topics(datetime.now(), topics)
        logging.info('Save completed')
if args.name:
    data = storage.load_topic_history(topic_base_name=args.name)
    if data:
        print('\n'.join([str(s) for s in data]))
    else:
        print('No matching data found!')
if args.all:
    data = storage.load_daily_topics(include_tweets=not args.no_tweets)
    for i in data:
        print(i)
if args.date:
    date = datetime.strptime(args.date, _DATE_FORMAT).date()
    data = storage.load_daily_topics(from_date=date, include_tweets=not args.no_tweets)
    for i in data:
        print(i)
if args.stats_all or args.stats_topic:
    data = storage.load_topic_summary(topic_name=args.stats_topic if args.stats_topic else None)
    for i in data:
        print(i)
