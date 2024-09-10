import pandas as pd
from pymongo import MongoClient
import os

# Configuration de la connexion MongoDB
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_DB_NAME = 'my_database'

def upload_csv_to_mongodb(csv_file_path):
    # Extraire le nom de la collection à partir du nom du fichier CSV
    collection_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    
    # Connexion à MongoDB
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    collection = db[collection_name]
    
    # Lire le fichier CSV en DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Convertir le DataFrame en une liste de dictionnaires
    data = df.to_dict(orient='records')
    
    # Insérer les documents dans la collection MongoDB
    if data:
        collection.insert_many(data)
        print(f"{len(data)} documents insérés dans la collection '{collection_name}'")
    else:
        print("Le fichier CSV est vide ou n'a pas pu être lu.")
    
    # Fermer la connexion
    client.close()

if __name__ == '__main__':
    # Remplacez 'your_file.csv' par le chemin vers votre fichier CSV
    csv_file_path = '/home/yvanoide/iadev-python/data - Copie/ProjetDatasets/src/datasets/brief-dataset-consumption1_kwt0BVU.csv'
    
    upload_csv_to_mongodb(csv_file_path)
