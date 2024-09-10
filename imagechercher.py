from pymongo import MongoClient

# Paramètres de connexion MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_DB_NAME = 'my_database_images'

def search_and_list_collections_with_keyword(keyword):
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_DB_NAME]
        collections = db.list_collection_names()

        found_collections = set()  # Utiliser un ensemble pour éviter les doublons

        for collection_name in collections:
            collection = db[collection_name]

            # Rechercher le mot-clé dans les titres et descriptions
            query = {'$or': [
                {'titre': {'$regex': keyword, '$options': 'i'}},
                {'description': {'$regex': keyword, '$options': 'i'}},
                {'mots-clés': {'$regex': keyword, '$options': 'i'}}
            ]}
            
            results = list(collection.find(query))

            if results:
                found_collections.add(collection_name)
        
        if found_collections:
            print(f"Collections contenant le mot-clé '{keyword}':")
            for collection in found_collections:
                print(f" - {collection}")
        else:
            print(f"Aucune collection trouvée contenant le mot-clé '{keyword}'.")
    
    finally:
        client.close()

if __name__ == '__main__':
    # Entrez le mot-clé à rechercher ici
    keyword = input("Entrez le mot-clé à rechercher: ")
    search_and_list_collections_with_keyword(keyword)
