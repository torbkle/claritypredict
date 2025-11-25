import streamlit as st
from app.icons import show_icon

# Kliniske cut-offs og kategorier
BIOMARKER_GROUPS = {
    "Inflammation": {
        "CRP": {"low": 0, "high": 5, "unit": "mg/L"},
        "Calprotectin": {"low": 0, "high": 50, "unit": "µg/g"}
    },
    "Renal function": {
        "Creatinine": {"low": 60, "high": 110, "unit": "µmol/L"},
        "Cystatin_C": {"low": 0.6, "high": 1.2, "unit": "mg/L"},
        "eGFR": {"low": 60, "high": 90, "unit": "mL/min"},
        "Urea": {"low": 2.5, "high": 7.5, "unit": "mmol/L"}
    },
    "Hematology": {
        "Hemoglobin": {"low": 12, "high": 16, "unit": "g/dL"},
        "WBC": {"low": 4, "high": 11, "unit": "×10⁹/L"}
    },
    "Metabolism": {
        "BMI": {"low": 18.5, "high": 25, "unit": "kg/m²"},
        "Albumin": {"low": 35, "high": 50, "unit": "g/L"}
    },
    "Cardiac marker": {
        "NT_proBNP": {"low": 0, "high": 300, "unit": "pg/mL"}
    }
}

def color_code(value, limits):
    """Returnerer farge basert på cut-offs"""
    try:
        if value < limits["low"]:
            return "🟦 Low"
        elif value > limits["high"]:
            return "🟥 High"
        else:
            return "🟩 Normal"
    except Exception:
        return "⚪ N/A"

def show_biomarker_profile(row):
    """Viser biomarkørprofilen til en pasient (én rad i DataFrame)."""
    show_icon("profile", "Biomarker profile", size=28)
    st.write("Biomarker profile for selected case:")

    # Pasientmetadata (hvis tilgjengelig)
    if "Age" in row.index:
        st.write(f"**Age**: {row['Age']}")
    if "Sex" in row.index:
        st.write(f"**Sex**: {row['Sex']}")
    if "Diagnosis" in row.index:
        st.write(f"**Diagnosis**: {row['Diagnosis']}")

    # Gå gjennom kategorier
    for category, biomarkers in BIOMARKER_GROUPS.items():
        st.markdown(f"### {category}")
        for biomarker, limits in biomarkers.items():
            if biomarker in row.index:
                val = row[biomarker]
                unit = limits.get("unit", "")
                if isinstance(val, (int, float)):
                    status = color_code(val, limits)
                    st.write(f"**{biomarker}**: {val:.2f} {unit} → {status}")
                else:
                    st.write(f"**{biomarker}**: {val}")
