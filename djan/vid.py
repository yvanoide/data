from pymongo import MongoClient
import gridfs

# Connexion à la base de données MongoDB
client = MongoClient('mongodb://root:pass12345@localhost:27017/')
db = client['video']

# Initialisation de GridFS
fs = gridfs.GridFS(db)

# Chemin vers la vidéo à stocker
file_path = '/home/yvanoide/iadev-python/djan/Écoutez la voix de Louis XIV.mp4'

# Lecture du fichier vidéo et stockage dans GridFS
with open(file_path, 'rb') as f:
    file_id = fs.put(f, filename='video.mp4')

print(f'Video stored with file ID: {file_id}')
