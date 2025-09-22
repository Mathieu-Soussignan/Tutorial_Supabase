# AI Projects Hub - Supabase + Python Tutorial

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Supabase](https://img.shields.io/badge/Supabase-Backend-green.svg)](https://supabase.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Une démonstration complète d'une application de gestion de projets IA utilisant Supabase comme backend et Python comme langage principal.**

## À propos du projet

Cette application illustre les **avantages de PostgreSQL pour les projets de Machine Learning** par rapport aux solutions NoSQL traditionnelles. Elle propose un système complet de gestion de projets IA avec authentification, CRUD avancé, et analytics temps réel.

### Fonctionnalités principales

- 🔐 **Authentification utilisateur** avec Supabase Auth
- 📋 **CRUD complet** pour les projets IA (NLP, Computer Vision, Deep Learning)
- 📊 **Gestion des datasets** avec métadonnées détaillées
- 🎛️ **Stockage des hyperparamètres** en JSONB PostgreSQL
- 📈 **Analytics temps réel** avec requêtes PostgreSQL avancées
- 🔍 **Recherche full-text** intelligente
- 📁 **Storage intégré** pour fichiers volumineux
- 🛡️ **Sécurité** avec Row Level Security (RLS)

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │◄──► │   Python App    │◄──► │    Supabase     │
│ (Presentation)  │     │ Models/Services │     │ PostgreSQL+Auth │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Stack technique

- **Backend** : Supabase (PostgreSQL + API REST + Auth + Storage)
- **Client** : Python 3.8+ avec supabase-py
- **Architecture** : Models/Services/Config pattern
- **Base de données** : PostgreSQL avec JSONB et RLS
- **Authentification** : JWT tokens avec Supabase Auth

## Installation rapide

### Prérequis

- Python 3.8 ou supérieur
- Git
- Compte Supabase (gratuit)

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/supabase-python-ai-tutorial.git
cd supabase-python-ai-tutorial
```

### 2. Créer l'environnement virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration Supabase

1. Créer un projet sur [supabase.com](https://supabase.com)
2. Exécuter le schema SQL (voir `schema.sql`)
3. Configurer les variables d'environnement

### 5. Variables d'environnement

Copier `.env.example` vers `.env` et remplir :

```env
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_KEY=votre-anon-key
SUPABASE_SERVICE_ROLE_KEY=votre-service-key
```

### 6. Test de connexion

```bash
python test_config.py
```

### 7. Lancer la démo

```bash
python main.py
```

## Structure du projet

```
supabase-python-ai-tutorial/
├── 📁 config/
│   ├── __init__.py
│   └── database.py          # Configuration Supabase
├── 📁 models/
│   ├── __init__.py
│   ├── projet.py            # Modèle ProjetIA
│   └── dataset.py           # Modèle Dataset
├── 📁 services/
│   ├── __init__.py
│   ├── auth_service.py      # Service authentification
│   ├── projet_service.py    # Service projets IA
│   ├── dataset_service.py   # Service datasets
│   └── storage_service.py   # Service fichiers
├── 📁 demos/
│   └── live_demo.py         # Démos interactives
├── main.py                  # Point d'entrée principal
├── test_config.py           # Tests de connexion
├── requirements.txt         # Dépendances Python
├── schema.sql               # Schéma PostgreSQL
├── .env.example             # Template environnement
├── .gitignore
└── README.md
```

## Utilisation

### Exemple d'usage de base

```python
from services.projet_service import ProjetService
from models.projet import ProjetIA

# Créer un nouveau projet IA
projet = ProjetIA(
    nom="Classification d'Images",
    description="CNN pour reconnaissance chats vs chiens",
    type_modele="Computer Vision",
    hyperparametres={
        "architecture": "ResNet50",
        "epochs": 25,
        "batch_size": 32,
        "learning_rate": 0.001
    }
)

# Sauvegarder en base
projet_sauve = ProjetService.creer_projet_ia(projet, user_id)
print(f"Projet créé: {projet_sauve.id}")
```

### Fonctionnalités avancées

- **Analytics** : `ProjetService.statistiques_projets(user_id)`
- **Recherche** : `ProjetService.rechercher_projets(user_id, "CNN")`
- **Datasets** : `DatasetService.statistiques_datasets(projet_id)`

## Schéma de base de données

### Tables principales

```sql
-- Projets IA avec hyperparamètres JSONB
CREATE TABLE projets_ia (
    id UUID PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    type_modele VARCHAR(100), -- 'NLP', 'Computer Vision', etc.
    hyperparametres JSONB,    -- Configuration flexible
    created_by UUID REFERENCES auth.users(id)
);

-- Datasets liés aux projets
CREATE TABLE datasets (
    id UUID PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    taille_mb DECIMAL(10,2),
    format_fichier VARCHAR(50),
    nb_lignes INTEGER,
    projet_id UUID REFERENCES projets_ia(id)
);
```

## Sécurité

- **Row Level Security (RLS)** : Chaque utilisateur ne voit que ses propres données
- **JWT Authentication** : Tokens sécurisés avec Supabase Auth
- **Variables d'environnement** : Clés API protégées
- **Validation des entrées** : Sanitization côté Python

## 📊 Démo et présentation

Le projet inclut une démo interactive :

```bash
python main.py
```

**Résultat attendu :**
```
=== DEMO SUPABASE + PYTHON ===

1️⃣ === AUTHENTIFICATION ===
✅ Utilisateur authentifié: demo@example.com

2️⃣ === CRUD PROJETS ===
✅ Projet créé: Classification d'Images
📋 Nombre de projets: 1
📊 Statistiques: Computer Vision (1)

3️⃣ === GESTION DATASETS ===
✅ Dataset: Images d'entraînement (157.3 MB)
📊 Total: 3 datasets, 194.2 MB

4️⃣ === HYPERPARAMÈTRES ===
🔧 Configuration ResNet50 avec 10 paramètres

🎉 === DEMO TERMINÉE === 🎉
```

## Tests

- **Test de connexion**  
  ```bash
  python test_config.py
  ```

## Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commiter** les changements (`git commit -m 'Add AmazingFeature'`)
4. **Pousser** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

## Issues connues

- RLS peut nécessiter une configuration manuelle pour certains cas d'usage
- Storage limité à 1GB en version gratuite Supabase

## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">

**Fait avec ❤️ pour la communauté dev IA Marseille*

</div>