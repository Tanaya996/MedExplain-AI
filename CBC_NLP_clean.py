import spacy
import pandas as pd

print("spaCy version:", spacy.__version__)
print("Pandas version:", pd.__version__)
import spacy

nlp = spacy.load("en_core_web_sm")

print("spaCy model loaded successfully!")
from google.colab import files

uploaded = files.upload()
import pandas as pd

cbc_df = pd.read_csv("cbc_medexplain.csv")
cbc_df.info()
cbc_df.head()
text = """
Patient CBC report shows hemoglobin 11.2 g/dL,
hematocrit 34%, platelet count 150000 per microliter,
MCV 72 fL, MCH 24 pg, MCHC 31 g/dL,
RDW 15%, neutrophils 65%, and lymphocytes 28%.
"""
doc = nlp(text)
print(doc)
for token in doc:
  print(token.text)
for token in doc:
  print(token.text,"+",token.pos_)
for token in doc:
  print(token.text,"->", token.lemma_)
for ent in doc.ents:
  print(ent.text, "->", ent.label_)
knowledge_df = pd.read_excel(
    "Medical_Explanation_Knowledge_Base_Cleaned.xlsx"
)
knowledge_df.head()
from google.colab import files

uploaded = files.upload()
import pandas as pd

print(knowledge_df.columns.tolist())
knowledge_df.info()
knowledge_df.shape
knowledge_df.isnull().sum()
import os
os.listdir()
cbc_df.isnull().sum()
knowledge_df.head(20)

print(knowledge_df.columns.tolist())
knowledge_df.to_string()
cbc_df.describe()

cbc_df.head()
print(cbc_df.columns.tolist())
print(cbc_df.loc[0, "raw_report_text"])
import spacy

nlp = spacy.load("en_core_web_sm")

print("Model loaded successfully")
report_text = cbc_df.loc[0, "raw_report_text"]

doc = nlp(report_text)

print(doc.text)
cbc_parameters = {
    "HGB": ["hemoglobin", "hb", "hgb"],
    "HCT": ["hematocrit", "hct"],
    "PLT": ["platelet", "platelets", "plt"],
    "MCV": ["mean corpuscular volume", "mcv"],
    "MCHC": ["mean corpuscular hemoglobin concentration", "mchc"],
    "MCH": ["mean corpuscular hemoglobin", "mch"],
    "RDW": ["red cell distribution width", "rdw"],
    "NE%": ["neutrophils", "neutrophil", "ne%"],
    "LY%": ["lymphocytes", "lymphocyte", "ly%"]
}
print(cbc_parameters)
print(cbc_df.loc[0, "raw_report_text"])
report_text = cbc_df.loc[0, "raw_report_text"]

doc = nlp(report_text)

print(doc.text)
for ent in doc.ents:
    print(ent.text, "→", ent.label_)
report_lower=report_text.lower()

for parameter, variations in cbc_parameters.items():
  for variation in variations:
    if variation.lower() in report_lower:
      print(parameter, "->",variation)
      break
import re
match = re.search(
    r"Hemoglobin:\s*([\d.]+)\s*(g/dL|g/L)",
    report_text,
    re.IGNORECASE
)

if match:
    print("Value:", match.group(1))
    print("Unit:", match.group(2))
match = re.search(
    r"Hemoglobin:\s*[\d.]+\s*(?:g/dL|g/L)\s*Reference:\s*([\d.]+)-([\d.]+)",
    report_text,
    re.IGNORECASE
)

if match:
    print("Lower:", match.group(1))
    print("Upper:", match.group(2))
def determine_status(value, low, high):
    if value < low:
        return "Low"
    elif value > high:
        return "High"
    else:
        return "Normal"
value = 14.3
low=12
high=18
status= determine_status(value,low,high)
print(status)

print(extracted_df)
parameters = [
    "HGB",
    "HCT",
    "PLT",
    "MCV",
    "MCHC",
    "MCH",
    "RDW",
    "NE%",
    "LY%"
]

for parameter in parameters:

    column = f"{parameter}_extracted"

    extracted_count = results_df[column].notna().sum()

    print(
        parameter,
        "→",
        extracted_count,
        "/",
        len(results_df)
    )
import re

def extract_cbc_report(report_text):

    results = {}

    patterns = {

        "HGB": r"(?:Hemoglobin|Hb|HGB)\s*:\s*([\d.]+)\s*(g/dL|g/L)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        "HCT": r"(?:Hematocrit|HCT|PCV)\s*:\s*([\d.]+)\s*(%|L/L)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        "PLT": r"(?:Platelet Count|Platelets|Platelet|PLT)\s*:\s*([\d,]+)\s*(/µL|×10⁹/L)\s*Reference\s*:\s*([\d,]+)\s*-\s*([\d,]+)",

        "MCV": r"(?:MCV|Mean Corpuscular Volume)\s*:\s*([\d.]+)\s*(fL)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        "MCHC": r"(?:Mean Corpuscular Hemoglobin Concentration|MCHC)\s*:\s*([\d.]+)\s*(g/dL|g/L)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        "MCH": r"(?:MCH|Mean Corpuscular Hemoglobin)\s*:\s*([\d.]+)\s*(pg)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        "RDW": r"(?:RDW|Red Cell Distribution Width)\s*:\s*([\d.]+)\s*(%)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        "NE%": r"(?:Neutrophils|Neutrophil\s*%|Neutrophil|NE%)\s*:\s*([\d.]+)\s*(%)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        "LY%": r"(?:Lymphocytes|Lymphocyte\s*%|Lymphocyte|LY%)\s*:\s*([\d.]+)\s*(%)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)"
    }

    for parameter, pattern in patterns.items():

        match = re.search(
            pattern,
            report_text,
            re.IGNORECASE
        )

        if match:

            value = float(match.group(1).replace(",", ""))
            unit = match.group(2)

            low = float(
                match.group(3).replace(",", "")
            )

            high = float(
                match.group(4).replace(",", "")
            )

            if value < low:
                status = "Low"

            elif value > high:
                status = "High"

            else:
                status = "Normal"

            results[parameter] = {
                "value": value,
                "unit": unit,
                "reference_low": low,
                "reference_high": high,
                "status": status
            }

    return results
report = cbc_df.loc[0, "raw_report_text"]

extracted = extract_cbc_report(report)

extracted_df = pd.DataFrame.from_dict(
    extracted,
    orient="index"
)

extracted_df
all_results = []

for index, row in cbc_df.iterrows():

    extracted = extract_cbc_report(
        row["raw_report_text"]
    )

    result = {
        "report_id": row["report_id"]
    }

    for parameter, data in extracted.items():

        result[f"{parameter}_extracted"] = data["value"]

        result[f"{parameter}_status_extracted"] = data["status"]

    all_results.append(result)


results_df = pd.DataFrame(all_results)
parameters = [
    "HGB",
    "HCT",
    "PLT",
    "MCV",
    "MCHC",
    "MCH",
    "RDW",
    "NE%",
    "LY%"
]

for parameter in parameters:

    column = f"{parameter}_extracted"

    extracted_count = results_df[column].notna().sum()

    percentage = (
        extracted_count / len(results_df)
    ) * 100

    print(
        parameter,
        "→",
        extracted_count,
        "/",
        len(results_df),
        "|",
        round(percentage, 2),
        "%"
    )
parameters_to_check = ["HCT", "NE%", "LY%"]

for parameter in parameters_to_check:

    column = f"{parameter}_extracted"

    print("\n" + "=" * 60)
    print(parameter)
    print("=" * 60)

    failed = cbc_df[results_df[column].isna()]

    print("Failed reports:", len(failed))

    for _, row in failed.head(10).iterrows():
        print("\nReport ID:", row["report_id"])
        print(row["raw_report_text"])
import re

def extract_cbc_report(report_text):

    results = {}

    patterns = {

        # Hemoglobin
        "HGB": r"(?:Hemoglobin|Hb|HGB)\s*:\s*([\d.]+)\s*(g/dL|g/L)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        # Hematocrit / PCV
        "HCT": r"(?:Hematocrit|HCT|PCV)\s*:\s*([\d.]+)\s*(%|L/L)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        # Platelets
        "PLT": r"(?:Platelet Count|Platelets|Platelet|PLT)\s*:\s*([\d,]+)\s*(/µL|×10⁹/L)\s*Reference\s*:\s*([\d,]+)\s*-\s*([\d,]+)",

        # MCV
        "MCV": r"(?:MCV|Mean Corpuscular Volume)\s*:\s*([\d.]+)\s*(fL)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        # MCHC
        "MCHC": r"(?:Mean Corpuscular Hemoglobin Concentration|MCHC)\s*:\s*([\d.]+)\s*(g/dL|g/L)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        # MCH
        "MCH": r"(?:MCH|Mean Corpuscular Hemoglobin)\s*:\s*([\d.]+)\s*(pg)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        # RDW
        "RDW": r"(?:RDW|Red Cell Distribution Width)\s*:\s*([\d.]+)\s*(%)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        # Neutrophils
        "NE%": r"(?:Neutrophils|Neutrophil\s*%|Neutrophil|NE%)\s*:\s*([\d.]+)\s*(%)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",

        # Lymphocytes
        "LY%": r"(?:Lymphocytes|Lymphocyte\s*%|Lymphocyte|LY%)\s*:\s*([\d.]+)\s*(%)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)"
    }

    for parameter, pattern in patterns.items():

        match = re.search(
            pattern,
            report_text,
            re.IGNORECASE
        )

        if match:

            value = float(
                match.group(1).replace(",", "")
            )

            unit = match.group(2)

            low = float(
                match.group(3).replace(",", "")
            )

            high = float(
                match.group(4).replace(",", "")
            )

            # Determine status
            if value < low:
                status = "Low"

            elif value > high:
                status = "High"

            else:
                status = "Normal"

            results[parameter] = {
                "value": value,
                "unit": unit,
                "reference_low": low,
                "reference_high": high,
                "status": status
            }

    return results
report = cbc_df.loc[
    cbc_df["report_id"] == "CBC_002",
    "raw_report_text"
].iloc[0]

extracted = extract_cbc_report(report)

pd.DataFrame.from_dict(
    extracted,
    orient="index"
)
all_results = []

for index, row in cbc_df.iterrows():

    extracted = extract_cbc_report(
        row["raw_report_text"]
    )

    result = {
        "report_id": row["report_id"]
    }

    for parameter, data in extracted.items():

        result[f"{parameter}_extracted"] = data["value"]

        result[f"{parameter}_status_extracted"] = data["status"]

    all_results.append(result)


results_df = pd.DataFrame(all_results)
parameters = [
    "HGB",
    "HCT",
    "PLT",
    "MCV",
    "MCHC",
    "MCH",
    "RDW",
    "NE%",
    "LY%"
]

for parameter in parameters:

    column = f"{parameter}_extracted"

    extracted_count = results_df[column].notna().sum()

    percentage = (
        extracted_count / len(results_df)
    ) * 100

    print(
        parameter,
        "→",
        extracted_count,
        "/",
        len(results_df),
        "|",
        round(percentage, 2),
        "%"
    )
parameters = [
    "HGB",
    "HCT",
    "PLT",
    "MCV",
    "MCHC",
    "MCH",
    "RDW",
    "NE%",
    "LY%"
]

for parameter in parameters:

    extracted_col = f"{parameter}_extracted"
    dataset_col = f"{parameter}_value"

    matches = (
        results_df[extracted_col].round(2)
        ==
        cbc_df[dataset_col].round(2)
    )

    accuracy = matches.mean() * 100

    print(
        parameter,
        "Value Accuracy:",
        round(accuracy, 2),
        "%"
    )
for parameter in parameters:

    extracted_col = f"{parameter}_status_extracted"
    dataset_col = f"{parameter}_status"

    matches = (
        results_df[extracted_col]
        ==
        cbc_df[dataset_col]
    )

    accuracy = matches.mean() * 100

    print(
        parameter,
        "Status Accuracy:",
        round(accuracy, 2),
        "%"
    )
knowledge_df
print(knowledge_df.columns.tolist())
knowledge_base = {}

for _, row in knowledge_df.iterrows():
    parameter = row["Parameter"]
    knowledge_base[parameter] = {
        "Meaning": row["Meaning"],
        "Simple Explanation": row["Simple Explanation"],
        "Unit": row["Unit"]
    }
knowledge_base


knowledge_base["HGB: "]
knowledge_df=knowledge_df.rename(columns={
    "parameter": "Parameter",
    "meaning": "Meaning",
    "simple explanation": "Simple Explanation",
    "Units": "Units",
    "Lower range":"Lower Range"
})
knowledge_df["Parameter"] = (
    knowledge_df["Parameter"]
    .astype(str)
    .str.strip()
    .str.rstrip(":")
    .str.strip()
)
knowledge_df["Parameter"].tolist()
standard_units = {
    "HGB": "g/dL",
    "HCT": "%",
    "PLT": "/µL",
    "MCV": "fL",
    "MCHC": "g/dL",
    "MCH": "pg",
    "RDW": "%",
    "NE%": "%",
    "LY%": "%"
}

knowledge_df["Unit"] = knowledge_df["Parameter"].map(standard_units)
range_data = []

for parameter in parameters:

    low = cbc_df[f"{parameter}_ref_low"].iloc[0]
    high = cbc_df[f"{parameter}_ref_high"].iloc[0]

    range_data.append({
        "Parameter": parameter,
        "Lower Range": low,
        "Upper Range": high
    })

range_df = pd.DataFrame(range_data)

range_df
knowledge_df= knowledge_df.drop(columns=["Lower Range"],
                                errors="ignore")
knowledge_df = knowledge_df.merge(
    range_df,
    on="Parameter",
    how="left"
)
knowledge_df

knowledge_df.to_excel(
    "Medical_Explanation_Knowledge_Base_Cleaned.xlsx",
    index=False
)
knowledge_df
from google.colab import files

files.download("cbc_medexplain.csv")
files.download("Medical_Explanation_Knowledge_Base_Cleaned.xlsx")
knowledge_base = (
    knowledge_df
    .set_index("Parameter")
    .to_dict(orient="index")
)

print(knowledge_base["HGB"])
print(knowledge_base["NE%"])
print("CBC Dataset:", cbc_df.shape)
print("Knowledge Base:", knowledge_df.shape)
print("Parameters:", parameters)
print(knowledge_df.columns.tolist())
print(knowledge_df["Parameter"].tolist())
knowledge_base =(
    knowledge_df
    .set_index("Parameter")
    .to_dict(orient="index")
)
print(knowledge_base["HGB"])
print(knowledge_base["NE%"])
def generate_explanation(parameter, result):
    info = knowledge_base.get(parameter)

    if info is None:
        return "Knowledge not available."

    return {
        "Parameter": parameter,
        "Value": result["value"],
        "Unit": result["unit"],
        "Reference Range": (
            f'{result["reference_low"]} - '
            f'{result["reference_high"]}'
        ),
        "Status": result["status"],
        "Meaning": info["Meaning"],
        "Simple Explanation": info["Simple Explanation"]
    }
sample_report = cbc_df.iloc[0]["raw_report_text"]

extracted_results = extract_cbc_report(sample_report)

hgb_result = generate_explanation(
    "HGB",
    extracted_results["HGB"]
)

print(hgb_result)
all_explanations = []

for parameter, result in extracted_results.items():
    explanation = generate_explanation(parameter, result)
    all_explanations.append(explanation)

explanations_df = pd.DataFrame(all_explanations)

display(explanations_df)
all_report_explanations = []

for _, row in cbc_df.iterrows():

    report_id = row["report_id"]
    report_text = row["raw_report_text"]

    extracted_results = extract_cbc_report(report_text)

    for parameter, result in extracted_results.items():

        explanation = generate_explanation(
            parameter,
            result
        )

        # Skip missing Knowledge Base entries
        if not isinstance(explanation, dict):
            print(
                f"Warning: Explanation unavailable for "
                f"{parameter} in {report_id}"
            )
            continue

        explanation["Report ID"] = report_id

        all_report_explanations.append(explanation)

all_explanations_df = pd.DataFrame(all_report_explanations)

print("Total explanations:", len(all_explanations_df))
print("Unique reports:", all_explanations_df["Report ID"].nunique())

display(all_explanations_df.head(10))
expected_parameters =set(parameters)

missing_results=[]
for report_id in cbc_df["report_id"]:
    report_results =all_explanations_df[
        all_explanations_df["Report ID"]==report_id
    ]
    extracted_parameters=set(report_results["Parameter"])
    missing_parameters = expected_parameters - extracted_parameters

    for parameter in missing_parameters:
      missing_results.append({
          "Report ID": report_id,
          "Missing Parameter":parameter
      })
missing_df = pd.DataFrame(missing_results)
print("Total missing parameter results:",len(missing_df))
display(missing_df.head(20))
print(
    missing_df["Missing Parameter"]
    .value_counts()
)
problem_reports = cbc_df[
    cbc_df["report_id"].isin(
        missing_df["Report ID"].unique()
    )
]

for _, row in problem_reports.head(3).iterrows():

    print("=" * 80)
    print(row["report_id"])
    print(row["raw_report_text"])
    print()
test_text = cbc_df[
    cbc_df["report_id"] == "CBC_002"
]["raw_report_text"].iloc[0]

print(test_text)

print("\nHCT match:")
print(re.search(
    r"(?:Hematocrit|HCT|PCV)\s*:\s*([\d.]+)\s*(%|L/L)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",
    test_text,
    re.IGNORECASE
))

print("\nNE% match:")
print(re.search(
    r"(?:Neutrophils|Neutrophil\s*%|Neutrophil|NE%)\s*:\s*([\d.]+)\s*(%)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",
    test_text,
    re.IGNORECASE
))

print("\nLY% match:")
print(re.search(
    r"(?:Lymphocytes|Lymphocyte\s*%|Lymphocyte|LY%)\s*:\s*([\d.]+)\s*(%)\s*Reference\s*:\s*([\d.]+)\s*-\s*([\d.]+)",
    test_text,
    re.IGNORECASE
))
test_results = extract_cbc_report(test_text)

print(test_results.keys())
print()

for parameter in ["HCT", "NE%", "LY%"]:
    print(parameter, ":", test_results.get(parameter))
for parameter in ["HCT", "NE%", "LY%"]:
    print("\n", parameter)
    print(knowledge_base.get(parameter))
test_results = extract_cbc_report(test_text)

print(test_results.keys())

for parameter in parameters:
    print(parameter, ":", test_results.get(parameter))
all_report_explanations = []

for _, row in cbc_df.iterrows():

    report_id = row["report_id"]
    report_text = row["raw_report_text"]

    extracted_results = extract_cbc_report(report_text)

    for parameter, result in extracted_results.items():

        explanation = generate_explanation(
            parameter,
            result
        )

        if not isinstance(explanation, dict):
            continue

        explanation["Report ID"] = report_id

        all_report_explanations.append(explanation)

all_explanations_df = pd.DataFrame(
    all_report_explanations
)

print("Total explanations:", len(all_explanations_df))
print(
    "Unique reports:",
    all_explanations_df["Report ID"].nunique()
)
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
def generate_structured_interpretation(parameter, result):

    # Clean parameter and status
    parameter = str(parameter).strip().upper()
    status = str(result["status"]).strip().title()

    # Get knowledge base information
    info = knowledge_base.get(parameter)

    if info is None:
        return {
            "Parameter": parameter,
            "Value": result["value"],
            "Unit": result["unit"],
            "Reference Range": (
                f'{result["reference_low"]} - '
                f'{result["reference_high"]}'
            ),
            "Status": status,
            "Meaning": "Knowledge not available.",
            "Simple Explanation": "Knowledge not available.",
            "Interpretation": "Knowledge not available.",
            "Suggestions": "Please discuss the result with a healthcare professional."
        }

    value = result["value"]
    unit = result["unit"]
    low = result["reference_low"]
    high = result["reference_high"]

    meaning = info["Meaning"]
    explanation = info["Simple Explanation"]

    reference_range = f"{low} - {high}"

    # -----------------------------
    # MEDICAL INTERPRETATION
    # -----------------------------

    if status == "Normal":

        interpretation = (
            f"{meaning} is within the provided reference range "
            f"({reference_range} {unit}). "
            f"{explanation}"
        )

    elif status == "Low":

        interpretation = (
            f"{meaning} is below the provided reference range "
            f"({reference_range} {unit}). "
            f"{explanation} "
            f"A low value may be associated with certain health conditions, "
            f"but clinical interpretation requires additional information."
        )

    elif status == "High":

        interpretation = (
            f"{meaning} is above the provided reference range "
            f"({reference_range} {unit}). "
            f"{explanation} "
            f"A high value may be associated with certain health conditions, "
            f"but clinical interpretation requires additional information."
        )

    else:

        interpretation = (
            "The status of this parameter could not be determined."
        )

    # -----------------------------
    # PARAMETER-SPECIFIC SUGGESTION
    # -----------------------------

    parameter_suggestions = suggestion_knowledge_base.get(
        parameter,
        {}
    )

    suggestions = parameter_suggestions.get(
        status,
        "Maintain a balanced lifestyle and discuss abnormal results with a healthcare professional."
    )

    # -----------------------------
    # FINAL STRUCTURED RESULT
    # -----------------------------

    return {
        "Parameter": parameter,
        "Value": value,
        "Unit": unit,
        "Reference Range": reference_range,
        "Status": status,
        "Meaning": meaning,
        "Simple Explanation": explanation,
        "Interpretation": interpretation,
        "Suggestions": suggestions
    }
test_results = extract_cbc_report(
    cbc_df.iloc[1]["raw_report_text"]
)
test_interpretation = generate_structured_interpretation(
    "HGB",
    test_results["HGB"]
)
test_interpretation
report_text = cbc_df.iloc[1]["raw_report_text"]

extracted = extract_cbc_report(report_text)

structured_results = []

for parameter, result in extracted.items():

    interpretation = generate_structured_interpretation(
        parameter,
        result
    )

    structured_results.append(interpretation)

structured_df = pd.DataFrame(structured_results)
structured_df.columns.tolist()
structured_df[
    [
        "Parameter",
        "Status",
        "Suggestions"
    ]
]
all_structured_results = []

for _, row in cbc_df.iterrows():

    report_id = row["report_id"]
    report_text = row["raw_report_text"]

    extracted = extract_cbc_report(report_text)

    for parameter, result in extracted.items():

        interpretation = generate_structured_interpretation(
            parameter,
            result
        )

        interpretation["Report ID"] = report_id

        all_structured_results.append(
            interpretation
        )

all_structured_df = pd.DataFrame(all_structured_results)
print("Total structured results:", len(all_structured_df))
print(
    "Unique reports:",
    all_structured_df["Report ID"].nunique()
)

print(
    "Unique parameters:",
    all_structured_df["Parameter"].nunique()
)
print(
    "Missing suggestions:",
    all_structured_df["Suggestions"].isna().sum()
)
print(
    "Missing suggestions:",
    all_structured_df["Suggestions"].isna().sum()
)
all_structured_df["Status"].value_counts()
all_structured_df.head(10)
report_001 = all_structured_df[
    all_structured_df["Report ID"] == "CBC_001"
]

report_001
abnormal_001 = report_001[
    report_001["Status"] != "Normal"
]

abnormal_001[
    [
        "Parameter",
        "Value",
        "Unit",
        "Reference Range",
        "Status"
    ]
]
def create_patient_summary(report_df):

    report_id = report_df["Report ID"].iloc[0]

    normal_parameters = report_df[
        report_df["Status"] == "Normal"
    ]["Parameter"].tolist()

    low_parameters = report_df[
        report_df["Status"] == "Low"
    ]["Parameter"].tolist()

    high_parameters = report_df[
        report_df["Status"] == "High"
    ]["Parameter"].tolist()

    interpretations = report_df[
        "Interpretation"
    ].tolist()

    suggestions = report_df[
        "Suggestions"
    ].tolist()

    return {
        "Report ID": report_id,
        "Normal Parameters": normal_parameters,
        "Low Parameters": low_parameters,
        "High Parameters": high_parameters,
        "Interpretations": interpretations,
        "Suggestions": suggestions
    }
summary_001 = create_patient_summary(report_001)

summary_001
patient_summaries = []

for report_id, report_group in all_structured_df.groupby("Report ID"):

    summary = create_patient_summary(report_group)

    patient_summaries.append(summary)

patient_summary_df = pd.DataFrame(patient_summaries)
print("Total patient summaries:", len(patient_summary_df))
patient_summary_df.columns.tolist()
patient_summary_df.iloc[0]
def create_compact_cbc_summary(report_df):

    report_id = report_df["Report ID"].iloc[0]

    lines = []

    for _, row in report_df.iterrows():

        line = (
            f'{row["Parameter"]}: '
            f'{row["Value"]} '
            f'{row["Unit"]} — '
            f'{row["Status"]}'
        )

        lines.append(line)

    summary = (
        f"CBC Report: {report_id}\n\n"
        + "\n".join(lines)
    )

    return summary
report_001 = all_structured_df[
    all_structured_df["Report ID"] == "CBC_001"
]

compact_summary_001 = create_compact_cbc_summary(
    report_001
)

print(compact_summary_001)
compact_summaries = []

for report_id, report_group in all_structured_df.groupby("Report ID"):

    compact_summary = create_compact_cbc_summary(
        report_group
    )

    compact_summaries.append({
        "Report ID": report_id,
        "CBC Summary": compact_summary
    })

compact_summary_df = pd.DataFrame(
    compact_summaries
)
compact_summary_df.head()
print(
    compact_summary_df.iloc[50]["CBC Summary"]
)
print(
    compact_summary_df.iloc[5]["CBC Summary"]
)
def generate_overall_cbc_summary(report_df):

    normal_params = report_df[
        report_df["Status"] == "Normal"
    ]["Parameter"].tolist()

    low_params = report_df[
        report_df["Status"] == "Low"
    ]["Parameter"].tolist()

    high_params = report_df[
        report_df["Status"] == "High"
    ]["Parameter"].tolist()

    total_parameters = len(report_df)
    normal_count = len(normal_params)
    low_count = len(low_params)
    high_count = len(high_params)

    # --------------------------------
    # Build overall summary
    # --------------------------------

    parts = []

    if normal_count == total_parameters:

        parts.append(
            "All measured CBC parameters are within the provided "
            "reference ranges."
        )

    else:

        if normal_count > 0:

            parts.append(
                f"{normal_count} of {total_parameters} measured CBC "
                f"parameters are within the provided reference ranges."
            )

        if low_count > 0:

            low_text = ", ".join(low_params)

            parts.append(
                f"The following parameter(s) are below the provided "
                f"reference ranges: {low_text}."
            )

        if high_count > 0:

            high_text = ", ".join(high_params)

            parts.append(
                f"The following parameter(s) are above the provided "
                f"reference ranges: {high_text}."
            )

        parts.append(
            "These findings should be interpreted together with the "
            "rest of the CBC, symptoms, medical history and other "
            "clinical information."
        )

    overall_summary = " ".join(parts)

    return overall_summary
report_001 = all_structured_df[
    all_structured_df["Report ID"] == "CBC_001"
]

overall_summary_001 = generate_overall_cbc_summary(
    report_001
)

print(overall_summary_001)
overall_summaries = []

for report_id, report_group in all_structured_df.groupby("Report ID"):

    overall_summary = generate_overall_cbc_summary(
        report_group
    )

    overall_summaries.append({
        "Report ID": report_id,
        "Overall CBC Summary": overall_summary
    })

overall_summary_df = pd.DataFrame(
    overall_summaries
)
print(
    "Total overall summaries:",
    len(overall_summary_df)
)
overall_summary_df.head(5)
final_report_df = compact_summary_df.merge(
    overall_summary_df,
    on="Report ID",
    how="left"
)

final_report_df.head()
final_report_df.columns.tolist()

def detect_related_findings(report_df):

    findings = []

    # Convert parameter-status information into a dictionary
    status = dict(
        zip(
            report_df["Parameter"],
            report_df["Status"]
        )
    )

    # --------------------------------------------------
    # 1. Low HGB + Low HCT
    # --------------------------------------------------
    if status.get("HGB") == "Low" and status.get("HCT") == "Low":

        findings.append(
            "HGB and HCT are both below the provided reference ranges. "
            "This combination may indicate a reduced red-cell related "
            "finding and should be interpreted with clinical context."
        )

    # --------------------------------------------------
    # 2. Low HGB + Low MCV
    # --------------------------------------------------
    if status.get("HGB") == "Low" and status.get("MCV") == "Low":

        findings.append(
            "Low HGB together with low MCV may indicate a microcytic "
            "pattern. Further clinical evaluation may be required."
        )

    # --------------------------------------------------
    # 3. Low HGB + Low MCH
    # --------------------------------------------------
    if status.get("HGB") == "Low" and status.get("MCH") == "Low":

        findings.append(
            "Low HGB together with low MCH may indicate reduced "
            "hemoglobin content in red blood cells. Clinical context "
            "is required for interpretation."
        )

    # --------------------------------------------------
    # 4. Low HGB + Low MCHC
    # --------------------------------------------------
    if status.get("HGB") == "Low" and status.get("MCHC") == "Low":

        findings.append(
            "Low HGB together with low MCHC may indicate a "
            "hypochromic pattern. This finding requires clinical context."
        )

    # --------------------------------------------------
    # 5. High MCV + High MCH
    # --------------------------------------------------
    if status.get("MCV") == "High" and status.get("MCH") == "High":

        findings.append(
            "High MCV together with high MCH may indicate a macrocytic "
            "pattern. Further clinical evaluation may be required."
        )

    # --------------------------------------------------
    # 6. High RDW + Low HGB
    # --------------------------------------------------
    if status.get("RDW") == "High" and status.get("HGB") == "Low":

        findings.append(
            "High RDW together with low HGB indicates variation in "
            "red blood cell size alongside low hemoglobin. Clinical "
            "evaluation may be required."
        )

    # --------------------------------------------------
    # 7. High NE% + Low LY%
    # --------------------------------------------------
    if status.get("NE%") == "High" and status.get("LY%") == "Low":

        findings.append(
            "NE% is high while LY% is low. This relative differential "
            "pattern should be interpreted together with the complete "
            "CBC and clinical context."
        )

    # --------------------------------------------------
    # 8. Low NE% + High LY%
    # --------------------------------------------------
    if status.get("NE%") == "Low" and status.get("LY%") == "High":

        findings.append(
            "NE% is low while LY% is high. This relative differential "
            "pattern should be interpreted together with the complete "
            "CBC and clinical context."
        )

    # --------------------------------------------------
    # If no relationship is detected
    # --------------------------------------------------
    if len(findings) == 0:

        findings.append(
            "No significant parameter relationship was identified "
            "from the available CBC parameters."
        )

    return findings
cbc001_df = all_structured_df[
    all_structured_df["Report ID"] == "CBC_001"
]

related_findings_001 = detect_related_findings(cbc001_df)

for i, finding in enumerate(related_findings_001, 1):

    print(f"{i}. {finding}")
related_findings_all = []

for report_id, report_group in all_structured_df.groupby("Report ID"):

    findings = detect_related_findings(report_group)

    related_findings_all.append({
        "Report ID": report_id,
        "Related Findings": findings
    })

related_findings_df = pd.DataFrame(
    related_findings_all
)
print("Total reports:", len(related_findings_df))
print("Unique reports:", related_findings_df["Report ID"].nunique())
related_findings_df["Related Findings Text"] = (
    related_findings_df["Related Findings"]
    .apply(lambda x: "\n".join(f"• {item}" for item in x))
)

related_findings_df[
    ["Report ID", "Related Findings Text"]
].head()
def generate_final_cbc_report(report_df):

    # -----------------------------------------
    # 1. Generate individual parameter results
    # -----------------------------------------
    structured_results = []

    for _, row in report_df.iterrows():

        report_id = row["report_id"]
        report_text = row["raw_report_text"]

        extracted = extract_cbc_report(report_text)

        for parameter, result in extracted.items():

            interpretation = generate_structured_interpretation(
                parameter,
                result
            )

            interpretation["Report ID"] = report_id

            structured_results.append(interpretation)

    structured_df = pd.DataFrame(structured_results)

    # -----------------------------------------
    # 2. Generate Related Findings
    # -----------------------------------------
    related_findings = []

    for report_id, report_group in structured_df.groupby("Report ID"):

        findings = detect_related_findings(report_group)

        related_findings.append({
            "Report ID": report_id,
            "Related Findings": findings
        })

    related_findings_df = pd.DataFrame(
        related_findings
    )

    # Convert list into readable text
    related_findings_df["Related Findings"] = (
        related_findings_df["Related Findings"]
        .apply(
            lambda x: "\n".join(
                f"• {finding}"
                for finding in x
            )
        )
    )

    # -----------------------------------------
    # 3. Create compact CBC summary
    # -----------------------------------------
    compact_summaries = []

    for report_id, report_group in structured_df.groupby("Report ID"):

        compact_summary = create_compact_cbc_summary(
            report_group
        )

        compact_summaries.append({
            "Report ID": report_id,
            "CBC Summary": compact_summary
        })

    compact_summary_df = pd.DataFrame(
        compact_summaries
    )

    # -----------------------------------------
    # 4. Create Overall CBC Summary
    # -----------------------------------------
    overall_summaries = []

    for report_id, report_group in structured_df.groupby("Report ID"):

        overall_summary = generate_overall_cbc_summary(
            report_group
        )

        overall_summaries.append({
            "Report ID": report_id,
            "Overall CBC Summary": overall_summary
        })

    overall_summary_df = pd.DataFrame(
        overall_summaries
    )

    # -----------------------------------------
    # 5. Merge everything together
    # -----------------------------------------
    final_report_df = (
        compact_summary_df
        .merge(
            overall_summary_df,
            on="Report ID",
            how="left"
        )
        .merge(
            related_findings_df,
            on="Report ID",
            how="left"
        )
    )

    return structured_df, final_report_df
all_structured_df, final_report_df = generate_final_cbc_report(
    cbc_df
)
print("Structured results:", len(all_structured_df))
print("Reports:", final_report_df["Report ID"].nunique())
print("Final columns:")
print(final_report_df.columns.tolist())
display(
    final_report_df[
        [
            "Report ID",
            "CBC Summary",
            "Overall CBC Summary",
            "Related Findings"
        ]
    ].head(3)
)
def process_cbc_report(report_text, report_id="Unknown"):

    # -----------------------------------------
    # 1. Extract CBC parameters
    # -----------------------------------------
    extracted = extract_cbc_report(report_text)

    structured_results = []

    # -----------------------------------------
    # 2. Generate interpretations
    # -----------------------------------------
    for parameter, result in extracted.items():

        interpretation = generate_structured_interpretation(
            parameter,
            result
        )

        interpretation["Report ID"] = report_id

        structured_results.append(
            interpretation
        )

    # Convert to DataFrame
    structured_df = pd.DataFrame(
        structured_results
    )

    # -----------------------------------------
    # 3. Detect related findings
    # -----------------------------------------
    related_findings = detect_related_findings(
        structured_df
    )

    related_findings_text = "\n".join(
        f"• {finding}"
        for finding in related_findings
    )

    # -----------------------------------------
    # 4. Generate overall summary
    # -----------------------------------------
    overall_summary = generate_overall_cbc_summary(
        structured_df
    )

    # -----------------------------------------
    # 5. Generate compact CBC summary
    # -----------------------------------------
    compact_summary = create_compact_cbc_summary(
        structured_df
    )

    # -----------------------------------------
    # 6. Final report information
    # -----------------------------------------
    final_report = {
        "Report ID": report_id,
        "CBC Summary": compact_summary,
        "Overall CBC Summary": overall_summary,
        "Related Findings": related_findings_text
    }

    return structured_df, final_report
test_report = cbc_df[
    cbc_df["report_id"] == "CBC_001"
].iloc[0]

structured_result, final_result = process_cbc_report(
    test_report["raw_report_text"],
    test_report["report_id"]
)

print(final_result)

