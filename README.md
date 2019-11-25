# RouleMaPouleSansNidDePoule

- *GitHub* : https://github.com/CLacaile/RouleMaPouleSansNidDePoule.git
- *Trello* : https://trello.com/b/NjvDcvLZ
- *Discord* : https://discord.gg/Hne3Haj

## Introduction

*RouleMaPouleSansNidDePoule* est un projet de recherche et développement mis en place en 2018-2019 par N.Monmarché et XXX avec pour but de concevoir un capteur destiné à recueillir des informations sur la rugosité des routes utilisées par les cyclistes. Le capteur est conçu sur la base d'un micro-contrôleur ESP32 qui une fois monté sur un vélo, permet de corréler la position GPS du cycliste avec des données de vibration fournies par un accéléromètre. Il est à noter que le dispositif peut être remplacé par un téléphone portable, qui, pour la plupart sont aujourd'hui dotés d'une puce GPS et d'un accéléromètre. Mais pour pouvoir maitriser le type de capteur et de fait recueillir des données de test cohérentes, il a paru évident de mettre au point une version externe du capteur dont tous les aspects techniques sont maîtrisés.

## Enjeux

Dans le cadre du projet SI de DI5, l'équipe, constituée de Yann Paillet, Timothé Sanouiller, Nathan Sarniguet, Guillem Orelle et Clément Lacaïle, devra s'occuper de la gestion des données du projet lancé l'an dernier. Les enjeux sont les suivants :

- Proposer une solution pour le stockage des données sur le serveur, en prenant en compte l'aspect collaboratif de l'applicatif par le recueil de données grâce à une multitude d'utilisateurs (depuis le boitier capteur ou, à terme, un smartphone)
- Définir un modèle d'analyse des données de vibration des routes à partir de la quantité de données mise à disposition par les utilisateurs
- Etablir une visualisation de l'état des routes en s'appuyant sur OpenStreetMap

## Paramétrage

Pour paramétrer l'environnement de développement, suivre la démarche suivante : 

1. Créer un environnement virtuel "venv" (il doit absoluement s'appeler "venv/") : 
   ```console
   RouleMaPouleSansNidDePoule$ python -m venv venv/ 
   ```
2. Activer l'environnement sous Linux/Mac OS (avec le bash):
    ```console
   RouleMaPouleSansNidDePoule$ source venv/bin/activate
   ```
3. Ou activer l'environnement sous Windows avec cmd (pas PowerShell):
    ```cmd
    C:\RouleMaPouleSansNidDePoule> venv\Scripts\activate.bat
    ```
4. Installer les dépendances : 
   ```console
   RouleMaPouleSansNidDePoule$ pip install requirements.txt
   ```
## Lancement du serveur

Pour lancer le serveur de développement, il faut utiliser la commande suivante : 

```console
RouleMaPouleSansNidDePoule$ python manage.py runserver
```

Si des modifications ont été apportées au modèle, n'oubliez pas de lancer : 
```console
RouleMaPouleSansNidDePoule$ python manage.py makemigrations
RouleMaPouleSansNidDePoule$ python manage.py migrate
```

## Installation de la base de données (en local)

1. Télécharger et installer Mongodb server community edition (https://www.mongodb.com/download-center/community)  
Pour l'installer sous macOS suivre les instructions du lien suivant (https://medium.com/@saurabhkumar_4718/install-mongodb-without-homebrew-on-mac-os-2a98b68ab09c)

2. Créer une base de données dans Mongodb
    - En ligne de commande  
    ```console
    mongod
   use RouleMaPoule_DB
    ```
    - Via l'interface graphique Mongodb Compass  (https://www.mongodb.com/download-center/compass)  
    Lancer Mongodb Compass et creer une connection à l'adresse *localhost:27017*  
    Clicker sur *create database*, entrer le nom de la db et creer la base de données    
3. Renseigner le nom de cette base de données dans le fichier *settings.py* ('NAME': 'RouleMaPoule_DB')

4. Charger le modèle dans la base de données une première fois, lancez : 
```console
RouleMaPouleSansNidDePoule$ python manage.py makemigrations
RouleMaPouleSansNidDePoule$ python manage.py migrate
```
## Population de la base de données

Pour populer la base de données lancez :
```console
RouleMaPouleSansNidDePoule$ python manage.py populate_db
```
Script de population : (RouleMaPoule/input/management/comands/populate_db.py)

## Insertion manuelle de données depuis un navigateur avec djangorestframework

Pour insérer des données dans l'application, on peut utiliser le client web fournit par Django Rest Framework (DRF).
Il faut ajouter manuellement chaque objet :
- Ajouter un objet Path en se connectant à l'adresse localhost:8000/api/v1.0/input/path"
- Ajouter un objet Waypoint en se connectant à l'adresse localhost:8000/api/v1.0/input/waypoint"
- Ajouter un objet Acceleration en se connectant à l'adresse localhost:8000/api/v1.0/input/acceleration"



## Installation de la partie front-end graphique: 

1. Pour Windows installer une application de serveur web ( Type wampp: http://www.wampserver.com/en/ )
   Pour Linux installer un serveur web et php
   ```console
    apt-get install apache2 php7.0 php7.0-mysql libapache2-mod-php7.0
   ```

2. Placer les fichiers contenue dans '/input_frontend' dans votre dossier de site web:
3. Changer les lignes suivantes :
  upload_no_connexion.html :
  - ligne 60 :
   ```javascript
      url : [url rest POST files],
   ```
  scripts.js :
  - ligne 11 :
   ```javascript
      url : [url rest POST connexion],
   ```
3. Lancer votre navigateur sur votre site.