from django.urls import path
from . import views
from .views import generate_image
from .views import download_data
from .views import download_chatbot_response

urlpatterns = [
    path('', views.home, name='home'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('list_datasets/', views.list_datasets, name='list_datasets'),
    path('download_data/<str:collection_name>/', views.download_data, name='download_data'),
    path('searchimage/', views.search_images, name='search_images'),
    path('generate-image/', generate_image, name='generate_image'),
    path('image-datasets/', views.list_image_datasets, name='image_datasets'),
    path('chatimagedernier/', views.chatimagedernier, name='chatimagedernier'),  # La nouvelle page
    path('download_image/<str:image_filename>/', views.download_image, name='download_image'),
    path('download/<str:collection_name>/', download_data, name='download_data'),
    path('delete_dataset/<int:dataset_id>/', views.delete_dataset, name='delete_dataset'),
    path('download_chatbot_response/', download_chatbot_response, name='download_chatbot_response'),

]
