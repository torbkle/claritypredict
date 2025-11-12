import streamlit as st
import pandas as pd

def upload_data():
    st.subheader("📁 Upload Patient Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"], key="upload_csv")


    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(df)
            return df
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None
    else:
        st.info("Awaiting CSV file upload...")
        return None
