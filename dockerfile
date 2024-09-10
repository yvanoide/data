# Utiliser une image de base Python 3.10
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements.txt dans le conteneur
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-dotenv

# Copier tout le contenu du projet dans le conteneur
COPY . /app/

# Exposer le port que Django utilise (par défaut 8000)
EXPOSE 8000

# Définir la commande de démarrage du conteneur
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "DataSetProjet.wsgi:application"]
