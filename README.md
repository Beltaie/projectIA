# SmartCampus AI — Démarrage local

Ce guide configure l'environnement de développement de SmartCampus AI : frontend React/Vite, API FastAPI et base PostgreSQL avec `pgvector`.

## Prérequis

- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) avec Docker Compose
- [Node.js](https://nodejs.org/) 20 ou plus récent (npm est inclus)
- Python 3.11 ou plus récent

## Récupérer le projet

Remplacez `VOTRE-ORGANISATION` par l'organisation GitHub de l'équipe :

```powershell
git clone https://github.com/VOTRE-ORGANISATION/SmartCampusAI.git
cd SmartCampusAI
```

## Configurer l'environnement

Depuis la racine du dépôt, créez le fichier local `.env` à partir du modèle :

```powershell
Copy-Item .env.example .env
```

Les valeurs de `.env.example` sont destinées au développement local uniquement. Modifiez-les si les ports sont déjà utilisés. Les variables de configuration LLM et Whisper sont préparées pour l'intégration; le backend actuel ne les consomme pas encore.

Le backend charge son fichier `.env` depuis le dossier `backend`. Copiez-y la configuration racine :

```powershell
Copy-Item .env backend\.env
```

Les deux fichiers `.env` sont ignorés par Git. Ne partagez pas de secrets réels dans le dépôt.

## Démarrer PostgreSQL et pgAdmin

Vérifiez que Docker Desktop est démarré, puis lancez depuis la racine :

```powershell
docker-compose up -d
```

PostgreSQL avec `pgvector` est disponible sur `localhost:5432`. Le script `init-db.sql` crée l'extension et les tables de démonstration et insère deux comptes, trois formations IIT et deux formations ISB à la première initialisation du volume.

- Interface pgAdmin : <http://localhost:5050>
- Identifiants pgAdmin : ceux de `PGADMIN_DEFAULT_EMAIL` et `PGADMIN_DEFAULT_PASSWORD` dans `.env`
- Pour enregistrer le serveur dans pgAdmin : hôte `db`, port `5432`, base, utilisateur et mot de passe selon `POSTGRES_DB`, `POSTGRES_USER` et `POSTGRES_PASSWORD` dans `.env`.

Le script d'initialisation n'est exécuté que lorsque PostgreSQL initialise un volume vide. Pour conserver les données existantes, ne supprimez pas le volume. Les comptes SQL de démonstration n'ont pas de mot de passe d'authentification applicatif (`password_hash` est nul); l'authentification n'est pas implémentée à ce stade.

## Installer les dépendances

### Backend

Dans un nouveau terminal PowerShell, depuis la racine du dépôt :

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si l'activation des scripts est bloquée par la stratégie PowerShell, vous pouvez appeler directement `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` et `.\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`.

### Frontend

Dans un autre terminal PowerShell, depuis la racine du dépôt :

```powershell
cd frontend
npm install
```

## Lancer les serveurs de développement

Lancez l'API depuis `backend` :

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API : <http://localhost:8000>
- Documentation interactive : <http://localhost:8000/docs>
- Vérification de santé : <http://localhost:8000/health>

Dans un autre terminal, lancez le frontend :

```powershell
cd frontend
npm run dev
```

Vite affiche l'adresse locale, normalement <http://localhost:5173>. La configuration API frontend par défaut est `http://localhost:8000`.
