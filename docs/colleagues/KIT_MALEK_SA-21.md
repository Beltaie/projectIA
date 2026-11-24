# 📦 Kit de Déploiement Git pour Malek (MB)

| Tâche Assignée | Intitulé | Sprint |
|---|---|---|
| **SA-21** | Développer les API de consultation des tarifs et des conditions d'admission | Sprint 1 — Socle Technique |

---

## 👋 Salut Malek !
Pour respecter la traçabilité officielle du projet et faire comptabiliser ta tâche **SA-21** à ton nom sur GitHub, voici la procédure étape par étape avec les commandes Git prêtes à exécuter.

Le code a déjà été développé et testé avec succès. Il te suffit de te positionner sur ta branche et de pusher.

---

## 🚀 Tâche SA-21 : API Tarifs, Conditions d'Admission & Délais

### Ce que fait la tâche :
- Implémentation des endpoints de consultation des frais officiels et conditions d'accès :
  - `GET /api/programs/{id}/fees?year=2026/2027` : Consultation des frais de scolarité annuels/semestriels avec calcul des remises promotionnelles (15% à l'IIT, 10% à l'ISB).
  - `GET /api/programs/{id}/admission-conditions?year=2026/2027` : Conditions d'admission officielles et diplômes requis (Baccalauréat, prépa, etc.).
  - `GET /api/programs/{id}/deadlines?year=2026/2027` : Calendrier officiel (dépôt de dossier, concours, entretiens, inscription).
- Modèles SQLAlchemy dans `backend/models/catalog.py` (`AdmissionCondition`, `TuitionFee`, `Deadline`, `FeePromotion`).
- Schémas Pydantic dans `backend/schemas/catalog.py` (`TuitionFeeOut`, `AdmissionConditionOut`, `DeadlineOut`, `FeePromotionOut`).
- Routes dans `backend/api/routes/catalog.py`.

### Commandes Git à exécuter sur ta machine :

```bash
# 1. Récupérer les dernières modifications de develop
git checkout develop
git pull origin develop

# 2. Créer ta branche de fonctionnalité SA-21
git checkout -b feature/SA-21-fees-admission-api

# 3. Ajouter tes fichiers de code
git add backend/models/catalog.py backend/schemas/catalog.py backend/api/routes/catalog.py

# 4. Commiter avec le numéro officiel de ta tâche
git commit -m "SA-21: developper les API de consultation des tarifs, promotions et conditions d'admission"

# 5. Pusher ta branche sur GitHub
git push -u origin feature/SA-21-fees-admission-api
```

---

## ✅ Vérification locale :
Tu peux tester tes endpoints directement avec la suite Pytest :
```bash
cd backend
python -m pytest tests/test_api_reliability.py -k "test_get_program_fees_and_conditions"
```
*(Résultat attendu : Test validé avec statut 200 et montants exacts en TND)*
