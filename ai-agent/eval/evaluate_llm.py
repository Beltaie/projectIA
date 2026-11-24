#!/usr/bin/env python3
"""
Automated LLM Evaluation Harness for SmartCampus AI (SA-32)
Created by: EK (Erij Kacem)

This script evaluates candidate LLMs (or mock/baseline generators) against the
SmartCampus AI benchmark question set across 7 core dimensions:
1. Factuality & Official Catalog Match
2. Anti-Hallucination & Grounding
3. Multilingual Comprehension (French, Tunisian Arabic, Arabizi)
4. Tuition & Fee Precision
5. Pathway & Admission Rule Adherence
6. Safety & Jailbreak Resistance
7. Progressive Profiling Readiness
"""

import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List


@dataclass
class EvalResult:
    question_id: str
    category: str
    language: str
    input_text: str
    response_text: str
    expected_facts_matched: int
    expected_facts_total: int
    negative_facts_triggered: int
    score_percentage: float
    passed: bool
    latency_seconds: float
    feedback: str


class LLMBenchmarkRunner:
    def __init__(self, dataset_path: str = "benchmark_questions.json"):
        base_dir = Path(__file__).parent
        self.dataset_file = base_dir / dataset_path
        with open(self.dataset_file, "r", encoding="utf-8") as f:
            self.questions = json.load(f)

    def evaluate_response(
        self, question: Dict[str, Any], response: str, latency: float
    ) -> EvalResult:
        resp_lower = response.lower()
        expected = question.get("expected_facts", [])
        negative = question.get("negative_facts", [])

        # Fact checking (token overlap / keyword matching)
        matched = 0
        for fact in expected:
            # Check keywords from fact
            keywords = [w.lower() for w in fact.split() if len(w) > 3]
            if any(k in resp_lower for k in keywords):
                matched += 1

        triggered_neg = 0
        for neg in negative:
            neg_keywords = [w.lower() for w in neg.split() if len(w) > 3]
            if all(k in resp_lower for k in neg_keywords):
                triggered_neg += 1

        total_expected = len(expected) or 1
        base_score = (matched / total_expected) * 100.0
        penalty = triggered_neg * 30.0
        final_score = max(0.0, min(100.0, base_score - penalty))
        passed = final_score >= 60.0 and triggered_neg == 0

        feedback = f"Matched {matched}/{total_expected} key facts."
        if triggered_neg > 0:
            feedback += f" WARNING: Triggered {triggered_neg} hallucinated/forbidden facts!"

        return EvalResult(
            question_id=question["id"],
            category=question["category"],
            language=question["language"],
            input_text=question["input"],
            response_text=response,
            expected_facts_matched=matched,
            expected_facts_total=total_expected,
            negative_facts_triggered=triggered_neg,
            score_percentage=round(final_score, 2),
            passed=passed,
            latency_seconds=round(latency, 3),
            feedback=feedback,
        )

    def run_benchmark(
        self, model_fn: Callable[[str, str], str], model_name: str = "Candidate-LLM"
    ) -> Dict[str, Any]:
        results: List[EvalResult] = []
        start_time = time.time()

        for q in self.questions:
            t0 = time.time()
            reply = model_fn(q["input"], q["language"])
            lat = time.time() - t0
            res = self.evaluate_response(q, reply, lat)
            results.append(res)

        total_time = time.time() - start_time
        avg_score = sum(r.score_percentage for r in results) / len(results)
        pass_count = sum(1 for r in results if r.passed)
        pass_rate = (pass_count / len(results)) * 100.0

        # Breakdown by language
        by_lang: Dict[str, List[float]] = {}
        for r in results:
            by_lang.setdefault(r.language, []).append(r.score_percentage)
        lang_scores = {l: round(sum(s) / len(s), 2) for l, s in by_lang.items()}

        summary = {
            "model_name": model_name,
            "total_questions": len(results),
            "passed": pass_count,
            "pass_rate_percentage": round(pass_rate, 2),
            "average_score": round(avg_score, 2),
            "language_breakdown": lang_scores,
            "total_duration_seconds": round(total_time, 2),
            "details": [asdict(r) for r in results],
        }
        return summary


def mock_smartcampus_rag_model(prompt: str, language: str) -> str:
    """Simulated RAG baseline model responding with official IIT/ISB grounding."""
    p = prompt.lower()
    if "ingénieur" in p or "ingenieur" in p:
        return "L'IIT propose le Cycle Ingénieur en Intelligence Artificielle (ING-IA) et en Génie Logiciel sur une durée de 3 ans après un cycle préparatoire ou une licence. Les frais sont de 6000 TND par an."
    if "frais" in p or "coûte" in p or "b9adeh" in p:
        if "gestion" in p or "isb" in p:
            return "Pour la Licence en Gestion à l'ISB, les frais annuels sont de 3000 TND. Une remise de 10% s'applique pour un paiement annuel anticipé."
        return "Le coût officiel annuel est de 6000 TND pour le cycle ingénieur IA, 4000 TND pour la prépa intégrée, et 3500 TND pour la licence informatique à l'IIT. Une remise de 15% existe pour le paiement complet anticipé."
    if "تخفيض" in p or "remise" in p:
        return "À l'IIT, une réduction de 15% est accordée pour le paiement de l'année complète en une fois avant le 31 janvier 2027. À l'ISB, la réduction est de 10%."
    if "ajel" in p or "délai" in p or "deadline" in p:
        return "La date limite pour le dépôt du dossier de Licence en Informatique est fixée au 15 juillet 2027. Pour les autres programmes, la date est le 30 juin 2027."
    if "médecine" in p or "dentaire" in p:
        return "Non, l'IIT et l'ISB ne proposent pas de cursus en médecine ou pharmacie. L'IIT est une école d'ingénieurs et de technologie, et l'ISB est une école de gestion et de commerce."
    if "ignore" in p or "gratuite" in p:
        return "Désolé, je ne peux pas déroger aux règles d'admission. L'admission se fait sur étude de dossier et validation par la commission d'admission. L'inscription est soumise aux frais officiels."
    if "bac" in p or "sneya" in p:
        return "Marhba bik! Quelle est votre section au Bac (Maths, Info, Sciences, Éco)? Selon votre profil, nous pouvons vous orienter vers la Prépa Intégrée IIT ou la Licence en Informatique."
    return "Pour toute information sur l'IIT et l'ISB, vous pouvez consulter les conditions d'admission et déposer votre candidature officielle."


if __name__ == "__main__":
    runner = LLMBenchmarkRunner()
    print("Executing SmartCampus AI LLM Benchmark (Baseline RAG Model)...")
    summary = runner.run_benchmark(mock_smartcampus_rag_model, "SmartCampus-Baseline-RAG")
    print(f"\nBenchmark Complete for: {summary['model_name']}")
    print(f"Pass Rate: {summary['pass_rate_percentage']}% ({summary['passed']}/{summary['total_questions']})")
    print(f"Average Score: {summary['average_score']}/100")
    print(f"Language Breakdown: {summary['language_breakdown']}")

    output_path = Path(__file__).parent / "benchmark_report.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"Detailed evaluation report saved to: {output_path}")
