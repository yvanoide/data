from pymongo import MongoClient
from bson import ObjectId

# Fonction pour récupérer les données en fonction des critères de recherche
def get_data(query_texte=None, query_id=None):
    # Modifier avec vos informations d'authentification MongoDB
    username = 'root'
    password = 'pass12345'
    client = MongoClient('mongodb://{}:{}@localhost:27017/'.format(username, password))
    
    db = client['data']
    db_texte = client['texte']

    blocs_texte_data = []

    try:
        if query_id:
            obj_id = ObjectId(query_id)
            bloc = db_texte.ecrit.find_one({"_id": obj_id})
            if bloc:
                bloc_info = {
                    'theme': bloc['theme'],
                    'colonnes': " ".join(bloc['colonnes'].split())  # Supprime les espaces doubles, conserve les autres
                }
                blocs_texte_data.append(bloc_info)
        elif query_texte:
            blocs_texte = db_texte.ecrit.find({"theme": {"$regex": query_texte, "$options": "i"}})
            for bloc in blocs_texte:
                bloc_info = {
                    'theme': bloc['theme'],
                    'colonnes': " ".join(bloc['colonnes'].split())  # Supprime les espaces doubles, conserve les autres
                }
                blocs_texte_data.append(bloc_info)
        else:
            blocs_texte = db_texte.ecrit.find()
            for bloc in blocs_texte:
                bloc_info = {
                    'theme': bloc['theme'],
                    'colonnes': " ".join(bloc['colonnes'].split())  # Supprime les espaces doubles, conserve les autres
                }
                blocs_texte_data.append(bloc_info)

    except Exception as e:
        print(f"Error while querying MongoDB: {e}")
    finally:
        client.close()

    return blocs_texte_data

# Fonction principale pour exécuter le script
def main():
    try:
        query_texte = input("Rechercher par thème (laissez vide pour ignorer) : ").strip()
        query_id = input("Rechercher par ID (laissez vide pour ignorer) : ").strip()

        # Appel à la fonction pour récupérer les données
        result = get_data(query_texte, query_id)

        # Affichage des résultats
        print("\nRésultats de la recherche :")
        for idx, bloc in enumerate(result, start=1):
            print(f"\nRésultat {idx}:")
            print(f"Thème : {bloc['theme']}")
            print(f"Colonnes : {bloc['colonnes']}")

    except KeyboardInterrupt:
        print("\nInterruption du script.")
    except Exception as ex:
        print(f"Une erreur s'est produite : {ex}")

# Vérifier si le script est exécuté en tant que programme principal
if __name__ == "__main__":
    main()
