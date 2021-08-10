# storage.py
""" provides storage for the trends """
import csv
import uuid
from dateutil import parser
from datetime import datetime
from pymongo import MongoClient
from common.data_structs import Topic, DailyTopics
from common.master_list import MasterList


def _get_db(conn_str):
    client = MongoClient(conn_str)
    db = client
    return db


class Storage:

    def __init__(self, mongo_connection_str):
        self._db = _get_db(mongo_connection_str).TrendTracker

    def find_topic_id(self, base_name):
        results = self._db.master_list.find_one(
            {'base_name': base_name},
            {'id': 1})
        if results:
            return results['id']
        else:
            return None

    def save_topic_to_master_list(self, base_name, name):
        new_id = uuid.uuid4().hex
        self._db.master_list.insert_one({
            'id': new_id,
            'base_name': base_name,
            'display_name': name})
        return new_id

    def save_time_topics(self, time, trends):
        data = {'date': time, 'topics': [
            {'id': topic.id, 'name': topic.name, 'volume': topic.volume, 'tweets': topic.tweets} for
            topic in trends]}
        self._db.topics.insert_one(data)

    def load_topics(self, date=None, topic_id=None, topic_base_name=None, include_tweets=False):
        query = {}
        if isinstance(date, datetime):
            query['date'] = {'$lt': datetime(date.year, date.month, date.day, 23, 59, 59),
                             '$gte': datetime(date.year, date.month, date.day, 0, 0, 0)}
        if topic_id:
            query['topics.id'] = topic_id
        if topic_base_name:
            query['topics.name'] = topic_base_name
            cursor = self._db.topics.find({'topics.id': topic_id})
        cursor = self._db.topics.find(query)
        data = []
        for document in cursor:
            daily = DailyTopics(time=str((document['date'])),
                                topics=[Topic(name=topic['name'],
                                              volume=topic['volume'],
                                              id=topic['id'],
                                              tweets=topic.get('tweets', []) if include_tweets else [])
                                        for topic in document['topics']])
            data.append(daily)
        return data


'''
    def load_mongo(self, date=None):
        db = _get_db()
        if date == None:
            cursor = db.TrendTracker.topics.find({})
        elif isinstance(date, datetime):
            cursor = db.TrendTracker.topics.find_one({'date': {
                '$lt': datetime(date.year, date.month, date.day, 23, 59, 59),
                '$gte': datetime(date.year, date.month, date.day, 0, 0, 0)}})
        else:
            return None
        data = []
        for document in cursor:
            daily = DailyTrends(date=str((document['date']).date()),
                                time=str((document['date']).time()),
                                topics=[Topic(name=topic['name'], volume=topic['volume']) for topic in
                                        document['topics']])
            data.append(daily)
        return data
'''
