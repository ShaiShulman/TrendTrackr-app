from pymongo import MongoClient
from django.conf import settings
from common.data_structs import Topic, DailyTrends, TopicSummary

_mongo_client = {}


def mongo_client():
    client = _mongo_client.get('client', None)
    if client is None:
        client = MongoClient(settings.MONGODB_URI)
        _mongo_client['client'] = client
    return client


def load_topics(date=None, topic_id=None, include_tweets=False):
    db = mongo_client().TrendTracker
    if date is None:
        cursor = db.topics.find({})
    elif isinstance(date, datetime):
        cursor = db.topics.find_one({'date': {'$lt': datetime(date.year, date.month, date.day, 23, 59, 59),
                                              '$gte': datetime(date.year, date.month, date.day, 0, 0, 0)}})
    elif topic_id:
        cursor = db.topics.find({'topics.id': topic_id})
    else:
        return None
    data = []
    for document in cursor:
        daily = DailyTrends(date=str((document['date']).date()),
                            time=str((document['date']).time()),
                            topics=[Topic(name=topic['name'],
                                          volume=topic['volume'],
                                          id=topic['id'],
                                          tweets=topic.get('tweets', []) if include_tweets else [])
                                    for topic in document['topics']])
        data.append(daily)
    return data


def load_summary(topic_id=None):
    db = mongo_client().TrendTracker
    params = [{'$unwind': '$topics'},
              {'$group': {'_id': '$topics.id', 'total_volume': {'$sum': '$topics.volume'},
                          'first_date': {'$min': '$date'}, 'last_date': {'$max': '$date'}, 'total_days': {'$sum': 1}}},
              {'$lookup': {'from': 'master_list', 'localField': '_id', 'foreignField': 'id', 'as': 'master'}},
              {'$unwind': '$master'},
              {'$project': {'id': 1, 'total_num': 1, 'first_date': 1, 'last_date': 1, 'total_volume': 1,
                            'total_days': 1, 'name': '$master.display_name'}},
              {'$sort': {'base_name': 1}}]

    if topic_id:
        params.insert(1, {'$match': {'topics.id': topic_id}})
    cursor = db.topics.aggregate(params)
    data = []
    for document in cursor:
        data.append(TopicSummary(id=document['_id'],
                                 name=document['name'],
                                 total_days=document['total_days'],
                                 total_volume=document['total_volume'],
                                 first_date=document['first_date'],
                                 last_date=document['last_date']))
    return data


def load_topic_history(topic_id, include_name=False):
    if include_name:
        params = [{'$unwind': '$topics'},
                  {'$match': {'topics.id': topic_id}},
                  {'$lookup': {'from': 'master_list', 'localField': 'topics.id', 'foreignField': 'id', 'as': 'master'}},
                  {'$unwind': '$master'},
                  {'$project': {'id': '$topics.id', 'date': 1, 'volume': '$topics.volume',
                                'name': '$master.display_name'}},
                  {'$sort': {'date': 1}}]
    else:
        params = [{'$unwind': '$topics'},
                  {'$match': {'topics.id': topic_id}},
                  {'$unwind': '$topics'},
                  {'$project': {'id': '$topics.id', 'date': 1, 'volume': '$topics.volume'}},
                  {'$sort': {'date': 1}}]
    db = mongo_client().TrendTracker
    return list(db.topics.aggregate(params))
