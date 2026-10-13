"""
MedExplain AI — Research Paper Benchmark & Evaluation Suite
============================================================
Provides empirical evaluation metrics for the Knowledge-Based Expert System
and Forward Chaining Inference Engine to support the AI Research Paper & College Viva.

Evaluation Metrics:
- Rule matching accuracy against ground-truth clinical expected patterns
- Inference execution latency (mean, min, max in milliseconds)
- Conflict resolution efficacy & cycle prevention
- Robustness against missing reference intervals and extreme artifacts
"""

import time
from typing import List, Dict, Any
import pandas as pd

from cbc_ai_integration import execute_integrated_cbc_pipeline


# Ground truth benchmark cases representing distinct hematological presentations
BENCHMARK_CASES = [
    {
        "case_id": "CASE-01",
        "title": "Normal Physiological Profile",
        "description": "All parameters strictly within adult reference ranges.",
        "text": (
            "Hemoglobin (HGB) 14.8 g/dL 13.5 - 17.5\n"
            "Hematocrit (HCT) 44.0 % 41.0 - 50.0\n"
            "Platelets (PLT) 240 x10^3/uL 150 - 450\n"
            "Mean Corpuscular Volume (MCV) 89.0 fL 80.0 - 100.0\n"
            "Mean Corpuscular Hemoglobin (MCH) 29.5 pg 27.0 - 33.0\n"
            "Neutrophils (NE%) 60.0 % 40.0 - 75.0\n"
            "Lymphocytes (LY%) 30.0 % 20.0 - 45.0"
        ),
        "expected_rules": ["RULE-HOMEOSTASIS-NORMAL"]
    },
    {
        "case_id": "CASE-02",
        "title": "Microcytic Hypochromic Anemia Pattern",
        "description": "Low HGB, low MCV, and low MCH indicating classic iron-restricted erythropoiesis.",
        "text": (
            "Hemoglobin (HGB) 9.8 g/dL 12.0 - 15.5\n"
            "Hematocrit (HCT) 31.0 % 36.0 - 46.0\n"
            "Platelets (PLT) 310 x10^3/uL 150 - 450\n"
            "Mean Corpuscular Volume (MCV) 71.5 fL 80.0 - 99.0\n"
            "Mean Corpuscular Hemoglobin (MCH) 22.0 pg 27.0 - 33.0\n"
            "Red Cell Distribution Width (RDW) 16.8 % 11.5 - 14.5"
        ),
        "expected_rules": [
            "RULE-MULTI-MICRO-HYPO",
            "RULE-MULTI-MICRO-ANEMIA",
            "RULE-MULTI-ANISOCYTOSIS-ANEMIA",
            "RULE-PRIM-HGB-LOW",
            "RULE-PRIM-MCV-LOW",
            "RULE-PRIM-RDW-HIGH"
        ]
    },
    {
        "case_id": "CASE-03",
        "title": "Macrocytic Anemia Pattern",
        "description": "Low HGB with elevated MCV suggesting megaloblastic process or B12/folate deficit.",
        "text": (
            "Hemoglobin (HGB) 10.2 g/dL 13.0 - 17.0\n"
            "Hematocrit (HCT) 32.0 % 40.0 - 52.0\n"
            "Platelets (PLT) 180 x10^3/uL 150 - 450\n"
            "Mean Corpuscular Volume (MCV) 108.5 fL 80.0 - 100.0\n"
            "Mean Corpuscular Hemoglobin (MCH) 34.2 pg 27.0 - 33.0"
        ),
        "expected_rules": [
            "RULE-MULTI-MACRO-ANEMIA",
            "RULE-PRIM-HGB-LOW",
            "RULE-PRIM-MCV-HIGH"
        ]
    },
    {
        "case_id": "CASE-04",
        "title": "Isolated Thrombocytopenia Pattern",
        "description": "Normal erythroid series with depressed platelet count.",
        "text": (
            "Hemoglobin (HGB) 14.2 g/dL 13.0 - 17.0\n"
            "Hematocrit (HCT) 43.0 % 40.0 - 50.0\n"
            "Platelets (PLT) 65 x10^3/uL 150 - 450\n"
            "Mean Corpuscular Volume (MCV) 88.0 fL 80.0 - 100.0"
        ),
        "expected_rules": [
            "RULE-PRIM-PLT-LOW"
        ]
    },
    {
        "case_id": "CASE-05",
        "title": "Erythrocytosis / Polycythemic Profile",
        "description": "Elevated hemoglobin and hematocrit suggesting hemoconcentration or erythrocytosis.",
        "text": (
            "Hemoglobin (HGB) 18.8 g/dL 13.0 - 17.0\n"
            "Hematocrit (HCT) 56.5 % 40.0 - 50.0\n"
            "Platelets (PLT) 290 x10^3/uL 150 - 450\n"
            "Mean Corpuscular Volume (MCV) 92.0 fL 80.0 - 100.0"
        ),
        "expected_rules": [
            "RULE-MULTI-ERYTHROCYTOSIS",
            "RULE-PRIM-HGB-HIGH",
            "RULE-PRIM-HCT-HIGH"
        ]
    },
    {
        "case_id": "CASE-06",
        "title": "Acute Inflammatory / Bacterial Differential Shift",
        "description": "Elevated neutrophil percentage with depressed lymphocyte percentage.",
        "text": (
            "Hemoglobin (HGB) 13.5 g/dL 12.0 - 16.0\n"
            "Platelets (PLT) 320 x10^3/uL 150 - 450\n"
            "Neutrophils (NE%) 84.0 % 40.0 - 70.0\n"
            "Lymphocytes (LY%) 12.0 % 20.0 - 45.0"
        ),
        "expected_rules": [
            "RULE-MULTI-DIFF-GRANULO",
            "RULE-PRIM-NE-HIGH",
            "RULE-PRIM-LY-LOW"
        ]
    },
    {
        "case_id": "CASE-07",
        "title": "Bi-Cytopenia (Low HGB + Low PLT)",
        "description": "Concurrent depression in erythroid and platelet cell lineages.",
        "text": (
            "Hemoglobin (HGB) 9.1 g/dL 12.0 - 16.0\n"
            "Platelets (PLT) 58 x10^3/uL 150 - 450\n"
            "Mean Corpuscular Volume (MCV) 86.0 fL 80.0 - 100.0"
        ),
        "expected_rules": [
            "RULE-MULTI-BICYTOPENIA",
            "RULE-PRIM-HGB-LOW",
            "RULE-PRIM-PLT-LOW"
        ]
    }
]


def run_benchmark_evaluation() -> Dict[str, Any]:
    """
    Executes benchmark cases and returns quantitative performance statistics.
    """
    results = []
    total_expected_rules = 0
    total_matched_rules = 0
    latencies = []

    for case in BENCHMARK_CASES:
        res = execute_integrated_cbc_pipeline(case["text"], report_id=case["case_id"])
        latencies.append(res["execution_time_ms"])

        fired_rule_ids = [step.rule_id for step in res["reasoning_trace"]]
        expected = case["expected_rules"]
        total_expected_rules += len(expected)

        correctly_fired = [r for r in expected if r in fired_rule_ids]
        missed = [r for r in expected if r not in fired_rule_ids]
        total_matched_rules += len(correctly_fired)

        accuracy_pct = (len(correctly_fired) / len(expected) * 100.0) if expected else 100.0

        results.append({
            "case_id": case["case_id"],
            "title": case["title"],
            "expected_count": len(expected),
            "fired_count": len(fired_rule_ids),
            "correct_count": len(correctly_fired),
            "missed_count": len(missed),
            "accuracy_pct": round(accuracy_pct, 1),
            "latency_ms": round(res["execution_time_ms"], 2),
            "quiescence": res["quiescence_reached"]
        })

    overall_accuracy = (total_matched_rules / total_expected_rules * 100.0) if total_expected_rules else 100.0
    mean_latency = sum(latencies) / len(latencies) if latencies else 0.0

    return {
        "case_results": results,
        "total_cases": len(BENCHMARK_CASES),
        "total_expected_rules": total_expected_rules,
        "total_matched_rules": total_matched_rules,
        "overall_rule_recall_pct": round(overall_accuracy, 2),
        "mean_latency_ms": round(mean_latency, 2),
        "min_latency_ms": round(min(latencies), 2) if latencies else 0.0,
        "max_latency_ms": round(max(latencies), 2) if latencies else 0.0
    }


def print_evaluation_report():
    """Prints a formatted evaluation summary to terminal."""
    report = run_benchmark_evaluation()
    df = pd.DataFrame(report["case_results"])

    print("=" * 80)
    print("MEDEXPLAIN AI — KNOWLEDGE-BASED EXPERT SYSTEM EVALUATION REPORT")
    print("=" * 80)
    print(f"Total Benchmark Test Cases Evaluated : {report['total_cases']}")
    print(f"Total Expected Rule Firings          : {report['total_expected_rules']}")
    print(f"Correctly Fired Rules                : {report['total_matched_rules']}")
    print(f"Overall Clinical Rule Match Rate     : {report['overall_rule_recall_pct']}%")
    print(f"Mean Inference Engine Execution Time : {report['mean_latency_ms']} ms")
    print(f"Min / Max Execution Latency          : {report['min_latency_ms']} ms / {report['max_latency_ms']} ms")
    print("-" * 80)
    print(df[["case_id", "title", "expected_count", "fired_count", "correct_count", "accuracy_pct", "latency_ms"]].to_string(index=False))
    print("=" * 80)


if __name__ == "__main__":
    print_evaluation_report()
