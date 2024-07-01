from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('index/', views.index, name='index'),
    path('download/images/', views.download_images, name='download_images'),
    path('download/faces/', views.download_faces, name='download_faces'),
    path('download/torax/', views.download_torax, name='download_torax'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('texte/', views.texte, name='texte'),
    path('date_texte/', views.date_texte, name='date_texte'),
    path('bdd/', views.bdd, name='bdd'),
    path('upload_csv/<str:dataset_name>/', views.upload_csv, name='upload_csv'),
    path('download-dataset-csv/', views.download_dataset_csv, name='download_dataset_csv'),
    path('collection/<str:collection_name>/', views.collection_detail, name='collection_detail'),
    path('download/collection/<str:collection_name>/', views.download_collection, name='download_collection'),
    path('upload_images/', views.upload_images, name='upload_images'),
    path('upload_image_folder/', views.upload_image_folder, name='upload_image_folder'),
    path('data_images/<str:folder_name>/', views.data_images, name='data_images'),
    path('search/', views.search, name='search'),
    path('search_collections/', views.bdd, name='search_collections'), 
    path('json_datasets/', views.json_datasets, name='json_datasets'),
    path('upload_json/', views.upload_json, name='upload_json'),  # Ajout de l'URL pour l'upload JSON
    path('download_json/<str:collection_name>/', views.download_json, name='download_json'),  # Définition unique pour télécharger JSON
    path('videos/', views.video_list, name='video_list'),
    path('download_video/<str:video_id>/', views.download_video, name='download_video'),
    path('videos/', views.video_list, name='video_list'),  # Ajoutez cette ligne
    path('download_video/<str:video_id>/', views.download_video, name='download_video'),  # Ajoutez cette ligne
    path('upload_videos/', views.upload_videos, name='upload_videos'),
    path('download/<str:file_id>/', views.download_file, name='download_file'),
    path('upload/images/', views.upload_images, name='upload_images'),
    path('upload_zip/', views.upload_zip, name='upload_zip'),


    
]
