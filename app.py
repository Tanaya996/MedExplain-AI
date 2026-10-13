import streamlit as st
import pandas as pd
import re
import os
import time

# ---------------------------------------------------------
# IMPORT BACKEND PIPELINE & NEW AI EXPERT SYSTEM
# ---------------------------------------------------------
try:
    from backend import process_cbc_report, extract_cbc_report, suggestion_knowledge_base
except ImportError:
    st.error("Backend module not found. Please ensure 'backend.py' is present.")
    st.stop()

from cbc_ai_integration import execute_integrated_cbc_pipeline
from cbc_knowledge_base import get_knowledge_base
from evaluate_ai_agent import BENCHMARK_CASES, run_benchmark_evaluation

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="MedExplain AI — Intelligent CBC Understanding",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# PROFESSIONAL MEDICAL-AI STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-color: #F8FAFC;
        --card-bg: #FFFFFF;
        --primary-navy: #0F2942;
        --primary-blue: #1E3A8A;
        --accent-teal: #0D9488;
        --text-primary: #1E293B;
        --text-secondary: #64748B;
        --text-muted: #94A3B8;
        --border-color: #E2E8F0;
        --normal-color: #059669;
        --normal-bg: #ECFDF5;
        --warning-color: #D97706;
        --warning-bg: #FFFBEB;
        --danger-color: #DC2626;
        --danger-bg: #FEF2F2;
        --info-color: #2563EB;
        --info-bg: #EFF6FF;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary);
    }
    
    .stApp {
        background-color: var(--bg-color);
    }
    
    /* Header Container */
    .med-header {
        background-color: var(--card-bg);
        border-bottom: 1px solid var(--border-color);
        padding: 1.5rem 2.5rem;
        margin: -4rem -3rem 1.75rem -3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .med-brand {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .med-brand-icon {
        font-size: 32px;
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        padding: 8px 12px;
        border-radius: 10px;
    }
    .med-title {
        font-size: 24px;
        font-weight: 700;
        color: var(--primary-navy);
        margin: 0;
        letter-spacing: -0.3px;
    }
    .med-subtitle {
        font-size: 13px;
        font-weight: 500;
        color: var(--text-secondary);
        margin: 2px 0 0 0;
    }
    .med-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
        background: #EFF6FF;
        color: var(--primary-blue);
        border: 1px solid #DBEAFE;
    }

    /* Content Cards */
    .med-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.5rem;
    }
    
    /* Summary Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.15rem 1rem;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
    }
    .metric-card-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: var(--text-secondary);
        margin-bottom: 6px;
    }
    .metric-card-value {
        font-size: 26px;
        font-weight: 700;
        color: var(--primary-navy);
        margin: 0;
        line-height: 1.1;
    }

    /* Status Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        font-size: 12px;
        font-weight: 600;
        border-radius: 12px;
        letter-spacing: 0.2px;
    }
    .badge-Normal {
        background-color: var(--normal-bg);
        color: var(--normal-color);
        border: 1px solid #A7F3D0;
    }
    .badge-Low, .badge-High {
        background-color: var(--danger-bg);
        color: var(--danger-color);
        border: 1px solid #FECACA;
    }
    .badge-Unassessed, .badge-Attention {
        background-color: var(--warning-bg);
        color: var(--warning-color);
        border: 1px solid #FDE68A;
    }

    /* Rule Trace Card */
    .trace-card {
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--primary-blue);
        border-radius: 6px;
        padding: 1.1rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .trace-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .trace-title {
        font-size: 15px;
        font-weight: 600;
        color: var(--primary-navy);
    }
    .trace-rule-id {
        font-size: 11px;
        font-family: monospace;
        font-weight: 600;
        background: #F1F5F9;
        color: #475569;
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #E2E8F0;
    }
    .trace-body {
        font-size: 13px;
        color: #334155;
        line-height: 1.55;
        margin-bottom: 0.6rem;
    }
    .trace-meta {
        font-size: 11px;
        color: var(--text-secondary);
        border-top: 1px dashed var(--border-color);
        padding-top: 6px;
        margin-top: 6px;
    }

    /* Reference Range Progress Bar */
    .ref-bar-wrap {
        width: 100%;
        margin-top: 6px;
        margin-bottom: 16px;
    }
    .ref-bar-labels {
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: var(--text-muted);
        margin-bottom: 4px;
    }
    .ref-bar-track {
        width: 100%;
        height: 8px;
        border-radius: 4px;
        position: relative;
        background: linear-gradient(90deg, #FEE2E2 0%, #FEE2E2 25%, #DCFCE7 25%, #DCFCE7 75%, #FEE2E2 75%, #FEE2E2 100%);
        border: 1px solid #E2E8F0;
    }
    .ref-bar-marker {
        position: absolute;
        top: -6px;
        width: 5px;
        height: 20px;
        background-color: var(--primary-navy);
        border-radius: 2.5px;
        transform: translateX(-50%);
        box-shadow: 0 0 3px rgba(0,0,0,0.3);
    }

    /* Distribution Bar */
    .dist-bar-wrap {
        display: flex;
        width: 100%;
        height: 10px;
        border-radius: 5px;
        overflow: hidden;
        margin: 10px 0;
        border: 1px solid var(--border-color);
    }

    /* Medical Disclaimer Footer */
    .med-disclaimer {
        background-color: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1.25rem;
        margin-top: 3rem;
        text-align: center;
        font-size: 12px;
        color: var(--text-secondary);
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------------------------
def calc_marker_position(val, range_str):
    """Calculates percentage position for CSS reference range indicator."""
    try:
        if not range_str or not isinstance(range_str, str):
            return 50
        nums = [float(x) for x in re.findall(r"[\d\.]+", range_str.replace(',', '.'))]
        if len(nums) == 2:
            r_min, r_max = nums[0], nums[1]
            val = float(val)
            span = r_max - r_min
            if span <= 0:
                return 50
            if val < r_min:
                lower_bound = max(0.0, r_min - span)
                if val <= lower_bound:
                    return 5
                return 25 * ((val - lower_bound) / (r_min - lower_bound))
            elif val > r_max:
                upper_bound = r_max + span
                if val >= upper_bound:
                    return 95
                return 75 + 25 * ((val - r_max) / (upper_bound - r_max))
            else:
                return 25 + 50 * ((val - r_min) / span)
    except Exception:
        pass
    return 50


# ---------------------------------------------------------
# APPLICATION HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="med-header">
    <div class="med-brand">
        <span class="med-brand-icon">⚕️</span>
        <div>
            <h1 class="med-title">MedExplain AI</h1>
            <p class="med-subtitle">Intelligent Complete Blood Count (CBC) Understanding via NLP & Knowledge-Based Forward Chaining</p>
        </div>
    </div>
    <div style="display: flex; gap: 8px; align-items: center;">
        <span class="med-pill">🎓 AI & NLP Research Prototype</span>
        <span class="med-pill" style="background:#F0FDF4; color:#166534; border-color:#DCFCE7;">⚡ Expert System v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SESSION STATE MANAGEMENT
# ---------------------------------------------------------
if 'report_processed' not in st.session_state:
    st.session_state.report_processed = False
if 'structured_df' not in st.session_state:
    st.session_state.structured_df = None
if 'final_report' not in st.session_state:
    st.session_state.final_report = None
if 'ai_payload' not in st.session_state:
    st.session_state.ai_payload = None
if 'active_report_id' not in st.session_state:
    st.session_state.active_report_id = "CBC-CASE-001"


# ---------------------------------------------------------
# REPORT INPUT SECTION
# ---------------------------------------------------------
if not st.session_state.report_processed:
    st.markdown('<div class="med-card" style="max-width: 900px; margin: 0 auto;">', unsafe_allow_html=True)
    st.markdown("<h2 style='font-size: 18px; font-weight: 700; color: #0F2942; margin-top:0;'>📥 Input CBC Report</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #64748B;'>Select an input method or load a verified clinical benchmark scenario for viva demonstration.</p>", unsafe_allow_html=True)

    input_mode = st.radio(
        "Input Method",
        ["Paste Report Text", "Upload Text File (.txt)", "Load Preset Clinical Scenario"],
        horizontal=True
    )

    report_text = ""
    case_id_input = "CBC-DEMO-001"

    if input_mode == "Paste Report Text":
        report_text = st.text_area(
            "Paste CBC Report text below:",
            height=200,
            placeholder="Hemoglobin (HGB) 11.2 g/dL 12.0 - 15.5\nMean Corpuscular Volume (MCV) 72.0 fL 80.0 - 100.0\nPlatelets 250 x10^3/uL 150 - 450..."
        )
    elif input_mode == "Upload Text File (.txt)":
        uploaded_file = st.file_uploader("Upload raw report text file", type=["txt"])
        if uploaded_file:
            report_text = uploaded_file.read().decode("utf-8", errors="replace")
            case_id_input = uploaded_file.name.replace(".txt", "")
            st.success(f"Report '{uploaded_file.name}' loaded successfully.")
    else:
        preset_names = [f"{c['case_id']} — {c['title']}" for c in BENCHMARK_CASES]
        selected_idx = st.selectbox("Select Benchmark Case:", range(len(preset_names)), format_func=lambda i: preset_names[i])
        selected_case = BENCHMARK_CASES[selected_idx]
        case_id_input = selected_case["case_id"]
        report_text = selected_case["text"]
        st.info(f"**Description:** {selected_case['description']}")
        st.text_area("Preview Case Report:", report_text, height=140, disabled=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚀 Analyze with MedExplain AI", type="primary", use_container_width=True):
            if report_text and report_text.strip():
                with st.spinner("Executing NLP extraction and Forward Chaining inference..."):
                    payload = execute_integrated_cbc_pipeline(report_text, report_id=case_id_input)
                    if payload["success"]:
                        if payload["structured_df"].empty and payload["valid_parameter_count"] == 0:
                            st.error("No supported CBC parameters were recognized in the provided report text. Please verify formatting.")
                        else:
                            st.session_state.structured_df = payload["structured_df"]
                            st.session_state.final_report = payload["final_report"]
                            st.session_state.ai_payload = payload
                            st.session_state.active_report_id = case_id_input
                            st.session_state.report_processed = True
                            st.rerun()
                    else:
                        st.error(payload.get("error", "Error executing analysis pipeline."))
            else:
                st.warning("Please provide CBC report content to analyze.")
    with col2:
        if st.button("Reset Form", use_container_width=True):
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Empty State Guide
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; color: #64748B; max-width: 650px; margin-left: auto; margin-right: auto;">
        <h4 style="color: #0F2942; margin-bottom: 6px;">How MedExplain AI Operates</h4>
        <p style="font-size: 13px; line-height: 1.6;">
            1. <strong>NLP Information Extraction</strong> identifies CBC parameters, quantities, units, and laboratory reference ranges.<br>
            2. <strong>Input Validation</strong> verifies numerical integrity and flags missing reference boundaries.<br>
            3. <strong>Forward Chaining Expert Engine</strong> matches validated facts against production rules to infer single and multi-parameter hematological patterns.<br>
            4. <strong>Reasoning Trace Generator</strong> displays step-by-step transparent justification suitable for academic defense.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# DASHBOARD RESULTS SECTION
# ---------------------------------------------------------
else:
    df = st.session_state.structured_df
    report_info = st.session_state.final_report
    ai_data = st.session_state.ai_payload

    # Pre-calculated summary numbers
    total_params = len(df) if df is not None else 0
    normal_count = len(df[df['Status'].str.lower() == 'normal']) if (df is not None and not df.empty) else 0
    attention_count = total_params - normal_count
    rules_fired_count = len(ai_data["reasoning_trace"]) if ai_data else 0
    exec_latency_ms = ai_data["execution_time_ms"] if ai_data else 0.0

    # Top Control Bar
    top_col, btn_col = st.columns([5, 1])
    with top_col:
        st.markdown(f"<h2 style='color:#0F2942; font-size:22px; font-weight:700; margin:0;'>📊 Analysis Results — {st.session_state.active_report_id}</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#64748B; margin-top:2px;'>Integrated Natural Language Processing & Forward Chaining Deduction Output</p>", unsafe_allow_html=True)
    with btn_col:
        if st.button("🔄 New Report", use_container_width=True):
            st.session_state.report_processed = False
            st.session_state.structured_df = None
            st.session_state.final_report = None
            st.session_state.ai_payload = None
            st.rerun()

    # KPI METRIC CARDS
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-card-label">Report Identifier</div>
            <div class="metric-card-value" style="font-size:18px; color:#475569; margin-top:4px;">{st.session_state.active_report_id}</div>
        </div>
        <div class="metric-card">
            <div class="metric-card-label">Parameters Extracted</div>
            <div class="metric-card-value">{total_params}</div>
        </div>
        <div class="metric-card">
            <div class="metric-card-label">Within Reference</div>
            <div class="metric-card-value" style="color:var(--normal-color);">{normal_count}</div>
        </div>
        <div class="metric-card">
            <div class="metric-card-label">Attention / Deviations</div>
            <div class="metric-card-value" style="color:{'#DC2626' if attention_count > 0 else '#059669'};">{attention_count}</div>
        </div>
        <div class="metric-card">
            <div class="metric-card-label">AI Rules Fired</div>
            <div class="metric-card-value" style="color:var(--primary-blue);">{rules_fired_count}</div>
        </div>
        <div class="metric-card">
            <div class="metric-card-label">Inference Latency</div>
            <div class="metric-card-value" style="font-size:20px; color:#0D9488; margin-top:3px;">{exec_latency_ms:.2f} ms</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Validation Warnings / Limitations Alert
    if ai_data and ai_data.get("validation_warnings"):
        for warn in ai_data["validation_warnings"]:
            st.warning(f"⚠️ **Validation Limitation:** {warn}")
    if ai_data and ai_data.get("validation_errors"):
        for err in ai_data["validation_errors"]:
            st.error(f"🛑 **Validation Error:** {err}")

    # ---------------------------------------------------------
    # MAIN TABBED CONTENT
    # ---------------------------------------------------------
    tab_ai, tab_params, tab_nlp, tab_research = st.tabs([
        "🧠 AI-Based CBC Interpretation",
        "📋 Parameter Overview & Ranges",
        "🔍 NLP Analysis & Explanations",
        "📑 Research Architecture & Benchmarks"
    ])

    # ---------------------------------------------------------
    # TAB 1: AI-BASED CBC INTERPRETATION (EXPERT SYSTEM)
    # ---------------------------------------------------------
    with tab_ai:
        st.markdown("<h3 style='color:#0F2942; font-size:18px; margin-top:0;'>AI-Based CBC Interpretation</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:13px; color:#64748B;'>Deductions generated by the rule-based expert system "
            "using Forward Chaining data-driven reasoning over validated CBC observations.</p>",
            unsafe_allow_html=True
        )

        trace = ai_data["reasoning_trace"] if ai_data else []
        if trace:
            # Highlight Multi-Parameter Syndromic Patterns First
            syndrome_steps = [s for s in trace if s.rule_category in ["hematology_pattern", "differential"]]
            primary_steps = [s for s in trace if s.rule_category not in ["hematology_pattern", "differential"]]

            if syndrome_steps:
                st.markdown("<h4 style='font-size:15px; font-weight:600; color:#1E3A8A; margin-bottom:10px;'>🧬 Inferred Multi-Parameter Hematological Patterns</h4>", unsafe_allow_html=True)
                for step in syndrome_steps:
                    st.markdown(f"""
                    <div class="trace-card" style="border-left-color: #0D9488; background-color: #F8FAFC;">
                        <div class="trace-header">
                            <span class="trace-title" style="color:#0F2942;">🎯 {step.inferred_fact.value}</span>
                            <span class="trace-rule-id">{step.rule_id}</span>
                        </div>
                        <div class="trace-body">
                            <strong>Matched Premises:</strong> {', '.join(f"<code>{f.subject}={f.value}</code>" for f in step.matched_facts)}<br>
                            <p style="margin: 8px 0 0 0;">{step.educational_explanation}</p>
                        </div>
                        <div class="trace-meta">
                            <strong>Source Reference:</strong> {step.reference_source}<br>
                            <strong>Academic Limitation:</strong> {step.limitations}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Chronological Forward Chaining Trace
            st.markdown("<h4 style='font-size:15px; font-weight:600; color:#0F2942; margin-top:1.5rem; margin-bottom:10px;'>📜 Complete Forward Chaining Reasoning Trace</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:12px; color:#64748B;'>Chronological execution log detailing rule activation, antecedent evaluation, and consequence assertion.</p>", unsafe_allow_html=True)

            for step in trace:
                st.markdown(f"""
                <div class="trace-card">
                    <div class="trace-header">
                        <span class="trace-title">Step #{step.step_number}: {step.rule_name}</span>
                        <span class="trace-rule-id">{step.rule_id}</span>
                    </div>
                    <div class="trace-body">
                        <div><strong>Condition Matched:</strong> {', '.join(f"<code>{f.subject} {f.predicate} {f.value}</code>" for f in step.matched_facts)}</div>
                        <div><strong>Consequent Inferred:</strong> <em>{step.inferred_fact.subject}</em> &rarr; <strong>{step.inferred_fact.value}</strong></div>
                        <p style="margin: 6px 0 0 0;">{step.educational_explanation}</p>
                    </div>
                    <div class="trace-meta">
                        <strong>Literature Reference:</strong> {step.reference_source}<br>
                        <strong>Scope Limitations:</strong> {step.limitations}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Working Memory Inspector (Viva feature)
            with st.expander("🔬 Inspect Expert System Working Memory State"):
                st.markdown("<p style='font-size:12px; color:#64748B;'>Complete state of Working Memory propositions at quiescence (initial asserted facts + derived conclusions):</p>", unsafe_allow_html=True)
                wm_data = []
                for f in ai_data["inference_result"].working_memory:
                    wm_data.append({
                        "Fact ID": f.fact_id,
                        "Category": f.category,
                        "Subject": f.subject,
                        "Predicate": f.predicate,
                        "Value": str(f.value),
                        "Source": f.source
                    })
                st.dataframe(pd.DataFrame(wm_data), use_container_width=True, hide_index=True)
        else:
            st.info("No inference rules fired. Parameters may be unassessed or outside the scope of current rules.")


    # ---------------------------------------------------------
    # TAB 2: PARAMETER OVERVIEW & REFERENCE RANGES
    # ---------------------------------------------------------
    with tab_params:
        st.markdown("<h3 style='color:#0F2942; font-size:18px; margin-top:0;'>CBC Parameter Reference Intervals</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#64748B;'>Observed numerical values positioned along laboratory reference boundaries.</p>", unsafe_allow_html=True)

        if df is not None and not df.empty:
            for idx, row in df.iterrows():
                param = row.get("Parameter", "Unknown")
                val = row.get("Value", "")
                unit = row.get("Unit", "")
                ref_range = row.get("Reference Range", "")
                status = row.get("Status", "Unknown")
                pct = calc_marker_position(val, ref_range)

                st.markdown(f"""
                <div class="med-card" style="padding: 1.1rem 1.25rem; margin-bottom: 0.85rem;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-weight:700; font-size:16px; color:#0F2942;">{param}</span>
                            <span style="font-size:13px; color:#64748B; margin-left:8px;">{row.get('Meaning', '')}</span>
                        </div>
                        <div style="display:flex; align-items:center; gap:12px;">
                            <span style="font-size:16px; font-weight:700; color:#0F2942;">{val} <span style="font-size:12px; font-weight:400; color:#64748B;">{unit}</span></span>
                            <span class="badge badge-{status}">{status}</span>
                        </div>
                    </div>
                    <div class="ref-bar-wrap">
                        <div class="ref-bar-labels">
                            <span>Low Zone (&lt; normal)</span>
                            <span style="color:#059669; font-weight:600;">Reference: {ref_range} {unit}</span>
                            <span>High Zone (&gt; normal)</span>
                        </div>
                        <div class="ref-bar-track">
                            <div class="ref-bar-marker" style="left: {pct}%;"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("📊 View Compact Numerical Data Table"):
                display_cols = ['Parameter', 'Value', 'Unit', 'Reference Range', 'Status']
                st.dataframe(df[display_cols], use_container_width=True, hide_index=True)


    # ---------------------------------------------------------
    # TAB 3: NLP ANALYSIS & RETRIEVED EXPLANATIONS
    # ---------------------------------------------------------
    with tab_nlp:
        st.markdown("<h3 style='color:#0F2942; font-size:18px; margin-top:0;'>Natural Language Processing & Retrieval Engine</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#64748B;'>Preserved NLP pipeline showcasing entity extraction, medical dictionary retrieval, and rule suggestions.</p>", unsafe_allow_html=True)

        nlp_col1, nlp_col2 = st.columns([1, 1])

        with nlp_col1:
            st.markdown('<div class="med-card">', unsafe_allow_html=True)
            st.markdown("<h4 style='font-size:14px; font-weight:600; color:#0F2942; margin-top:0;'>🏷️ spaCy Named Entity Recognition</h4>", unsafe_allow_html=True)
            entities = ai_data.get("nlp_entities", []) if ai_data else []
            if entities:
                ent_df = pd.DataFrame(entities)
                st.dataframe(ent_df, use_container_width=True, hide_index=True)
            else:
                st.info("No standard linguistic entities detected by general model in the current raw snippet.")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="med-card">', unsafe_allow_html=True)
            st.markdown("<h4 style='font-size:14px; font-weight:600; color:#0F2942; margin-top:0;'>📊 Status Distribution</h4>", unsafe_allow_html=True)
            if df is not None and not df.empty:
                low_c = len(df[df['Status'].str.lower() == 'low'])
                norm_c = len(df[df['Status'].str.lower() == 'normal'])
                high_c = len(df[df['Status'].str.lower() == 'high'])

                l_pct = (low_c / total_params * 100) if total_params > 0 else 0
                n_pct = (norm_c / total_params * 100) if total_params > 0 else 0
                h_pct = (high_c / total_params * 100) if total_params > 0 else 0

                st.markdown(f"""
                <div class="dist-bar-wrap">
                    <div style="width: {l_pct}%; background-color: #DC2626;" title="Low: {low_c}"></div>
                    <div style="width: {n_pct}%; background-color: #059669;" title="Normal: {norm_c}"></div>
                    <div style="width: {h_pct}%; background-color: #D97706;" title="High: {high_c}"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:12px; color:#475569;">
                    <span><strong style="color:#DC2626;">{low_c}</strong> Below</span>
                    <span><strong style="color:#059669;">{norm_c}</strong> Normal</span>
                    <span><strong style="color:#D97706;">{high_c}</strong> Above</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with nlp_col2:
            st.markdown('<div class="med-card">', unsafe_allow_html=True)
            st.markdown("<h4 style='font-size:14px; font-weight:600; color:#0F2942; margin-top:0;'>📝 Overall CBC Summary</h4>", unsafe_allow_html=True)
            st.write(report_info.get("Overall CBC Summary", "No overall summary available."))
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="med-card">', unsafe_allow_html=True)
            st.markdown("<h4 style='font-size:14px; font-weight:600; color:#0F2942; margin-top:0;'>💡 Educational Suggestions</h4>", unsafe_allow_html=True)
            if df is not None and not df.empty:
                unique_sugs = df['Suggestions'].dropna().unique().tolist()
                for s in unique_sugs:
                    st.markdown(f"• {s}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<h4 style='font-size:15px; font-weight:600; color:#0F2942; margin-top:1rem;'>📖 Parameter Meanings & Explanations</h4>", unsafe_allow_html=True)
        if df is not None and not df.empty:
            for _, r in df.iterrows():
                with st.expander(f"{r.get('Parameter')} — {r.get('Meaning')}"):
                    st.markdown(f"**Simple Explanation:** {r.get('Simple Explanation')}")
                    st.markdown(f"**Interpretation:** {r.get('Interpretation')}")
                    st.markdown(f"**Suggestions:** {r.get('Suggestions')}")


    # ---------------------------------------------------------
    # TAB 4: RESEARCH ARCHITECTURE & BENCHMARK SUITE
    # ---------------------------------------------------------
    with tab_research:
        st.markdown("<h3 style='color:#0F2942; font-size:18px; margin-top:0;'>AI Research Paper & Syllabus Specification</h3>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:13px; color:#64748B;'>Theoretical grounding, algorithmic specification, and "
            "empirical evaluation metrics supporting college viva defense and publication.</p>",
            unsafe_allow_html=True
        )

        col_arch1, col_arch2 = st.columns([1, 1])

        with col_arch1:
            st.markdown("""
            <div class="med-card">
                <h4 style="font-size:14px; font-weight:700; color:#0F2942; margin-top:0;">🎓 Syllabus Topic Mapping</h4>
                <table style="width:100%; font-size:12px; border-collapse:collapse;">
                    <tr style="border-bottom:1px solid #E2E8F0;">
                        <th style="text-align:left; padding:6px;">Topic</th>
                        <th style="text-align:left; padding:6px;">Implementation in MedExplain AI</th>
                    </tr>
                    <tr style="border-bottom:1px solid #E2E8F0;">
                        <td style="padding:6px; font-weight:600;">Intelligent Agents</td>
                        <td style="padding:6px;">Goal-driven perception (Sensors &rarr; NLP), reasoning (KB), and action (Explanations).</td>
                    </tr>
                    <tr style="border-bottom:1px solid #E2E8F0;">
                        <td style="padding:6px; font-weight:600;">Knowledge Representation</td>
                        <td style="padding:6px;">Declarative Horn clauses (IF Premises THEN Consequent) with medical metadata.</td>
                    </tr>
                    <tr style="border-bottom:1px solid #E2E8F0;">
                        <td style="padding:6px; font-weight:600;">Forward Chaining</td>
                        <td style="padding:6px;">Data-driven Match-Resolve-Act cycle from observed facts to hematological patterns.</td>
                    </tr>
                    <tr style="border-bottom:1px solid #E2E8F0;">
                        <td style="padding:6px; font-weight:600;">Conflict Resolution</td>
                        <td style="padding:6px;">Salience priority and specificity matching (multi-parameter patterns preferred over single).</td>
                    </tr>
                    <tr>
                        <td style="padding:6px; font-weight:600;">Cycle Prevention</td>
                        <td style="padding:6px;">Strict proposition indexing and rule firing history to prevent infinite loops.</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

        with col_arch2:
            st.markdown("""
            <div class="med-card">
                <h4 style="font-size:14px; font-weight:700; color:#0F2942; margin-top:0;">⚙️ Forward Chaining Algorithm Pseudocode</h4>
                <pre style="background:#F1F5F9; padding:10px; border-radius:6px; font-size:11px; line-height:1.45; overflow-x:auto;">
Algorithm FORWARD-CHAINING-ENGINE(Facts, Rules, MaxIter):
  WorkingMemory &larr; copy(Facts)
  FiredRules &larr; empty_set()
  Trace &larr; empty_list()
  
  Loop step = 1 to MaxIter:
    Agenda &larr; []
    For each Rule in Rules:
      If Rule.id not in FiredRules:
        matched &larr; Rule.match(WorkingMemory)
        If matched &ne; null:
          Agenda.append((Rule, matched))
          
    If Agenda is empty:
      Break (Quiescence reached)
      
    # Conflict Resolution
    sort(Agenda, key=&lambda; r: (r.salience, len(r.conditions)), desc)
    selected_rule, matched_facts &larr; Agenda[0]
    
    # Act / Fire Phase
    new_fact &larr; Fact(selected_rule.consequent)
    WorkingMemory.assert(new_fact)
    FiredRules.add(selected_rule.id)
    Trace.record(selected_rule, matched_facts, new_fact)
    
  Return WorkingMemory, Trace, Quiescence
                </pre>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<h4 style='font-size:15px; font-weight:600; color:#0F2942; margin-top:1rem;'>🧪 Live Benchmark Evaluation Results</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:12px; color:#64748B;'>Automated evaluation executed over synthetic clinical test cases:</p>", unsafe_allow_html=True)

        if st.button("▶️ Execute Benchmark Suite Now"):
            with st.spinner("Running benchmark cases..."):
                report = run_benchmark_evaluation()
                bench_df = pd.DataFrame(report["case_results"])
                st.success(
                    f"Benchmark Completed: {report['total_cases']} cases evaluated. "
                    f"Overall Rule Recall: {report['overall_rule_recall_pct']}%. "
                    f"Mean Latency: {report['mean_latency_ms']} ms."
                )
                st.dataframe(bench_df, use_container_width=True, hide_index=True)


    # ---------------------------------------------------------
    # MEDICAL & ACADEMIC DISCLAIMER FOOTER
    # ---------------------------------------------------------
    st.markdown("""
    <div class="med-disclaimer">
        <strong>Academic & Educational Prototype Disclaimer:</strong><br>
        MedExplain AI is developed strictly for educational research and computer science academic submission. 
        It provides educational insights using rule-based reasoning and NLP information extraction. 
        It does not constitute medical diagnosis, clinical judgment, or medical advice. 
        Clinical interpretations must be performed by qualified medical professionals considering full history and symptoms.
    </div>
    """, unsafe_allow_html=True)
