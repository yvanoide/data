# settings.py

from pymongo import MongoClient

# Connexion MongoDB
MONGO_DB_SETTINGS = {
    'HOST': 'mongodb://admin:admin123@localhost:27017/',
    'DB_TEXTE': 'texte',
    'DB_IMAGE': 'image'
}

# Configuration MongoDB dans settings.py
client = MongoClient(MONGO_DB_SETTINGS['HOST'])
db_texte = client[MONGO_DB_SETTINGS['DB_TEXTE']]
db_image = client[MONGO_DB_SETTINGS['DB_IMAGE']]

# Afficher pour confirmer la connexion
print(f"Connecté à MongoDB : Base de données Texte = {MONGO_DB_SETTINGS['DB_TEXTE']}, Image = {MONGO_DB_SETTINGS['DB_IMAGE']}")
