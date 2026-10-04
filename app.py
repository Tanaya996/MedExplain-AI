import streamlit as st
import pandas as pd
import re
import os

# ---------------------------------------------------------
# IMPORT BACKEND PIPELINE
# ---------------------------------------------------------
# The application requires the backend pipeline to function.
# Ensure your backend script is named 'backend.py' or update this import.
try:
    # Try importing from a backend script
    from backend import process_cbc_report
except ImportError:
    try:
        # If the user exported the notebook as CBC_NLP.py
        from CBC_NLP import process_cbc_report
    except ImportError:
        st.error("Backend module not found. Please ensure your backend script (e.g., backend.py or CBC_NLP.py) containing 'process_cbc_report' is in the same directory as this app.")
        st.stop()


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="MedExplain AI",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# CSS STYLING (No external visualization dependencies)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-color: #F7F9FB;
        --primary-color: #123B5D;
        --accent-color: #287C8E;
        --normal-color: #2E7D5B;
        --attention-color: #C58A22;
        --abnormal-color: #C84B4B;
        --text-primary: #1F2933;
        --text-secondary: #667085;
        --border-color: #E3E8EE;
        --white: #FFFFFF;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: var(--text-primary);
    }
    
    .stApp { background-color: var(--bg-color); }
    
    /* Header Container */
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 1.5rem 2rem; border-bottom: 1px solid var(--border-color);
        margin-bottom: 2rem; background-color: var(--white);
        margin-top: -4rem; box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .logo-section { display: flex; align-items: center; gap: 0.75rem; }
    .logo-text { font-size: 24px; font-weight: 700; color: var(--primary-color); margin: 0; line-height: 1.2; }
    .logo-subtitle { font-size: 13px; font-weight: 500; color: var(--text-secondary); margin: 0; }
    .nav-links { display: flex; gap: 1.5rem; font-size: 14px; font-weight: 500; color: var(--text-secondary); }
    .nav-links span { text-decoration: none; color: inherit; cursor: pointer; transition: color 0.2s ease; }
    .nav-links span:hover { color: var(--primary-color); }
    
    /* Content Cards */
    .content-card {
        background-color: var(--white); border: 1px solid var(--border-color);
        border-radius: 8px; padding: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02); margin-bottom: 1.5rem;
    }
    
    /* Summary Metrics */
    .summary-card {
        text-align: center; padding: 1.25rem 1rem; background: var(--white);
        border: 1px solid var(--border-color); border-radius: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .summary-card h4 { font-size: 13px; color: var(--text-secondary); margin: 0 0 0.5rem 0; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;}
    .summary-card .value { font-size: 28px; font-weight: 600; color: var(--primary-color); margin: 0; }
    
    /* Typography Overrides */
    h1, h2, h3 { color: var(--primary-color) !important; font-weight: 600 !important; }
    h1 { font-size: 24px !important; margin-bottom: 0.5rem !important; }
    h2 { font-size: 20px !important; margin-top: 1rem !important; margin-bottom: 1rem !important; }
    h3 { font-size: 16px !important; margin-bottom: 0.75rem !important; }
    p { color: var(--text-primary); font-size: 15px; line-height: 1.6; margin-bottom: 1rem; }
    
    /* Status Labels */
    .status-badge {
        display: inline-flex; align-items: center; gap: 0.35rem; font-size: 13px; font-weight: 600;
        padding: 0.25rem 0.75rem; border-radius: 12px; border: 1px solid var(--border-color);
    }
    .status-Normal { color: var(--normal-color); border-color: #E2EFE9; background-color: #F2F9F5; }
    .status-Low, .status-High, .status-Abnormal { color: var(--abnormal-color); border-color: #FDECEC; background-color: #FFF5F5; }
    .status-Review, .status-Attention { color: var(--attention-color); border-color: #FDF4E7; background-color: #FFFBF4; }
    
    /* Reference Range Indicator */
    .ref-container {
        width: 100%; margin-top: 8px; margin-bottom: 16px; position: relative;
    }
    .ref-labels {
        display: flex; justify-content: space-between; font-size: 12px; color: var(--text-secondary); margin-bottom: 4px;
    }
    .ref-bar {
        width: 100%; height: 8px; border-radius: 4px; position: relative;
        background: linear-gradient(90deg, #FDECEC 0%, #FDECEC 25%, #E2EFE9 25%, #E2EFE9 75%, #FDECEC 75%, #FDECEC 100%);
    }
    .ref-marker {
        position: absolute; top: -6px; width: 4px; height: 20px;
        background-color: var(--primary-color); border-radius: 2px;
        transform: translateX(-50%); box-shadow: 0 0 2px rgba(0,0,0,0.3);
    }
    
    /* Related Findings Card */
    .insight-card {
        background-color: #FFFBF4; border: 1px solid #FDF4E7;
        border-left: 4px solid var(--attention-color); padding: 1.25rem;
        border-radius: 4px; margin-bottom: 1rem;
    }
    .insight-title {
        font-size: 13px; font-weight: 700; text-transform: uppercase;
        color: var(--attention-color); margin-bottom: 0.5rem; letter-spacing: 0.5px;
    }
    
    /* Distribution Bar */
    .dist-bar-container {
        display: flex; width: 100%; height: 12px; border-radius: 6px; overflow: hidden; margin-top: 10px; margin-bottom: 10px;
    }
    
    /* General Utilities */
    .small-text { font-size: 13px; color: var(--text-secondary); }
    
    .disclaimer {
        background-color: var(--white); border: 1px solid var(--border-color);
        padding: 1.25rem; margin-top: 3rem; font-size: 13px;
        color: var(--text-secondary); border-radius: 8px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------------------------
def calc_marker_position(val, range_str):
    """Calculates the percentage position for the CSS reference range bar."""
    try:
        if not range_str or not isinstance(range_str, str): return 50
        # Extract numbers like "12.0 - 16.0"
        nums = [float(x) for x in re.findall(r"[\d\.]+", range_str.replace(',', '.'))]
        if len(nums) == 2:
            r_min, r_max = nums[0], nums[1]
            val = float(val)
            
            span = r_max - r_min
            if span == 0: return 50
            
            if val < r_min:
                lower_bound = max(0, r_min - span)
                if val <= lower_bound: return 5
                return 25 * ((val - lower_bound) / (r_min - lower_bound))
            elif val > r_max:
                upper_bound = r_max + span
                if val >= upper_bound: return 95
                return 75 + 25 * ((val - r_max) / (upper_bound - r_max))
            else:
                return 25 + 50 * ((val - r_min) / span)
    except Exception:
        pass
    return 50

# ---------------------------------------------------------
# HEADER NAVIGATION
# ---------------------------------------------------------
st.markdown("""
<div class="header-container">
    <div class="logo-section">
        <span style="font-size: 28px; color: #287C8E;">⚕️</span>
        <div>
            <h1 class="logo-text">MedExplain AI</h1>
            <p class="logo-subtitle">Intelligent CBC Medical Report Understanding</p>
            <p class="small-text" style="margin:0;">Transforming CBC values into simple, structured and understandable insights.</p>
        </div>
    </div>
    <div class="nav-links">
        <span>Analyze Report</span>
        <span>Results</span>
        <span>About</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# STATE MANAGEMENT
# ---------------------------------------------------------
if 'report_processed' not in st.session_state:
    st.session_state.report_processed = False
if 'structured_df' not in st.session_state:
    st.session_state.structured_df = None
if 'final_report' not in st.session_state:
    st.session_state.final_report = None

# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------
if not st.session_state.report_processed:
    st.markdown('<div class="content-card" style="max-width: 800px; margin: 0 auto;">', unsafe_allow_html=True)
    st.markdown("<h2>Analyze CBC Report</h2>", unsafe_allow_html=True)
    
    upload_method = st.radio("Input Method", ["Paste text", "Upload file (.txt)"], horizontal=True, label_visibility="collapsed")
    
    report_text = ""
    if upload_method == "Upload file (.txt)":
        uploaded_file = st.file_uploader("Upload your CBC report (.txt only)", type=["txt"])
        if uploaded_file:
            report_text = str(uploaded_file.read(), "utf-8")
            st.success("Report loaded successfully.")
    else:
        report_text = st.text_area("Paste CBC report text here:", height=200, placeholder="E.g., HGB 14.2 g/dL\nMCV 82 fL...")
        
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Analyze Report", type="primary", use_container_width=True):
            if report_text and report_text.strip():
                with st.spinner("Processing report with MedExplain AI..."):
                    try:
                        structured_df, final_report = process_cbc_report(report_text, "CBC_AUTO_ID")
                        
                        if structured_df.empty:
                            st.error("No supported CBC parameters were detected. Please check the report format and try again.")
                        else:
                            st.session_state.structured_df = structured_df
                            st.session_state.final_report = final_report
                            st.session_state.report_processed = True
                            st.rerun()
                    except Exception as e:
                        import traceback
                        st.error(f"An error occurred during report processing: {e}")
                        st.error(traceback.format_exc())
            else:
                st.warning("Please provide a CBC report to analyze.")
    with col2:
        if st.button("Clear / Reset", use_container_width=True):
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # EMPTY STATE
    st.markdown("""
    <div style="text-align: center; margin-top: 4rem; color: var(--text-secondary); max-width: 600px; margin-left: auto; margin-right: auto;">
        <h3 style="color: var(--text-secondary) !important;">Upload or paste a CBC report to begin analysis.</h3>
        <p>MedExplain AI extracts supported CBC parameters, compares them with supplied reference ranges, and presents simple explanations.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# DASHBOARD RESULTS
# ---------------------------------------------------------
else:
    df = st.session_state.structured_df
    report_info = st.session_state.final_report
    
    # Pre-calculate counts
    total_params = len(df)
    normal_count = len(df[df['Status'].str.lower() == 'normal'])
    review_count = total_params - normal_count
    
    # Top Actions
    col_t, col_a = st.columns([4, 1])
    with col_t:
        st.markdown("<h1>CBC Analysis Results</h1>", unsafe_allow_html=True)
    with col_a:
        if st.button("Clear / Reset", use_container_width=True):
            st.session_state.report_processed = False
            st.session_state.structured_df = None
            st.session_state.final_report = None
            st.rerun()
            
    # SECTION A: OVERVIEW CARDS
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="summary-card"><h4>Report ID</h4><p class="value" style="font-size:18px; color:var(--text-secondary); margin-top:8px;">{report_info.get("Report ID", "N/A")}</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="summary-card"><h4>Parameters Analyzed</h4><p class="value">{total_params}</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="summary-card"><h4>Normal</h4><p class="value" style="color:var(--normal-color);">{normal_count}</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="summary-card"><h4>Needs Review</h4><p class="value" style="color:var(--abnormal-color);">{review_count}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    main_col, side_col = st.columns([7, 4])
    
    with main_col:
        # SECTION B: CBC STATUS OVERVIEW
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<h2>CBC Parameter Overview</h2>", unsafe_allow_html=True)
        
        for idx, row in df.iterrows():
            param_abbr = row.get("Parameter", "Unknown")
            val = row.get("Value", "")
            unit = row.get("Unit", "")
            ref_range = row.get("Reference Range", "")
            status = row.get("Status", "Unknown")
            
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border-color); padding: 12px 0;">
                <div>
                    <div style="font-weight:600; color:var(--primary-color); font-size:15px;">{param_abbr}</div>
                    <div class="small-text">Reference range: {ref_range} {unit}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:15px; font-weight:600; margin-bottom:4px;">{val} <span style="font-weight:400; color:var(--text-secondary); font-size:13px;">{unit}</span></div>
                    <span class="status-badge status-{status}">{status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SECTION C: REFERENCE RANGE VISUALIZATION
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<h2>Where Your Results Fall</h2>", unsafe_allow_html=True)
        st.markdown("<p class='small-text'>Visual representation of your results relative to the normal reference interval.</p>", unsafe_allow_html=True)
        
        for idx, row in df.iterrows():
            pct = calc_marker_position(row.get("Value", 0), row.get("Reference Range", ""))
            
            st.markdown(f"""
            <div style="margin-bottom: 24px;">
                <div style="display:flex; justify-content:space-between; margin-bottom: 6px;">
                    <strong style="color:var(--primary-color); font-size:14px;">{row.get("Parameter")}</strong>
                    <span style="font-size:14px; font-weight:500;">{row.get("Value")}</span>
                </div>
                <div class="ref-container">
                    <div class="ref-labels">
                        <span style="width:25%; text-align:left;">Low Zone</span>
                        <span style="width:50%; text-align:center; color:var(--normal-color); font-weight:500;">Normal Reference Range</span>
                        <span style="width:25%; text-align:right;">High Zone</span>
                    </div>
                    <div class="ref-bar">
                        <div class="ref-marker" style="left: {pct}%;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SECTION 7: PARAMETER INSIGHTS
        st.markdown("<h2>Understand Your Results</h2>", unsafe_allow_html=True)
        for idx, row in df.iterrows():
            status = row.get("Status", "Unknown")
            status_indicator = "🟢" if status.lower() == "normal" else "🔴" if status.lower() in ["low", "high"] else "🟡"
            expander_title = f"{status_indicator} {row.get('Parameter')} &nbsp;&nbsp;|&nbsp;&nbsp; {row.get('Value')} {row.get('Unit')} &nbsp;&nbsp;|&nbsp;&nbsp; {status}"
            
            with st.expander(expander_title):
                st.markdown(f"**Meaning:** {row.get('Meaning', 'N/A')}")
                st.markdown(f"**Simple Explanation:** {row.get('Simple Explanation', 'N/A')}")
                st.markdown(f"**Interpretation:** {row.get('Interpretation', 'N/A')}")
                st.markdown(f"**Reference Range:** {row.get('Reference Range', '')} {row.get('Unit', '')}")
                st.markdown(f"**Suggestions:** {row.get('Suggestions', 'Discuss with a healthcare professional.')}")

    with side_col:
        # SECTION D: STATUS DISTRIBUTION
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<h3>Status Distribution</h3>", unsafe_allow_html=True)
        
        low_count = len(df[df['Status'].str.lower() == 'low'])
        high_count = len(df[df['Status'].str.lower() == 'high'])
        
        norm_pct = (normal_count / total_params * 100) if total_params > 0 else 0
        low_pct = (low_count / total_params * 100) if total_params > 0 else 0
        high_pct = (high_count / total_params * 100) if total_params > 0 else 0
        
        st.markdown(f"""
        <div class="dist-bar-container">
            <div style="width: {low_pct}%; background-color: var(--abnormal-color);" title="Low: {low_count}"></div>
            <div style="width: {norm_pct}%; background-color: var(--normal-color);" title="Normal: {normal_count}"></div>
            <div style="width: {high_pct}%; background-color: var(--attention-color);" title="High: {high_count}"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:13px; margin-top:8px;">
            <span><span style="color:var(--abnormal-color); font-weight:bold;">{low_count}</span> Low</span>
            <span><span style="color:var(--normal-color); font-weight:bold;">{normal_count}</span> Normal</span>
            <span><span style="color:var(--attention-color); font-weight:bold;">{high_count}</span> High</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # SECTION 8: RELATED FINDINGS
        st.markdown("<h3>Related Findings</h3>", unsafe_allow_html=True)
        rf_text = report_info.get("Related Findings", "")
        if rf_text and rf_text.strip():
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">Identified Pattern</div>
                <div style="font-size:14px; line-height:1.5;">{rf_text.replace(chr(10), '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="content-card" style="background-color:#F8F9FA;">
                <p class="small-text" style="margin:0;">No significant parameter relationship was identified from the available CBC parameters.</p>
            </div>
            """, unsafe_allow_html=True)
            
        # SECTION 9: OVERALL SUMMARY
        st.markdown("<h3>Overall CBC Summary</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="content-card" style="background-color:#F4F8FA; border-color:#D3E6ED;">
            <p style="font-size:14px; margin:0; line-height:1.6;">{report_info.get("Overall CBC Summary", "Summary not available.")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # SECTION 10: GENERAL SUGGESTIONS
        st.markdown("<h3>General Suggestions</h3>", unsafe_allow_html=True)
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        # Aggregate unique suggestions from the structured_df
        unique_suggestions = df['Suggestions'].dropna().unique().tolist()
        
        if unique_suggestions:
            sug_html = "<ul style='padding-left: 20px; font-size: 14px; margin:0;'>"
            for sug in unique_suggestions:
                if sug and isinstance(sug, str):
                    sug_html += f"<li style='margin-bottom: 8px;'>{sug}</li>"
            sug_html += "</ul>"
            st.markdown(sug_html, unsafe_allow_html=True)
        else:
            st.markdown("<p class='small-text'>Discuss your results with a qualified healthcare professional.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # SECTION 11: OPTIONAL DETAILED RESULTS (The Table)
    st.markdown("---")
    with st.expander("View Detailed Numerical Results"):
        st.markdown("<p class='small-text'>Compact view of all extracted parameters and their values.</p>", unsafe_allow_html=True)
        
        # Display as a lightweight static dataframe to avoid large heavy tables
        display_df = df[['Parameter', 'Value', 'Unit', 'Reference Range', 'Status']].copy()
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
    # SECTION 12: ABOUT SECTION
    st.markdown("---")
    st.markdown("<h3>About MedExplain AI</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p class="small-text">
    MedExplain AI is an educational project that extracts supported CBC parameters from report text, 
    compares results with supplied reference ranges, and retrieves explanations from a structured knowledge base 
    to produce understandable summaries.
    </p>
    """, unsafe_allow_html=True)

    # SECTION 13: MEDICAL DISCLAIMER
    st.markdown("""
    <div class="disclaimer">
        MedExplain AI is an educational and informational tool. It does not provide a medical diagnosis or replace professional medical advice. CBC results should be interpreted by a qualified healthcare professional in the context of symptoms, medical history, and other investigations.
    </div>
    """, unsafe_allow_html=True)
