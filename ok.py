from pymongo import MongoClient

def test_mongo_connection():
    try:
        client = MongoClient('mongodb://root:pass12345@localhost:27017/?authSource=admin')
        db = client['yourDatabaseName']
        collections = db.list_collection_names()
        print("Collections:", collections)
        print("Connection successful!")
    except Exception as e:
        print("Failed to connect:", e)

if __name__ == "__main__":
    test_mongo_connection()
