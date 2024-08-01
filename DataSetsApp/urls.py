from django.urls import path
from . import views  # Importation des vues depuis le fichier views.py

urlpatterns = [
    path('upload/', views.upload_dataset, name='upload_dataset'),  # Route pour uploader un dataset
    path('upload_images/', views.upload_image_folder, name='upload_image_folder'),
    path('datasets/', views.list_datasets, name='list_datasets'),  # Route pour la liste des datasets
    path('', views.home, name='home'),  # Route pour la page d'accueil
    path('signup/', views.signup, name='signup'),
    path('delete_image_folder/<str:folder_name>/', views.delete_image_folder, name='delete_image_folder'),
    path('delete_dataset/<str:dataset_id>/', views.delete_dataset, name='delete_dataset'),
    path('download_data/<str:collection_name>/<str:fichier_type>/', views.download_data, name='download_data'),
    path('download_all_images/<str:image_collection_name>/', views.download_all_images, name='download_all_images'),
    path('download_collection/<str:collection_name>/', views.download_collection, name='download_collection'),
    path('search/', views.search_collections, name='search_collections'),
    path('download_data/<str:collection_name>/<str:fichier_type>/', views.download_data, name='download_data'),
    path('search_images/', views.search_images, name='search_images'),

]
