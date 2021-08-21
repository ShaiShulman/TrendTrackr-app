# TrendTracker.py
""" Main trend tracker file """

import sys
import logging
import twitter
import argparse
from decimal import Decimal
from datetime import datetime
from common.keys import Keys
from common.storage import Storage
from common.master_list import MasterList


def init_args():
    parser = argparse.ArgumentParser(description='Collect Twitter trends for specific location')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--save', action='store', type=int, dest='location',
                       help='save trending topic for location (specify Twitter location id)')
    group.add_argument('-n', '--name', action='store',
                       help='extract topic history by base name')
    group.add_argument('-d', '--date', action='store',
                       help='extract trending topic for date')
    group.add_argument('-a', '--all', action='store_true',
                       help='extract trending topic for all days collected')
    group.add_argument('-stt', '--stats_topic', action='store', metavar='topic',
                       help='extract statistics for topic')
    group.add_argument('-sta', '--stats_all', action='store_true',
                       help='extract statistics for all')
    parser.add_argument('-nt', '--no_tweets', action='store_true',
                        help='omit sample tweets for each topic')
    parser.add_argument('-cl', '--closest_locations', action='store', nargs=2,
                        help='Show list of available locations closest to latitude and longitude')

    return parser.parse_args()


logging.basicConfig(level=logging.INFO,
                    handlers=[
                        logging.FileHandler("trends_app.log"),
                        logging.StreamHandler(sys.stdout)
                    ], format='%(asctime)s - %(message)s')

keys = Keys()
storage = Storage(keys.mongo_db_connection)

LOCATION_ID = 1968212
args = init_args()

if args.location:
    ms = MasterList(storage)
    logging.info(f'Collecting topics for location {args.location}')
    try:
        topics = twitter.get_trends(args.location, keys)
    except IndexError as e:  # Exception as e:
        logging.error(e)
    else:
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
    print(data)
if args.all:
    data = storage.load_daily_topics(include_tweets=not args.no_tweets)
    for i in data:
        print(i)
if args.date:
    date = datetime.strptime(args.date).date
    data = storage.load_daily_topics(date, include_tweets=not args.no_tweets)
    for i in data:
        print(i)
if args.stats_all or args.stats_topic:
    data = storage.load_topic_summary(topic_name=args.stats_topic if args.stats_topic else None)
    for i in data:
        print(i)

if args.closest_locations:
    locs = twitter.available_locations(keys, Decimal(args.closest_locations[0]), Decimal(args.closest_locations[1]))
    for i in locs:
        print(f'{i[0]}\t{i[1]}')
