import os
import gridfs
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client['photosquelette']
fs = gridfs.GridFS(db)

# Chemin vers le répertoire contenant les images
directory = '/home/yvanoide/iadev-python/ProjetDatasets - Copie/images'

# Importer chaque image dans GridFS
for filename in os.listdir(directory):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Ajoutez les extensions d'image que vous souhaitez prendre en charge
        filepath = os.path.join(directory, filename)
        with open(filepath, 'rb') as f:
            fs.put(f, filename=filename)
