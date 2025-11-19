import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from app.icons import show_icon

def explore_data(df):
    st.markdown("---")
    show_icon("search", "Data Exploration", size=32)

    # 📋 Oversikt over datasettet
    st.write("### Dataset preview")
    st.write(df.head())

    # 📊 Statistisk beskrivelse
    st.write("### Summary statistics")
    st.write(df.describe())

    # 🔗 Korrelasjonsmatrise (kun numeriske kolonner)
    st.write("### Correlation matrix (numeric features only)")
    numeric_df = df.select_dtypes(include=["number"])
    st.write(numeric_df.corr())

    # 🔥 Heatmap for korrelasjoner
    st.write("### Correlation heatmap")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # 📈 Histogrammer for utvalgte biomarkører
    st.write("### Histograms")
    selected_col = st.selectbox("Select biomarker to visualize", numeric_df.columns)
    fig_hist, ax_hist = plt.subplots()
    numeric_df[selected_col].hist(ax=ax_hist, bins=20, color="lightblue", edgecolor="black")
    ax_hist.set_title(f"Histogram of {selected_col}")
    st.pyplot(fig_hist)

    # 🧑‍⚕️ Profilvisning per pasient
    st.write("### Patient biomarker profile")
    idx = st.number_input("Select patient index", min_value=0, max_value=len(df)-1, value=0)
    patient = df.iloc[idx]

    st.write(f"**Patient {idx} profile:**")
    profile = {}
    for col in numeric_df.columns:
        val = patient[col]
        if col == "CRP":
            status = "High" if val > 5 else "Normal"
        elif col == "Creatinine":
            status = "High" if val > 100 else "Normal"
        elif col == "Albumin":
            status = "Low" if val < 35 else "Normal"
        elif col == "BMI":
            status = "High" if val > 25 else "Normal"
        else:
            status = "Normal"
        profile[col] = f"{val} → {status}"
    st.json(profile)

    # 🌐 Radar-plot (spider chart) for pasientprofil
    st.write("### Radar plot of patient biomarkers")
    categories = list(numeric_df.columns)
    values = [patient[col] for col in categories]

    # Normaliser verdier (0-1 skala for sammenligning)
    max_vals = numeric_df[categories].max()
    min_vals = numeric_df[categories].min()
    norm_values = [(val - min_vals[col]) / (max_vals[col] - min_vals[col]) if max_vals[col] != min_vals[col] else 0.5 for col, val in zip(categories, values)]

    # Radar-plot setup
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    norm_values += norm_values[:1]
    angles += angles[:1]

    fig_radar, ax_radar = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax_radar.plot(angles, norm_values, color="blue", linewidth=2)
    ax_radar.fill(angles, norm_values, color="lightblue", alpha=0.4)
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(categories)
    ax_radar.set_yticklabels([])
    ax_radar.set_title(f"Patient {idx} biomarker profile (normalized)", size=14)

    st.pyplot(fig_radar)
