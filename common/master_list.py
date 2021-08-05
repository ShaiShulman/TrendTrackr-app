# master_list.py
""" Master list of unique topics and their alternate spellings and IDs """

import uuid
from db import mongo_client


def _get_base_name(name):
    source_name = name.replace('#', '')
    return source_name.lower()


class MasterList():
    def __init__(self, existing_mongo=None):
        if existing_mongo:
            self._db = existing_mongo.TrendTracker.master_list
        else:
            self._db = mongo_client().TrendTracker.master_list

    def get_topic_id(self, name):
        results = self._db.find_one(
            {'base_name': _get_base_name(name)},
            {'id': 1})
        if results:
            return results['id']
        else:
            return self._add_topic(name)

    def _add_topic(self, name):
        new_id = uuid.uuid4().hex
        self._db.insert_one({
            'id': new_id,
            'base_name': _get_base_name(name),
            'display_name': name})
        return new_id

