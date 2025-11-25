import streamlit as st
import matplotlib.pyplot as plt
from app.icons import show_icon
from app.components import compare_profiles

def show_overview(df):
    st.markdown("---")
    show_icon("chart", "Biomarker overview", size=28)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg CRP", f"{df['CRP'].mean():.2f} mg/L")
    col2.metric("Avg Cystatin C", f"{df['Cystatin_C'].mean():.2f} mg/L")
    col3.metric("Avg Creatinine", f"{df['Creatinine'].mean():.1f} µmol/L")
    col4.metric("Avg eGFR", f"{df['eGFR'].mean():.1f} mL/min")

    st.markdown("---")
    show_icon("chart", "CRP Distribution", size=28)
    fig, ax = plt.subplots()
    df["CRP"].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
    ax.set_title("CRP Histogram")
    st.pyplot(fig)

    st.markdown("---")
    show_icon("search", "Compare two cases", size=28)
    idx1 = st.number_input("Select first row", min_value=0, max_value=len(df)-1, value=0)
    idx2 = st.number_input("Select second row", min_value=0, max_value=len(df)-1, value=1)
    compare_profiles(df.iloc[idx1], df.iloc[idx2])
