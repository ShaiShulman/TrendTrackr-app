# master_list.py
""" Master list of unique topics and their alternate spellings and IDs """

from common.data_structs import UniqueTopic


def _get_base_name(name):
    source_name = name.replace('#', '')
    return source_name.lower()


class MasterList:
    def __init__(self, storage):
        self._storage = storage
        self._list = []

    def get_id(self, name):
        try:
            result = next(filter(lambda x:x.base_name == _get_base_name(name), self._list)).id
        except StopIteration:
            result = self._storage.find_topic_id(_get_base_name(name))
            if result:
                self._list.append(UniqueTopic(
                    result,
                    _get_base_name(name),
                    name
                ))
                return result
            else:
                return self.add_topic(_get_base_name(name))
        else:
            return result

    def add_topic(self, name):
        result = self._storage.save_topic_to_master_list(_get_base_name(name), name)
        self._list.append(UniqueTopic(
            result,
            _get_base_name(name),
            name
        ))
        return result


'''
        if existing_mongo:
            self._db = existing_mongo.TrendTracker.master_list
        else:
            self._db = mongo_client().TrendTracker.master_list
'''