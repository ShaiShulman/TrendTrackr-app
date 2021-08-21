# storage.py
"""
Provides interface with MongoDB for storing and retreiving master list of topics and daily ropics
"""
import uuid
from dateutil import parser
from datetime import datetime
from pymongo import MongoClient
from common.data_structs import Topic, DailyTopics, DailyVolume, TopicSummary
from common.master_list import MasterList


def _get_db(conn_str):
    """
    get object for MongoDB client
    @param conn_str: full MongoDB connection string
    @return: db object
    """
    client = MongoClient(conn_str)
    db = client
    return db


class Storage:

    def __init__(self, mongo_connection_str):
        """
        Constructor for storage object
        @param mongo_connection_str: full MongoDB connection string
        """
        self._db = _get_db(mongo_connection_str).TrendTracker

    def find_topic_id(self, base_name):
        """
        get id of a topic from the master list
        @param base_name: base name to search (lowercase without #)
        @return: id (None if not found)
        """
        results = self._db.master_list.find_one(
            {'base_name': base_name},
            {'id': 1})
        if results:
            return results['id']
        else:
            return None

    def save_topic_to_master_list(self, base_name, name):
        """
        add new topic to the master list
        @param base_name: base name (lowercase withotu #)
        @param name: display name (as shown in Twitter app)
        @return: id of new topic
        """
        new_id = uuid.uuid4().hex
        self._db.master_list.insert_one({
            'id': new_id,
            'base_name': base_name,
            'display_name': name})
        return new_id

    def save_time_topics(self, time, topics):
        """
        save snapshot of collected trending topics in MongoDB
        @param time: time+date of collection
        @param topics: list of Topic objects (can also include the sample tweets)
        """
        data = {'date': time, 'topics': [
            {'id': topic.id, 'name': topic.name, 'volume': topic.volume, 'tweets': topic.tweets} for
            topic in topics]}
        self._db.topics.insert_one(data)

    def load_daily_topics(self, date=None, topic_id=None, topic_base_name=None, include_tweets=True):
        """
        load the trending topics for each date from MongoDB
        @param date: optional. date to search for (time part will be ignored).
        @param topic_id: optional. id of topic to search.
        @param topic_base_name: optional. base name of topic to seach. will search by only one parameter.
        @param include_tweets: shoudl sample sweets be included in the result.
        @return: list of daily topic objects based on query. will return all dates if no query is provided.
        """
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

    def load_topic_history(self, topic_id=None, topic_base_name=None, include_name=False):
        """
        load tweeting volume of each topic from MongoDB
        @param topic_id: optional. id of topic to seach.
        @param topic_base_name: optional. base name of topic to search. Will search be either topic_id or name
        @param include_name: True name should be included in output (only of topic_id is provided).
        @return: List of DailyVolume objects based on criteria. Will return all of no criteria is provided.
        """
        query = [{'$unwind': '$topics'}]
        if topic_id and not topic_base_name:
            query.append({'$match': {'topics.id': topic_id}})
        elif topic_base_name and not topic_id:
            query.append({'$match': {'topics.name': topic_base_name}})
        else:
            raise ValueError('either topic id or name must be provided')
        if include_name:
            query.extend([
                {'$lookup': {'from': 'master_list', 'localField': 'topics.id', 'foreignField': 'id',
                             'as': 'master'}},
                {'$unwind': '$master'},
                {'$project': {'id': '$topics.id', 'date': 1, 'volume': '$topics.volume',
                              'name': '$master.display_name'}}
            ])
        else:
            query.extend([
                {'$unwind': '$topics'},
                {'$project': {'id': '$topics.id', 'date': 1, 'volume': '$topics.volume'}}
            ])
        query.append({'$sort': {'date': 1}})
        raw_data = list(self._db.topics.aggregate(query))
        data = [DailyVolume(daily['date'].date(), daily['volume']) for daily in raw_data]
        if len(data) > 0:
            if include_name:
                return data, data[0]['name']
            else:
                return data
        else:
            return None

    def load_topic_summary(self, topic_id=None, topic_name=None):
        """
        Load summary statistics for topics from MongoDB
        @param topic_id: optional. id of topic to search.
        @param topic_name: optional. name of topic to search. Will search by either id or name.
        @return: List of TopicSummary objects.
        """
        query = [{'$unwind': '$topics'}]
        if topic_id:
            query.extend([{'$match': {'topics.id': topic_id}}])

        query.extend([{'$group': {'_id': '$topics.id', 'total_volume': {'$sum': '$topics.volume'},
                                  'first_date': {'$min': '$date'}, 'last_date': {'$max': '$date'},
                                  'total_days': {'$sum': 1}}},
                      {'$lookup': {'from': 'master_list', 'localField': '_id', 'foreignField': 'id', 'as': 'master'}},
                      {'$unwind': '$master'}])
        if topic_name:
            query.extend([{'$match': {'master.base_name': topic_name}}])
        query.extend([{'$project': {'id': 1, 'total_num': 1, 'first_date': 1, 'last_date': 1, 'total_volume': 1,
                                    'total_days': 1, 'name': '$master.display_name'}},
                      {'$sort': {'base_name': 1}}])

        raw_data = list(self._db.topics.aggregate(query))
        return [TopicSummary(id=document['_id'],
                             name=document['name'],
                             total_days=document['total_days'],
                             total_volume=document['total_volume'],
                             first_date=document['first_date'],
                             last_date=document['last_date']) for document in raw_data]
        return data
