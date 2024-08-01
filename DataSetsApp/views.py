import os
import csv
import json
import io
import logging
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pymongo import MongoClient
from bson import json_util, binary
from bson.objectid import ObjectId
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Dataset, ImageFolderMetadata
from .forms import DatasetForm, ImageUploadForm
from django.shortcuts import render
from pymongo import MongoClient
from django.conf import settings

logger = logging.getLogger(__name__)

# Constante pour dossiers d'images
MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_USERNAME = 'root'
MONGO_PASSWORD = 'pass12345'

# Vue pour la page d'accueil
def home(request):
    return render(request, 'DataSetsApp/home.html')

# Fonction pour ajouter un utilisateur au groupe "Professeurs"
def add_user_to_professors_group(username):
    user = User.objects.get(username=username)
    group = Group.objects.get(name='Professeurs')
    group.user_set.add(user)

# Vue pour la gestion de l'inscription des utilisateurs
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
@csrf_exempt
def upload_image_folder(request):
    if not request.user.groups.filter(name='Professeurs').exists():
        return HttpResponse('Accès non autorisé', status=403)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST)
        if form.is_valid():
            image_dir = form.cleaned_data['image_dir']
            fichier_type = form.cleaned_data['fichier_type']
            description = form.cleaned_data['description']
            try:
                if not os.path.exists(image_dir):
                    return HttpResponse(f"Directory {image_dir} does not exist", status=400)
                
                # Uploader les images depuis le répertoire
                upload_images_to_mongo(image_dir, MONGO_URI, request.user, fichier_type)
                
                # Enregistrer les métadonnées du dossier
                folder_name = os.path.basename(image_dir)
                ImageFolderMetadata.objects.create(
                    folder_name=folder_name,
                    description=description,    
                    fichier_type=fichier_type,
                    Auteur=request.user
                )
                return redirect('list_datasets')
            except Exception as e:
                return HttpResponse(f"Error during upload: {e}", status=500)
    else:
        form = ImageUploadForm()
    return render(request, 'datasets/upload_image_folder.html', {'form': form})

def upload_images_to_mongo(image_dir, mongo_uri, user, fichier_type):
    client = MongoClient(mongo_uri)
    collection_name = os.path.basename(image_dir)
    db_name = 'my_database_images'
    collection = client[db_name][collection_name]

    for image_file in os.listdir(image_dir):
        if image_file.lower().endswith(f'.{fichier_type}'):
            image_path = os.path.join(image_dir, image_file)
            with open(image_path, 'rb') as file:
                encoded_image = binary.Binary(file.read())
                image_document = {
                    'image_name': image_file,
                    'image_data': encoded_image
                }
                collection.insert_one(image_document)

    client.close()

@login_required
def upload_dataset(request):
    if not request.user.groups.filter(name='Professeurs').exists():
        return HttpResponse('Accès non autorisé', status=403)
    
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.Auteur = request.user

            fichier = request.FILES['fichier']
            fichier_type = fichier.name.split('.')[-1].lower()
            if fichier_type in ['csv', 'json']:
                dataset.fichier_type = fichier_type
            else:
                return HttpResponse("Type de fichier non supporté", status=400)

            dataset.save()

            try:
                client = MongoClient(f'mongodb://root:pass12345@localhost:27017/')
                db = client['my_database']
                collection_name = dataset.titre.replace(" ", "_").lower()
                collection = db[collection_name]

                # Nettoyez la collection avant d'insérer de nouveaux documents
                collection.delete_many({})

                if fichier_type == 'csv':
                    handle_csv(fichier, collection)
                elif fichier_type == 'json':
                    handle_json(fichier, collection)

                client.close()
            except Exception as e:
                logger.error("Erreur lors de l'accès à la base de données MongoDB : %s", e)
                return HttpResponse("Erreur lors de l'accès à la base de données", status=500)

            return redirect('list_datasets')
    else:
        form = DatasetForm()
    return render(request, 'datasets/upload_dataset.html', {'form': form})

def handle_csv(fichier, collection):
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'utf-16']
    for encoding in encodings:
        try:
            fichier.seek(0)
            csv_data = fichier.read().decode(encoding)
            csv_reader = csv.DictReader(io.StringIO(csv_data))
            for row in csv_reader:
                collection.insert_one(row)
            break
        except (UnicodeDecodeError, StopIteration):
            continue

def handle_json(fichier, collection):
    try:
        fichier.seek(0)
        file_data = fichier.read().decode('utf-8')
        json_data = json.loads(file_data)
        if isinstance(json_data, list):
            collection.insert_many(json_data)
        else:
            collection.insert_one(json_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {str(e)}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {str(e)}")

def is_professor(user):
    return user.groups.filter(name='Professeurs').exists()

@login_required
@user_passes_test(is_professor)
def delete_image_folder(request, folder_name):
    logger.info(f"Received folder_name: {folder_name}")

    try:
        client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
        db_metadata = client['my_database']
        db_images = client['my_database_images']

        folder_metadata = db_metadata['datasetimagefolder(metadata)'].find_one({'folder_name': folder_name})
        if not folder_metadata:
            logger.error(f"Folder metadata not found for folder_name: {folder_name}")
            return HttpResponse(f"Dossier d'images non trouvé: {folder_name}", status=404)

        logger.info(f"Found folder metadata: {folder_metadata}")

        logger.info(f"Deleting image collection: {folder_name}")
        db_images.drop_collection(folder_name)

        logger.info(f"Deleting metadata in MongoDB for folder: {folder_name}")
        db_metadata['datasetimagefolder(metadata)'].delete_one({'folder_name': folder_name})

        client.close()

        return redirect('list_datasets')
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du dossier d'images: {e}")
        return HttpResponse(f"Erreur lors de la suppression: {e}", status=500)

MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_DB_NAME = 'my_database'
@login_required
def list_collections(request):
    client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
    db = client[settings.MONGO_DB_NAME]
    collections = db.list_collection_names()
    return render(request, 'list_collections.html', {'collections': collections})

@login_required
def list_datasets(request):
    query = request.GET.get('q', '').lower()
    file_type = request.GET.get('file_type', '').lower()
    client = MongoClient(MONGO_URI)

    try:
        db = client[MONGO_DB_NAME]
        metadata_collection = db['dataset(metadata)']
        metadata_list = list(metadata_collection.find())
        print(f"Metadata list: {metadata_list}")  # Debug print

        if query or file_type:
            filtered_metadata_list = []
            for metadata in metadata_list:
                matches_query = query in metadata.get('description', '').lower() or query in metadata.get('titre', '').lower()
                matches_file_type = file_type == metadata.get('fichier_type', '').lower() if file_type else True
                if matches_query and matches_file_type:
                    filtered_metadata_list.append(metadata)
        else:
            filtered_metadata_list = metadata_list

        datasets = []
        for metadata in filtered_metadata_list:
            collection_name = metadata['titre'].replace(" ", "_").lower()
            dataset_sample = list(db[collection_name].find().limit(3))
            metadata['formatted_titre'] = metadata['titre'].replace(" ", "_").lower()

            try:
                user = User.objects.get(id=metadata['Auteur_id'])
                metadata['Auteur'] = user.username
            except User.DoesNotExist:
                metadata['Auteur'] = 'Inconnu'

            datasets.append({
                'metadata': metadata,
                'sample': dataset_sample
            })

        image_folder_metadata_list = list(db['datasetimagefolder(metadata)'].find())
        print(f"Image folder metadata list: {image_folder_metadata_list}")  # Debug print

        if query or file_type:
            filtered_image_folder_metadata_list = []
            for metadata in image_folder_metadata_list:
                matches_query = query in metadata.get('description', '').lower() or query in metadata.get('folder_name', '').lower()
                matches_file_type = file_type == metadata.get('fichier_type', '').lower() if file_type else True
                if matches_query and matches_file_type:
                    filtered_image_folder_metadata_list.append(metadata)
        else:
            filtered_image_folder_metadata_list = image_folder_metadata_list

        is_professor = request.user.groups.filter(name='Professeurs').exists()

        # Liste des collections dans la base de données
        collections = db.list_collection_names()

        return render(request, 'datasets/list_datasets.html', {
            'datasets': datasets,
            'image_folder_metadata_list': filtered_image_folder_metadata_list,
            'query': query,
            'file_type': file_type,
            'is_professor': is_professor,
            'collections': collections
        })
    finally:
        client.close()

@login_required
@user_passes_test(is_professor)
def delete_dataset(request, dataset_id):
    try:
        client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
        db = client['my_database']
        metadata_collection = db['dataset(metadata)']

        result = metadata_collection.find_one_and_delete({"_id": ObjectId(dataset_id)})
        if not result:
            client.close()
            return HttpResponse("Dataset non trouvé", status=404)

        collection_name = result['titre'].replace(" ", "_").lower()
        db.drop_collection(collection_name)

        client.close()
        return redirect('list_datasets')
    except Exception as e:
        return HttpResponse(f"Erreur lors de la suppression: {e}", status=500)

def download_all_images(request, image_collection_name):
    try:
        base_path = '/path/to/your/image/folders'
        folder_path = os.path.join(base_path, image_collection_name)

        if os.path.exists(folder_path):
            zip_file_name = f"{image_collection_name}.zip"
            zip_file_path = os.path.join(base_path, zip_file_name)

            with ZipFile(zip_file_path, 'w') as zip_file:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, folder_path))

            with open(zip_file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type="application/zip")
                response['Content-Disposition'] = f'attachment; filename="{zip_file_name}"'
                return response
        else:
            raise Http404("Folder does not exist")
    except Exception as e:
        raise Http404("Error during folder download: " + str(e))

from django.http import HttpResponse, Http404
import os

def download_data(request, collection_name, fichier_type):
    try:
        base_path = '/path/to/your/dataset/folder'
        file_path = os.path.join(base_path, collection_name + '.' + fichier_type)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type="application/force-download")
                response['Content-Disposition'] = f'attachment; filename="{collection_name}.{fichier_type}"'
                return response
        else:
            raise Http404("File does not exist")
    except Exception as e:
        raise Http404("Error during file download: " + str(e))


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pymongo import MongoClient
from django.contrib.auth.models import User

MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_DB_NAME = 'my_database'

@login_required
def list_datasets(request):
    query = request.GET.get('q', '').lower()
    file_type = request.GET.get('file_type', '').lower()
    client = MongoClient(MONGO_URI)

    try:
        db = client[MONGO_DB_NAME]
        metadata_collection = db['dataset(metadata)']
        metadata_list = list(metadata_collection.find())
        print(f"Metadata list: {metadata_list}")  # Debug print

        if query or file_type:
            filtered_metadata_list = []
            for metadata in metadata_list:
                matches_query = query in metadata.get('description', '').lower() or query in metadata.get('titre', '').lower()
                matches_file_type = file_type == metadata.get('fichier_type', '').lower() if file_type else True
                if matches_query and matches_file_type:
                    filtered_metadata_list.append(metadata)
        else:
            filtered_metadata_list = metadata_list

        datasets = []
        for metadata in filtered_metadata_list:
            collection_name = metadata['titre'].replace(" ", "_").lower()
            dataset_sample = list(db[collection_name].find().limit(3))
            metadata['formatted_titre'] = metadata['titre'].replace(" ", "_").lower()

            try:
                user = User.objects.get(id=metadata['Auteur_id'])
                metadata['Auteur'] = user.username
            except User.DoesNotExist:
                metadata['Auteur'] = 'Inconnu'

            datasets.append({
                'metadata': metadata,
                'sample': dataset_sample
            })

        image_folder_metadata_list = list(db['datasetimagefolder(metadata)'].find())
        print(f"Image folder metadata list: {image_folder_metadata_list}")  # Debug print

        if query or file_type:
            filtered_image_folder_metadata_list = []
            for metadata in image_folder_metadata_list:
                matches_query = query in metadata.get('description', '').lower() or query in metadata.get('folder_name', '').lower()
                matches_file_type = file_type == metadata.get('fichier_type', '').lower() if file_type else True
                if matches_query and matches_file_type:
                    filtered_image_folder_metadata_list.append(metadata)
        else:
            filtered_image_folder_metadata_list = image_folder_metadata_list

        is_professor = request.user.groups.filter(name='Professeurs').exists()

        # Liste des collections dans la base de données
        collections = db.list_collection_names()

        return render(request, 'datasets/list_datasets.html', {
            'datasets': datasets,
            'image_folder_metadata_list': filtered_image_folder_metadata_list,
            'query': query,
            'file_type': file_type,
            'is_professor': is_professor,
            'collections': collections
        })
    finally:
        client.close()

from .models import Collection  

from django.http import HttpResponse, Http404
import os

import csv
from django.http import HttpResponse
from pymongo import MongoClient

def download_collection(request, collection_name):
    try:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]
        collection = db[collection_name]

        documents = list(collection.find())
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{collection_name}.csv"'
        
        writer = csv.writer(response)

        if documents:
            headers = documents[0].keys()
            writer.writerow(headers)
            for doc in documents:
                writer.writerow([doc.get(header, '') for header in headers])
        else:
            writer.writerow(['No data available'])

        return response
    except Exception as e:
        logger.error("Error during collection download: %s", e)
        return HttpResponse(f"Error during collection download: {e}", status=500)



MONGO_URI = 'mongodb://root:pass12345@localhost:27017/'
MONGO_DB_NAME = 'my_database'

def search_collections(request):
    query = request.GET.get('q', '').strip()
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]

    collections_with_keyword = []
    try:
        collections = db.list_collection_names()
        for collection_name in collections:
            collection = db[collection_name]
            if collection.count_documents({'mots-clés': query}) > 0:
                collections_with_keyword.append(collection_name)
    finally:
        client.close()

    return render(request, 'datasets/search_results.html', {'query': query})


def rechercher_par_mot_cle(mot_cle):
    client = MongoClient(MONGO_URI)
    try:
        db = client[MONGO_DB_NAME]
        collections = db.list_collection_names()
        collections_avec_mot_cle = []
        for collection_name in collections:
            collection = db[collection_name]
            count = collection.count_documents({'mots-clés': mot_cle})
            if count > 0:
                collections_avec_mot_cle.append(collection_name)
        return collections_avec_mot_cle
    finally:
        client.close()

def search_collections(request):
    query = request.GET.get('q', '').strip()
    collections = []
    if query:
        collections = rechercher_par_mot_cle(query)
    return render(request, 'datasets/search_results.html', {'collections': collections, 'query': query})

def download_data(request, collection_name, fichier_type):
    try:
        if fichier_type == 'csv':
            client = MongoClient(settings.MONGO_URI)
            db = client[settings.MONGO_DB_NAME]
            collection = db[collection_name]

            documents = list(collection.find())
            
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{collection_name}.csv"'
            
            writer = csv.writer(response)

            if documents:
                headers = documents[0].keys()
                writer.writerow(headers)
                for doc in documents:
                    writer.writerow([doc.get(header, '') for header in headers])
            else:
                writer.writerow(['No data available'])

            return response
        else:
            raise Http404("Unsupported file type")

    except Exception as e:
        logger.error("Error during collection download: %s", e)
        return HttpResponse(f"Error during collection download: {e}", status=500)
    
def search_images(request):
    query = request.GET.get('q', '').strip()
    print(f"Mot-clé de recherche: '{query}'")
    
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['my_database_images']
    
    collections_with_keyword = []
    collections = db.list_collection_names()
    print(f"Collections disponibles: {collections}")
    
    for collection_name in collections:
        collection = db[collection_name]
        count = collection.count_documents({'titre': {'$regex': query, '$options': 'i'}})
        print(f"Collection '{collection_name}' a {count} documents correspondant")
        if count > 0:
            collections_with_keyword.append(collection_name)
    
    client.close()
    
    print(f"Collections avec le mot-clé: {collections_with_keyword}")
    
    return render(request, 'datasets/search_images.html', {'collections': collections_with_keyword, 'query': query})
