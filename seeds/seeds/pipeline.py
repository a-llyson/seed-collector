import pymongo
import logging
from itemadapter import ItemAdapter

class MongoPipeline():

    collection_name = 'greta'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        logging.info(f"login? {self.client}")
        self.db = self.client[self.mongo_db]
        logging.info(f"db? {self.db}")
        print(self.db.command("ismaster"))
        try:
            self.client.admin.command('ping')
        except ConnectionFailure:
            print("Server not available")


    
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        logging.info(f"in progress: {item}")
        logging.info(f"db: {self.db}")
        logging.info(f"collection: {self.collection_name}")
        logging.info(f"together: {self.db[self.collection_name]}")
        logging.info(f"item inserting: {ItemAdapter(item).asdict()}")
        res = self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        
        logging.info("processed item")
        print(res)
        print(self.db[self.collection_name].find_one())
        return item