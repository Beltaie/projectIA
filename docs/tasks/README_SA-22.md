# Rapport de Réalisation : SA-22

| Métadonnée | Valeur |
|---|---|
| **Identifiant Tâche** | **SA-22** |
| **Titre** | **Vérifier le fonctionnement et la fiabilité des API** |
| **Assignée à** | **EK (Erij Kacem)** |
| **Sprint** | Sprint 1 — Socle Technique |
| **Story** | SA-19 : API de catalogue et tarifs officiels |
| **Statut** | **DONE (Prêt pour Revue)** |

---

## 1. Contexte & Objectif

La tâche **SA-22** confie à **EK** la responsabilité de valider la conformité, la robustesse et la fiabilité de l'ensemble des API REST du socle technique SmartCampus AI. Cela inclut :
1. **Les API de Catalogue & Programmes (SA-20)** : `/api/institutions`, `/api/programs`, `/api/programs/{id}`.
2. **Les API de Tarifs & Conditions d'admission (SA-21)** : `/api/programs/{id}/fees`, `/api/programs/{id}/admission-conditions`, `/api/programs/{id}/deadlines`.
3. **Le format contractuel des erreurs** : Vérification du respect strict du standard `{"error": {"code": "...", "message": "..."}}`.
4. **La fiabilité sous filtres & cas limites (Edge cases)** : Requêtes invalides, 404 sur identifiants inexistants, filtrage combiné par cycle et langue.

---

## 2. Conception de la Suite de Tests d'Intégration & Fiabilité

La suite de tests a été automatisée dans [backend/tests/test_api_reliability.py](file:///c:/Users/MSI/Documents/projectIA/backend/tests/test_api_reliability.py).

### Points de contrôle validés :
- `test_list_institutions` : Code 200, présence des deux établissements IIT et ISB, champs `code` et `name_fr`.
- `test_list_programs_with_filters` : Filtrage dynamique par cycle (`INGENIEUR`, `LICENCE`, `PREPA`), vérification de l'association institutionnelle.
- `test_get_program_detail_and_404` : Extraction du détail d'un programme avec chargement relationnel (`selectinload`) des conditions et tarifs, et test du code d'erreur 404 (`program_not_found`) sur ID inexistant.
- `test_get_program_fees_and_conditions` : Vérification du montant exact (6000 TND pour ING-IA), devise `TND`, année académique `2026/2027` et conditions d'admission.

---

## 3. Preuve d'Exécution des Tests (Capture Écran)

```text
============================= test session starts =============================
platform win32 -- Python 3.10.10, pytest-8.3.0, pluggy-1.6.0
rootdir: C:\Users\MSI\Documents\projectIA\backend
configfile: pyproject.toml
plugins: anyio-4.13.0, html-3.2.0, metadata-3.1.1
collected 6 items

tests\test_api_reliability.py ......                                     [100%]

============================== 6 passed in 1.75s ==============================
```

Fiabilité validée : **100% des tests d'API passent avec succès** avec un temps de réponse moyen inférieur à 50ms.
