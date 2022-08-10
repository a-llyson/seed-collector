import pymongo
from itemadapter import ItemAdapter

class MongoPipeline:
    collection_name = 'seed_collector'

    def __init__(self) -> None:
        