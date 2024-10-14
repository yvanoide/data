from django.shortcuts import render
import csv
from io import StringIO
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from hugchat import hugchat
from hugchat.login import Login
from .models import ChatResponse
import requests
from django.conf import settings
from diffusers import StableDiffusionPipeline
import torch
from django.http import FileResponse
import os
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import redirect, get_object_or_404
from .models import DatasetText  

def get_mongo_client():
    # Informations de connexion à MongoDB
    username = 'admin'  # Remplacez par votre nom d'utilisateur
    password = 'admin123'  # Remplacez par votre mot de passe
    db_name = 'texte'  # Nom de la base de données

    # Connexion au client MongoDB
    client = MongoClient(f"mongodb://{username}:{password}@localhost:27017/")
    
    return client

def home(request):
    """Page d'accueil affichant le contenu de la base de données 'texte' depuis MongoDB."""
    # Connexion au client MongoDB en utilisant les paramètres de DATABASES
    client = MongoClient(
        f"mongodb://{settings.DATABASES['default']['CLIENT']['username']}:{settings.DATABASES['default']['CLIENT']['password']}@localhost:27017/"
    )

    db_text = client['texte']  # Base de données pour les textes
    db_images = client['images']  # Base de données pour les images, si applicable

    try:
        # Récupération de la liste des collections de texte
        text_collections = db_text.list_collection_names()

        # Récupération de la liste des métadonnées des images
        image_folder_metadata_list = []
        for collection_name in db_images.list_collection_names():
            # Supposons que vous avez un document pour chaque dossier d'images
            image_metadata = db_images[collection_name].find_one()  # Vous pouvez adapter cela selon votre structure
            if image_metadata:
                image_folder_metadata_list.append(image_metadata)
                
    except Exception as e:
        print(f"Erreur lors de la récupération des collections : {e}")
        text_collections = []
        image_folder_metadata_list = []

    # Vérification si l'utilisateur est un professeur
    is_professor = request.user.is_authenticated and request.user.is_professor  # Vous devez adapter cela selon votre logique

    context = {
        'text_collections': text_collections,  # Passer les noms de collections de texte au contexte
        'image_folder_metadata_list': image_folder_metadata_list,  # Passer les métadonnées d'images
        'is_professor': is_professor,  # Passer le statut de l'utilisateur
        'query': request.GET.get('q', ''),  # Passer la requête de recherche si applicable
        'file_type': request.GET.get('file_type', ''),  # Passer le type de fichier si applicable
    }

    client.close()  # Ne pas oublier de fermer la connexion

    return render(request, 'chatbot/home.html', context)

def chatbot_view(request):
    response_text = None  # Initialise la variable pour la réponse
    rows = 1  # Valeur par défaut
    cols = 1  # Valeur par défaut
    table_data = []  # Variable pour stocker les lignes et colonnes

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        prompt = request.POST.get('prompt')

        try:
            # Récupérer les valeurs des champs "num_rows" et "num_cols"
            rows = int(request.POST.get('num_rows', 1))
            cols = int(request.POST.get('num_cols', 1))

            # Créer un chatbot Hugging Face
            sign = Login(email, password)
            cookies = sign.login()
            chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

            # Générer la réponse
            response = chatbot.chat(prompt)
            response_text = str(response)

            # Stocker la réponse dans la session
            request.session['chatbot_response'] = response_text

            # Générer le tableau en fonction des lignes et colonnes spécifiées
            table_data = [
                [f"Réponse {i + 1}, Col {j + 1}" for j in range(cols)] 
                for i in range(rows)
            ]

            # Connexion à MongoDB
            client = MongoClient(f"mongodb://admin:admin123@localhost:27017/")
            db = client['texte']

            # Déterminer le nom de la collection
            existing_collections = db.list_collection_names()
            next_collection_index = len(existing_collections)
            collection_name = str(next_collection_index)

            # Sauvegarder uniquement la réponse dans MongoDB
            responses_collection = db[collection_name]
            responses_collection.insert_one({
                'content': response_text,
                'email': email,
                'timestamp': datetime.now()
            })

        except Exception as e:
            print(f"Erreur: {e}")
            response_text = str(e)

    return render(request, 'chatbot/chatbot.html', {'response': response_text, 'table_data': table_data})


def download_chatbot_response(request):
    """Télécharge la réponse du chatbot sous forme de fichier CSV."""
    response_text = request.session.get('chatbot_response', 'Pas de réponse disponible.')

    # Créer la réponse HTTP
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chatbot_response.csv"'

    writer = csv.writer(response)
    writer.writerow(['Réponse'])  # Écrire l'en-tête

    # Écrire la réponse du chatbot
    writer.writerow([response_text])  # Écrire la réponse dans le tableau

    return response


def download_data(request, collection_name):
    """Télécharge les données de la collection spécifiée sous forme de fichier CSV."""
    try:
        client = MongoClient(
            f"mongodb://{settings.MONGO_DATABASES['default']['USER']}:{settings.MONGO_DATABASES['default']['PASSWORD']}@localhost:27017/"
        )
        db = client['texte']  # Nom de la base de données
        collection = db[collection_name]  # Récupérer la collection spécifiée

        # Créer la réponse HTTP
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{collection_name}.csv"'

        writer = csv.writer(response)
        
        # Écrire les en-têtes (ajustez selon vos besoins)
        writer.writerow(['_id', 'data'])  # Change cela selon les champs de ta collection

        # Écrire les données
        for document in collection.find():
            writer.writerow([document['_id'], document.get('data', '')])  # Change 'data' selon ta structure

    except Exception as e:
        print(f"Erreur lors du téléchargement des données : {e}")
        return HttpResponse("Erreur lors du téléchargement des données.", status=500)
    
    finally:
        client.close()  # Assurez-vous de toujours fermer la connexion

    return response



def search_images(request):
    query = request.GET.get('query', 'chien')
    api_key = 'HD8HViav9ZDLUy7Rxfphq8yAVLJLBgnmifDv64lpBkkRvjyv3oMCDvN4'
    headers = {'Authorization': api_key}
    params = {'query': query, 'per_page': 10}
    try:
        response = requests.get('https://api.pexels.com/v1/search', headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()
        images = [
            {
                'url': photo['src']['medium'],
                'photographer': photo['photographer'],
                'photographer_url': photo['photographer_url']
            }
            for photo in search_results.get('photos', [])
        ]
        return render(request, 'chatbot/results.html', {'images': images})
    except requests.exceptions.RequestException as e:
        print(f'Erreur lors de la recherche d\'images: {e}')
        return render(request, 'chatbot/results.html', {'error': 'Erreur lors de la recherche d\'images.'})

def generate_image(request):
    image_url = None
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        hf_token = "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"

        # Charger le pipeline Stable Diffusion
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", 
            torch_dtype=torch.float32,
            use_auth_token=hf_token
        ).to("cpu")

        # Générer l'image
        image = pipe(prompt).images[0]
        image.save("output_image.png")  # Sauvegarder l'image sur le serveur

        image_url = "output_image.png"

    return render(request, 'chatbot/generate_image.html', {'image_url': image_url})

def list_image_datasets(request):
    """Récupère les collections d'images et les affiche."""
    client = get_mongo_client()
    if not client:
        return render(request, 'chatbot/image_datasets.html', {'datasets': []})

    db_image = client[settings.MONGO_DATABASES['image']['NAME']]
    collections = db_image.list_collection_names()
    return render(request, 'chatbot/image_datasets.html', {'datasets': collections})



def list_datasets(request):
    # Connexion à MongoDB
    mongo_uri = f"mongodb://{settings.MONGO_DATABASES['default']['USER']}:{settings.MONGO_DATABASES['default']['PASSWORD']}@{settings.MONGO_DATABASES['default']['HOST']}:{settings.MONGO_DATABASES['default']['PORT']}/{settings.MONGO_DATABASES['default']['NAME']}"
    client = MongoClient(mongo_uri)
    db = client[settings.MONGO_DATABASES['default']['NAME']]
    
    # Récupération des paramètres de recherche
    query = request.GET.get('q', '')
    file_type = request.GET.get('file_type', '')
    dataset_type = request.GET.get('dataset_type', 'text')  # Valeur par défaut

    # Création d'un filtre de recherche
    filter_criteria = {}
    
    if query:
        filter_criteria['title'] = {'$regex': query, '$options': 'i'}  # Filtre insensible à la casse par titre

    # Récupérer les datasets de texte ou d'images en fonction de `dataset_type`
    if dataset_type == 'text':
        datasets = list(db.text_datasets.find(filter_criteria))  # Remplacez par le nom de votre collection pour les textes
    else:
        datasets = list(db.image_datasets.find(filter_criteria))  # Remplacez par le nom de votre collection pour les images
    
    return render(request, 'chatbot/home.html', {'datasets': datasets, 'query': query, 'file_type': file_type})



def chatimagedernier(request):
    image_url = None
    if request.method == 'POST':
        num_images = int(request.POST.get('num_images', 1))
        theme = request.POST.get('theme', '')
        decor = request.POST.get('decor', '')

        # Chemin vers le modèle Stable Diffusion local
        model_path = "/home/yvanoide/iadev-python/djanchat/stable_diffusion_model"
        pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float32)
        pipe = pipe.to("cpu")  # Utiliser le CPU

        # Générer les images
        for i in range(num_images):
            prompt = f"{theme}, {decor}"
            image = pipe(prompt).images[0]

            # Chemin vers le répertoire 'static' pour sauvegarder les images
            image_path = os.path.join(settings.BASE_DIR, 'chatbot/static', f"output_image_{i}.png")
            image.save(image_path)

            # Mettre à jour l'URL de l'image pour l'affichage
            image_url = f"/static/output_image_{i}.png"  # Conserver seulement la dernière image générée

    return render(request, 'chatbot/chatimagedernier.html', {'image_url': image_url})




def download_image(request, image_filename):
    # Chemin complet vers l'image dans le répertoire static
    image_path = os.path.join(settings.BASE_DIR, 'chatbot/static', image_filename)
    if os.path.exists(image_path):
        return FileResponse(open(image_path, 'rb'), as_attachment=True, filename=image_filename)
    else:
        return render(request, 'chatbot/chatimagedernier.html', {'error': 'Image not found'})

from django.shortcuts import redirect

def delete_dataset(request, collection_name):
    """Supprime la collection spécifiée de la base de données MongoDB."""
    client = get_mongo_client()  # Assure-toi que la connexion à MongoDB fonctionne
    if client:
        db = client['texte']
        try:
            # Supprime la collection spécifiée
            db.drop_collection(collection_name)
            print(f"Collection {collection_name} supprimée avec succès.")
        except Exception as e:
            print(f"Erreur lors de la suppression de la collection : {e}")
    client.close()  # Fermer la connexion

    # Redirige vers la page d'accueil après la suppression
    return redirect('home')


def delete_dataset(request, dataset_id):
    dataset = get_object_or_404(DatasetText, id=dataset_id)
    if request.method == "POST":
        dataset.delete()
        return redirect('list_datasets')  # Redirige vers la page des datasets
    return redirect('list_datasets')  # Redirige même si la méthode n'est pas POST

