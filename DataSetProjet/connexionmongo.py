from pymongo import MongoClient

# Connexion MongoDB
MONGO_DB_SETTINGS = {
    'HOST': 'mongodb://admin:admin123@localhost:27017/',
    'DB_TEXTE': 'texte',
    'DB_IMAGE': 'image'
}

# Configuration MongoDB
client = MongoClient(MONGO_DB_SETTINGS['HOST'])
db_texte = client[MONGO_DB_SETTINGS['DB_TEXTE']]
db_image = client[MONGO_DB_SETTINGS['DB_IMAGE']]

def print_collections(db, db_name):
    """Affiche les collections dans une base de données spécifiée."""
    try:
        collections = db.list_collection_names()
        print(f"\nCollections dans la base de données '{db_name}' :")
        if not collections:
            print("Aucune collection trouvée.")
        else:
            for collection_name in collections:
                print(f"- {collection_name}")
    except Exception as e:
        print(f"Une erreur s'est produite lors de l'affichage des collections pour '{db_name}' : {e}")

# Afficher les collections pour chaque base de données
print_collections(db_texte, MONGO_DB_SETTINGS['DB_TEXTE'])
print_collections(db_image, MONGO_DB_SETTINGS['DB_IMAGE'])
