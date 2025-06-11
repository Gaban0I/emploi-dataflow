
#  Projet Bloc 2 – Infrastructure Data sur le Cloud

##  Objectif
Ce projet vise à mettre en place un pipeline data complet sur le Cloud, depuis la collecte des offres d'emploi via l'API France Travail jusqu'au stockage des données dans AWS S3 et PostgreSQL RDS, avec orchestration Python.

---

##  Structure du projet

```
.
├── main.py               # Point d'entrée du pipeline
├── requirements.txt      # Dépendances Python
├── .env                  # Variables d'environnement (non commit)
│
├── data/                 # Données brutes JSON
├── figures/              # Graphiques générés automatiquement
│
└── src/
    ├── config.py         # Chargement des variables depuis .env
    ├── token.py          # Récupération du token d'accès API
    ├── scraper.py        # Requête à l'API et sauvegarde JSON
    ├── s3.py             # Upload de fichiers vers AWS S3
    ├── db.py             # Connexion, création de table, insertion PostgreSQL
    └── analyse.py        # Génération de graphiques et analyses statistiques
```

---

##  Pipeline automatisé

```bash
python main.py
```

### Étapes exécutées automatiquement :

-  Authentification France Travail (OAuth2)
-  Récupération des offres d'emploi
-  Sauvegarde en `.json` dans `data/`
-  Upload dans AWS S3 (bucket : `077805585531-data-lake`)
-  Création de la table `job_offers` dans PostgreSQL (AWS RDS)
-  Insertion des données dans la base
-  Génération automatique de graphiques dans `figures/`

---

##  Analyses statistiques générées

- Répartition des types de contrat
- Évolution des offres par date de publication
- Top 10 des localisations d'offres

---

##  Sécurité et Cloud

-  Chiffrement au repos activé sur la base PostgreSQL RDS (via AWS KMS)
-  Système de logs/monitoring activé via AWS CloudWatch (logs S3/RDS visibles dans la console)
-  Variables sensibles stockées dans `.env` non versionné
-  Bucket S3 restreint à l'utilisateur via clés IAM

---

##  Dépendances

```bash
pip install -r requirements.txt
```

Contenu du fichier `requirements.txt` :

```
requests
boto3
psycopg2-binary
python-dotenv
pandas
matplotlib
seaborn
sqlalchemy
```
---

##  Configuration `.env`

Fichier `.env.example` fourni pour aide à la configuration.

```env
CLIENT_ID=...
CLIENT_SECRET=...
TOKEN_URL=...
SEARCH_URL=...

DB_HOST=...
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_PORT=5432

AWS_ACCESS_KEY=...
AWS_SECRET_KEY=...
REGION=eu-north-1
BUCKET_NAME=...
```