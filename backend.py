suggestion_knowledge_base = {

    "HGB": {
        "Low": (
            "Maintain a balanced diet containing iron-rich foods such as "
            "leafy green vegetables, beans and fortified foods. Include "
            "vitamin C-rich foods to support iron absorption. If the low "
            "level persists, discuss it with a healthcare professional."
        ),
        "Normal": (
            "Maintain a balanced diet containing adequate iron, folate "
            "and vitamin B12, and continue routine health monitoring."
        ),
        "High": (
            "Maintain good hydration and a balanced lifestyle. If the "
            "elevated level persists, discuss the result with a healthcare professional."
        )
    },

    "HCT": {
        "Low": (
            "Maintain a balanced diet and adequate nutritional intake. "
            "If the value remains low, discuss the result with a healthcare professional."
        ),
        "Normal": (
            "Maintain a balanced diet, adequate hydration and regular health monitoring."
        ),
        "High": (
            "Maintain adequate hydration and discuss a persistently high "
            "value with a healthcare professional."
        )
    },

    "PLT": {
        "Low": (
            "Avoid self-medication and discuss a persistently low platelet "
            "count with a healthcare professional. Follow medical advice "
            "regarding medications and activities."
        ),
        "Normal": (
            "Maintain balanced nutrition and continue routine health monitoring."
        ),
        "High": (
            "Maintain a balanced lifestyle and discuss a persistently high "
            "platelet count with a healthcare professional."
        )
    },

    "MCV": {
        "Low": (
            "Maintain a balanced diet containing iron, folate and vitamin B12. "
            "If the value remains low, discuss possible nutritional causes "
            "with a healthcare professional."
        ),
        "Normal": (
            "Maintain a balanced diet and continue routine health monitoring."
        ),
        "High": (
            "Maintain a balanced diet containing adequate vitamin B12 and folate. "
            "If the value remains high, discuss the result with a healthcare professional."
        )
    },

    "MCHC": {
        "Low": (
            "Maintain a balanced diet with adequate iron and other essential "
            "nutrients. If the value remains low, discuss the result with "
            "a healthcare professional."
        ),
        "Normal": (
            "Maintain balanced nutrition and continue routine health monitoring."
        ),
        "High": (
            "Maintain a balanced diet and discuss a persistently elevated "
            "value with a healthcare professional."
        )
    },

    "MCH": {
        "Low": (
            "Maintain a balanced diet containing adequate iron and other "
            "essential nutrients. Persistent abnormalities should be discussed "
            "with a healthcare professional."
        ),
        "Normal": (
            "Maintain balanced nutrition and continue routine health monitoring."
        ),
        "High": (
            "Maintain a balanced diet containing adequate vitamin B12 and folate. "
            "Discuss persistent abnormalities with a healthcare professional."
        )
    },

    "RDW": {
        "Low": (
            "A slightly low RDW generally does not require a specific dietary "
            "measure by itself. Maintain a balanced diet and discuss persistent "
            "abnormalities with a healthcare professional."
        ),
        "Normal": (
            "Maintain a balanced diet and continue routine health monitoring."
        ),
        "High": (
            "Maintain a balanced diet containing iron, folate and vitamin B12. "
            "If the value remains elevated, discuss the result with a healthcare professional."
        )
    },

    "NE%": {
        "Low": (
            "Maintain a balanced diet and good general health practices. "
            "If the value remains low or symptoms are present, discuss the "
            "result with a healthcare professional."
        ),
        "Normal": (
            "Maintain a balanced diet and continue routine health monitoring."
        ),
        "High": (
            "Interpret the result together with the rest of the CBC and clinical "
            "context. If the elevation persists or symptoms are present, discuss "
            "the result with a healthcare professional."
        )
    },

    "LY%": {
        "Low": (
            "Maintain a balanced diet and healthy lifestyle. Interpret the result "
            "together with the rest of the CBC. Persistent abnormalities should "
            "be discussed with a healthcare professional."
        ),
        "Normal": (
            "Maintain a balanced diet and continue routine health monitoring."
        ),
        "High": (
            "Maintain a balanced diet and healthy lifestyle. If the elevation "
            "persists or symptoms are present, discuss the result with a "
            "healthcare professional."
        )
    }
}

import spacy
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')
import pandas as pd
cbc_df = pd.read_csv('cbc_medexplain_cleaned.csv')
text = '\nPatient CBC report shows hemoglobin 11.2 g/dL,\nhematocrit 34%, platelet count 150000 per microliter,\nMCV 72 fL, MCH 24 pg, MCHC 31 g/dL,\nRDW 15%, neutrophils 65%, and lymphocytes 28%.\n'
doc = nlp(text)
knowledge_df = pd.read_excel('Medical explanation knowledge base.xlsx')
import pandas as pd
import os
import spacy
nlp = spacy.load('en_core_web_sm')
report_text = cbc_df.loc[0, 'raw_report_text']
doc = nlp(report_text)
cbc_parameters = {'HGB': ['hemoglobin', 'hb', 'hgb'], 'HCT': ['hematocrit', 'hct'], 'PLT': ['platelet', 'platelets', 'plt'], 'MCV': ['mean corpuscular volume', 'mcv'], 'MCHC': ['mean corpuscular hemoglobin concentration', 'mchc'], 'MCH': ['mean corpuscular hemoglobin', 'mch'], 'RDW': ['red cell distribution width', 'rdw'], 'NE%': ['neutrophils', 'neutrophil', 'ne%'], 'LY%': ['lymphocytes', 'lymphocyte', 'ly%']}
report_text = cbc_df.loc[0, 'raw_report_text']
doc = nlp(report_text)
report_lower = report_text.lower()
import re
match = re.search('Hemoglobin:\\s*([\\d.]+)\\s*(g/dL|g/L)', report_text, re.IGNORECASE)
match = re.search('Hemoglobin:\\s*[\\d.]+\\s*(?:g/dL|g/L)\\s*Reference:\\s*([\\d.]+)-([\\d.]+)', report_text, re.IGNORECASE)

def determine_status(value, low, high):
    if value < low:
        return 'Low'
    elif value > high:
        return 'High'
    else:
        return 'Normal'
value = 14.3
low = 12
high = 18
status = determine_status(value, low, high)
parameters = ['HGB', 'HCT', 'PLT', 'MCV', 'MCHC', 'MCH', 'RDW', 'NE%', 'LY%']
import re

def extract_cbc_report(report_text):
    results = {}
    patterns = {
        'HGB': r'(?:Hemoglobin|Hb|HGB).*?([\d.]+)\s*(g/dL|g/L).*?([\d.]+)\s*-\s*([\d.]+)',
        'HCT': r'(?:Hematocrit|HCT|PCV).*?([\d.]+)\s*(%|L/L).*?([\d.]+)\s*-\s*([\d.]+)',
        'PLT': r'(?:Platelet Count|Platelets|Platelet|PLT).*?([\d,]+)\s*(x10\^3/uL|/µL|×10⁹/L).*?([\d,]+)\s*-\s*([\d,]+)',
        'MCV': r'(?:MCV|Mean Corpuscular Volume).*?([\d.]+)\s*(fL).*?([\d.]+)\s*-\s*([\d.]+)',
        'MCHC': r'(?:Mean Corpuscular MCH Concentration|Mean Corpuscular Hemoglobin Concentration|MCHC).*?([\d.]+)\s*(g/dL|g/L).*?([\d.]+)\s*-\s*([\d.]+)',
        'MCH': r'(?:MCH|Mean Corpuscular Hemoglobin).*?([\d.]+)\s*(pg).*?([\d.]+)\s*-\s*([\d.]+)',
        'RDW': r'(?:RDW|Red Cell Distribution Width).*?([\d.]+)\s*(%).*?([\d.]+)\s*-\s*([\d.]+)',
        'NE%': r'(?:Neutrophils|Neutrophil\s*%|Neutrophil|NE%).*?([\d.]+)\s*(%).*?([\d.]+)\s*-\s*([\d.]+)',
        'LY%': r'(?:Lymphocytes|Lymphocyte\s*%|Lymphocyte|LY%).*?([\d.]+)\s*(%).*?([\d.]+)\s*-\s*([\d.]+)'
    }
    for (parameter, pattern) in patterns.items():
        match = re.search(pattern, report_text, re.IGNORECASE)
        if match:
            value = float(match.group(1).replace(',', ''))
            unit = match.group(2)
            low = float(match.group(3).replace(',', ''))
            high = float(match.group(4).replace(',', ''))
            status = 'Low' if value < low else 'High' if value > high else 'Normal'
            results[parameter] = {'value': value, 'unit': unit, 'reference_low': low, 'reference_high': high, 'status': status}
    return results
report = cbc_df.loc[0, 'raw_report_text']
extracted = extract_cbc_report(report)
extracted_df = pd.DataFrame.from_dict(extracted, orient='index')
all_results = []
results_df = pd.DataFrame(all_results)
parameters = ['HGB', 'HCT', 'PLT', 'MCV', 'MCHC', 'MCH', 'RDW', 'NE%', 'LY%']
parameters_to_check = ['HCT', 'NE%', 'LY%']
import re

def extract_cbc_report(report_text):
    results = {}
    patterns = {
        'HGB': r'(?:Hemoglobin|Hb|HGB).*?([\d.]+)\s*(g/dL|g/L).*?([\d.]+)\s*-\s*([\d.]+)',
        'HCT': r'(?:Hematocrit|HCT|PCV).*?([\d.]+)\s*(%|L/L).*?([\d.]+)\s*-\s*([\d.]+)',
        'PLT': r'(?:Platelet Count|Platelets|Platelet|PLT).*?([\d,]+)\s*(x10\^3/uL|/µL|×10⁹/L).*?([\d,]+)\s*-\s*([\d,]+)',
        'MCV': r'(?:MCV|Mean Corpuscular Volume).*?([\d.]+)\s*(fL).*?([\d.]+)\s*-\s*([\d.]+)',
        'MCHC': r'(?:Mean Corpuscular MCH Concentration|Mean Corpuscular Hemoglobin Concentration|MCHC).*?([\d.]+)\s*(g/dL|g/L).*?([\d.]+)\s*-\s*([\d.]+)',
        'MCH': r'(?:MCH|Mean Corpuscular Hemoglobin).*?([\d.]+)\s*(pg).*?([\d.]+)\s*-\s*([\d.]+)',
        'RDW': r'(?:RDW|Red Cell Distribution Width).*?([\d.]+)\s*(%).*?([\d.]+)\s*-\s*([\d.]+)',
        'NE%': r'(?:Neutrophils|Neutrophil\s*%|Neutrophil|NE%).*?([\d.]+)\s*(%).*?([\d.]+)\s*-\s*([\d.]+)',
        'LY%': r'(?:Lymphocytes|Lymphocyte\s*%|Lymphocyte|LY%).*?([\d.]+)\s*(%).*?([\d.]+)\s*-\s*([\d.]+)'
    }
    for (parameter, pattern) in patterns.items():
        match = re.search(pattern, report_text, re.IGNORECASE)
        if match:
            value = float(match.group(1).replace(',', ''))
            unit = match.group(2)
            low = float(match.group(3).replace(',', ''))
            high = float(match.group(4).replace(',', ''))
            status = 'Low' if value < low else 'High' if value > high else 'Normal'
            results[parameter] = {'value': value, 'unit': unit, 'reference_low': low, 'reference_high': high, 'status': status}
    return results
report = cbc_df.loc[cbc_df['report_id'] == 'CBC_002', 'raw_report_text'].iloc[0]
extracted = extract_cbc_report(report)
all_results = []
results_df = pd.DataFrame(all_results)
parameters = ['HGB', 'HCT', 'PLT', 'MCV', 'MCHC', 'MCH', 'RDW', 'NE%', 'LY%']
parameters = ['HGB', 'HCT', 'PLT', 'MCV', 'MCHC', 'MCH', 'RDW', 'NE%', 'LY%']
knowledge_base = {}
knowledge_df = knowledge_df.rename(columns={'parameter': 'Parameter', 'meaning': 'Meaning', 'simple explanation': 'Simple Explanation', 'Units': 'Units', 'Lower range': 'Lower Range'})
knowledge_df['Parameter'] = knowledge_df['Parameter'].astype(str).str.strip().str.rstrip(':').str.strip()
standard_units = {'HGB': 'g/dL', 'HCT': '%', 'PLT': '/µL', 'MCV': 'fL', 'MCHC': 'g/dL', 'MCH': 'pg', 'RDW': '%', 'NE%': '%', 'LY%': '%'}
knowledge_df['Unit'] = knowledge_df['Parameter'].map(standard_units)
range_data = []
range_df = pd.DataFrame(range_data)
knowledge_df = knowledge_df.drop(columns=['Lower Range'], errors='ignore')
# knowledge_df = knowledge_df.merge(range_df, on='Parameter', how='left')
knowledge_base = knowledge_df.set_index('Parameter').to_dict(orient='index')
knowledge_base = knowledge_df.set_index('Parameter').to_dict(orient='index')

def generate_explanation(parameter, result):
    info = knowledge_base.get(parameter)
    if info is None:
        return 'Knowledge not available.'
    return {'Parameter': parameter, 'Value': result['value'], 'Unit': result['unit'], 'Reference Range': f"{result['reference_low']} - {result['reference_high']}", 'Status': result['status'], 'Meaning': info['Meaning'], 'Simple Explanation': info['Simple Explanation']}
sample_report = cbc_df.iloc[0]['raw_report_text']
extracted_results = extract_cbc_report(sample_report)
hgb_result = generate_explanation('HGB', extracted_results['HGB'])
all_explanations = []
explanations_df = pd.DataFrame(all_explanations)
all_report_explanations = []
all_explanations_df = pd.DataFrame(all_report_explanations)
expected_parameters = set(parameters)
missing_results = []
missing_df = pd.DataFrame(missing_results)
# problem_reports = cbc_df[cbc_df['report_id'].isin(missing_df['Report ID'].unique())]
test_text = cbc_df[cbc_df['report_id'] == 'CBC_002']['raw_report_text'].iloc[0]
test_results = extract_cbc_report(test_text)
test_results = extract_cbc_report(test_text)
all_report_explanations = []
all_explanations_df = pd.DataFrame(all_report_explanations)
suggestion_knowledge_base = {'HGB': {'Low': 'Maintain a balanced diet containing iron-rich foods such as leafy green vegetables, beans and fortified foods. Include vitamin C-rich foods to support iron absorption. If the low level persists, discuss it with a healthcare professional.', 'Normal': 'Maintain a balanced diet containing adequate iron, folate and vitamin B12, and continue routine health monitoring.', 'High': 'Maintain good hydration and a balanced lifestyle. If the elevated level persists, discuss the result with a healthcare professional.'}, 'HCT': {'Low': 'Maintain a balanced diet and adequate nutritional intake. If the value remains low, discuss the result with a healthcare professional.', 'Normal': 'Maintain a balanced diet, adequate hydration and regular health monitoring.', 'High': 'Maintain adequate hydration and discuss a persistently high value with a healthcare professional.'}, 'PLT': {'Low': 'Avoid self-medication and discuss a persistently low platelet count with a healthcare professional. Follow medical advice regarding medications and activities.', 'Normal': 'Maintain balanced nutrition and continue routine health monitoring.', 'High': 'Maintain a balanced lifestyle and discuss a persistently high platelet count with a healthcare professional.'}, 'MCV': {'Low': 'Maintain a balanced diet containing iron, folate and vitamin B12. If the value remains low, discuss possible nutritional causes with a healthcare professional.', 'Normal': 'Maintain a balanced diet and continue routine health monitoring.', 'High': 'Maintain a balanced diet containing adequate vitamin B12 and folate. If the value remains high, discuss the result with a healthcare professional.'}, 'MCHC': {'Low': 'Maintain a balanced diet with adequate iron and other essential nutrients. If the value remains low, discuss the result with a healthcare professional.', 'Normal': 'Maintain balanced nutrition and continue routine health monitoring.', 'High': 'Maintain a balanced diet and discuss a persistently elevated value with a healthcare professional.'}, 'MCH': {'Low': 'Maintain a balanced diet containing adequate iron and other essential nutrients. Persistent abnormalities should be discussed with a healthcare professional.', 'Normal': 'Maintain balanced nutrition and continue routine health monitoring.', 'High': 'Maintain a balanced diet containing adequate vitamin B12 and folate. Discuss persistent abnormalities with a healthcare professional.'}, 'RDW': {'Low': 'A slightly low RDW generally does not require a specific dietary measure by itself. Maintain a balanced diet and discuss persistent abnormalities with a healthcare professional.', 'Normal': 'Maintain a balanced diet and continue routine health monitoring.', 'High': 'Maintain a balanced diet containing iron, folate and vitamin B12. If the value remains elevated, discuss the result with a healthcare professional.'}, 'NE%': {'Low': 'Maintain a balanced diet and good general health practices. If the value remains low or symptoms are present, discuss the result with a healthcare professional.', 'Normal': 'Maintain a balanced diet and continue routine health monitoring.', 'High': 'Interpret the result together with the rest of the CBC and clinical context. If the elevation persists or symptoms are present, discuss the result with a healthcare professional.'}, 'LY%': {'Low': 'Maintain a balanced diet and healthy lifestyle. Interpret the result together with the rest of the CBC. Persistent abnormalities should be discussed with a healthcare professional.', 'Normal': 'Maintain a balanced diet and continue routine health monitoring.', 'High': 'Maintain a balanced diet and healthy lifestyle. If the elevation persists or symptoms are present, discuss the result with a healthcare professional.'}}

def generate_structured_interpretation(parameter, result):
    parameter = str(parameter).strip().upper()
    status = str(result['status']).strip().title()
    info = knowledge_base.get(parameter)
    if info is None:
        return {'Parameter': parameter, 'Value': result['value'], 'Unit': result['unit'], 'Reference Range': f"{result['reference_low']} - {result['reference_high']}", 'Status': status, 'Meaning': 'Knowledge not available.', 'Simple Explanation': 'Knowledge not available.', 'Interpretation': 'Knowledge not available.', 'Suggestions': 'Please discuss the result with a healthcare professional.'}
    value = result['value']
    unit = result['unit']
    low = result['reference_low']
    high = result['reference_high']
    meaning = info['Meaning']
    explanation = info['Simple Explanation']
    reference_range = f'{low} - {high}'
    if status == 'Normal':
        interpretation = f'{meaning} is within the provided reference range ({reference_range} {unit}). {explanation}'
    elif status == 'Low':
        interpretation = f'{meaning} is below the provided reference range ({reference_range} {unit}). {explanation} A low value may be associated with certain health conditions, but clinical interpretation requires additional information.'
    elif status == 'High':
        interpretation = f'{meaning} is above the provided reference range ({reference_range} {unit}). {explanation} A high value may be associated with certain health conditions, but clinical interpretation requires additional information.'
    else:
        interpretation = 'The status of this parameter could not be determined.'
    parameter_suggestions = suggestion_knowledge_base.get(parameter, {})
    suggestions = parameter_suggestions.get(status, 'Maintain a balanced lifestyle and discuss abnormal results with a healthcare professional.')
    return {'Parameter': parameter, 'Value': value, 'Unit': unit, 'Reference Range': reference_range, 'Status': status, 'Meaning': meaning, 'Simple Explanation': explanation, 'Interpretation': interpretation, 'Suggestions': suggestions}
test_results = extract_cbc_report(cbc_df.iloc[1]['raw_report_text'])
test_interpretation = generate_structured_interpretation('HGB', test_results['HGB'])
report_text = cbc_df.iloc[1]['raw_report_text']
extracted = extract_cbc_report(report_text)
structured_results = []
structured_df = pd.DataFrame(structured_results)
all_structured_results = []
all_structured_df = pd.DataFrame(all_structured_results)
# report_001 = all_structured_df[all_structured_df['Report ID'] == 'CBC_001']
# abnormal_001 = report_001[report_001['Status'] != 'Normal']

def create_patient_summary(report_df):
    report_id = report_df['Report ID'].iloc[0]
    normal_parameters = report_df[report_df['Status'] == 'Normal']['Parameter'].tolist()
    low_parameters = report_df[report_df['Status'] == 'Low']['Parameter'].tolist()
    high_parameters = report_df[report_df['Status'] == 'High']['Parameter'].tolist()
    interpretations = report_df['Interpretation'].tolist()
    suggestions = report_df['Suggestions'].tolist()
    return {'Report ID': report_id, 'Normal Parameters': normal_parameters, 'Low Parameters': low_parameters, 'High Parameters': high_parameters, 'Interpretations': interpretations, 'Suggestions': suggestions}
# summary_001 = create_patient_summary(report_001)
patient_summaries = []
patient_summary_df = pd.DataFrame(patient_summaries)

def create_compact_cbc_summary(report_df):
    report_id = report_df['Report ID'].iloc[0]
    lines = []
    for (_, row) in report_df.iterrows():
        line = f"{row['Parameter']}: {row['Value']} {row['Unit']} — {row['Status']}"
        lines.append(line)
    summary = f'CBC Report: {report_id}\n\n' + '\n'.join(lines)
    return summary
# report_001 = all_structured_df[all_structured_df['Report ID'] == 'CBC_001']
# compact_summary_001 = create_compact_cbc_summary(report_001)
compact_summaries = []
compact_summary_df = pd.DataFrame(compact_summaries)

def generate_overall_cbc_summary(report_df):
    normal_params = report_df[report_df['Status'] == 'Normal']['Parameter'].tolist()
    low_params = report_df[report_df['Status'] == 'Low']['Parameter'].tolist()
    high_params = report_df[report_df['Status'] == 'High']['Parameter'].tolist()
    total_parameters = len(report_df)
    normal_count = len(normal_params)
    low_count = len(low_params)
    high_count = len(high_params)
    parts = []
    if normal_count == total_parameters:
        parts.append('All measured CBC parameters are within the provided reference ranges.')
    else:
        if normal_count > 0:
            parts.append(f'{normal_count} of {total_parameters} measured CBC parameters are within the provided reference ranges.')
        if low_count > 0:
            low_text = ', '.join(low_params)
            parts.append(f'The following parameter(s) are below the provided reference ranges: {low_text}.')
        if high_count > 0:
            high_text = ', '.join(high_params)
            parts.append(f'The following parameter(s) are above the provided reference ranges: {high_text}.')
        parts.append('These findings should be interpreted together with the rest of the CBC, symptoms, medical history and other clinical information.')
    overall_summary = ' '.join(parts)
    return overall_summary
# report_001 = all_structured_df[all_structured_df['Report ID'] == 'CBC_001']
# overall_summary_001 = generate_overall_cbc_summary(report_001)
overall_summaries = []
overall_summary_df = pd.DataFrame(overall_summaries)
# final_report_df = compact_summary_df.merge(overall_summary_df, on='Report ID', how='left')

def detect_related_findings(report_df):
    findings = []
    status = dict(zip(report_df['Parameter'], report_df['Status']))
    if status.get('HGB') == 'Low' and status.get('HCT') == 'Low':
        findings.append('HGB and HCT are both below the provided reference ranges. This combination may indicate a reduced red-cell related finding and should be interpreted with clinical context.')
    if status.get('HGB') == 'Low' and status.get('MCV') == 'Low':
        findings.append('Low HGB together with low MCV may indicate a microcytic pattern. Further clinical evaluation may be required.')
    if status.get('HGB') == 'Low' and status.get('MCH') == 'Low':
        findings.append('Low HGB together with low MCH may indicate reduced hemoglobin content in red blood cells. Clinical context is required for interpretation.')
    if status.get('HGB') == 'Low' and status.get('MCHC') == 'Low':
        findings.append('Low HGB together with low MCHC may indicate a hypochromic pattern. This finding requires clinical context.')
    if status.get('MCV') == 'High' and status.get('MCH') == 'High':
        findings.append('High MCV together with high MCH may indicate a macrocytic pattern. Further clinical evaluation may be required.')
    if status.get('RDW') == 'High' and status.get('HGB') == 'Low':
        findings.append('High RDW together with low HGB indicates variation in red blood cell size alongside low hemoglobin. Clinical evaluation may be required.')
    if status.get('NE%') == 'High' and status.get('LY%') == 'Low':
        findings.append('NE% is high while LY% is low. This relative differential pattern should be interpreted together with the complete CBC and clinical context.')
    if status.get('NE%') == 'Low' and status.get('LY%') == 'High':
        findings.append('NE% is low while LY% is high. This relative differential pattern should be interpreted together with the complete CBC and clinical context.')
    if len(findings) == 0:
        findings.append('No significant parameter relationship was identified from the available CBC parameters.')
    return findings
# cbc001_df = all_structured_df[all_structured_df['Report ID'] == 'CBC_001']
# related_findings_001 = detect_related_findings(cbc001_df)
related_findings_all = []
related_findings_df = pd.DataFrame(related_findings_all)
# related_findings_df['Related Findings Text'] = related_findings_df['Related Findings'].apply(lambda x: '\n'.join((f'• {item}' for item in x)))

def generate_final_cbc_report(report_df):
    structured_results = []
    for (_, row) in report_df.iterrows():
        report_id = row['report_id']
        report_text = row['raw_report_text']
        extracted = extract_cbc_report(report_text)
        for (parameter, result) in extracted.items():
            interpretation = generate_structured_interpretation(parameter, result)
            interpretation['Report ID'] = report_id
            structured_results.append(interpretation)
    structured_df = pd.DataFrame(structured_results)
    related_findings = []
    for (report_id, report_group) in structured_df.groupby('Report ID'):
        findings = detect_related_findings(report_group)
        related_findings.append({'Report ID': report_id, 'Related Findings': findings})
    related_findings_df = pd.DataFrame(related_findings)
    related_findings_df['Related Findings'] = related_findings_df['Related Findings'].apply(lambda x: '\n'.join((f'• {finding}' for finding in x)))
    compact_summaries = []
    for (report_id, report_group) in structured_df.groupby('Report ID'):
        compact_summary = create_compact_cbc_summary(report_group)
        compact_summaries.append({'Report ID': report_id, 'CBC Summary': compact_summary})
    compact_summary_df = pd.DataFrame(compact_summaries)
    overall_summaries = []
    for (report_id, report_group) in structured_df.groupby('Report ID'):
        overall_summary = generate_overall_cbc_summary(report_group)
        overall_summaries.append({'Report ID': report_id, 'Overall CBC Summary': overall_summary})
    overall_summary_df = pd.DataFrame(overall_summaries)
    final_report_df = compact_summary_df.merge(overall_summary_df, on='Report ID', how='left').merge(related_findings_df, on='Report ID', how='left')
    return (structured_df, final_report_df)
(all_structured_df, final_report_df) = generate_final_cbc_report(cbc_df)

def process_cbc_report(report_text, report_id='Unknown'):
    extracted = extract_cbc_report(report_text)
    structured_results = []
    for (parameter, result) in extracted.items():
        interpretation = generate_structured_interpretation(parameter, result)
        interpretation['Report ID'] = report_id
        structured_results.append(interpretation)
    structured_df = pd.DataFrame(structured_results)
    if structured_df.empty:
        return structured_df, {'Report ID': report_id, 'CBC Summary': 'No supported CBC parameters were detected.', 'Overall CBC Summary': '', 'Related Findings': ''}
    related_findings = detect_related_findings(structured_df)
    related_findings_text = '\n'.join((f'• {finding}' for finding in related_findings))
    overall_summary = generate_overall_cbc_summary(structured_df)
    compact_summary = create_compact_cbc_summary(structured_df)
    final_report = {'Report ID': report_id, 'CBC Summary': compact_summary, 'Overall CBC Summary': overall_summary, 'Related Findings': related_findings_text}
    return (structured_df, final_report)
test_report = cbc_df[cbc_df['report_id'] == 'CBC_001'].iloc[0]
(structured_result, final_result) = process_cbc_report(test_report['raw_report_text'], test_report['report_id'])