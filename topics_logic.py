# topic_logic.py

from common.db import load_topics, mongo_client, load_summary, load_topic_history
from common.master_list import MasterList
from operator import attrgetter


def create_master_list():
    ml = MasterList()
    trends = load_topics()
    topics_updated = {}
    for daily in trends:
        for topic in daily.topics:
            new_id = ml.get_topic_id(topic.name)
            if new_id != topic.id:
                mongo_client().TrendTracker.topics.update_many({'topics.name': topic.name},
                                                               {'$set': {'topics.$.id': new_id}})


def add_ids_to_trends(trends):
    ml = MasterList()
    for daily in trends:
        for topic in daily.topics:
            topic.id = ml.get_topic_id(topic.name)
    ml.save_changes()


def _sort_trends(trends):
    trends.sort(key=attrgetter('date', 'time'))
    for daily in trends:
        daily.topics.sort(key=attrgetter('volume'), reverse=True)


def _remove_duplicates(trends):
    last_date = ''
    size = len(trends)
    i = 0
    while i < size:
        if trends[i].date == last_date:
            del trends[i]
            size -= 1
        else:
            last_date = trends[i].date
            i += 1


def _min_topics_num(trends):
    minima = 0
    for daily in trends:
        if minima == 0 or len(daily.topics) < minima:
            minima = len(daily.topics)
    return minima


""" return topics by rank for each date """


def topic_by_date():
    trends = load_topics()
    _sort_trends(trends)
    _remove_duplicates(trends)
    minimum_topics = _min_topics_num(trends)
    dates = [daily.date for daily in trends]
    topics = []
    for daily in trends:
        topics.append({'date': daily.date,
                       'topics': [{'name': topic.name, 'volume': topic.volume, 'id': topic.id} for topic in
                                  daily.topics[:minimum_topics]]})
    return topics


""" return history for specific topic """


def topic_history(topic_id, include_name=False):
    history = load_topic_history(topic_id, include_name)
    results = [{'date': daily['date'].date(),
                'volume': daily['volume']} for daily in history]
    if len(results) > 0:
        if include_name:
            return results, history[0]['name']
        else:
            return results
    else:
        return None


def topic_tweets(topic_id):
    trends = load_topics(topic_id=topic_id, include_tweets=True)
    _sort_trends(trends)
    _remove_duplicates(trends)
    results = []
    for daily in trends:
        for num, topic in enumerate(daily.topics):
            if topic.id == topic_id:
                results.append({'date': daily.date,
                                'tweets': topic.tweets})

    if len(results) > 0:
        return results
    else:
        return None


def topics_summary():
    data = load_summary()
    if len(data) > 0:
        results = [{'id': topic.id,
                    'name': topic.name,
                    'total_days': topic.total_days,
                    'total_volume': topic.total_volume,
                    'first_date': topic.first_date,
                    'last_date': topic.last_date} for topic in data]
        return results
    else:
        return None
