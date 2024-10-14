# chatbot/models.py

from django.db import models

class ChatResponse(models.Model):
    role = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return f'{self.role}: {self.content[:50]}'
from django.db import models

class Dataset(models.Model):
    # Définitions des champs de ton modèle
    title = models.CharField(max_length=255)
    content = models.TextField()
    # Ajoute d'autres champs si nécessaire

    def __str__(self):
        return self.title
from django.db import models

class DatasetText(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    # Ajoutez d'autres champs selon vos besoins

    def __str__(self):
        return self.title
