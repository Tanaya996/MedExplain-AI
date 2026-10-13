"""
MedExplain AI — Knowledge Base Module
======================================
Implements Knowledge Representation for CBC Interpretation in accordance with
the college Artificial Intelligence syllabus (Knowledge-Based Agents & Rule-Based Expert Systems).

Knowledge Representation Scheme:
- Declarative Production Rules (Horn Clauses: Antecedents -> Consequent)
- Structured Facts with attributes: Parameter, Value, Unit, Reference Low/High, Status
- Medical grounding with educational explanations, literature references, and explicit limitations.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable


@dataclass
class Fact:
    """
    Atomic proposition in Working Memory.
    Represents an asserted observation or a derived finding.
    """
    fact_id: str
    category: str              # 'parameter', 'derived_pattern', 'limitation', 'validation'
    subject: str               # e.g., 'HGB', 'MCV', 'ANEMIA_PATTERN', 'ERYTHROCYTE_SIZE'
    predicate: str             # e.g., 'status_is', 'pattern_detected', 'value_is'
    value: Any                 # e.g., 'Low', 'Microcytic', 11.2
    unit: Optional[str] = None
    ref_low: Optional[float] = None
    ref_high: Optional[float] = None
    confidence: float = 1.0    # 1.0 for deterministic rule deductions
    source: str = "input"      # 'input', 'nlp_extractor', or 'rule_deduction'
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        if self.ref_low is not None and self.ref_high is not None:
            return f"Fact({self.subject} {self.predicate} {self.value} [{self.ref_low}-{self.ref_high} {self.unit}])"
        return f"Fact({self.subject} {self.predicate} {self.value})"


@dataclass
class RuleCondition:
    """
    Antecedent condition of a rule.
    Matches a fact in Working Memory by subject, predicate, and target value or comparison.
    """
    subject: str
    predicate: str = "status_is"
    expected_value: Any = None
    comparator: Optional[str] = None  # '==', '!=', '<', '>', 'in'

    def matches(self, fact: Fact) -> bool:
        if fact.subject != self.subject:
            return False
        if fact.predicate != self.predicate:
            return False
        if self.comparator == "in" and isinstance(self.expected_value, (list, tuple, set)):
            return fact.value in self.expected_value
        if self.comparator == "<":
            return float(fact.value) < float(self.expected_value)
        if self.comparator == ">":
            return float(fact.value) > float(self.expected_value)
        if self.comparator == "!=":
            return fact.value != self.expected_value
        # Default equality
        return fact.value == self.expected_value


@dataclass
class Rule:
    """
    Production Rule representation in the Expert System Knowledge Base.
    Format: IF (Antecedents) THEN (Consequent) with Educational & Reference Metadata.
    """
    rule_id: str
    name: str
    category: str                     # 'primary_status', 'hematology_pattern', 'differential', 'limitation'
    conditions: List[RuleCondition]  # All must match (Conjunction: A1 AND A2 ... AND An)
    consequent_subject: str
    consequent_predicate: str
    consequent_value: Any
    educational_explanation: str
    clinical_rationale: str
    reference_source: str
    limitations: str
    salience: int = 10               # Higher salience fires first in Conflict Resolution

    def check_match(self, working_memory: List[Fact]) -> Optional[List[Fact]]:
        """
        Evaluates rule antecedents against working memory.
        Returns list of matched facts if ALL conditions are satisfied; else None.
        """
        matched_facts = []
        for cond in self.conditions:
            found = False
            for fact in working_memory:
                if cond.matches(fact):
                    matched_facts.append(fact)
                    found = True
                    break
            if not found:
                return None
        return matched_facts


# -------------------------------------------------------------------------
# MEDICAL KNOWLEDGE BASE DEFINITION
# Expert hematological rules formulated in accordance with standard laboratory
# reference guides (e.g., WHO Anemia Criteria, Wintrobe's Clinical Hematology)
# -------------------------------------------------------------------------

CBC_RULES: List[Rule] = [
    # ---------------------------------------------------------------------
    # 1. PRIMARY PARAMETER STATUS RULES (Salience 10)
    # ---------------------------------------------------------------------
    Rule(
        rule_id="RULE-PRIM-HGB-LOW",
        name="Hemoglobin Below Reference Range",
        category="primary_status",
        conditions=[RuleCondition(subject="HGB", predicate="status_is", expected_value="Low")],
        consequent_subject="HGB_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Low Hemoglobin (Subnormal oxygen-carrying capacity)",
        educational_explanation=(
            "Hemoglobin is the iron-containing protein in red blood cells that transports oxygen "
            "from lungs to tissues. A level below the laboratory reference interval suggests subnormal "
            "oxygen-carrying capacity, commonly referred to as an anemic state."
        ),
        clinical_rationale="Circulating hemoglobin level is below reference baseline.",
        reference_source="WHO Haemoglobin concentrations for the diagnosis of anaemia (WHO/NMH/NHD/MNM/11.1)",
        limitations="Does not specify the underlying etiology (nutritional, hemolytic, blood loss, or chronic illness).",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-HGB-HIGH",
        name="Hemoglobin Above Reference Range",
        category="primary_status",
        conditions=[RuleCondition(subject="HGB", predicate="status_is", expected_value="High")],
        consequent_subject="HGB_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Elevated Hemoglobin (Possible hemoconcentration or erythrocytosis)",
        educational_explanation=(
            "An elevated hemoglobin level indicates a higher-than-normal concentration of hemoglobin. "
            "This can occur transiently due to dehydration (relative hemoconcentration) or as an absolute "
            "increase in red blood cell mass (hypoxia, smoking, high altitude, or myeloproliferative disorders)."
        ),
        clinical_rationale="Circulating hemoglobin level is above laboratory reference baseline.",
        reference_source="Wintrobe's Clinical Hematology, 14th Edition; NCCLS Laboratory Guidelines",
        limitations="Hydration status must be assessed prior to considering absolute polycythemia.",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-HCT-LOW",
        name="Hematocrit Below Reference Range",
        category="primary_status",
        conditions=[RuleCondition(subject="HCT", predicate="status_is", expected_value="Low")],
        consequent_subject="HCT_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Low Hematocrit (Reduced red cell fraction)",
        educational_explanation=(
            "Hematocrit represents the fraction of total blood volume occupied by red blood cells. "
            "A low hematocrit corresponds to a lower volume percentage of red cells, tracking closely with hemoglobin."
        ),
        clinical_rationale="Packed cell volume is below reference interval.",
        reference_source="Henry's Clinical Diagnosis and Management by Laboratory Methods, 24th Ed.",
        limitations="Hematocrit is affected by plasma volume variations and fluid shifts.",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-HCT-HIGH",
        name="Hematocrit Above Reference Range",
        category="primary_status",
        conditions=[RuleCondition(subject="HCT", predicate="status_is", expected_value="High")],
        consequent_subject="HCT_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Elevated Hematocrit (Increased red cell volume fraction)",
        educational_explanation=(
            "Hematocrit above the reference interval indicates an increased fraction of red cells in blood. "
            "Often mirrors elevated hemoglobin and may increase blood viscosity."
        ),
        clinical_rationale="Packed cell volume exceeds reference interval.",
        reference_source="Henry's Clinical Diagnosis and Management by Laboratory Methods, 24th Ed.",
        limitations="Spurious elevation can occur with severe hemoconcentration / fluid deficit.",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-PLT-LOW",
        name="Platelet Count Below Reference Range",
        category="primary_status",
        conditions=[RuleCondition(subject="PLT", predicate="status_is", expected_value="Low")],
        consequent_subject="PLT_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Thrombocytopenia (Decreased platelet count)",
        educational_explanation=(
            "Platelets (thrombocytes) are essential cellular fragments for blood coagulation and primary hemostasis. "
            "A low platelet count (thrombocytopenia) may predispose to prolonged bleeding or bruising if markedly reduced."
        ),
        clinical_rationale="Circulating platelet count is below laboratory reference interval.",
        reference_source="Harrison's Principles of Internal Medicine, Hematologic Alterations",
        limitations="Mild reductions may be asymptomatic; pseudothrombocytopenia from EDTA-clumping must be ruled out.",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-PLT-HIGH",
        name="Platelet Count Above Reference Range",
        category="primary_status",
        conditions=[RuleCondition(subject="PLT", predicate="status_is", expected_value="High")],
        consequent_subject="PLT_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Thrombocytosis (Elevated platelet count)",
        educational_explanation=(
            "An elevated platelet count (thrombocytosis) is most commonly reactive (secondary to infection, "
            "systemic inflammation, iron deficiency, or tissue trauma) and less commonly primary/essential."
        ),
        clinical_rationale="Circulating platelet count exceeds reference upper boundary.",
        reference_source="British Journal of Haematology, Investigation of Thrombocytosis (2010)",
        limitations="Reactive vs autonomous thrombocytosis cannot be determined from CBC alone.",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-MCV-LOW",
        name="Mean Corpuscular Volume Subnormal",
        category="primary_status",
        conditions=[RuleCondition(subject="MCV", predicate="status_is", expected_value="Low")],
        consequent_subject="MCV_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Microcytosis (Reduced average erythrocyte size)",
        educational_explanation=(
            "Mean Corpuscular Volume (MCV) quantifies the average volume of individual red blood cells in femtoliters (fL). "
            "An MCV below range indicates microcytic erythrocytes (smaller than normal cells)."
        ),
        clinical_rationale="Erythrocyte mean volume is below reference threshold.",
        reference_source="Hoffman: Hematology Basic Principles and Practice, Red Cell Indices",
        limitations="Requires correlation with hemoglobin, RDW, and ferritin.",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-MCV-HIGH",
        name="Mean Corpuscular Volume Elevated",
        category="primary_status",
        conditions=[RuleCondition(subject="MCV", predicate="status_is", expected_value="High")],
        consequent_subject="MCV_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Macrocytosis (Enlarged average erythrocyte size)",
        educational_explanation=(
            "An MCV above reference interval signifies macrocytic red cells (larger than average). "
            "Potential educational associations include vitamin B12 / folate deficiency, reticulocytosis, "
            "alcohol intake, or medication effects."
        ),
        clinical_rationale="Erythrocyte mean volume exceeds reference threshold.",
        reference_source="Hoffman: Hematology Basic Principles and Practice",
        limitations="Macrocytosis can exist with or without overt clinical anemia.",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-RDW-HIGH",
        name="Red Cell Distribution Width Elevated",
        category="primary_status",
        conditions=[RuleCondition(subject="RDW", predicate="status_is", expected_value="High")],
        consequent_subject="RDW_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Anisocytosis (Significant variability in red blood cell volume)",
        educational_explanation=(
            "RDW is a mathematical index measuring the degree of heterogeneity in red cell sizes. "
            "A high RDW indicates anisocytosis (unequal cell sizes), frequently seen in evolving nutritional "
            "deficiencies (e.g., early iron or B12 deficiency) or mixed etiologies."
        ),
        clinical_rationale="Coefficient of variation in red blood cell sizing exceeds threshold.",
        reference_source="American Family Physician: Using the Complete Blood Count to Evaluate Anemia",
        limitations="Elevated RDW is sensitive but not specific for any single disorder.",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-NE-HIGH",
        name="Neutrophil Percentage Elevated",
        category="primary_status",
        conditions=[RuleCondition(subject="NE%", predicate="status_is", expected_value="High")],
        consequent_subject="NE_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Neutrophilia (Elevated relative neutrophil proportion)",
        educational_explanation=(
            "Neutrophils are first-responder phagocytic leukocytes. Elevated relative neutrophil percentage "
            "is commonly associated with acute bacterial infection, physical stress, tissue necrosis, or inflammation."
        ),
        clinical_rationale="Proportion of polymorphonuclear neutrophils exceeds reference upper bound.",
        reference_source="Williams Hematology, 9th Edition, Chapter on Leukocyte Biology",
        limitations="Must be evaluated with absolute leukocyte count; relative percentage can be skewed.",
        salience=10
    ),
    Rule(
        rule_id="RULE-PRIM-LY-LOW",
        name="Lymphocyte Percentage Subnormal",
        category="primary_status",
        conditions=[RuleCondition(subject="LY%", predicate="status_is", expected_value="Low")],
        consequent_subject="LY_INTERPRETATION",
        consequent_predicate="finding",
        consequent_value="Relative Lymphopenia (Decreased lymphocyte percentage)",
        educational_explanation=(
            "Lymphocytes mediate adaptive cellular and humoral immunity. A decreased relative percentage often "
            "accompanies an increase in neutrophil percentage (relative shift) or acute physiological stress."
        ),
        clinical_rationale="Proportion of circulating lymphocytes is below reference boundary.",
        reference_source="Williams Hematology, Leukocyte Variations",
        limitations="Relative lymphopenia does not always equate to absolute lymphopenia.",
        salience=10
    ),

    # ---------------------------------------------------------------------
    # 2. MULTI-PARAMETER HEMATOLOGY PATTERN RULES (Salience 20 - 30)
    # Higher salience: Fires first to synthesize cross-parameter reasoning!
    # ---------------------------------------------------------------------
    Rule(
        rule_id="RULE-MULTI-MICRO-HYPO",
        name="Microcytic Hypochromic Pattern",
        category="hematology_pattern",
        conditions=[
            RuleCondition(subject="HGB", predicate="status_is", expected_value="Low"),
            RuleCondition(subject="MCV", predicate="status_is", expected_value="Low"),
            RuleCondition(subject="MCH", predicate="status_is", expected_value="Low")
        ],
        consequent_subject="HEMATOLOGY_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Microcytic Hypochromic Anemia Pattern",
        educational_explanation=(
            "The simultaneous occurrence of subnormal Hemoglobin, reduced MCV (<80 fL), and low MCH (<27 pg) "
            "defines a classical microcytic hypochromic erythrocyte pattern. The red cells are smaller and contain less "
            "hemoglobin per cell than normal. Common educational differential considerations include iron deficiency, "
            "thalassemia trait, anemia of chronic disease, or sideroblastic anemia."
        ),
        clinical_rationale="Concurrent defects in red cell mass (HGB), cell volume (MCV), and chromicity (MCH).",
        reference_source="Wintrobe's Clinical Hematology: Classification of Anemias by Morphology",
        limitations=(
            "Educational pattern match only. Differentiating iron deficiency from thalassemia minor requires serum ferritin, "
            "iron studies, and hemoglobin electrophoresis."
        ),
        salience=30
    ),
    Rule(
        rule_id="RULE-MULTI-MICRO-ANEMIA",
        name="Microcytic Anemia Pattern",
        category="hematology_pattern",
        conditions=[
            RuleCondition(subject="HGB", predicate="status_is", expected_value="Low"),
            RuleCondition(subject="MCV", predicate="status_is", expected_value="Low")
        ],
        consequent_subject="HEMATOLOGY_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Microcytic Anemia Pattern",
        educational_explanation=(
            "Low Hemoglobin combined with low MCV indicates microcytic anemia. Red blood cells have a smaller "
            "average volume alongside reduced total circulating oxygen carrier."
        ),
        clinical_rationale="Concomitant subnormal hemoglobin and erythrocyte volume.",
        reference_source="American College of Physicians (ACP) Practice Guidelines on Anemia Evaluation",
        limitations="Requires iron panel and clinical history for diagnostic determination.",
        salience=25
    ),
    Rule(
        rule_id="RULE-MULTI-MACRO-ANEMIA",
        name="Macrocytic Anemia Pattern",
        category="hematology_pattern",
        conditions=[
            RuleCondition(subject="HGB", predicate="status_is", expected_value="Low"),
            RuleCondition(subject="MCV", predicate="status_is", expected_value="High")
        ],
        consequent_subject="HEMATOLOGY_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Macrocytic Anemia Pattern",
        educational_explanation=(
            "Low Hemoglobin coupled with elevated MCV (>100 fL) indicates a macrocytic anemic pattern. "
            "Erythrocytes are larger than normal. Common educational differential considerations include megaloblastic "
            "processes (Vitamin B12 or folic acid deficiency), drug-induced changes, liver disease, or marked reticulocytosis."
        ),
        clinical_rationale="Concomitant subnormal hemoglobin and supra-normal erythrocyte volume.",
        reference_source="British Society for Haematology Guidelines for the diagnosis and treatment of cobalamin and folate disorders",
        limitations="Serum B12, folate, and peripheral blood smear review are required to evaluate hypersegmented neutrophils.",
        salience=25
    ),
    Rule(
        rule_id="RULE-MULTI-NORMOCYTIC-ANEMIA",
        name="Normocytic Anemia Pattern",
        category="hematology_pattern",
        conditions=[
            RuleCondition(subject="HGB", predicate="status_is", expected_value="Low"),
            RuleCondition(subject="MCV", predicate="status_is", expected_value="Normal")
        ],
        consequent_subject="HEMATOLOGY_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Normocytic Anemia Pattern",
        educational_explanation=(
            "Low Hemoglobin in the presence of a normal MCV represents normocytic anemia (normal cell size, "
            "reduced cell number). Common causes include early nutritional deficiency, anemia of chronic inflammation/illness, "
            "acute blood loss, renal impairment, or mixed deficiencies where micro- and macro-cytosis balance out."
        ),
        clinical_rationale="Subnormal hemoglobin with normal average red cell sizing.",
        reference_source="Harrison's Principles of Internal Medicine: Anemia and Polycythemia",
        limitations="Retinol, renal parameters (creatinine/eGFR), and reticulocyte count are necessary to determine bone marrow response.",
        salience=25
    ),
    Rule(
        rule_id="RULE-MULTI-ANISOCYTOSIS-ANEMIA",
        name="Anemia with Anisocytosis (Heterogeneous Cell Sizing)",
        category="hematology_pattern",
        conditions=[
            RuleCondition(subject="HGB", predicate="status_is", expected_value="Low"),
            RuleCondition(subject="RDW", predicate="status_is", expected_value="High")
        ],
        consequent_subject="HEMATOLOGY_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Anemia with Anisocytosis (Variable Sizing)",
        educational_explanation=(
            "The combination of low Hemoglobin with an elevated RDW indicates that red blood cells vary markedly in size. "
            "In microcytic states, elevated RDW strongly supports nutritional iron deficiency over uncomplicated thalassemia trait "
            "(which typically presents with a uniform, normal RDW)."
        ),
        clinical_rationale="Red cell distribution width is elevated in the setting of decreased hemoglobin.",
        reference_source="Bessman JD et al. Improved classification of anemias by MCV and RDW. Am J Clin Pathol 1983",
        limitations="RDW elevation can also be seen post-transfusion or during response to hematinic therapy.",
        salience=25
    ),
    Rule(
        rule_id="RULE-MULTI-ERYTHROCYTOSIS",
        name="Erythrocytosis / Polycythemic Profile",
        category="hematology_pattern",
        conditions=[
            RuleCondition(subject="HGB", predicate="status_is", expected_value="High"),
            RuleCondition(subject="HCT", predicate="status_is", expected_value="High")
        ],
        consequent_subject="HEMATOLOGY_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Erythrocytosis / Elevated Red Cell Mass Pattern",
        educational_explanation=(
            "Concurrent elevation of both Hemoglobin and Hematocrit suggests increased red blood cell volume. "
            "This can be relative (hemoconcentration due to dehydration, burns, or diuretic therapy) or absolute "
            "(secondary to chronic hypoxemia, sleep apnea, smoking, or primary polycythemia vera)."
        ),
        clinical_rationale="Co-elevation of both key red cell concentration markers.",
        reference_source="WHO Diagnostic Criteria for Myeloproliferative Neoplasms (Polycythemia Vera)",
        limitations="Hydration state must be normalized before assessing erythropoietin levels or JAK2 mutation status.",
        salience=25
    ),
    Rule(
        rule_id="RULE-MULTI-BICYTOPENIA",
        name="Concurrent Anemia and Thrombocytopenia",
        category="hematology_pattern",
        conditions=[
            RuleCondition(subject="HGB", predicate="status_is", expected_value="Low"),
            RuleCondition(subject="PLT", predicate="status_is", expected_value="Low")
        ],
        consequent_subject="HEMATOLOGY_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Bi-Cytopenia (Concomitant Anemia and Thrombocytopenia)",
        educational_explanation=(
            "Simultaneous reduction of both red cell (HGB) and platelet (PLT) lineages indicates involvement of multiple "
            "hematopoietic cell lines. Potential considerations include splenic sequestration, immune-mediated destruction (e.g., Evans syndrome), "
            "severe nutritional deficits, or marrow suppressive processes."
        ),
        clinical_rationale="Depression of two distinct peripheral blood cell lineages.",
        reference_source="Williams Hematology, Chapter on Pancytopenia and Bone Marrow Failure",
        limitations="Requires urgent clinical correlation, peripheral smear examination, and reticulocyte evaluation.",
        salience=28
    ),
    Rule(
        rule_id="RULE-MULTI-DIFF-GRANULO",
        name="Granulocytic Predominance (Neutrophilia with Relative Lymphopenia)",
        category="differential",
        conditions=[
            RuleCondition(subject="NE%", predicate="status_is", expected_value="High"),
            RuleCondition(subject="LY%", predicate="status_is", expected_value="Low")
        ],
        consequent_subject="DIFFERENTIAL_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Relative Granulocytic / Acute Inflammatory Shift",
        educational_explanation=(
            "An elevated neutrophil percentage alongside decreased lymphocyte percentage represents a classic "
            "granulocytic predominance pattern on the leukocyte differential. This relative shift frequently reflects an acute "
            "physiological stress response, acute bacterial infection, corticosteroid administration, or tissue inflammation."
        ),
        clinical_rationale="Relative proportion of neutrophils is increased with corresponding depression in lymphocyte fraction.",
        reference_source="Clinical Methods: The History, Physical, and Laboratory Examinations (Chapter on Leukocyte Count)",
        limitations="Absolute counts (neutrophils and lymphocytes per microliter) are required for definitive differential assessment.",
        salience=20
    ),
    Rule(
        rule_id="RULE-MULTI-DIFF-LYMPHO",
        name="Lymphocytic Predominance (Relative Neutropenia)",
        category="differential",
        conditions=[
            RuleCondition(subject="NE%", predicate="status_is", expected_value="Low"),
            RuleCondition(subject="LY%", predicate="status_is", expected_value="High")
        ],
        consequent_subject="DIFFERENTIAL_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Relative Lymphocytic / Viral Shift Pattern",
        educational_explanation=(
            "Decreased neutrophil proportion with elevated lymphocyte percentage suggests relative lymphocytic predominance. "
            "This pattern is frequently observed during recovering bacterial infections, acute viral infections (e.g., EBV, CMV, hepatitis), "
            "or benign relative shifts."
        ),
        clinical_rationale="Relative proportion of lymphocytes is elevated while neutrophil percentage is suppressed.",
        reference_source="Clinical Hematology and Fundamentals of Hemostasis, Leukocyte Disorders",
        limitations="Pediatric populations naturally have higher lymphocyte proportions than adults.",
        salience=20
    ),

    # ---------------------------------------------------------------------
    # 3. NORMAL PHYSIOLOGICAL HOMEOSTASIS RULE
    # ---------------------------------------------------------------------
    Rule(
        rule_id="RULE-HOMEOSTASIS-NORMAL",
        name="CBC Parameters Within Reference Range",
        category="primary_status",
        conditions=[
            RuleCondition(subject="HGB", predicate="status_is", expected_value="Normal"),
            RuleCondition(subject="PLT", predicate="status_is", expected_value="Normal"),
            RuleCondition(subject="MCV", predicate="status_is", expected_value="Normal")
        ],
        consequent_subject="HEMATOLOGY_SYNDROME",
        consequent_predicate="inferred_pattern",
        consequent_value="Erythroid and Platelet Homeostasis Preserved",
        educational_explanation=(
            "Core measured erythroid parameters (Hemoglobin, MCV) and platelet counts are within established reference "
            "intervals. This suggests preserved red cell oxygen delivery capacity and quantitative platelet adequacy."
        ),
        clinical_rationale="Key CBC parameters align with laboratory reference boundaries.",
        reference_source="Laboratory Medicine: The Diagnosis of Disease in the Clinical Laboratory",
        limitations="Normal CBC parameters do not completely exclude non-hematologic pathology or latent iron depletion.",
        salience=15
    )
]


def get_knowledge_base() -> List[Rule]:
    """Returns the expert system rules in the knowledge base."""
    return CBC_RULES
