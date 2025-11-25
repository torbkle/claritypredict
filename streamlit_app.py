import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from app.branding import show_logo, apply_custom_style
from app.footer import show_footer
from app.upload import upload_data
from app.prediction import run_prediction
from app.explore import explore_data
from app.example import show_demo_section
from app.profile import show_biomarker_profile
from app.facts import show_random_fact
from app.about import show_about
from app.icons import show_icon

# App config
st.set_page_config(page_title="ClarityPredict", layout="centered")

# Branding
apply_custom_style()
show_logo()

# Init state
if "show_info" not in st.session_state:
    st.session_state["show_info"] = False

# --- Demo-seksjon ---
show_demo_section()

# --- Filopplasting og prediksjon ---
df = upload_data()

if "example_df" in st.session_state:
    df = st.session_state.example_df

if df is not None:
    explore_data(df)
    show_icon("chart", "Data is ready for prediction module", size=28)
    run_prediction(df)

    st.markdown("---")
    selected_idx = st.number_input("Select a case to inspect", min_value=0, max_value=len(df) - 1, value=0)
    patient_data = df.iloc[selected_idx]

    st.markdown("## 🧑‍⚕️ Patient Profile")
    age = patient_data.get("Age", "NA")
    sex = patient_data.get("Sex", "NA")
    diagnosis = patient_data.get("Diagnosis", "NA")

    diagnosis_map = {
        "Frisk": "Healthy",
        "Diabetes": "Diabetes",
        "Hypertensjon": "Hypertension",
        "Kreft": "Cancer",
        "Hjertesvikt": "Heart Failure"
    }
    diagnosis_en = diagnosis_map.get(str(diagnosis), diagnosis)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Age:** {age}")
    with col2:
        st.write(f"**Sex:** {sex}")
    with col3:
        st.write(f"**Diagnosis:** {diagnosis_en}")

    st.markdown(f"📋 **Summary:** {age} year old {sex.lower()} with diagnosis: {diagnosis_en}.")
    show_biomarker_profile(patient_data)

    st.markdown("## 📊 Clinical Categories of Biomarkers")
    biomarker_groups = {
        "🧪 Kidney Function": ["Creatinine", "eGFR", "Urea", "Cystatin_C"],
        "🔥 Inflammation": ["CRP", "Calprotectin", "WBC"],
        "🩸 Hematology": ["Hemoglobin"],
        "⚖️ Metabolism": ["Albumin", "BMI"],
        "❤️ Cardiology": ["NT_proBNP"]
    }

    selected_categories = st.multiselect(
        "Select one or more biomarker categories",
        list(biomarker_groups.keys()),
        default=list(biomarker_groups.keys())[:1]
    )

    show_radar = st.checkbox("Display combined radar plot for chosen categories", value=True)

    reference_ranges = {
        "Creatinine": (50, 110),
        "eGFR": (30, 90),
        "Urea": (2.5, 7.5),
        "Cystatin_C": (0.6, 1.3),
        "CRP": (0, 10),
        "Calprotectin": (0, 200),
        "WBC": (4, 11),
        "Hemoglobin": (12, 17),
        "Albumin": (35, 50),
        "BMI": (18.5, 30),
        "NT_proBNP": (0, 400)
    }

    for category in selected_categories:
        st.markdown(f"### {category}")
        for marker in biomarker_groups[category]:
            if marker in patient_data:
                st.write(f"**{marker}:** {patient_data[marker]}")

    if show_radar and selected_categories:
        combined_markers = []
        for cat in selected_categories:
            combined_markers.extend(biomarker_groups[cat])

        values, statuses = [], []
        for m in combined_markers:
            if m in patient_data and m in reference_ranges:
                min_val, max_val = reference_ranges[m]
                val = patient_data[m]
                norm_val = (val - min_val) / (max_val - min_val)
                norm_val = max(0, min(1, norm_val))
                values.append(norm_val)

                if 0.3 <= norm_val <= 0.7:
                    statuses.append("Normal")
                elif 0.2 <= norm_val < 0.3 or 0.7 < norm_val <= 0.8:
                    statuses.append("Borderline")
                else:
                    statuses.append("Abnormal")
            else:
                values.append(0)
                statuses.append("Missing")

        if len(values) > 1:
            n_vars = len(combined_markers)
            angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False).tolist()
            values_cycle = values + values[:1]
            angles_cycle = angles + angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles_cycle, values_cycle, "o-", linewidth=2, color="navy")
            ax.fill(angles_cycle, values_cycle, alpha=0.25, color="skyblue")
            ax.grid(color="gray", linestyle="--", linewidth=0.5)
            ax.set_facecolor("#f9f9f9")

            cmap = plt.cm.coolwarm
            for angle, val in zip(angles_cycle, values_cycle):
                ax.plot(angle, val, "o", color=cmap(val), markersize=8)

            ax.set_xticks(angles)
            ax.set_xticklabels(combined_markers, rotation=30, ha="right", fontsize=10, fontweight="bold")
            ax.set_title("Combined Radar Plot", fontsize=14, fontweight="bold")

            st.pyplot(fig)

            st.markdown("**Legend:**")
            st.markdown("- 🟢 Normal")
            st.markdown("- 🟡 Borderline")
            st.markdown("- 🔴 Abnormal")
            st.markdown("- ⚪ Missing")

            table_data = {
                "Biomarker": combined_markers,
                "Value": [patient_data.get(m, "NA") for m in combined_markers],
                "Normalized (0–1)": values,
                "Status": statuses
            }
            df_table = pd.DataFrame(table_data)
            st.markdown("### 📋 Table Overview")
            st.dataframe(df_table, use_container_width=True)

    st.markdown("---")
    show_random_fact()

# --- Info toggle med knapp til høyre ---
st.markdown("---")
col1, col2 = st.columns([7,3])
with col2:
    if not st.session_state.get("show_info", False):
        if st.button("ℹ️ About ClarityPredict", key="show_info_btn"):
            st.session_state["show_info"] = True
            st.rerun()
    else:
        if st.button("Hide info", key="hide_info_btn"):
            st.session_state["show_info"] = False
            st.rerun()

# --- Info-seksjon ---
if st.session_state.get("show_info", False):
    show_about()

# --- Footer ---
show_footer()
