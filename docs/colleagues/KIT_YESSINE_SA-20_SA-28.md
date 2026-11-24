# 📦 Kit de Déploiement Git pour Yessine (YE)

| Tâches Assignées | Intitulé | Sprint |
|---|---|---|
| **SA-20** | Développer les API de gestion des formations et des programmes | Sprint 1 — Socle Technique |
| **SA-28** | Développer l'authentification et la gestion des rôles | Sprint 1 — Socle Technique |

---

## 👋 Salut Yessine !
Pour respecter la traçabilité officielle du projet et faire comptabiliser tes tâches **SA-20** et **SA-28** à ton nom sur GitHub, voici la procédure étape par étape avec les commandes Git prêtes à exécuter.

Le code a déjà été développé et testé avec succès. Il te suffit de te positionner sur tes branches respectives et de pusher.

---

## 🚀 Étape 1 : Tâche SA-20 (API Programmes & Formations)

### Ce que fait la tâche :
- Implémentation des routes de consultation et de gestion des programmes académiques IIT & ISB :
  - `GET /api/institutions` : Liste des institutions.
  - `GET /api/programs` : Liste avec filtres par filière (`LICENCE`, `PREPA`, `INGENIEUR`) et par langue (`FR`, `EN`).
  - `GET /api/programs/{id}` : Détails complets du programme.
  - `POST /api/programs` : Ajout sécurisé réservé aux responsables d'établissement.
- Modèles SQLAlchemy dans `backend/models/catalog.py` (`Institution`, `Program`, `ProgramPathway`).
- Schémas Pydantic dans `backend/schemas/catalog.py`.

### Commandes Git à exécuter sur ta machine :

```bash
# 1. Récupérer les dernières mises à jour
git checkout develop
git pull origin develop

# 2. Créer ta branche de fonctionnalité SA-20
git checkout -b feature/SA-20-programs-api

# 3. Ajouter tes fichiers de code
git add backend/models/catalog.py backend/schemas/catalog.py backend/api/routes/catalog.py

# 4. Commiter avec le numéro officiel de ta tâche
git commit -m "SA-20: developper les API de gestion des formations et des programmes IIT et ISB"

# 5. Pusher ta branche sur GitHub
git push -u origin feature/SA-20-programs-api
```

---

## 🚀 Étape 2 : Tâche SA-28 (Authentification & Rôles RBAC)

### Ce que fait la tâche :
- Endpoints d'authentification complète :
  - `POST /api/auth/register` : Inscription d'un nouveau candidat avec création de son profil initial.
  - `POST /api/auth/login` : Connexion sécurisée et génération de token JWT Bearer.
  - `GET /api/auth/me` : Récupération du profil de l'utilisateur connecté.
- Hachage de mot de passe sécurisé (PBKDF2-SHA256) et validation des rôles (`CANDIDAT`, `RESPONSABLE`, `ADMINISTRATEUR`).
- Fichiers associés : `backend/services/auth_service.py`, `backend/schemas/auth.py`, `backend/api/routes/auth.py`.

### Commandes Git à exécuter sur ta machine :

```bash
# 1. Se baser sur develop à jour
git checkout develop

# 2. Créer ta branche de fonctionnalité SA-28
git checkout -b feature/SA-28-auth-roles

# 3. Ajouter tes fichiers de code
git add backend/services/auth_service.py backend/schemas/auth.py backend/api/routes/auth.py

# 4. Commiter avec le numéro officiel de ta tâche
git commit -m "SA-28: developper l'authentification securisee JWT et la gestion des roles RBAC"

# 5. Pusher ta branche sur GitHub
git push -u origin feature/SA-28-auth-roles
```

---

## ✅ Vérification locale :
Tu peux vérifier que tout fonctionne chez toi en lançant les tests unitaires :
```bash
cd backend
python -m pytest tests/test_api_reliability.py
```
*(Résultat attendu : 6/6 tests passés en < 2 secondes)*
