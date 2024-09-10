import csv
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client['data']
collection = db['info']

# Lecture du fichier CSV et insertion des données dans MongoDB
with open('/home/yvanoide/iadev-python/djan/image.csv', 'r') as file:
    reader = csv.DictReader(file)
    collection.insert_many(reader)
