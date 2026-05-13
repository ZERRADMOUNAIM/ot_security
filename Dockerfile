# Utiliser une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du projet
COPY . .

# Créer le dossier instance pour la base de données SQLite et donner les permissions
RUN mkdir -p instance && chmod 777 instance

# Exposer le port utilisé par Hugging Face
EXPOSE 7860

# Lancer l'application avec Gunicorn sur le port 7860
# --bind 0.0.0.0:7860 est crucial pour Hugging Face
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "run:app"]
