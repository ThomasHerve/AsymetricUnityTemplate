# Utiliser une image de base Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le script Python dans le répertoire de travail
COPY instance/app.py .

# Installer les dépendances nécessaires
RUN pip install websockets
RUN pip install requests

# Exposer le port 80 pour les connexions WebSocket
EXPOSE 8000

# Commande pour exécuter le script Python
CMD ["python", "app.py"]