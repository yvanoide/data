from pymongo import MongoClient
from bson import ObjectId

# Connexion à MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db_image = client['image']
files_collection = db_image['fs.files']

# ID à rechercher (remplacez 'votre_id' par l'ID réel que vous souhaitez rechercher)
id_to_find = '666c49b4a502808b7f3c712f'

# Convertir l'ID en ObjectId
query_id = ObjectId(id_to_find)

# Rechercher le document par ID
document = files_collection.find_one({"_id": query_id})

if document:
    print(f"Document trouvé : {document}")
else:
    print("Aucun document trouvé avec cet ID.")

# Fermer la connexion à MongoDB
client.close()
