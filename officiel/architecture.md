# Structure du Module Réseau

## 1. Dossier DATA/

### network/
**Rôle** : Stockage des données statiques du réseau  
**Contenu** :  
- `plants.json` : Données des centrales
  ```json
  {
    "id": "BEA",
    "name": "Beauharnois",
    "nominal_power": 1912,
    "coordinates": [45.3119, -73.9128],
    "voltage": 735
  }
  ```
- `lines.json` : Données des lignes de transmission
  ```json
  {
    "id": "L7040",
    "voltage": 735,
    "from_bus": "BEA",
    "to_bus": "HER",
    "length": 150.5,
    "num_parallel": 2,
    "resistance": 0.0001,
    "reactance": 0.001
  }
  ```
- `substations.json` : Données des postes électriques
- `load_zones.json` : Zones de consommation

**Utilisation** : 
- Base pour la construction du réseau dans PyPSA
- Référence pour les analyses de flux de puissance

### timeseries/
**Rôle** : Stockage des données variables dans le temps  
**Contenu** :
- `consumption/` : Profils de consommation par zone (données horaires)
- `generation/` : Profils de production des centrales (données horaires)

**Utilisation** : 
- Données d'entrée pour les simulations temporelles
- Analyse des flux de puissance variables

## 2. Dossier CORE/

### __init__.py
**Rôle** : Définir le package core  
**Contenu** :
- Imports des classes principales
- Définition des exports

**Utilisation** :
- Organisation du package
- Simplification des imports

### network_builder.py
**Rôle** : Construction du réseau PyPSA  
**Contenu** :
- Classe NetworkBuilder
- Création des composants réseau
- Intégration des données temporelles

**Utilisation** :
- Point d'entrée pour la création du réseau
- Construction du modèle PyPSA

### power_flow.py
**Rôle** : Calculs de flux de puissance  
**Contenu** :
- Méthodes de calcul AC/DC
- Analyse des pertes
- Gestion des contraintes réseau

**Utilisation** :
- Calculs de flux de puissance
- Analyse des contraintes de transport

### optimization.py
**Rôle** : Optimisation du dispatch  
**Contenu** :
- Algorithmes d'optimisation
- Contraintes du réseau
- Fonctions objectifs

**Utilisation** :
- Optimisation de la production
- Minimisation des pertes

## 3. Dossier UTILS/

### __init__.py
**Rôle** : Définir le package utils  
**Contenu** :
- Imports des fonctions utilitaires
- Définition des exports

### data_loader.py
**Rôle** : Chargement des données  
**Contenu** :
- Lecture des fichiers JSON
- Chargement des séries temporelles
- Gestion des erreurs

**Utilisation** :
- Chargement des données du réseau
- Import des séries temporelles

### validators.py
**Rôle** : Validation des données  
**Contenu** :
- Schémas de validation
- Vérification des contraintes électriques
- Détection des erreurs

**Utilisation** :
- Validation des données d'entrée
- Vérification de la cohérence

### geo_utils.py
**Rôle** : Calculs géographiques  
**Contenu** :
- Calcul des distances
- Optimisation des tracés
- Contraintes géographiques

**Utilisation** :
- Calcul des longueurs de lignes
- Optimisation des tracés

### time_utils.py
**Rôle** : Gestion des données temporelles  
**Contenu** :
- Synchronisation des séries temporelles
- Agrégation des données
- Gestion des périodes

**Utilisation** :
- Traitement des données horaires
- Préparation des simulations temporelles

### visualization_utils.py
**Rôle** : Visualisation des résultats  
**Contenu** :
- Génération de graphiques
- Visualisation du réseau
- Export des résultats

**Utilisation** :
- Présentation des résultats
- Création de rapports

## 4. Dossier TESTS/

### __init__.py
**Rôle** : Configuration des tests  
**Contenu** :
- Configuration du framework de test
- Fixtures communes

### test_network_builder.py
**Rôle** : Tests du constructeur de réseau  
**Contenu** :
- Tests unitaires NetworkBuilder
- Vérification de la topologie

### test_power_flow.py
**Rôle** : Tests des calculs de flux  
**Contenu** :
- Tests des calculs AC/DC
- Vérification des résultats

### test_data_loader.py
**Rôle** : Tests du chargement des données  
**Contenu** :
- Tests de lecture des fichiers
- Validation des formats