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
   ```bash
   RouleMaPouleSansNidDePoule$ python -m venv venv/ 
   ```
2. Activer l'environnement sous Linux/Mac OS (avec le bash):
    ```bash
   RouleMaPouleSansNidDePoule$ source venv/bin/activate
   ```
3. Ou activer l'environnement sous Windows avec cmd (pas PowerShell):
    ```cmd
    C:\RouleMaPouleSansNidDePoule> venv\Scripts\activate.bat
    ```
4. Installer les dépendances : 
   ```cmd
   RouleMaPouleSansNidDePoule$ pip install requirements.txt
   ```