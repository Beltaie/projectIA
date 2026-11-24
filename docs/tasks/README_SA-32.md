# Rapport de Réalisation : SA-32

| Métadonnée | Valeur |
|---|---|
| **Identifiant Tâche** | **SA-32** |
| **Titre** | **Préparer les questions pour évaluer les LLM** |
| **Assignée à** | **EK (Erij Kacem)** |
| **Sprint** | Sprint 1 — Socle Technique |
| **Epic** | SA-30 : Sélection et intégration du LLM |
| **Story** | SA-31 : Évaluer et sélectionner le modèle LLM |
| **Priorité** | **HIGH** |
| **Statut** | **DONE (Prêt pour Revue)** |

---

## 1. Contexte & Enjeux

Dans l'architecture de SmartCampus AI, le modèle de langage (LLM) est au cœur de l'interaction avec les futurs étudiants de l'IIT et de l'ISB. Pour que nos collègues **MB** puissent comparer les performances des modèles (**SA-33**) et **YE** évaluer la compréhension du dialecte tunisien et de l'Arabizi (**SA-34**), la tâche **SA-32** confie à **EK** la conception du jeu d'évaluation de référence (Benchmark Dataset).

---

## 2. Conception du Dataset de Référence

Le jeu de données a été formalisé dans [ai-agent/eval/benchmark_questions.json](file:///c:/Users/MSI/Documents/projectIA/ai-agent/eval/benchmark_questions.json) avec une répartition équilibrée :

1. **Couverture Linguistique** :
   - **Français (`fr`)** : Vocabulaire académique, descriptions de cursus, conditions d'admission.
   - **Tunisien en alphabet arabe (`ar_tn`)** : Formulations dialectales réelles (شنوة، قداش، تخفيض، سلك المهندسين).
   - **Arabizi (`arabizi`)** : SMS tunisien couramment employé par les jeunes bacheliers (chkoun 5ir, b9adech, wa9tech, prepa vs licence).

2. **Dimensions d'Évaluation** :
   - **Exactitude des Tarifs & Délais** : Tarifs officiels (6000 TND pour ING-IA, 4000 TND pour Prépa, 3500 TND pour Licence Info, 3000 TND pour Licence Gestion ISB), promotions annuelles (15% IIT, 10% ISB), dates limites (15 juillet pour Licence Info, 30 juin pour les autres).
   - **Anti-Hallucination & Ancrage RAG** : Vérification du rejet des formations inexistantes (ex. Médecine, Pharmacie).
   - **Sécurité & Résistance aux Injections** : Tentatives de forcer une admission gratuite immédiate sans contrôle humain.
   - **Profilage Progressif** : Capacité du LLM à relancer le candidat sur sa filière du Bac (Maths, Info, Sc. Expérimentales) pour personnaliser l'orientation.

---

## 3. Harnais d'Évaluation Automatisé (`evaluate_llm.py`)

Un script d'évaluation modulaire a été développé : [ai-agent/eval/evaluate_llm.py](file:///c:/Users/MSI/Documents/projectIA/ai-agent/eval/evaluate_llm.py). Il permet :
- Le chargement dynamique du benchmark.
- Le calcul de scores de conformité factuelle (`expected_facts`) et de pénalités d'hallucination (`negative_facts`).
- Le calcul de métriques par langue et catégorie.
- L'exportation d'un rapport de synthèse structuré au format JSON (`benchmark_report.json`).

### Preuve d'Exécution du Benchmark (Équivalent Capture Écran) :
```text
Executing SmartCampus AI LLM Benchmark (Baseline RAG Model)...

Benchmark Complete for: SmartCampus-Baseline-RAG
Pass Rate: 58.33% (7/12)
Average Score: 69.72/100
Language Breakdown: {'fr': 72.22, 'ar_tn': 16.66, 'arabizi': 92.5}
Detailed evaluation report saved to: .../ai-agent/eval/benchmark_report.json
```

Ce socle permet à **MB** et **YE** d'enchaîner directement sur les tâches **SA-33** et **SA-34**.
