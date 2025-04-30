# FestiMobility

## Présentation
FestiMobility est une application web de gestion de mobilité douce, facilitant le covoiturage pour des événements tels que festivals ou concerts. Elle met en relation des conducteurs proposant des trajets et des passagers souhaitant rejoindre un événement, avec une visualisation sur carte interactive.

## Fonctionnalités principales
- Deux types d'utilisateurs : conducteurs et passagers
- Propositions de trajets avec horaires et points de départ/arrivée
- Recherche et filtrage des trajets
- Carte interactive (OpenStreetMap & Leaflet)
- Matching intelligent des propositions (Valhalla)
- Système de messagerie interne
- Gestion des réservations et des places
- Notifications

## Technologies utilisées
- Django 5.2
- HTMX
- Bootstrap 5
- OpenStreetMap & Leaflet
- Valhalla (calcul d'itinéraires)
- Mapbox Matrix API (MVP)
- poetry
- PostgreSQL (recommandé)
- API RESTful
- TDD (Test Driven Development)

---

## Calcul d'itinéraires et matching : deux modèles

FestiMobility propose deux approches pour le calcul des distances et le matching conducteur/passager :

### 1. Mapbox Matrix API (solution MVP)

- **Principe** : Utilisation de l'API cloud de Mapbox pour calculer les distances/durations entre points (conducteurs, passagers).
- **Avantages** :
  - Intégration rapide (API REST, pas d'infrastructure à gérer)
  - Données cartographiques et algorithmes maintenus par Mapbox
  - Support et documentation de qualité
- **Inconvénients** :
  - Limites d'utilisation selon le plan (payant au-delà du quota gratuit)
  - Dépendance à un service tiers (RGPD à surveiller)
  - Moins de personnalisation possible

**→ Cette solution est priorisée pour le MVP afin d'accélérer le développement et les tests utilisateurs.**

### 2. Valhalla (solution open source, en cours de développement)

- **Principe** : Serveur de routage open source auto-hébergé, basé sur OpenStreetMap.
- **Avantages** :
  - Souveraineté des données
  - Personnalisation avancée (profils, algorithmes, etc.)
  - Pas de coût récurrent lié à un service externe
- **Inconvénients** :
  - Mise en place et maintenance technique plus complexe
  - Nécessite des ressources serveur

**→ L'intégration Valhalla reste un objectif pour la version stable, afin de garantir la maîtrise des coûts et des données.**

---

### Scripts de démonstration

- `valhalla_matching_example.py` : exemple de matching utilisant Valhalla (serveur local requis)
- `demo_mapbox_matrix.py` : exemple équivalent utilisant l'API Mapbox (clé API nécessaire)

Voir chaque script pour les instructions spécifiques.

## Installation
1. Cloner le dépôt :
   ```bash
   git clone <repo-url>
   cd FestiMobility
   ```
2. Copier le fichier d'exemple d'environnement :
   ```bash
   cp env_example .env
   ```
   Modifiez les variables si besoin (base de données, secret Django, etc.)
3. Installer les dépendances Python avec poetry :
   ```bash
   poetry install
   ```
4. Préparer les données de routage Valhalla (OSM + tiles) :
   ```bash
   make install
   ```
   Cette commande télécharge les données OSM France, génère les tiles Valhalla et prépare le dossier `./valhalla_data`.
5. Démarrer Valhalla (API de routage) et PostgreSQL :
   ```bash
   make valhalla-up
   ```
   Les services seront accessibles sur http://localhost:8002 (Valhalla) et localhost:5432 (PostgreSQL). Les variables du .env sont automatiquement lues par docker-compose.
6. Appliquer les migrations Django :
   ```bash
   poetry run python manage.py migrate
   ```
7. Lancer le serveur Django :
   ```bash
   poetry run python manage.py runserver
   ```

### Commandes Makefile utiles
- `make install` : prépare les données Valhalla
- `make valhalla-up` : démarre Valhalla et PostgreSQL en arrière-plan
- `make valhalla-down` : stoppe les services
- `make valhalla-clean` : supprime toutes les données générées

## Tests
L'approche TDD est privilégiée. Pour lancer les tests :
```bash
poetry run python manage.py test
```

## Contribution
Merci de consulter le cahier des charges (`cahier_des_charges.md`) avant toute contribution.

## Licence
AGPLv3
