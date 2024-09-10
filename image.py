from pymongo import MongoClient

# Définir les paramètres de connexion
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_DB_NAME = 'my_database_images'

def check_database():
    # Connexion à MongoDB
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]

    # Liste des collections dans la base de données
    collections = db.list_collection_names()
    print("Collections dans la base de données :", collections)

    # Vérifier le contenu de chaque collection
    for collection_name in collections:
        collection = db[collection_name]
        count = collection.count_documents({})
        print(f"Collection '{collection_name}' contient {count} documents.")

        # Afficher les premiers documents si la collection contient des documents
        if count > 0:
            print(f"Premiers documents de la collection '{collection_name}':")
            for doc in collection.find().limit(3):
                print(doc)

if __name__ == '__main__':
    check_database()
