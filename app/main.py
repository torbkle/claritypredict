import streamlit as st
from footer import show_footer
from upload import upload_data
from prediction import run_prediction
from pathlib import Path
from branding import show_logo, apply_custom_style
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Toggle for midlertidige og eksperimentelle seksjoner
dev_mode = True

st.set_page_config(page_title="ClarityPredict", layout="centered")

# Header
apply_custom_style()
show_logo()

# --- Mobilvennlig testseksjon ---
if dev_mode:
    st.markdown("---")
    st.markdown("### 🧪 Test ClarityPredict instantly")

    st.markdown(
        """
This feature is designed for mobile users and others who don't have a CSV file ready.  
Click the button to test the app using pre-filled example data.
"""
    )

    if st.button("🔄 Load and run example data"):
        np.random.seed(42)
        st.session_state.example_df = pd.DataFrame({
            "CRP": np.random.normal(loc=5.0, scale=2.0, size=50).round(2),
            "Albumin": np.random.normal(loc=38.0, scale=1.5, size=50).round(1),
            "Creatinine": np.random.normal(loc=90, scale=10, size=50).round(0),
            "BMI": np.random.normal(loc=25.0, scale=3.0, size=50).round(1)
        })
        st.success("Example data loaded! Scroll down to see predictions.")

# --- Filopplasting og prediksjon ---
df = upload_data()

# Bruk eksempeldata hvis tilgjengelig
if "example_df" in st.session_state:
    df = st.session_state.example_df

if df is not None:
    st.info("Data is ready for prediction module.")
    run_prediction(df)

    if dev_mode:
        # --- Informativ oversikt ---
        st.markdown("---")
        st.markdown("### 📊 Data overview")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg CRP", f"{df['CRP'].mean():.2f}")
        col2.metric("Avg Albumin", f"{df['Albumin'].mean():.2f}")
        col3.metric("Avg Creatinine", f"{df['Creatinine'].mean():.2f}")
        col4.metric("Avg BMI", f"{df['BMI'].mean():.2f}")

        # --- Histogram ---
        st.markdown("### 🧬 CRP Distribution")
        fig, ax = plt.subplots()
        df["CRP"].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
        ax.set_title("CRP Histogram")
        ax.set_xlabel("CRP value")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # --- Sammenlign to rader ---
        st.markdown("### 🔍 Compare two cases")
        idx1 = st.number_input("Select first row", min_value=0, max_value=len(df)-1, value=0)
        idx2 = st.number_input("Select second row", min_value=0, max_value=len(df)-1, value=1)
        st.write("🔬 Case 1", df.iloc[idx1])
        st.write("🧬 Case 2", df.iloc[idx2])

        # --- Fakta ---
        st.markdown("### 💡 Did you know?")
        st.info("CRP is a marker of inflammation and can rise dramatically during infection or trauma.")

# --- Footer ---
show_footer()
