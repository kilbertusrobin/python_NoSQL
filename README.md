# Projet Python NoSQL

Ce projet est une application Python conçue pour interagir avec une base de données NoSQL. Il utilise Docker pour la gestion des services et un environnement virtuel Python pour l'isolation des dépendances.

## Fonctionnalités

- Interaction avec une base de données NoSQL
- Utilisation de Docker pour le déploiement
- Environnement Python virtualisé

## Installation

### Prérequis

- Python 3.x
- Docker et Docker Compose installés

### Étapes

1. Cloner le dépôt :
```
   git clone https://github.com/kilbertusrobin/python_NoSQL.git
   cd python_NoSQL
```

2. Créer et activer l’environnement virtuel :

   Sous Windows :

       python -m venv venv
       venv\Scripts\activate

   Sous macOS/Linux :

       python3 -m venv venv
       source venv/bin/activate

3. Installer les dépendances Python :

       pip install -r requirements.txt

4. Lancer les services Docker :

       docker-compose up -d

5. Exécuter l’application :

       python run.py

## Structure du projet

```
python_NoSQL/
├── app/                  -> Code principal de l’application
├── docker-compose.yml    -> Configuration Docker
├── requirements.txt      -> Dépendances Python
├── run.py                -> Point d’entrée de l’application
└── .env                  -> Variables d’environnement (optionnel)
```

