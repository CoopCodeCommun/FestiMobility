# Cahier des Charges — Application de Gestion de Mobilité Douce pour Événements

## 1. Présentation du projet

L’application vise à faciliter le covoiturage pour des événements culturels (festivals, concerts, etc.), en mettant en relation des conducteurs proposant un trajet et des passagers cherchant à se rendre à un événement. L’accent est mis sur la visualisation des trajets sur une carte interactive, la simplicité d’utilisation et la sécurité des échanges.

---

## 2. Objectifs fonctionnels

### 2.1. Utilisateurs

- Deux types d’utilisateurs :
  - Conducteurs : proposent un trajet (horaire, lieu de départ, nombre de places, etc.).
  - Passagers : recherchent un trajet pour rejoindre un événement.
- Inscription et authentification sécurisée (email, mot de passe, éventuellement réseaux sociaux).

### 2.2. Gestion des trajets

- Création, modification et suppression d’une proposition de trajet par un conducteur.
- Recherche et filtrage des trajets par les passagers (par événement, horaire, lieu de départ).
- Affichage des trajets sur une carte interactive (OpenStreetMap + Leaflet).
- Visualisation des horaires et points de départ/arrivée.
- Matching intelligent des propositions grâce à Valhalla (calcul d’itinéraires et suggestions optimisées).

### 2.3. Messagerie

- Système de messagerie interne pour permettre la prise de contact entre conducteurs et passagers.
- Notifications lors de la réception d’un nouveau message ou d’une demande de réservation.

### 2.4. Réservation et gestion des places

- Les passagers peuvent envoyer une demande pour réserver une place sur un trajet.
- Les conducteurs peuvent accepter ou refuser les demandes.
- Mise à jour automatique du nombre de places disponibles.

---

## 3. Objectifs non-fonctionnels

- Application responsive (Bootstrap 5).
- Interface utilisateur fluide et dynamique (HTMX).
- Sécurité des données et des échanges.
- Performance (temps de réponse rapide, gestion efficace des requêtes cartographiques).
- Respect de la vie privée (RGPD).

---

## 4. Spécifications techniques

- Backend : Django 5.2
- Frontend : HTMX, Bootstrap 5
- Cartographie : OpenStreetMap & Leaflet
- Calcul d’itinéraires et matching : Valhalla
- Gestion des dépendances : poetry
- Philosophie de développement : Test Driven Development (TDD)
- Base de données : PostgreSQL (recommandé pour gestion géospatiale)
- API RESTful pour les échanges front/back

---

## 5. Parcours utilisateur

### 5.1. Conducteur

1. S’inscrit/se connecte.
2. Propose un trajet (lieu, horaire, nombre de places, etc.).
3. Visualise sa proposition sur la carte.
4. Reçoit des messages/demandes de passagers.
5. Gère les réservations.

### 5.2. Passager

1. S’inscrit/se connecte.
2. Recherche un trajet pour un événement.
3. Visualise les propositions sur la carte.
4. Envoie une demande de réservation/message au conducteur.
5. Suit l’état de sa demande.

---

## 6. Sécurité & RGPD

- Stockage sécurisé des mots de passe (hashing).
- Validation des emails.
- Journalisation des actions sensibles.
- Suppression des données sur demande.
- Consentement explicite pour la collecte des données personnelles.

---

## 7. Méthodologie & livrables

- Développement piloté par les tests (TDD) : chaque fonctionnalité est couverte par des tests unitaires et d’intégration.
- Documentation technique et utilisateur.
- Déploiement continu (CI/CD).
- Livraison d’un MVP fonctionnel, puis itérations selon les retours utilisateurs.

---

## 8. Planning prévisionnel (exemple)

1. Spécification détaillée & maquettage : 1 semaine
2. Mise en place du socle technique, CI/CD, TDD : 1 semaine
3. Authentification & gestion des utilisateurs : 1 semaine
4. Création/recherche de trajets & cartographie : 2 semaines
5. Messagerie et notifications : 1 semaine
6. Matching intelligent avec Valhalla : 1 semaine
7. Tests, débogage, documentation : 1 semaine
8. Déploiement MVP : 1 semaine

---

## 9. Annexes

- Liens vers les API et documentations utilisées (Leaflet, Valhalla, HTMX, Bootstrap).
- Exemples de wireframes (à réaliser).
- Règles de nommage et conventions de code.

---
