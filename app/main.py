import sys
import streamlit as st
from footer import show_footer
from upload import upload_data
from prediction import run_prediction
from pathlib import Path
from branding import show_logo, apply_custom_style
from scripts.generate_data import generate_synthetic_data
import pandas as pd
import matplotlib.pyplot as plt

# Toggle for midlertidige og eksperimentelle seksjoner
dev_mode = True

# Eksempeldata-funksjon
def load_example_data():
    df = generate_synthetic_data(n_samples=100, seed=42)
    st.session_state.example_df = df
    st.success("Example data loaded! Scroll down to see predictions.")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download example data as CSV", data=csv, file_name="example_data.csv", mime="text/csv")


# App config
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
        load_example_data()

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
