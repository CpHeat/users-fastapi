# 📦 GitHub Users Extractor & FastAPI API

Ce projet Python est structuré en deux volets :

1. **Extraction, nettoyage et filtrage de données d'utilisateurs GitHub**
2. **Exposition de ces données via une API REST sécurisée avec FastAPI**

---

## 📂 Structure du projet

```
.
├── api/
│   ├── main.py             # Point d'entrée de l'API FastAPI
│   ├── models.py           # Modèles Pydantic
│   ├── routes.py           # Endpoints de l'API
│   ├── security.py         # Logique de sécurité
│
├── data/
│   ├── users.json          # Données brutes extraites de GitHub
│   └── filtered_user.json  # Données nettoyées/filtrées prêtes à servir via l'API
│
├── tests/
│   └── test_api.py         # Tests unitaires de l'API
│
├── .env                    # Token GitHub & utilisateurs de l'API
├── .gitignore
├── extract_users.py
├── filtered_users.py
├── LICENSE
├── main.py                 # Script principal pour interroger l’API GitHub
├── README.md
├── requirements.txt        # Dépendances
```

---

## ⚖️ Prérequis

* Python **3.10**
* Un compte GitHub avec un **token personnel** (PAT)

---

## ⚙️ Installation et configuration

### 1. Créer un environnement virtuel

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
pip install "fastapi[standard]"
```

> Le paquet `fastapi[standard]` est requis pour utiliser les commandes FastAPI en CLI.

### 3. Configurer le token GitHub

Dans le fichier `.env` à la racine du projet, ajouter :

```env
GITHUB_TOKEN=ton_token_github_ici
```

---

## 🧰 Extraction et traitement des utilisateurs

### 1. Extraire les données de GitHub

```bash
python main.py
```

→ Génère `data/users.json` & `data/filtered_user.json`

---

## 🌐 Lancer l’API FastAPI

```bash
uvicorn api.main:app --reload
```

API disponible par défaut sur `http://127.0.0.1:8000`
Documentation et tests disponibles par défaut sur `http://127.0.0.1:8000/redoc` & `http://127.0.0.1:8000/docs`
---

## 📚 Endpoints principaux

* `GET /users` — Liste filtrée des utilisateurs (`id`, `login`)
* `GET /users/{login}` — Détails d’un utilisateur (`id`, `login`, `created_at`, `avatar_url`, `bio`)
* `GET /users/search?q=<texte>` — Recherche partielle sur le login (`id`, `login`)

---

## 🔒 Sécurité

L’API est conçue pour être sécurisée. La logique est gérée dans `api/security.py`.
La liste d'utilisateurs autorisés se trouve dans `.env`

---

## ✅ Lancer les tests

```bash
pytest tests/test_api.py
```

---

## 🛠️ Technologies

* Python 3.10
* FastAPI
* Uvicorn
* dotenv
* GitHub REST API

---

## 📄 Licence

Ce projet est sous licence MIT.

---

## 👤 Auteur

Développé par [@CpHeat](https://github.com/CpHeat)