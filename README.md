# Digikofy

Table des matières :

- Présentation globale du projet
- Routes


## Présentation globale du projet

Le projet Digikofy est une application mobile Android. Cette application mobile permet de multiples interactions avec des cafetières compatibles et la gestion et planification de préparations de cafés. 

Le projet est divisé en 2 partie, ici nous nous concentrons sur la partie backend, pour la partie frontend (<a href="https://github.com/MaximeDubost/Digikofy">ici</a>) 

L’objectif de cette partie est intéragir avec la base de données (Firestore) à l'aide d'une API faite en Python avec la librairie FastAPI, et cette dernière devra pouvoir faire les actions suivantes :

- Gérer les machines, leurs détails, mettre à jour leurs informations et de pouvoir supprimer une 
machine (CRUD)
- Gérer les préparations, leurs détails, mettre à jour leurs informations et de pouvoir supprimer 
une préparation (CRUD)
- Récupérer la dernière préparation qui a été accomplie
- Récupérer la prochaine préparation à accomplir
- Faire un rapport à l’application mobile en cas de succès d’une préparation
- Faire un rapport à l’application mobile en cas d’échec d’une préparation
- Récupérer la liste de tous les types de cafés disponibles (R)

## Routes 
### Machine

*Méthode* : `GET`<br/>
*Route* : `/machines`<br/>
*Retourne* : La liste de toutes les machines disponibles sous forme de liste et retourne un code de statut<br/>

*Méthode* : `GET`<br/>
*Route* : `/machine/{id}`<br/>
*Retourne* : La machine ayant pour identifiant celui passé dans la route et retourne un code de statut<br/>

*Méthode* : `POST`<br/>
*Route* : `/machine`<br/>
*Données d’entrée* :
  - `Id` : Identifiant de la machine à café
  - `State` : Etat de la machine à café
  - `Type` : Type de machine à café
  - `Name` : Nom de la machine à café donné par l’utilisateur
  
*Retourne* : La machine ayant pour identifiant celui passé dans la route et retourne un code de statut

*Méthode* : `PUT`<br/>
*Route* : `/machine/{id}`<br/>
*Données d’entrée* :
  - `Name` : Nom de la machine à café donné par l’utilisateur<br/>

*Retourne* : Ne retourne rien et modifie le nom de la machine ayant pour identifiant celui passé dans la 
route avec le nom passé en entrée et retourne un code de statut

*Méthode* : `DELETE`<br/>
*Route* : `/machine/{id}`<br/>
*Retourne* : Ne retourne rien et supprime la machine ayant pour identifiant celui passé dans la route
ainsi que toutes les préparations ayant pour machine attitrée cette dernière et retourne un code de 
statut

### Café

*Méthode* : `GET`<br/>
*Route* : `/coffees`<br/>
*Retourne* : La liste de tous les cafés sous forme de liste et retourne un code de statut

*Méthode* : `GET`<br/>
*Route* : `/coffee/{id}`<br/>
*Retourne* : Le café ayant pour identifiant celui passé dans la route et retourne un code de statut

### Préparation

*Méthode* : `POST`<br/>
*Route* : `/preparation`<br/>
*Données d’entrée* :<br/>
Si `saved` est égal à vrai :<br/>
  - `Coffee_id` : Identifiant du café voulu
  - `DaysOfWeek` : Liste de jours pour la prochaine préparation (0 = Lundi, 1=Mardi etc.)
  - `Hours` : Liste d’heures pour la prochaine préparation
  - `Machine_id` : Identifiant de la machine concernée
  - `Name` : Nom de la préparation
  - `Saved` : Si la préparation est sauvegardée alors vrai sinon faux<br/>
  
Si `saved` est égal à faux :<br/>
  - `Coffee_id` : Identifiant du café voulu
  - `Machine_id` : Identifiant de la machine concernée
  - `Name` : Nom de la préparation
  - `Saved` : Si la préparation est sauvegardée alors vrai sinon faux<br/>
*Retourne* : Ajoute une préparation avec les informations données et retourne un code de statut

*Méthode* : `GET`<br/>
*Route* : `/preparations`<br/>
*Retourne* : Retourne toutes les préparations de l’utilisateur et retourne un code de statut

*Méthode* : `PUT`<br/>
*Route* : `/preparation/{id}`<br/>
*Données d’entrée* :
  - `Coffee_id` : Identifiant du café déjà existant
  - `Machine_id` : Identifiant de la machine déjà existant
  - `DaysOfWeek` : Liste de jours de la semaine
  - `Hours` : Liste d’heures
  - `Name` : Nom de la préparation<br/>
  
*Retourne* : Met à jour une préparation ayant l’identifiant donné dans la route et retourne un code de 
statut

*Méthode* : `DELETE`<br/>
*Route* : `/preparation/{id}`<br/>
*Retourne* : Supprime la préparation ayant l’identifiant donnée dans la route et retourne un code de 
statut

*Méthode* : `GET`<br/>
*Route* : `/preparation/next`<br/>
*Retourne* : Retourne la prochaine préparation de café prévu et retourne un code de statut

*Méthode* : `GET`<br/>
*Route* : `/preparation/last`<br/>
*Retourne* : Retourne la dernière préparation de café et retourne un code de statut

*Méthode*: `GET`<br/>
*Route*: `/preparation/{id}/started`<br/>
*Retourne* : Met à jour l’état de la préparation (1) et de la machine lié (1) puis ajoute une notification 
dans la collection de notifications afin de déclencher une notification sur l’application mobile et 
retourne un code de statut

*Méthode*: `GET`<br/>
*Route*: `/preparation/{id}/succeeded`<br/>
*Retourne* : Met à jour l’état de la préparation (1) et de la machine lié (0) ensuite met à jour l’attribut 
next_time si c’est une préparation sauvegardée en le calculant avec l’attribut daysOfWeek et hours de 
la préparation et enfin ajoute une notification dans la collection de notifications afin de déclencher 
une notification sur l’application mobile et retourne un code de statut

*Méthode* : `GET`<br/>
*Route* : `/preparation/{id}/failed`<br/>
*Retourne* : Met à jour l’état de la préparation (0) et de la machine lié (0) ensuite met à jour l’attribut 
next_time si c’est une préparation sauvegardée en le calculant avec l’attribut daysOfWeek et hours de 
la préparation et enfin ajoute une notification dans la collection de notifications afin de déclencher 
une notification sur l’application mobile et retourne un code de statut

