Créer un environnement virtuel sous Python 3.10
Installer les dépendances : pip install -r requirements.txt
installer fastapi[standard] (nécessaire pour avoir accès au lancement en ligne de commande) : pip install "fastapi[standard]"

Pour récupérer de nouvelles données depuis GitHub:
Fournir un token dans .env
lancer main.py

Pour lancer l'API : uvicorn api.main:app


