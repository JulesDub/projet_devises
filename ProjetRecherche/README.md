# Mini-Projet : Application de Suivi des Cours des Devises

## Equipe :
Jules Dubayle

## Description
L'objectif de ce projet est de créer une application pour suivre les cours de certaines devises (dollars, livre sterling, couronne suédoise) et de les stocker dans une base de données. Les utilisateurs peuvent visualiser l'évolution des cours à l'aide de graphiques, ajouter de nouvelles monnaies via un fichier CSV, et accéder aux données via une API REST.

## Technologies Utilisées
- **Backend** : Flask (Python) - Pour la création de l'API REST et la gestion des requêtes.
- **Frontend** : HTML, CSS, JavaScript, Chart.js - Pour l'interface utilisateur et l'affichage des graphiques.
- **Base de Données** : MySQL - Pour le stockage des données des devises.
- **Plugin** : Chart.js Zoom - Pour ajouter des fonctionnalités de zoom et de pan aux graphiques.

## Modèles de Données
- **Devise** :
  - `id` : Identifiant unique de la devise.
  - `nom` : Nom de la devise.
  - `symbole` : Symbole de la devise (ex: USD, EUR).

- **Cours** :
  - `id` : Identifiant unique du cours.
  - `devise_id` : Identifiant de la devise associée.
  - `valeur` : Valeur du cours.
  - `date` : Date du cours.

## Script SQL pour Créer la Base de Données

```sql
-- Créer la base de données
CREATE DATABASE IF NOT EXISTS suivi_devises;
USE suivi_devises;

-- Créer la table 'devises'
CREATE TABLE IF NOT EXISTS devises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL,
    symbole VARCHAR(10) NOT NULL
);

-- Créer la table 'cours'
CREATE TABLE IF NOT EXISTS cours (
    id INT AUTO_INCREMENT PRIMARY KEY,
    devise_id INT NOT NULL,
    valeur DECIMAL(20, 15) NOT NULL, -- Haute précision pour les valeurs de cours
    date DATETIME NOT NULL,
    FOREIGN KEY (devise_id) REFERENCES devises(id)
);
```


## Fonctionnalités
- Affichage des cours des devises sous forme graphique.
- Chargement de nouvelles devises et de cours via un fichier CSV.
- Accès aux données via une API REST.

## Problèmes Rencontrés et Solutions
1. **Problème** : Les valeurs des cours n'étaient pas affichées correctement en raison d'une précision insuffisante dans la base de données.
   - **Solution** : Nous avons modifié le type de données de la colonne `valeur` dans la table `cours` pour utiliser `DECIMAL(20, 15)` afin de stocker des valeurs avec une haute précision.

2. **Problème** : Le graphique ne se mettait pas à jour correctement lors de la sélection d'une nouvelle devise.
   - **Solution** : Nous avons ajouté une logique pour détruire l'ancien graphique avant d'en créer un nouveau à chaque changement de devise.

3. **Problème** : Le sélecteur de devises devenait invisible lorsque le graphique était affiché.
   - **Solution** : Nous avons ajusté le CSS pour garantir que le sélecteur de devises reste visible et bien positionné.

4. **Problème** : Le chargement de fichiers CSV pouvait échouer en raison de différents formats de colonnes.
   - **Solution** : Nous avons ajouté une logique pour identifier dynamiquement les colonnes de devises dans le fichier CSV et les traiter correctement.

5. **Problème** : Le zoom du graphique affectait l'ensemble de la page.
   - **Solution** : Nous avons intégré le plugin Chart.js Zoom pour permettre le zoom sur le graphique sans affecter le reste de la page.

## Installation

### Backend
1. Cloner le dépôt :
   ```sh
   git clone https://github.com/JulesDub/projet_devises.git
   cd projet_devises
