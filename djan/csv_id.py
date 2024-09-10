from pymongo import MongoClient
from bson.objectid import ObjectId

def find_collection_by_id(database_name, search_id):
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client[database_name]

    # Lister toutes les collections
    collections = db.list_collection_names()

    # Chercher l'ID dans chaque collection
    for collection_name in collections:
        collection = db[collection_name]

        # Tenter de convertir l'ID en ObjectId
        try:
            search_object_id = ObjectId(search_id)
            # Rechercher le document par ObjectId
            document = collection.find_one({'_id': search_object_id})
            if document:
                client.close()
                return {
                    'collection_name': collection_name,
                    'document': document
                }
        except:
            # Si la conversion échoue, rechercher l'ID comme une chaîne de caractères
            document = collection.find_one({'_id': search_id})
            if document:
                client.close()
                return {
                    'collection_name': collection_name,
                    'document': document
                }

    # Fermer la connexion s'il n'y a pas de résultats
    client.close()
    return None

# ID que vous voulez rechercher
search_id = '666b079b0d1be4cb9ba07101'
result = find_collection_by_id('data', search_id)

if result:
    print(f"Collection trouvée : {result['collection_name']}")
    print("Document correspondant :", result['document'])
else:
    print("Aucune collection correspondante trouvée.")
