from pymongo import MongoClient

# Informations de connexion à MongoDB
username = 'admin'       # Remplacez par votre nom d'utilisateur
password = 'admin123'    # Remplacez par votre mot de passe
db_name = 'texte'        # Nom de la base de données

# Connexion au client MongoDB
client = MongoClient(f"mongodb://{username}:{password}@localhost:27017/")

# Sélection de la base de données
db = client[db_name]

# Récupération de la liste des collections dans la base de données
collections = db.list_collection_names()

# Affichage de la liste des collections
print("Collections dans la base de données 'texte' :")
for collection_name in collections:
    print(f"- {collection_name}")

# Fermeture de la connexion
client.close()
