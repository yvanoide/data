import subprocess
import os

# Définir les chemins et l'URL du dépôt distant
local_repo_path = "~/iadev-python/data - Copie/ProjetDatasets"
remote_repo_url = "https://github.com/yvanoide/data"

# S'assurer que le chemin local est correct
local_repo_path = os.path.expanduser(local_repo_path)

# Fonction pour exécuter une commande et vérifier son succès
def run_command(command, cwd=None):
    result = subprocess.run(command, cwd=cwd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)
    return result.returncode == 0

# Initialiser le dépôt Git local
if not os.path.exists(os.path.join(local_repo_path, '.git')):
    print("Initializing Git repository...")
    if run_command("git init", cwd=local_repo_path):
        print("Git repository initialized successfully.")
    else:
        print("Failed to initialize Git repository.")
        exit(1)

# Ajouter tous les fichiers au suivi sauf les sous-modules
print("Adding files to Git...")
try:
    for root, dirs, files in os.walk(local_repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, local_repo_path)
            if not run_command(f"git add {relative_path}", cwd=local_repo_path):
                print(f"Failed to add {relative_path}")
except Exception as e:
    print(f"Error while adding files: {e}")
    exit(1)

# Créer un commit avec un message pertinent
print("Committing changes...")
if run_command('git commit -m "Initial commit"', cwd=local_repo_path):
    print("Changes committed successfully.")
else:
    print("Failed to commit changes.")
    exit(1)

# Ajouter le dépôt distant (si ce n'est pas déjà fait)
print("Adding remote repository...")
if run_command(f"git remote add origin {remote_repo_url}", cwd=local_repo_path):
    print("Remote repository added successfully.")
else:
    print("Failed to add remote repository.")
    exit(1)

# Pousser les modifications vers le dépôt distant
print("Pushing to remote repository...")
if run_command("git push -u origin master", cwd=local_repo_path):
    print("Pushed to remote repository successfully.")
else:
    print("Failed to push to remote repository.")
    exit(1)
