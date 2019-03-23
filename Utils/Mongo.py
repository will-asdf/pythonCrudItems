import pymongo
from bson.json_util import dumps

class mongo_controller:
    def __init__(self, mongo_config):
        self.client = pymongo.MongoClient(mongo_config['connection'])
        self.db = self.client[mongo_config['database']]
        self.items_collection = self.db[mongo_config['collection']]

    def insert(self, item):
        self.items_collection.insert_one(item)

    def update(self, item_id, attrs):
        self.items_collection.find_one_and_update({'_id': item_id}, {'$set': attrs})

    def delete(self, item_id):
        self.items_collection.delete_one({'_id': item_id})

    def get_all(self):
        mongo_result = self.items_collection.find({})
        list_result = list(mongo_result)
        results = dumps(list_result)
        return results