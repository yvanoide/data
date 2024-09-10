from pymongo import MongoClient

# URI de connexion à MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
# Nom de la base de données
MONGO_DB_NAME = 'my_database'

def rechercher_par_mot_cle(mot_cle):
    client = MongoClient(MONGO_URI)
    try:
        # Connexion à la base de données
        db = client[MONGO_DB_NAME]
        # Récupération des noms de toutes les collections
        collections = db.list_collection_names()
        
        # Liste pour stocker les collections qui contiennent le mot-clé
        collections_avec_mot_cle = []

        # Recherche du mot-clé dans chaque collection
        for collection_name in collections:
            collection = db[collection_name]
            # Cherche les documents où le mot-clé est présent dans le champ 'mots-clés'
            count = collection.count_documents({'mots-clés': mot_cle})
            
            if count > 0:
                collections_avec_mot_cle.append(collection_name)
        
        if collections_avec_mot_cle:
            print(f"Collections contenant le mot-clé '{mot_cle}':")
            for coll in collections_avec_mot_cle:
                print(f" - {coll}")
        else:
            print(f"Aucune collection ne contient le mot-clé '{mot_cle}'.")
    
    finally:
        # Fermeture de la connexion
        client.close()

if __name__ == '__main__':
    # Entrez le mot-clé à rechercher ici
    mot_cle = input("Entrez le mot-clé à rechercher: ").strip()
    rechercher_par_mot_cle(mot_cle)
