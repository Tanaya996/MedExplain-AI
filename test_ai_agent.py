"""
MedExplain AI — Comprehensive Test Suite
========================================
Verifies Knowledge Base integrity, Forward Chaining Inference Engine correctness,
Reasoning Trace explainability, Edge Cases, and Existing NLP Pipeline Compatibility.

Checks the 12 Verification Criteria Specified in Section 7 of the Instructions.
"""

import unittest
import pandas as pd
from typing import List

from cbc_knowledge_base import Fact, Rule, RuleCondition, get_knowledge_base
from cbc_inference_engine import ForwardChainingEngine, InferenceResult
from cbc_ai_integration import (
    execute_integrated_cbc_pipeline,
    validate_extracted_cbc_parameters,
    convert_parameters_to_facts
)
import backend


class TestCBCKnowledgeBase(unittest.TestCase):
    """Test Suite 1: Knowledge Base Integrity and Rule Structure."""

    def test_knowledge_base_loading(self):
        """Verifies knowledge base loads valid rules with complete metadata."""
        rules = get_knowledge_base()
        self.assertGreater(len(rules), 10, "Knowledge base should contain at least 10 rules.")
        for r in rules:
            self.assertTrue(r.rule_id.startswith("RULE-"), f"Invalid Rule ID format: {r.rule_id}")
            self.assertGreater(len(r.conditions), 0, f"Rule {r.rule_id} has no antecedent conditions.")
            self.assertTrue(r.educational_explanation, f"Rule {r.rule_id} missing educational explanation.")
            self.assertTrue(r.reference_source, f"Rule {r.rule_id} missing reference source.")
            self.assertTrue(r.limitations, f"Rule {r.rule_id} missing explicit limitation statement.")


class TestForwardChainingEngine(unittest.TestCase):
    """Test Suite 2: Forward Chaining Inference Algorithm."""

    def setUp(self):
        self.engine = ForwardChainingEngine()

    def test_single_parameter_rule_firing(self):
        """Verifies single-parameter fact fires appropriate rule."""
        facts = [
            Fact(fact_id="F1", category="parameter", subject="HGB", predicate="status_is", value="Low")
        ]
        result: InferenceResult = self.engine.run_inference(facts)
        fired_ids = [r.rule_id for r in result.fired_rules]
        self.assertIn("RULE-PRIM-HGB-LOW", fired_ids)
        self.assertEqual(len(result.reasoning_trace), 1)
        self.assertEqual(result.reasoning_trace[0].rule_id, "RULE-PRIM-HGB-LOW")

    def test_multi_parameter_microcytic_hypochromic_pattern(self):
        """Verifies multi-parameter synthesis fires higher-salience syndrome rule."""
        facts = [
            Fact(fact_id="F1", category="parameter", subject="HGB", predicate="status_is", value="Low"),
            Fact(fact_id="F2", category="parameter", subject="MCV", predicate="status_is", value="Low"),
            Fact(fact_id="F3", category="parameter", subject="MCH", predicate="status_is", value="Low")
        ]
        result: InferenceResult = self.engine.run_inference(facts)
        fired_ids = [r.rule_id for r in result.fired_rules]

        # Multi-parameter rule must fire due to high salience (salience=30)
        self.assertIn("RULE-MULTI-MICRO-HYPO", fired_ids)
        self.assertEqual(result.reasoning_trace[0].rule_id, "RULE-MULTI-MICRO-HYPO")

    def test_cycle_prevention_and_termination(self):
        """Verifies that engine stops at quiescence and never enters an infinite loop."""
        facts = [
            Fact(fact_id="F1", category="parameter", subject="HGB", predicate="status_is", value="Low"),
            Fact(fact_id="F2", category="parameter", subject="HCT", predicate="status_is", value="Low")
        ]
        result: InferenceResult = self.engine.run_inference(facts)
        self.assertTrue(result.quiescence_reached)
        self.assertLessEqual(result.iterations_count, len(self.engine.rules))
        # Ensure no rule fired more than once
        fired_ids = [r.rule_id for r in result.fired_rules]
        self.assertEqual(len(fired_ids), len(set(fired_ids)), "Duplicate rule firing detected!")

    def test_reasoning_trace_integrity(self):
        """Verifies reasoning trace contains matched premises and sources."""
        facts = [
            Fact(fact_id="F1", category="parameter", subject="NE%", predicate="status_is", value="High"),
            Fact(fact_id="F2", category="parameter", subject="LY%", predicate="status_is", value="Low")
        ]
        result: InferenceResult = self.engine.run_inference(facts)
        self.assertGreater(len(result.reasoning_trace), 0)
        step = result.reasoning_trace[0]
        self.assertTrue(len(step.matched_facts) >= 2)
        self.assertTrue(step.reference_source)
        self.assertTrue(step.limitations)


class TestInputValidationAndEdgeCases(unittest.TestCase):
    """Test Suite 3: Input Validation, Missing Values, and Anomalies."""

    def test_missing_reference_range_flagged(self):
        """Verifies missing reference interval produces limitation, not unsupported diagnosis."""
        raw_data = {
            "HGB": {"value": 11.5, "unit": "g/dL", "reference_low": None, "reference_high": None, "status": "Low"}
        }
        valid_params, warnings, errors = validate_extracted_cbc_parameters(raw_data)
        self.assertEqual(valid_params["HGB"]["status"], "Unassessed")
        self.assertIn("Missing Reference Interval", valid_params["HGB"]["limitation_flag"])
        self.assertGreater(len(warnings), 0)

    def test_physiologically_impossible_value_rejected(self):
        """Verifies out-of-bounds artifact (e.g. HGB 99 g/dL) is flagged as an error."""
        raw_data = {
            "HGB": {"value": 99.0, "unit": "g/dL", "reference_low": 12.0, "reference_high": 16.0, "status": "High"}
        }
        valid_params, warnings, errors = validate_extracted_cbc_parameters(raw_data)
        self.assertNotIn("HGB", valid_params)
        self.assertGreater(len(errors), 0)

    def test_empty_input_handled_gracefully(self):
        """Verifies empty or whitespace text does not crash the pipeline."""
        res = execute_integrated_cbc_pipeline("", "EMPTY-001")
        self.assertFalse(res["success"])
        self.assertEqual(len(res["structured_df"]), 0)


class TestNLPCompatibilityAndIntegration(unittest.TestCase):
    """Test Suite 4: Preservation of Original NLP Pipeline."""

    def test_original_backend_extraction_works(self):
        """Verifies original backend.extract_cbc_report still parses clinical reports."""
        sample_text = (
            "Hemoglobin (HGB) 11.2 g/dL 12.0 - 15.5\n"
            "Hematocrit (HCT) 34.0 % 37.0 - 48.0\n"
            "Platelets 140 x10^3/uL 150 - 450\n"
            "Mean Corpuscular Volume (MCV) 72.0 fL 80.0 - 100.0\n"
            "Mean Corpuscular Hemoglobin (MCH) 24.0 pg 27.0 - 33.0"
        )
        extracted = backend.extract_cbc_report(sample_text)
        self.assertIn("HGB", extracted)
        self.assertEqual(extracted["HGB"]["status"], "Low")
        self.assertIn("MCV", extracted)
        self.assertEqual(extracted["MCV"]["status"], "Low")

    def test_original_process_cbc_report_works(self):
        """Verifies backend.process_cbc_report returns valid dataframe and final report."""
        sample_text = "Hemoglobin 14.5 g/dL 13.0 - 17.5\nPlatelets 250 x10^3/uL 150 - 450"
        df, rep = backend.process_cbc_report(sample_text, "TEST-ORIG-001")
        self.assertFalse(df.empty)
        self.assertIn("CBC Summary", rep)
        self.assertIn("Overall CBC Summary", rep)

    def test_end_to_end_integrated_pipeline(self):
        """Verifies combined NLP + Validation + Forward Chaining pipeline end-to-end."""
        sample_text = (
            "Hemoglobin (HGB) 10.5 g/dL 12.0 - 16.0\n"
            "Mean Corpuscular Volume (MCV) 74.0 fL 80.0 - 99.0\n"
            "Mean Corpuscular Hemoglobin (MCH) 23.5 pg 27.0 - 33.0\n"
            "Platelets (PLT) 210 x10^3/uL 150 - 450"
        )
        res = execute_integrated_cbc_pipeline(sample_text, "TEST-INTEG-001")
        self.assertTrue(res["success"])
        self.assertGreater(len(res["derived_findings"]), 0)
        self.assertGreater(len(res["reasoning_trace"]), 0)
        self.assertLess(res["execution_time_ms"], 100.0, "Inference must complete rapidly (<100ms).")


if __name__ == "__main__":
    unittest.main()
