from pymongo import MongoClient

# Indexes
# ==============
# db.data.source.airbnb_listing.createIndex({location:"2dsphere"});

class MongoDb:

    def __init__(self, database, host='localhost', port=27017):
        client = MongoClient(host, port, connect=False)
        self.db = client[database]

    def load(self, collection_class, filters=None, columns=None):
        filters = filters or {}

        collection = collection_class.__module__

        for result in self.db[collection].find(filters, columns):
            yield collection_class(result)

    def save(self, record):
        collection = record.__module__

        value = record.value()
        value['_id'] = record.key()

        self.db[collection].save(value)
