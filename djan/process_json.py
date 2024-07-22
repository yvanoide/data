import os
import json
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')

# Nom de la base de données
db = client['json']

# Chemin vers le fichier JSON unique
json_file_path = '/home/yvanoide/iadev-python/djan/output.json'

# Lecture et insertion des données JSON dans MongoDB
def insert_json_file_to_mongodb(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        # Le nom de la collection est le nom du fichier sans l'extension .json
        collection_name = os.path.splitext(os.path.basename(file_path))[0]
        collection = db[collection_name]
        if isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)
    print(f'Données insérées dans la collection: {collection_name}')

# Appel de la fonction pour insérer le fichier JSON
insert_json_file_to_mongodb(json_file_path)
