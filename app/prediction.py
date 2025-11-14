import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import shap
import matplotlib.pyplot as plt
from app.icons import show_icon
def run_prediction(df: pd.DataFrame):
    st.markdown("---")
    show_icon("search", "Run Prediction", size=32)
    required_columns = ["CRP", "Creatinine", "Albumin", "BMI"]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error(f"Missing required columns: {missing}")
        st.markdown("### 📋 Columns found in uploaded file:")
        st.write(list(df.columns))
        return

    # Dummy target for testing
    df["target"] = (df["CRP"] > 5).astype(int)

    # Modellflyt
    X = df[required_columns]
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression()
    model.fit(X_train_scaled, y_train)

    predictions = model.predict(X_test_scaled)
    df_result = X_test.copy()
    df_result["Prediction"] = predictions
    df_result["True Label"] = y_test.values

    st.success("✅ Prediction completed!")
    st.dataframe(df_result)

    # 📊 SHAP explanations with correct feature names
    st.markdown("---")
    show_icon("chart", "SHAP Feature Importance", size=32)
    st.markdown("These plots show which biomarkers most influence the model's predictions.")

    # Create SHAP values with column names
    explainer = shap.Explainer(model, X_train_scaled, feature_names=X.columns)
    shap_values = explainer(X_test_scaled)
    st.markdown("---")
    # 🔹 Bar plot – average impact per feature
    st.markdown("**Average impact per biomarker:**")
    fig_bar, ax_bar = plt.subplots()
    shap.plots.bar(shap_values, show=False)
    st.pyplot(fig_bar)

    # 🔹 Beeswarm plot – individual impact per patient
    st.markdown("**Individual impact per patient:**")
    fig_swarm, ax_swarm = plt.subplots()
    shap.plots.beeswarm(shap_values, show=False)
    st.pyplot(fig_swarm)

