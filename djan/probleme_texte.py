from pymongo import MongoClient

def afficher_documents_ecrit():
    try:
        # Connexion à MongoDB
        client = MongoClient('mongodb://root:pass12345@localhost:27017/')
        
        # Nom de la base de données MongoDB
        database_name = 'texte'
        
        # Nom de la collection MongoDB
        collection_name = 'ecrit'
        
        # Récupérer la collection
        db = client[database_name]
        collection = db[collection_name]
        
        # Récupérer tous les documents dans la collection
        documents = collection.find()
        
        # Afficher les documents
        print("Affichage des documents dans la collection 'ecrit':")
        for document in documents:
            print("ID:", document['_id'])
            print("Theme:", document['theme'])
            if 'colonnes' in document:
                print("Colonnes:", document['colonnes'])
            print("\n")
        
        # Fermer la connexion à MongoDB
        client.close()

    except Exception as e:
        print(f"Erreur lors de la récupération des documents : {e}")

# Appel de la fonction pour afficher les documents dans la collection "ecrit"
afficher_documents_ecrit()
