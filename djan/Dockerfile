# Utilisation de l'image Python officielle comme base
FROM python:3.8-slim

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Installation des dépendances du projet
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copie du code de l'application dans le conteneur
COPY . /app/

# Commande par défaut pour exécuter votre application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
