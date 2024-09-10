from pymongo import MongoClient

MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_DB_NAME = 'my_database'

def test_mongo_connection():
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_DB_NAME]
        collections = db.list_collection_names()
        print(f"Collections in database '{MONGO_DB_NAME}': {collections}")
    finally:
        client.close()

if __name__ == '__main__':
    test_mongo_connection()