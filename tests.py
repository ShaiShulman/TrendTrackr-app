import unittest
from common.keys import Keys
from common.storage import Storage


def get_db():
    keys = Keys()
    return Storage(keys.mongo_db_connection)


class TestDb(unittest.TestCase):
    def test_find_topic_id(self):
        storage = get_db()
        self.assertTrue(storage.find_topic_id('indiedev'))
        self.assertFalse(storage.find_topic_id('indiedfdfsdfsdev'))

    def test_load_topic_ic(self):
        storage = get_db()
        self.assertTrue(storage.load_daily_topics(topic_id='3e0c7ee5d8934f8782a993286ce36049'))
        self.assertTrue(storage.load_daily_topics(topic_base_name='poland'))

    def test_load_topic_history(self):
        storage = get_db()
        self.assertTrue(storage.load_topic_history(topic_id='3e0c7ee5d8934f8782a993286ce36049'))

    def test_load_topic_history_error(self):
        storage = get_db()
        with self.assertRaises(ValueError):
            result = storage.load_topic_history(topic_id='fdfdf', topic_base_name='fdfsd')
