import streamlit as st
from icons import show_icon

# Normalområder for referanse
normal_ranges = {
    "CRP": (0, 5),
    "Cystatin_C": (0.6, 1.2),
    "Creatinine": (60, 105),
    "eGFR": (90, 120),
    "Albumin": (35, 50),
    "Urea": (2.5, 7.5),
    "Hemoglobin": (12, 18),
    "WBC": (3.5, 10.5),
    "BMI": (18.5, 24.9),
}

def show_biomarker_profile(row):
    show_icon("profile", f" Biomarker profile for case {row.name}", size=28)
    st.markdown(f"""
    <div style='line-height: 1.6; font-size: 16px;'>
        <b>Age:</b> {row['Age']}<br>
        <b>Sex:</b> {row['Sex']}<br>
        <b>Diagnosis:</b> {row['Diagnosis']}<br><br>
    """, unsafe_allow_html=True)

    for marker, (low, high) in normal_ranges.items():
        value = row[marker]
        unit = "mg/L" if "CRP" in marker or "Cystatin" in marker else \
               "µmol/L" if marker == "Creatinine" else \
               "mL/min" if marker == "eGFR" else \
               "g/L" if marker == "Albumin" else \
               "mmol/L" if marker == "Urea" else \
               "g/dL" if marker == "Hemoglobin" else \
               "×10⁹/L" if marker == "WBC" else \
               "kg/m²" if marker == "BMI" else ""

        if value < low:
            status = f"🟦 Low ({value} {unit})"
        elif value > high:
            status = f"🟥 High ({value} {unit})"
        else:
            status = f"🟩 Normal ({value} {unit})"

        st.markdown(f"<b>{marker}:</b> {status}", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def compare_profiles(row1, row2):
    show_icon("search", f" Comparing case {row1.name} vs case {row2.name}", size=28)

    def format_diff(val1, val2, unit, marker):
        diff = val1 - val2
        if abs(diff) < 0.01:
            return f"{val1:.2f} {unit} = {val2:.2f} {unit}"
        arrow = "⬆️" if diff > 0 else "⬇️"
        color = "🟥" if abs(diff) > 10 else "🟨" if abs(diff) > 3 else "🟩"
        return f"{color} {val1:.2f} {unit} {arrow} {val2:.2f} {unit}"

    st.markdown("### 🔬 Key biomarker differences")
    for marker, (low, high) in normal_ranges.items():
        unit = "mg/L" if "CRP" in marker or "Cystatin" in marker else \
               "µmol/L" if marker == "Creatinine" else \
               "mL/min" if marker == "eGFR" else \
               "g/L" if marker == "Albumin" else \
               "mmol/L" if marker == "Urea" else \
               "g/dL" if marker == "Hemoglobin" else \
               "×10⁹/L" if marker == "WBC" else \
               "kg/m²" if marker == "BMI" else ""

        val1 = row1[marker]
        val2 = row2[marker]
        st.markdown(f"<b>{marker}:</b> {format_diff(val1, val2, unit, marker)}", unsafe_allow_html=True)
