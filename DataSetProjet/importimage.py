import csv
from pymongo import MongoClient

# Connexion à MongoDB (utilise tes paramètres existants)
client = MongoClient("mongodb://admin:admin123@localhost:27017/")
db = client['texte']  # Nom de la base de données

# Chemins des fichiers CSV
csv_files = {
    'brief_dataset': '/home/yvanoide/iadev-python/djanchat/Brief-Dataset-Consumption.csv'
}

# Fonction pour insérer les données CSV dans MongoDB
def insert_csv_to_mongo(collection_name, file_path):
    collection = db[collection_name]  # Sélectionner la collection
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Lire le fichier CSV comme un dictionnaire
        for row in reader:
            # Insérer chaque ligne dans la collection MongoDB
            collection.insert_one(row)

# Insérer les données de chaque fichier CSV dans les collections correspondantes
for collection_name, csv_file in csv_files.items():
    insert_csv_to_mongo(collection_name, csv_file)
    print(f"Données de {csv_file} insérées dans la collection '{collection_name}'.")

print("Importation terminée.")
