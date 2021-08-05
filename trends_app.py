# TrendTracker.py
""" Main trend tracker file """

import twitter
from datetime import datetime
from common.storage import TrendStorage as TS
from operator import attrgetter
import pandas as pd
import sys
#from flask import Flask, request
#from flask_restful import Resource, Api
#from flask import jsonify

import logging
logging.basicConfig(level=logging.INFO, 
    handlers=[  
        logging.FileHandler("trends_app.log"),
        logging.StreamHandler(sys.stdout) 
    ], format='%(asctime)s - %(message)s')

FILE_NAME = 'trends.csv'
LOCATION_ID = 23424852

#application = Flask(__name__)
#api = Api(application)

#class Topics(Resource):
#    def get(self):
#        ts = TS(FILE_NAME)
#        data = ts.load_mongo()
#        results = {'data' : data}
#        return jsonify(results)


#class TopicsDate(Resource):
#    def get(self, date):
#        ts = TS(FILE_NAME)
#        search_date=parser.parse(date)
#        data = ts.load_mongo(search_date)
#        results = {'data' : data}
#        return jsonify(results)

def sort_trends(trends):
    trends.sort(key=attrgetter('date', 'time'))
    for daily in trends:
        daily.topics.sort(key=attrgetter('volume'), reverse=True)
    return trends

def print_trends():
    trends = sort_trends(TS(FILE_NAME).load())
    for daily in trends:
        print(f'{daily.date:<10}')
        for topic in daily.topics:
            print(f'{"":<10} {topic.name:<15} {topic.volume:>10}')

def remove_duplicates(trends):
    last_date=''
    size = len(trends)
    i = 0
    while i < size:
        if trends[i].date == last_date:
            del trends[i]
            size -= 1
        else:
            last_date = trends[i].date
            i += 1

def min_topics_num(trends):
    minima = 0
    for daily in trends:
        if minima==0 or len(daily.topics)<minima:
            minima = len(daily.topics)
    return minima

def volume_by_topic(trends):
    trends = sort_trends(TS(FILE_NAME).load())
    remove_duplicates(trends)
    dates = [daily.date for daily in trends]
    topics = {}
    date_index = 0
    while date_index<len(dates):
        for topic in trends[date_index].topics:
            if topic.name not in topics.keys():
                topics[topic.name] = [0]*len(dates)
            topics[topic.name][date_index] = topic.volume
        date_index += 1
    df = pd.DataFrame(data=topics, index=dates)
    return df

def topic_by_date(trends):
    trends = sort_trends(TS(FILE_NAME).load())
    remove_duplicates(trends)
    minimum_topics = min_topics_num(trends)
    dates = [daily.date for daily in trends]
    topics = {}
    for daily in trends:
        topics[daily.date]=[f'{topic.name} ({topic.volume/1000:.0f}k)' for topic in daily.topics[:minimum_topics]]
    df = pd.DataFrame(data=topics)
    return df

#api.add_resource(Topics, '/topics')
#api.add_resource(TopicsDate, '/topics_date/<date>')

if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1] == 'save':
        logging.info('Starting to save into MongoDB...')
        ts = TS(FILE_NAME)
        try:
            topics = twitter.get_trends(LOCATION_ID)
        except Exception as e:
            logging.error(e)
        else:
            tweets = twitter.get_stream([topic.name for topic in topics])
            for topic in topics:
                topic.tweets = tweets[topic.name.lower()]
            ts.append_mongo(datetime.now(), topics) 
            logging.info('Saved trends to MondoDB')

    elif len(sys.argv)>1 and sys.argv[1] == 'save-csv':
        logging.info('Starting to save to CSV...')
        ts = TS(FILE_NAME)
        try:
            ts.append_csv(str(datetime.now()), twitter.get_trends(LOCATION_ID)) 
        except Exception as e:
            logging.error(e)
        else:
            logging.info('Saved trends to CSV')
    #else:
    #    #application.run(port='5002')
    #    application.debug = True
    #    application.run()