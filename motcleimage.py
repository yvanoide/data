from pymongo import MongoClient

# URI de connexion à MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
# Nom de la base de données
MONGO_DB_NAME = 'my_database_images'

def ajouter_champ_mots_cles_et_supprimer_image():
    client = MongoClient(MONGO_URI)
    try:
        # Connexion à la base de données
        db = client[MONGO_DB_NAME]
        # Récupération des noms de toutes les collections
        collections = db.list_collection_names()
        for collection_name in collections:
            # Sélection de la collection actuelle
            collection = db[collection_name]
            # Mise à jour de chaque document en ajoutant le champ 'mots-clés' et en supprimant le champ 'image'
            collection.update_many({}, {'$set': {'mots-clés': ['image', 'jpg']}, '$unset': {'image': ''}})
            print(f"Champ 'mots-clés' ajouté et champ 'image' supprimé dans la collection '{collection_name}'")
    finally:
        # Fermeture de la connexion
        client.close()

if __name__ == '__main__':
    ajouter_champ_mots_cles_et_supprimer_image()
