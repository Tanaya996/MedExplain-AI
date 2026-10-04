import re

with open('backend.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_extract = """def extract_cbc_report(report_text):
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
    return results"""

content = re.sub(r'def extract_cbc_report\(report_text\):.*?return results', lambda m: new_extract, content, flags=re.DOTALL)

with open('backend.py', 'w', encoding='utf-8') as f:
    f.write(content)
