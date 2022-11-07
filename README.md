# Digikofy

Table des matières
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

<b>Méthode</b> : `GET`<br/>
<b>Route</b> : `/machines`<br/>
<b>Retourne</b> : La liste de toutes les machines disponibles sous forme de liste et retourne un code de statut<br/>

<b>Méthode</b> : `GET`<br/>
<b>Route</b> : `/machine/{id}`<br/>
<b>Retourne</b> : La machine ayant pour identifiant celui passé dans la route et retourne un code de statut<br/>

<b>Méthode</b> : `POST`<br/>
<b>Route</b> : `/machine`<br/>
<b>Données d’entrée</b> :
  - `Id` : Identifiant de la machine à café
  - `State` : Etat de la machine à café
  - `Type` : Type de machine à café
  - `Name` : Nom de la machine à café donné par l’utilisateur
  
<b>Retourne</b> : La machine ayant pour identifiant celui passé dans la route et retourne un code de statut

<b>Méthode</b> : `PUT`<br/>
<b>Route</b> : `/machine/{id}`<br/>
<b>Données d’entrée</b> :
  - `Name` : Nom de la machine à café donné par l’utilisateur<br/>

<b>Retourne</b> : Ne retourne rien et modifie le nom de la machine ayant pour identifiant celui passé dans la 
route avec le nom passé en entrée et retourne un code de statut

<b>Méthode</b> : `DELETE`<br/>
<b>Route</b> : `/machine/{id}`<br/>
<b>Retourne</b> : Ne retourne rien et supprime la machine ayant pour identifiant celui passé dans la route
ainsi que toutes les préparations ayant pour machine attitrée cette dernière et retourne un code de 
statut

### Café

<b>Méthode</b> : `GET`<br/>
<b>Route</b> : `/coffees`<br/>
<b>Retourne</b> : La liste de tous les cafés sous forme de liste et retourne un code de statut

<b>Méthode</b> : `GET`<br/>
<b>Route</b> : `/coffee/{id}`<br/>
<b>Retourne</b> : Le café ayant pour identifiant celui passé dans la route et retourne un code de statut

### Préparation

<b>Méthode</b> : `POST`<br/>
<b>Route</b> : `/preparation`<br/>
<b>Données d’entrée</b> :<br/>
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
<b>Retourne</b> : Ajoute une préparation avec les informations données et retourne un code de statut

<b>Méthode</b> : `GET`<br/>
<b>Route</b> : `/preparations`<br/>
<b>Retourne</b> : Retourne toutes les préparations de l’utilisateur et retourne un code de statut

<b>Méthode</b> : `PUT`<br/>
<b>Route</b> : `/preparation/{id}`<br/>
<b>Données d’entrée</b> :
  - `Coffee_id` : Identifiant du café déjà existant
  - `Machine_id` : Identifiant de la machine déjà existant
  - `DaysOfWeek` : Liste de jours de la semaine
  - `Hours` : Liste d’heures
  - `Name` : Nom de la préparation<br/>
  
<b>Retourne</b> : Met à jour une préparation ayant l’identifiant donné dans la route et retourne un code de 
statut

<b>Méthode</b> : `DELETE`<br/>
<b>Route</b> : `/preparation/{id}`<br/>
<b>Retourne</b> : Supprime la préparation ayant l’identifiant donnée dans la route et retourne un code de 
statut

<b>Méthode</b> : `GET`<br/>
<b>Route</b> : `/preparation/next`<br/>
<b>Retourne</b> : Retourne la prochaine préparation de café prévu et retourne un code de statut

<b>Méthode</b> : `GET`<br/>
<b>Route</b> : `/preparation/last`<br/>
<b>Retourne</b> : Retourne la dernière préparation de café et retourne un code de statut

<b>Méthode</b>: `GET`<br/>
<b>Route</b>: `/preparation/{id}/started`<br/>
<b>Retourne</b> : Met à jour l’état de la préparation (1) et de la machine lié (1) puis ajoute une notification 
dans la collection de notifications afin de déclencher une notification sur l’application mobile et 
retourne un code de statut

<b>Méthode</b>: `GET`<br/>
<b>Route</b>: `/preparation/{id}/succeeded`<br/>
<b>Retourne</b> : Met à jour l’état de la préparation (1) et de la machine lié (0) ensuite met à jour l’attribut 
next_time si c’est une préparation sauvegardée en le calculant avec l’attribut daysOfWeek et hours de 
la préparation et enfin ajoute une notification dans la collection de notifications afin de déclencher 
une notification sur l’application mobile et retourne un code de statut

<b>Méthode</b> : `GET`<br/>
<b>Route</b> : `/preparation/{id}/failed`<br/>
<b>Retourne</b> : Met à jour l’état de la préparation (0) et de la machine lié (0) ensuite met à jour l’attribut 
next_time si c’est une préparation sauvegardée en le calculant avec l’attribut daysOfWeek et hours de 
la préparation et enfin ajoute une notification dans la collection de notifications afin de déclencher 
une notification sur l’application mobile et retourne un code de statut

