import logging
import libs.database as database

from libs.config import MONGO_URI_DESTINATION, MONGO_DESTINATION_DATABASE, MONGO_DESTINATION_COLLECTION, MONGO_URI_SOURCE, MONGO_SOURCE_DATABASE, MONGO_SOURCE_COLLECTION

logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)

mongo_source = database.conn_mongodb(MONGO_URI_SOURCE, MONGO_SOURCE_DATABASE)
mongo_destination = database.conn_mongodb(MONGO_URI_DESTINATION, MONGO_DESTINATION_DATABASE)

def start():
    cursor = mongo_source[MONGO_SOURCE_COLLECTION]
    results = collection_iterator(cursor, limit=500)
    for item in results:
        migrate_records(item)
    
def records_count():
    return database.count(mongo_source[MONGO_SOURCE_COLLECTION])

def migrate_records(item):
    _id = item["_id"]
    if database.ifExist(mongo_destination[MONGO_DESTINATION_COLLECTION], _id):
       logger.debug("%s Already exist. Deleting..." %_id)
       try:
           database.delete(mongo_source[MONGO_SOURCE_COLLECTION], _id)
       except Exception as e:
            logger.error("Cleanup failed: %s" %e)
    else:
        try: 
            result = database.insert(mongo_destination[MONGO_DESTINATION_COLLECTION], item, None)
            if result:
                try:
                    database.delete(mongo_source[MONGO_SOURCE_COLLECTION], result)
                except Exception as e:
                    logger.error("Cleanup failed: %s" %e)
            logger.info("%s Successfully migrated" % str(result))
        except Exception as e:
            logger.error("Migration failed: %s" % e)

def collection_iterator(cursor, limit=1000):
        total_records = database.count(cursor)
        while True:
            try:
                results = database.find(cursor).limit(limit)
                print(total_records)
                if total_records <= 0:
                    count = database.count(cursor)
                    if count == 0:
                        break
            except Exception as e:
                logger.error(e)
                break
            for result in results:
                yield result
            total_records -= limit 

def main():
    start()
 
if __name__ == "__main__":
    main()