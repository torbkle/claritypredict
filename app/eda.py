import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda(df: pd.DataFrame, required_columns=None):
    st.markdown("---")
    st.markdown("## 🔎 Exploratory Data Analysis")

    # Hvis required_columns ikke er gitt, bruk alle kolonner
    if required_columns is None:
        required_columns = df.columns.tolist()

    # 1. Distribusjoner
    st.markdown("### 📊 Distributions")
    for col in required_columns:
        fig, ax = plt.subplots()
        df[col].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
        ax.set_title(f"Distribution of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    # 2. Korrelasjoner
    st.markdown("### 🔗 Correlation Heatmap")
    corr = df[required_columns].corr()
    fig_corr, ax_corr = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax_corr)
    st.pyplot(fig_corr)

    # 3. Outliers
    st.markdown("### 🚨 Outliers (Boxplots)")
    fig_box, ax_box = plt.subplots()
    df[required_columns].boxplot(ax=ax_box)
    ax_box.set_title("Boxplots of Biomarkers")
    st.pyplot(fig_box)
