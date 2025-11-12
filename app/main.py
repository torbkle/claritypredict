import streamlit as st
from footer import show_footer
from upload import upload_data
from prediction import run_prediction
from pathlib import Path
from branding import show_logo, apply_custom_style



st.set_page_config(page_title="ClarityPredict", layout="centered")

# Header
apply_custom_style()
show_logo()
# st.title("🔬 ClarityPredict")

# st.markdown("""
# Welcome to ClarityPredict – a prototype for explainable biomarker prediction using machine learning.
# """)

# Filopplasting og prediksjon
df = upload_data()

if df is not None:
    st.info("Data is ready for prediction module.")
    run_prediction(df)

# Footer
show_footer()
