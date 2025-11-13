import sys
from pathlib import Path
scripts_path = Path(__file__).parent.parent / "scripts"
sys.path.append(str(scripts_path))

from generate_data import generate_synthetic_data

import streamlit as st

from icons import show_icon
from footer import show_footer
from upload import upload_data
from prediction import run_prediction
from branding import show_logo, apply_custom_style
import matplotlib.pyplot as plt
from facts import show_random_fact
from components import show_biomarker_profile, compare_profiles



# Toggle for midlertidige og eksperimentelle seksjoner
dev_mode = True

# Eksempeldata-funksjon
def load_example_data():
    df = generate_synthetic_data(n_samples=100, seed=42)
    st.session_state.example_df = df
    st.success("✅ Example data loaded! Scroll down to see predictions.")



    # Vis data

    show_icon("search", "Preview of synthetic biomarker data", size=32)
    st.dataframe(df)

    # Nedlastbar CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download example data as CSV", data=csv, file_name="example_data.csv", mime="text/csv")


# App config
st.set_page_config(page_title="ClarityPredict", layout="centered")

# Header
apply_custom_style()
show_logo()

# --- Mobilvennlig testseksjon ---
if dev_mode:
    show_icon("search", "Test ClarityPredict instantly", size=32)

    st.markdown(
        """
This feature is designed for mobile users and others who don't have a CSV file ready.  
Click the button to test the app using pre-filled example data.
"""
    )

    if st.button("🔄 Load and run example data"):
        load_example_data()

# --- Filopplasting og prediksjon ---
df = upload_data()

# Bruk eksempeldata hvis tilgjengelig
if "example_df" in st.session_state:
    df = st.session_state.example_df

if df is not None:
    show_icon("chart", "Data is ready for prediction module", size=28)
    run_prediction(df)

    if dev_mode:
        # --- Informativ oversikt ---
        st.markdown("---")
        show_icon("chart", "Biomarker overview", size=28)

        # Vis gjennomsnitt for utvalgte markører
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg CRP", f"{df['CRP'].mean():.2f} mg/L")
        col2.metric("Avg Cystatin C", f"{df['Cystatin_C'].mean():.2f} mg/L")
        col3.metric("Avg Creatinine", f"{df['Creatinine'].mean():.1f} µmol/L")
        col4.metric("Avg eGFR", f"{df['eGFR'].mean():.1f} mL/min")

        # Histogram for CRP
        show_icon("chart", " CRP Distribution", size=28)
        fig, ax = plt.subplots()
        df["CRP"].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
        ax.set_title("CRP Histogram")
        ax.set_xlabel("CRP value (mg/L)")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)


        # --- Sammenlign to rader ---
        st.markdown("---")
        show_icon("search", "Compare two cases", size=28)
        idx1 = st.number_input("Select first row", min_value=0, max_value=len(df) - 1, value=0)
        idx2 = st.number_input("Select second row", min_value=0, max_value=len(df) - 1, value=1)
        compare_profiles(df.iloc[idx1], df.iloc[idx2])

        # --- Biomarkørprofil ---
        st.markdown("---")
        show_icon("profile", "Explore individual biomarker profile", size=28)
        selected_idx = st.number_input("Select a case to inspect", min_value=0, max_value=len(df)-1, value=0)
        show_biomarker_profile(df.iloc[selected_idx])
        compare_profiles(df.iloc[idx1], df.iloc[idx2])


        # --- Fakta ---
        st.markdown("---")
        # Randomly facts
        show_icon("bulb", "💡 Did you know?", size=28)
        show_random_fact()



# --- Footer ---
show_footer()
