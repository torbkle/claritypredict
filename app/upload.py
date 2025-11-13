import streamlit as st
import pandas as pd
from icons import show_icon

REQUIRED_COLUMNS = ["CRP", "Albumin", "Creatinine", "BMI"]

def upload_data():

    show_icon("upload", "Upload your CSV file", size=32)
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding="utf-8")
        except UnicodeDecodeError:
            st.error("❌ File must be encoded in UTF-8. Please re-save your CSV with UTF-8 encoding.")
            return None
        except Exception as e:
            st.error(f"❌ Could not read file: {e}")
            return None

        missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
            return None

        st.success("✅ File uploaded and validated successfully.")
        return df

    return None
