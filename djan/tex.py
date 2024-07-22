from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('localhost', 27017, username='root', password='pass12345')
db = client['texte']  # Utilisation de la base de données nommée 'texte'
collection_ecrit = db['ecrit']  # Utilisation de la collection 'ecrit'

# Exemple de données à insérer dans 'ecrit'
data_ecrit = [
    {
        'theme': 'philosophie',
        'colonnes': 'Socrate est un philosophe grec du ve siècle av. J.-C., né vers -470/469 et mort en -399 à Athènes.'
    },
    {
        'theme': 'philosophie',
        'colonnes': 'La plupart de nos connaissances sur la vie de Socrate concernent le procès de -399.'
    },
    # Ajoutez autant d'entrées que nécessaire
]

# Insérer les données dans MongoDB
collection_ecrit.insert_many(data_ecrit)
print("Les données ont été insérées avec succès dans MongoDB dans la collection 'ecrit'.")
