# Rapport de Réalisation : SA-17

| Métadonnée | Valeur |
|---|---|
| **Identifiant Tâche** | **SA-17** |
| **Titre** | **Créer les tables et les relations de la base de données** |
| **Assignée à** | **EK (Erij Kacem)** |
| **Sprint** | Sprint 1 — Socle Technique |
| **Epic** | SA-10 : Données relationnelles et référentiels |
| **Story** | SA-15 : Base PostgreSQL et migrations |
| **Priorité** | **HIGH** |
| **Statut** | **DONE (Prêt pour Revue)** |

---

## 1. Contexte & Objectifs

La tâche **SA-17** concrétise au niveau physique la conception réalisée en **SA-13**. Elle a pour objectifs :
1. **Écriture du script de migration Flyway / PostgreSQL** : Implémenter le fichier `V2__users_and_applications.sql` intégrant toutes les tables du domaine Utilisateurs, Candidats, Candidatures, Évaluations, Entretiens, et la liaison avec les sessions de chat.
2. **Implémentation des modèles ORM SQLAlchemy 2.0** : Modéliser en Python (`models/user.py`, `models/application.py`, `models/chat.py`) les entités correspondantes avec typage statique moderne (`Mapped`, `mapped_column`, relations bidirectionnelles, cascades et contraintes Check).
3. **Alimentation en données de test réalistes** : Développer le script de seed `V101__users_and_applications_demo.sql` pour valider l'intégration locale (comptes Admin, Responsable IIT, Responsable ISB, Candidat Mohamed Ben Salem, Candidate Erij Kacem, profils, dossiers et entretiens).
4. **Validation par tests automatisés** : Écrire et exécuter la suite de tests unitaires (`tests/test_users_and_applications.py`).

---

## 2. Réalisations Techniques

### A. Migration PostgreSQL Flyway (`V2__users_and_applications.sql`)
- Extension cryptographique `pgcrypto` activée.
- Table `users` avec contrainte d'isolation institutionnelle :
  ```sql
  CONSTRAINT chk_responsable_institution
    CHECK (
      (role = 'RESPONSABLE' AND institution_id IS NOT NULL) OR
      (role <> 'RESPONSABLE')
    )
  ```
- Table `candidate_profiles` avec vérifications strictes (`bac_year BETWEEN 1990 AND 2035`, `bac_average BETWEEN 0 AND 20`, `confidence_score BETWEEN 0 AND 100`).
- Table `applications` avec unicité `(candidate_id, program_id, academic_year)` et domaine d'année académique réutilisé depuis `V1__catalog.sql`.
- Extension non destructive de la table `chat_sessions` avec `user_id UUID REFERENCES users(id)` et `claimed_at TIMESTAMPTZ` pour préparer la tâche **SA-29**.
- Triggers d'horodatage automatique `set_updated_at()` sur toutes les tables modifiables.
- Index B-Tree sur les colonnes de filtrage et clés étrangères (`email`, `(role, institution_id)`, `user_id`, `(program_id, status)`, `academic_year`).

### B. Modèles SQLAlchemy 2.0 (`backend/models/`)
- [backend/models/user.py](file:///c:/Users/MSI/Documents/projectIA/backend/models/user.py) : Classes `User` et `CandidateProfile` avec relation 1-1.
- [backend/models/application.py](file:///c:/Users/MSI/Documents/projectIA/backend/models/application.py) : Classes `Application`, `ApplicationReview`, `InterviewSlot` avec relations et contraintes d'intégrité.
- [backend/models/chat.py](file:///c:/Users/MSI/Documents/projectIA/backend/models/chat.py) : Extension de `ChatSession` pour la traçabilité de réclamation par un candidat.

### C. Données de Démonstration (`backend/bd/seed/V101__users_and_applications_demo.sql`)
- 5 utilisateurs complets avec UUIDs prédictibles et rôles diversifiés.
- Profils candidats avec détails du Baccalauréat tunisien (Mathématiques 16.20/20, Sciences Informatiques 15.75/20).
- Dossiers de candidature pour l'IIT (`ING-IA-FR` et `PREPA-INT-FR`) avec scores QCM réels et avis de commission.
- Créneau d'entretien Google Meet planifié pour le candidat.

---

## 3. Preuves de Validation & Tests (Équivalent Captures d'Écran)

### Résultat de l'exécution des tests unitaires Pytest :
```text
============================= test session starts =============================
platform win32 -- Python 3.10.10, pytest-8.3.0, pluggy-1.6.0
rootdir: C:\Users\MSI\Documents\projectIA\backend
configfile: pyproject.toml
testpaths: tests
plugins: anyio-4.13.0, html-3.2.0, metadata-3.1.1
collected 7 items

tests\test_app.py .                                                      [ 14%]
tests\test_errors.py .                                                   [ 28%]
tests\test_users_and_applications.py .....                               [100%]

============================== 7 passed in 1.50s ==============================
```

Tous les tests de validation des modèles, contraintes d'intégrité, relations et liaison chat_session passent avec succès à 100%.
