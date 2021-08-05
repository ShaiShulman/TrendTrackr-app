# storage.py
""" provides storage for the trends """
import csv
import uuid
from dateutil import parser
from datetime import datetime
from pymongo import MongoClient
from common.data_structs import Topic, DailyTrends
from common.master_list import MasterList


def _get_db(conn_str):
    client = MongoClient(conn_str)
    db = client
    return db


class TrendStorage:

    def __init__(self, mongo_connection_str):
        self._db = _get_db(mongo_connection_str).TrendTracker

    def find_topic_id(self, base_name):
        results = self._db.find_one(
            {'base_name': base_name},
            {'id': 1})
        if results:
            return results['id']
        else:
            return None

    def _save_topic_to_master_list(self, base_name, name):
        new_id = uuid.uuid4().hex
        self._db.insert_one({
            'id': new_id,
            'base_name': base_name,
            'display_name': name})
        return new_id

    def save_time_topics(self, time, trends):
        data = {'date': time, 'topics': [
            {'id': ml.get_topic_id(topic.name), 'name': topic.name, 'volume': topic.volume, 'tweets': topic.tweets} for
            topic in trends]}
        _db.TrendTracker.topics.insert_one(data)

    def load(self):
        history = []
        with open(self.FILE_NAME, mode='r+', encoding='utf-8', newline='') as history_file:
            reader = csv.reader(history_file)
            for record in reader:
                try:
                    daily = DailyTrends(date=parser.parse(record[0]).date(), time=parser.parse(record[0]).time(),
                                        topics=[])
                except ValueError:
                    print("Error converting record")
                else:
                    i = 1
                    while i < len(record):
                        topic = Topic(name=record[i], volume=int(record[i + 1]))
                        daily.topics.append(topic)
                        i += 2
                    history.append(daily)

        print(f'{len(history)} records loaded')
        return history

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
