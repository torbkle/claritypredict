import streamlit as st
from footer import show_footer
from upload import upload_data
from prediction import run_prediction
from pathlib import Path
from branding import show_logo, apply_custom_style
import pandas as pd  # nødvendig for testdata

st.set_page_config(page_title="ClarityPredict", layout="centered")

# Header
apply_custom_style()
show_logo()

# Filopplasting og prediksjon
df = upload_data()

if df is not None:
    st.info("Data is ready for prediction module.")
    run_prediction(df)

# Midlertidig testseksjon
st.markdown("---")
st.markdown("### 🧪 Test the app")

st.markdown(
    """
If you don't have your own data, you can:

- [Download example CSV](https://github.com/torbkle/claritypredict/raw/main/data/example.csv)
- Or generate a test row below
"""
)

if st.button("Generate example data"):
    example_df = pd.DataFrame({
        "CRP": [4.8],
        "Albumin": [39.2],
        "Creatinine": [88],
        "BMI": [23.7]
    })
    st.dataframe(example_df)
    st.markdown("⬆️ You can copy this format into your own CSV file.")

st.markdown(
    """
**Required CSV columns:**

- `CRP`
- `Albumin`
- `Creatinine`
- `BMI`

Make sure your file includes these headers and numerical values.
"""
)

# Footer
show_footer()
