"""
MedExplain AI — AI & NLP Integration Adapter
=============================================
Bridges the existing NLP extraction pipeline (backend.py) with the new
Knowledge-Based Forward Chaining Expert System (cbc_knowledge_base.py & cbc_inference_engine.py).

Workflow:
1. Raw CBC Report Text -> NLP Extraction (reusing backend.extract_cbc_report & spaCy).
2. Input Validation -> Data integrity, clinical plausibility boundaries, missing reference ranges.
3. Fact Generation -> Populates atomic propositions into Expert System Working Memory.
4. Forward Chaining Inference -> Evaluates production rules, derives patterns, builds reasoning trace.
5. Explanation Synthesis -> Integrates rule inferences with existing medical dictionary & suggestions.
"""

from typing import Dict, Any, List, Optional, Tuple
import re
import pandas as pd
import spacy

# Import existing working backend functions (Preserving original NLP implementation)
from backend import (
    extract_cbc_report,
    process_cbc_report,
    suggestion_knowledge_base,
    DATA_DIR
)
from cbc_knowledge_base import Fact
from cbc_inference_engine import ForwardChainingEngine, InferenceResult


# Biological plausibility sanity boundaries for automated validation
BIOLOGICAL_BOUNDARIES = {
    "HGB": {"min": 1.0, "max": 28.0, "unit": "g/dL", "name": "Hemoglobin"},
    "HCT": {"min": 5.0, "max": 80.0, "unit": "%", "name": "Hematocrit"},
    "PLT": {"min": 1.0, "max": 2500.0, "unit": "x10^3/uL", "name": "Platelet Count"},
    "MCV": {"min": 35.0, "max": 160.0, "unit": "fL", "name": "Mean Corpuscular Volume"},
    "MCH": {"min": 10.0, "max": 60.0, "unit": "pg", "name": "Mean Corpuscular Hemoglobin"},
    "MCHC": {"min": 15.0, "max": 45.0, "unit": "g/dL", "name": "MCHC"},
    "RDW": {"min": 8.0, "max": 35.0, "unit": "%", "name": "Red Cell Distribution Width"},
    "NE%": {"min": 0.0, "max": 100.0, "unit": "%", "name": "Neutrophil Percentage"},
    "LY%": {"min": 0.0, "max": 100.0, "unit": "%", "name": "Lymphocyte Percentage"}
}


# Lazy-loaded spaCy model for NLP entity visualizer in dashboard
_spacy_nlp = None

def get_spacy_model():
    """Lazily loads spaCy model to optimize startup time."""
    global _spacy_nlp
    if _spacy_nlp is None:
        try:
            _spacy_nlp = spacy.load("en_core_web_sm")
        except Exception:
            _spacy_nlp = None
    return _spacy_nlp


def validate_extracted_cbc_parameters(extracted_data: Dict[str, Dict[str, Any]]) -> Tuple[Dict[str, Dict[str, Any]], List[str], List[str]]:
    """
    Validates extracted parameters against clinical plausibility bounds and reference range presence.
    
    Returns:
        valid_params: Dictionary of validated parameters with verified status.
        validation_warnings: Non-fatal notices (e.g. missing reference interval flagged).
        validation_errors: Fatal parameter errors (e.g. physiologically impossible value).
    """
    valid_params = {}
    validation_warnings = []
    validation_errors = []

    for param, data in extracted_data.items():
        val = data.get("value")
        ref_low = data.get("reference_low")
        ref_high = data.get("reference_high")
        unit = data.get("unit", "")
        status = data.get("status", "Unknown")

        # 1. Numerical sanity check
        if val is None or not isinstance(val, (int, float)):
            validation_errors.append(f"{param}: Non-numerical value encountered ({val}).")
            continue

        bounds = BIOLOGICAL_BOUNDARIES.get(param)
        if bounds:
            if val < bounds["min"] or val > bounds["max"]:
                validation_errors.append(
                    f"{param}: Extracted value {val} {unit} is outside physiologically plausible range "
                    f"({bounds['min']} - {bounds['max']} {bounds['unit']}). Flagged as potential extraction artifact."
                )
                continue

        # 2. Reference range integrity check
        if ref_low is None or ref_high is None or ref_low >= ref_high:
            validation_warnings.append(
                f"{param}: Laboratory reference interval missing or invalid ({ref_low} - {ref_high}). "
                f"Automated status classification cannot be verified without laboratory context."
            )
            # Retain parameter but flag status as Unassessed
            valid_params[param] = {
                **data,
                "status": "Unassessed",
                "limitation_flag": "Missing Reference Interval"
            }
            continue

        valid_params[param] = data

    return valid_params, validation_warnings, validation_errors


def convert_parameters_to_facts(valid_params: Dict[str, Dict[str, Any]]) -> List[Fact]:
    """
    Translates validated CBC dictionary findings into declarative Fact objects for Working Memory.
    """
    facts: List[Fact] = []
    idx = 1

    for param, data in valid_params.items():
        status = data.get("status", "Unknown")
        val = data.get("value")
        unit = data.get("unit")
        ref_low = data.get("reference_low")
        ref_high = data.get("reference_high")

        # Fact A: Status proposition (e.g. HGB status_is Low)
        facts.append(Fact(
            fact_id=f"FACT-INP-{idx:02d}",
            category="parameter_status",
            subject=param,
            predicate="status_is",
            value=status,
            unit=unit,
            ref_low=ref_low,
            ref_high=ref_high,
            source="nlp_extractor",
            metadata={"numerical_value": val}
        ))
        idx += 1

        # Fact B: Exact numerical observation
        facts.append(Fact(
            fact_id=f"FACT-INP-{idx:02d}",
            category="parameter_value",
            subject=param,
            predicate="value_is",
            value=val,
            unit=unit,
            ref_low=ref_low,
            ref_high=ref_high,
            source="nlp_extractor"
        ))
        idx += 1

        # Fact C: Limitation proposition if unassessed
        if status == "Unassessed" or data.get("limitation_flag"):
            facts.append(Fact(
                fact_id=f"FACT-INP-{idx:02d}",
                category="limitation",
                subject=f"{param}_LIMITATION",
                predicate="limitation_flagged",
                value=data.get("limitation_flag", "Reference Interval Missing"),
                source="validation"
            ))
            idx += 1

    return facts


def extract_nlp_entities_from_text(text: str) -> List[Dict[str, str]]:
    """
    Extracts recognized Named Entities and medical tokens using spaCy.
    Preserves and showcases the original NLP pipeline in the dashboard.
    """
    nlp_model = get_spacy_model()
    entities = []
    if nlp_model and text:
        try:
            doc = nlp_model(text)
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "explanation": spacy.explain(ent.label_) or ent.label_
                })
        except Exception:
            pass
    return entities


def execute_integrated_cbc_pipeline(
    report_text: str,
    report_id: str = "CBC-CASE-001"
) -> Dict[str, Any]:
    """
    Master pipeline integrating:
    1. Existing NLP extraction (backend.process_cbc_report)
    2. Input validation & physiological boundary checking
    3. Forward Chaining inference engine execution
    4. Reasoning trace generation
    5. Knowledge base educational retrieval
    """
    if not report_text or not report_text.strip():
        return {
            "success": False,
            "error": "Empty report text provided.",
            "structured_df": pd.DataFrame(),
            "inference_result": None
        }

    # Step 1: Run existing backend NLP report processor
    structured_df, final_report = process_cbc_report(report_text, report_id=report_id)

    # Step 2: Extract raw parameter dictionary using existing regex patterns
    raw_extracted = extract_cbc_report(report_text)

    # Step 3: Run input validation
    valid_params, validation_warnings, validation_errors = validate_extracted_cbc_parameters(raw_extracted)

    # Step 4: Populate Working Memory with validated atomic facts
    initial_facts = convert_parameters_to_facts(valid_params)

    # Step 5: Execute Forward Chaining Inference Engine
    engine = ForwardChainingEngine()
    inference_result: InferenceResult = engine.run_inference(initial_facts)

    # Step 6: Extract spaCy Named Entities for NLP demonstration
    nlp_entities = extract_nlp_entities_from_text(report_text)

    # Step 7: Format synthesized result payload
    return {
        "success": True,
        "report_id": report_id,
        "structured_df": structured_df,
        "final_report": final_report,
        "extracted_parameters": valid_params,
        "raw_parameter_count": len(raw_extracted),
        "valid_parameter_count": len(valid_params),
        "validation_warnings": validation_warnings,
        "validation_errors": validation_errors,
        "initial_facts": initial_facts,
        "inference_result": inference_result,
        "reasoning_trace": inference_result.reasoning_trace,
        "derived_findings": inference_result.get_summary_findings(),
        "execution_time_ms": inference_result.execution_time_ms,
        "quiescence_reached": inference_result.quiescence_reached,
        "nlp_entities": nlp_entities
    }
