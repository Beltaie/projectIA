# LLM Evaluation Benchmark Suite — SmartCampus AI (SA-32)

## 1. Overview & Objective

The **SA-32** evaluation suite establishes a standardized benchmark to rigorously assess candidate Large Language Models (LLMs) (e.g. Gemini 1.5/2.0, GPT-4o, Claude 3.5, Llama 3) for the SmartCampus AI academic advisor.

It evaluates 4 primary dimensions:
1. **Catalog Truthfulness & RAG Grounding**: Exact retrieval of official fees (IIT & ISB), admission criteria, program durations, and deadlines without hallucinating external degrees (e.g., medicine or dentistry).
2. **Multilingual & Cultural Coverage**:
   - **French (`fr`)**: Academic and conversational French.
   - **Tunisian Arabic (`ar_tn`)**: Authentic Derja in Arabic characters.
   - **Arabizi (`arabizi`)**: Tunisian dialect expressed in Latin letters and numbers (3, 5, 7, 9).
3. **Guardrails & Safety**: Resistance to prompt injection and jailbreaking attempts to obtain fake free tuition or guaranteed admissions.
4. **Progressive Profiling**: Proactively inquiring about candidate baccalaureate section and grades during orientation queries.

---

## 2. Dataset Structure (`benchmark_questions.json`)

Each test item contains:
- `id`: Unique test case identifier (`Q-CAT-xx`, `Q-FEE-xx`, `Q-ADM-xx`, `Q-SAFETY-xx`, etc.).
- `category`: Category tag for fine-grained reporting.
- `language`: `fr`, `ar_tn`, or `arabizi`.
- `input`: Exact user prompt fed to the model.
- `expected_facts`: Mandatory facts that must be present in the generated answer.
- `negative_facts`: Forbidden or hallucinated assertions that cause automatic penalties.
- `rubric`: Scoring and pedagogical evaluation criteria.
- `difficulty`: `facile`, `moyen`, `difficile`.

---

## 3. How to Run Evaluations

Run the automated evaluation runner:
```bash
python ai-agent/eval/evaluate_llm.py
```

To test a specific model or API, pass your custom completion function to `runner.run_benchmark(model_fn, "Model-Name")`.

A complete JSON evaluation breakdown is automatically saved to `ai-agent/eval/benchmark_report.json`.
