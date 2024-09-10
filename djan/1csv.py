import os
import csv
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client['maths']
collection = db['info']

# Chemin vers le répertoire contenant le fichier CSV
directory = '/chemin/vers/votre/repertoire/'

# Nom du fichier CSV
filename = '/home/yvanoide/iadev-python/djan/csv/student-mat.csv'

# Chemin complet du fichier CSV
csv_file_path = os.path.join(directory, filename)

# Lecture du fichier CSV et insertion dans la base de données
with open(csv_file_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Insérer chaque ligne dans la collection MongoDB
        collection.insert_one(row)

print("Données insérées avec succès dans la collection MongoDB.")
