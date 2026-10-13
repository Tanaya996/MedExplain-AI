"""
MedExplain AI — Forward Chaining Inference Engine
=================================================
Implements a genuine Forward Chaining (Data-Driven) Expert System Inference Engine
for medical knowledge reasoning.

AI Syllabus Concepts Implemented:
1. Intelligent Agents & Knowledge-Based Architecture:
   - Working Memory (Percepts -> Asserted Knowledge)
   - Knowledge Base (Production Rules: Premise -> Conclusion)
   - Inference Engine (Match-Resolve-Act Cycle)
2. Forward Chaining Algorithm:
   - Step 1: Initialize Working Memory with validated atomic facts.
   - Step 2: MATCH phase — find all rules whose antecedents are satisfied by facts in Working Memory.
   - Step 3: RESOLVE phase (Conflict Resolution) — order candidate rules by Salience (Priority) & Specificity.
   - Step 4: ACT / FIRE phase — fire selected rule, assert consequent as new Fact into Working Memory.
   - Step 5: Cycle Prevention — maintain set of fired rules and asserted propositions to prevent loops.
   - Step 6: Repeat until Quiescence (no new rules can fire) or max iterations reached.
3. Transparent Reasoning Trace:
   - Generates an auditable chronological trace of deductions for viva presentation and research documentation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Any, Optional, Tuple
import time

from cbc_knowledge_base import Fact, Rule, RuleCondition, get_knowledge_base


@dataclass
class ReasoningTraceStep:
    """
    Records an individual deductive step in the Forward Chaining process.
    Provides complete transparency for educational explanation and research documentation.
    """
    step_number: int
    rule_id: str
    rule_name: str
    rule_category: str
    matched_facts: List[Fact]
    inferred_fact: Fact
    educational_explanation: str
    clinical_rationale: str
    reference_source: str
    limitations: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step_number,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "category": self.rule_category,
            "matched_facts": [str(f) for f in self.matched_facts],
            "inferred_fact": str(self.inferred_fact),
            "inferred_subject": self.inferred_fact.subject,
            "inferred_value": self.inferred_fact.value,
            "explanation": self.educational_explanation,
            "clinical_rationale": self.clinical_rationale,
            "reference": self.reference_source,
            "limitations": self.limitations
        }


@dataclass
class InferenceResult:
    """Encapsulates the complete result of a Forward Chaining inference session."""
    working_memory: List[Fact]
    initial_facts: List[Fact]
    derived_facts: List[Fact]
    fired_rules: List[Rule]
    reasoning_trace: List[ReasoningTraceStep]
    iterations_count: int
    execution_time_ms: float
    quiescence_reached: bool

    def get_summary_findings(self) -> List[Dict[str, Any]]:
        """Returns structured findings suitable for dashboard display."""
        findings = []
        for step in self.reasoning_trace:
            findings.append({
                "rule_id": step.rule_id,
                "rule_name": step.rule_name,
                "category": step.rule_category,
                "finding": step.inferred_fact.value,
                "matched_premises": ", ".join(f"{f.subject}={f.value}" for f in step.matched_facts),
                "explanation": step.educational_explanation,
                "rationale": step.clinical_rationale,
                "reference": step.reference_source,
                "limitations": step.limitations
            })
        return findings


class ForwardChainingEngine:
    """
    Forward Chaining Inference Engine.
    Executes the classic expert system Match-Resolve-Act reasoning loop.
    """

    def __init__(self, knowledge_base: Optional[List[Rule]] = None, max_iterations: int = 50):
        self.rules: List[Rule] = knowledge_base if knowledge_base is not None else get_knowledge_base()
        self.max_iterations: int = max_iterations

    def run_inference(self, initial_facts: List[Fact]) -> InferenceResult:
        """
        Executes the Forward Chaining reasoning cycle:
        
        Algorithm (Forward Chaining with Salience-based Conflict Resolution):
        ---------------------------------------------------------------------
        1. WorkingMemory <- copy(initial_facts)
        2. FiredRules <- empty_set
        3. Trace <- empty_list
        4. Loop:
             a. Agenda <- []
             b. For each Rule in KnowledgeBase:
                  if Rule not in FiredRules:
                     matched_facts = Rule.check_match(WorkingMemory)
                     if matched_facts is not None:
                        Agenda.append((Rule, matched_facts))
             c. If Agenda is empty:
                  Break (Quiescence reached)
             d. Conflict Resolution:
                  Sort Agenda by Rule.salience (descending), then len(Rule.conditions) (descending)
                  Select candidate_rule, matched_facts = Agenda[0]
             e. Act / Fire:
                  Assert new Fact(candidate_rule.consequent) into WorkingMemory
                  Add candidate_rule.rule_id to FiredRules
                  Record Step in Trace
             f. If iteration >= max_iterations:
                  Break (Safety limit reached)
        5. Return InferenceResult
        """
        start_time = time.perf_counter()

        # Step 1: Initialize Working Memory
        working_memory: List[Fact] = list(initial_facts)
        fired_rule_ids: Set[str] = set()
        fired_rules: List[Rule] = []
        reasoning_trace: List[ReasoningTraceStep] = []
        derived_facts: List[Fact] = []

        step = 0
        quiescence_reached = False

        while step < self.max_iterations:
            # Step 2: MATCH PHASE — Find all candidate rules whose antecedents are satisfied
            agenda: List[Tuple[Rule, List[Fact]]] = []

            for rule in self.rules:
                if rule.rule_id in fired_rule_ids:
                    continue  # Cycle prevention: Rule has already fired in this session

                matched_facts = rule.check_match(working_memory)
                if matched_facts is not None:
                    agenda.append((rule, matched_facts))

            # Quiescence check
            if not agenda:
                quiescence_reached = True
                break

            # Step 3: CONFLICT RESOLUTION PHASE
            # Strategy:
            # 1. Higher Salience (Priority) first
            # 2. Higher number of conditions (Specificity / most specific pattern first)
            agenda.sort(key=lambda item: (item[0].salience, len(item[0].conditions)), reverse=True)

            # Select the highest-priority rule from the agenda
            selected_rule, matched_facts = agenda[0]

            # Step 4: ACT / FIRE PHASE
            step += 1
            new_fact = Fact(
                fact_id=f"FACT-INFERRED-{step:02d}",
                category=selected_rule.category,
                subject=selected_rule.consequent_subject,
                predicate=selected_rule.consequent_predicate,
                value=selected_rule.consequent_value,
                confidence=1.0,
                source=f"rule:{selected_rule.rule_id}",
                metadata={
                    "derived_by_rule": selected_rule.rule_id,
                    "matched_fact_ids": [f.fact_id for f in matched_facts]
                }
            )

            # Assert new knowledge into Working Memory
            working_memory.append(new_fact)
            derived_facts.append(new_fact)
            fired_rule_ids.add(selected_rule.rule_id)
            fired_rules.append(selected_rule)

            # Record reasoning trace step
            trace_step = ReasoningTraceStep(
                step_number=step,
                rule_id=selected_rule.rule_id,
                rule_name=selected_rule.name,
                rule_category=selected_rule.category,
                matched_facts=matched_facts,
                inferred_fact=new_fact,
                educational_explanation=selected_rule.educational_explanation,
                clinical_rationale=selected_rule.clinical_rationale,
                reference_source=selected_rule.reference_source,
                limitations=selected_rule.limitations
            )
            reasoning_trace.append(trace_step)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return InferenceResult(
            working_memory=working_memory,
            initial_facts=list(initial_facts),
            derived_facts=derived_facts,
            fired_rules=fired_rules,
            reasoning_trace=reasoning_trace,
            iterations_count=step,
            execution_time_ms=elapsed_ms,
            quiescence_reached=quiescence_reached
        )
