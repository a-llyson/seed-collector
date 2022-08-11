import pymongo
import logging


class MongoPipeline():

    collection_name = 'greta'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        logging.info(mongo_uri)
        logging.info(mongo_db)

    @classmethod
    def from_crawler(cls, crawler):
        mongo_uri=crawler.settings.get('MONGO_URI')
        mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        logging.INFO(mongo_uri)
        logging.INFO(mongo_db)
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        logging.info("processed item")
        logging.info(item)
        return item