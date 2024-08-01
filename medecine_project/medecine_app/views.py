from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import FileResponse
from django.urls import reverse
from pymongo import MongoClient
import csv
import json
from bson import json_util
from django.http import HttpResponse
from pymongo import MongoClient
import json
import os
from bson import ObjectId
from django.http import HttpResponse, Http404
from gridfs import GridFS
from bson import ObjectId
import gridfs
from django.http import HttpResponse, Http404

def accueil(request):
    return render(request, 'accueil.html')

from django.shortcuts import render
from pymongo import MongoClient

def index(request):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['image']
    files_collection = db['fs.files']
    
    query = request.GET.get('q')
    if query:
        files = files_collection.find({"filename": {"$regex": query, "$options": "i"}})
    else:
        files = files_collection.find()
    
    files_data = []
    for file in files:
        file_info = {
            'id': str(file['_id']),
            'filename': file['filename'],
            'uploadDate': file['uploadDate'],
            'length': file['length'],
            'contentType': file.get('contentType', 'Unknown')
        }
        files_data.append(file_info)
    
    client.close()
    
    context = {
        'files_data': files_data,
        'query': query
    }
    return render(request, 'index.html', context)


def download_file(request, file_id):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['image']
    fs = gridfs.GridFS(db)
    
    try:
        file = fs.get(ObjectId(file_id))
        response = HttpResponse(file.read(), content_type=file.content_type)
        response['Content-Disposition'] = f'attachment; filename="{file.filename}"'
        return response
    except gridfs.NoFile:
        raise Http404("File not found")

def upload_zip(request):
    if request.method == 'POST' and request.FILES.get('zip_file'):
        zip_file = request.FILES['zip_file']
        
        # Connexion à MongoDB
        client = MongoClient('mongodb://root:pass12345@localhost:27017/')
        db = client['image']
        fs = gridfs.GridFS(db)
        
        # Enregistrer le fichier ZIP dans GridFS
        fs.put(zip_file, filename=zip_file.name)
        
        client.close()
        return HttpResponse("Fichier ZIP uploadé avec succès")
    
    return render(request, 'upload_zip.html')
    

def download_images(request):
    filepath = '/home/yvanoide/iadev-python/base/zip/images.zip'
    return FileResponse(open(filepath, 'rb'), as_attachment=True)

def download_faces(request):
    filepath = '/home/yvanoide/iadev-python/base/zip/Faces.zip'
    return FileResponse(open(filepath, 'rb'), as_attachment=True)

def download_torax(request):
    filepath = '/home/yvanoide/iadev-python/djan/zip/torax.zip'
    return FileResponse(open(filepath, 'rb'), as_attachment=True)

def texte(request):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    squelette_db = client['squelette']
    collection = squelette_db['data']
    data = list(collection.find())
    client.close()
    context = {
        'data': data
    }
    return render(request, 'texte.html', context)

def date_texte(request):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['maths']
    collection = db['info']
    data = list(collection.find())
    client.close()
    return render(request, 'date_texte.html', {'data': data})

def bdd(request):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['data']
    query = request.GET.get('q')
    if query:
        collections = [col for col in db.list_collection_names() if query.lower() in col.lower()]
    else:
        collections = db.list_collection_names()
    client.close()
    return render(request, 'bdd.html', {'collections': collections})

def collection_detail(request, collection_name):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['data']
    collection_data = list(db[collection_name].find())
    client.close()
    return render(request, 'collection_detail.html', {'collection_name': collection_name, 'collection_data': collection_data})

def connect_to_mongodb(database_name, collection_name):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client[database_name]
    collection = db[collection_name]
    return client, collection

def upload_csv(request, dataset_name=None):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        dataset_name = csv_file.name.split('.')[0]
        collection_name = dataset_name.replace(" ", "_").lower()
        client, collection = connect_to_mongodb('data', collection_name)
        file_data = csv_file.read().decode('latin-1').splitlines()
        csv_reader = csv.reader(file_data)
        headers = next(csv_reader)
        for row in csv_reader:
            data = {headers[i]: row[i] for i in range(len(headers))}
            try:
                collection.insert_one(data)
            except DuplicateKeyError:
                pass  # Ignorer les doublons
        client.close()
        return HttpResponse("Fichier CSV uploadé avec succès")
    return render(request, 'upload_csv.html')


def upload_image_folder(request):
    if request.method == 'POST' and request.FILES.getlist('image_folder'):
        image_files = request.FILES.getlist('image_folder')
        client, collection = connect_to_mongodb('dataimage', 'images')
        for image_file in image_files:
            image_data = image_file.read()
            collection.insert_one({'filename': image_file.name, 'data': image_data})
        client.close()
        return HttpResponse("Dossier d'images uploadé avec succès")
    return render(request, 'upload_image_folder.html')

def download_dataset_csv(request, dataset):
    dataset_content = [
        {"col1": "value1", "col2": "value2"},
        {"col1": "value3", "col2": "value4"}
    ]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dataset.csv"'
    writer = csv.DictWriter(response, fieldnames=dataset_content[0].keys())
    writer.writeheader()
    for row in dataset_content:
        writer.writerow(row)
    return response

def data_images(request, folder_name):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['dataimage']
    collection = db[folder_name]
    data = list(collection.find())
    client.close()
    return render(request, 'data_images.html', {'data': data})

def search(request):
    query = request.GET.get('q')
    if not query:
        return HttpResponseRedirect(reverse('accueil'))
    themes = {
        'medecine': 'download_images',
        'visage': 'download_faces',
        'torax': 'download_torax'
    }
    if query.lower() in themes:
        url = reverse(themes[query.lower()])
        return HttpResponseRedirect(url)
    else:
        return HttpResponse(f'Aucun résultat trouvé pour "{query}"')

def download_collection(request, collection_name):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['data']
    collection = db[collection_name]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{collection_name}.csv"'
    writer = csv.writer(response)
    cursor = collection.find()
    if collection.count_documents({}) > 0:
        headers = cursor[0].keys()
        writer.writerow(headers)
        for document in cursor:
            writer.writerow(document.values())
    client.close()
    return response

def upload_images(request):
    if request.method == 'POST' and request.FILES.getlist('image_folder'):
        image_files = request.FILES.getlist('image_folder')
        
        # Connect to MongoDB
        client = MongoClient('mongodb://root:pass12345@localhost:27017/')
        db = client['dataimage']
        collection = db['images']
        
        for image_file in image_files:
            image_data = image_file.read()
            collection.insert_one({'filename': image_file.name, 'data': image_data})
        
        client.close()
        return HttpResponse("Dossier d'images uploadé avec succès")
    
    return render(request, 'upload_images.html')


def json_datasets(request):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['json']  # Remplacez 'json' par le nom de votre base de données MongoDB
    collections = db.list_collection_names()

    query = request.GET.get('q')
    matching_collections = []

    if query:
        for collection_name in collections:
            if query.lower() in collection_name.lower():
                matching_collections.append(collection_name)
    else:
        matching_collections = collections

    client.close()

    context = {
        'query': query,
        'collections': matching_collections
    }
    return render(request, 'json_datasets.html', context)

def download_json(request, collection_name):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['json']  # Remplacez 'json' par le nom de votre base de données MongoDB
    collection = db[collection_name]

    dataset_content = list(collection.find())

    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{collection_name}.json"'
    json.dump(dataset_content, response, indent=2)

    client.close()
    return response

def download_json(request, collection_name):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['json']  # Connexion à la base de données nommée 'json'
    collection = db[collection_name]
    data = list(collection.find({}, {'_id': 0}))
    client.close()
    response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{collection_name}.json"'
    return response

# Connexion à MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client['json']  # Nom de la base de données

def upload_json(request):
    if request.method == 'POST' and request.FILES['json_file']:
        json_file = request.FILES['json_file']
        
        # Déterminer le nom de la collection à partir du nom de fichier
        collection_name = os.path.splitext(json_file.name)[0]
        collection = db[collection_name]
        
        # Charger les données JSON et les insérer dans MongoDB
        data = json.load(json_file)
        if isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)
        
        return HttpResponse(f'Fichier JSON "{json_file.name}" uploadé avec succès')
    
    return render(request, 'upload_json.html')



def video_list(request):
    # Connexion à MongoDB
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['video']  # Nom de la base de données contenant les vidéos
    fs = gridfs.GridFS(db)  # Initialisation de GridFS pour stocker les vidéos
    
    # Récupération de toutes les vidéos
    videos = []
    for file in fs.find():
        videos.append({
            'id': str(file._id),
            'filename': file.filename
        })
    
    # Fermeture de la connexion à MongoDB
    client.close()

    context = {
        'videos': videos
    }

    return render(request, 'video.html', context)


def download_video(request, video_id):
    client = MongoClient('mongodb://root:pass12345@localhost:27017/')
    db = client['video']
    fs = gridfs.GridFS(db)
    try:
        video = fs.get(ObjectId(video_id))
        response = HttpResponse(video.read(), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{video.filename}"'
        return response
    except gridfs.errors.NoFile:
        raise Http404("Vidéo non trouvée")

def video_list(request):
    if request.method == 'GET' and 'search_query' in request.GET:
        search_query = request.GET.get('search_query')
        
        # Connexion à MongoDB
        client = MongoClient('mongodb://root:pass12345@localhost:27017/')
        db = client['video']  # Nom de la base de données contenant les vidéos
        fs = gridfs.GridFS(db)  # Initialisation de GridFS
        
        # Recherche des vidéos par titre
        videos = []
        for file in fs.find({'filename': {'$regex': f'.*{search_query}.*', '$options': 'i'}}):
            video = {
                'id': str(file._id),
                'filename': file.filename,
                'upload_date': file.upload_date,
                'length': file.length,
                'content_type': file.content_type,
            }
            videos.append(video)
        
        # Fermeture de la connexion à MongoDB
        client.close()
        
        context = {
            'videos': videos,
            'search_query': search_query,
        }
        
        return render(request, 'video_list.html', context)
    
    # Si aucune recherche n'est effectuée, afficher toutes les vidéos
    else:
        # Connexion à MongoDB
        client = MongoClient('mongodb://root:pass12345@localhost:27017/')
        db = client['video']  # Nom de la base de données contenant les vidéos
        fs = gridfs.GridFS(db)  # Initialisation de GridFS
        
        # Récupération de toutes les vidéos
        videos = []
        for file in fs.find():
            video = {
                'id': str(file._id),
                'filename': file.filename,
                'upload_date': file.upload_date,
                'length': file.length,
                'content_type': file.content_type,
            }
            videos.append(video)
        
        # Fermeture de la connexion à MongoDB
        client.close()
        
        context = {
            'videos': videos,
        }
        
        return render(request, 'video_list.html', context)


def upload_videos(request):
    if request.method == 'POST' and request.FILES.getlist('video_files'):
        video_files = request.FILES.getlist('video_files')
        
        # Connect to MongoDB
        client = MongoClient('mongodb://root:pass12345@localhost:27017/')
        db = client['video']
        fs = gridfs.GridFS(db)
        
        for video_file in video_files:
            fs.put(video_file, filename=video_file.name)
        
        client.close()
        return HttpResponse("Vidéos uploadées avec succès")
    
    return render(request, 'upload_videos.html')

