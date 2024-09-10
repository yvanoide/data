from pymongo import MongoClient

# Paramètres de connexion MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_DB_NAME = 'my_database'

def search_by_keyword(keyword):
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_DB_NAME]
        metadata_collection = db['dataset(metadata)']
        
        # Rechercher le mot-clé dans les titres et descriptions
        query = {'$or': [
            {'titre': {'$regex': keyword, '$options': 'i'}},
            {'description': {'$regex': keyword, '$options': 'i'}}
        ]}
        
        results = list(metadata_collection.find(query))
        
        if results:
            print(f"Datasets trouvés contenant le mot-clé '{keyword}':")
            for result in results:
                print(f" - {result.get('titre', 'Sans titre')}")
        else:
            print(f"Aucun dataset trouvé contenant le mot-clé '{keyword}'.")
    
    finally:
        client.close()

if __name__ == '__main__':
    # Entrez le mot-clé à rechercher ici
    keyword = input("Entrez le mot-clé à rechercher: ")
    search_by_keyword(keyword)
