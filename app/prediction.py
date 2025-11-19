import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import shap
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

from app.icons import show_icon
from app.eda import run_eda   # 👈 riktig import

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

    # Modellvalg
    model_choice = st.radio("Select model:", ["Logistic Regression", "Random Forest"])

    if model_choice == "Logistic Regression":
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        model = LogisticRegression()
        model.fit(X_train_scaled, y_train)
        predictions = model.predict(X_test_scaled)
        X_used_train, X_used_test = X_train_scaled, X_test_scaled
        explainer = shap.LinearExplainer(model, X_train_scaled, feature_names=X.columns)
        shap_values = explainer(X_test_scaled)
    else:
        model = RandomForestClassifier(n_estimators=200, random_state=42)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        X_used_train, X_used_test = X_train, X_test
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(X_test, check_additivity=False)

    # Resultater
    df_result = X_test.copy()
    df_result["Prediction"] = predictions
    df_result["True Label"] = y_test.values

    st.success("✅ Prediction completed!")
    st.dataframe(df_result)

    # Evaluering
    st.markdown("### 📊 Classification Report")
    st.text(classification_report(y_test, predictions))

    st.markdown("### 🧩 Confusion Matrix")
    cm = confusion_matrix(y_test, predictions)
    st.write(pd.DataFrame(cm, index=["True 0","True 1"], columns=["Pred 0","Pred 1"]))

    # 🔹 ROC Curve & AUC
    st.markdown("### 📈 ROC Curve & AUC")
    try:
        from sklearn.metrics import roc_curve, roc_auc_score

        if model_choice == "Logistic Regression":
            y_score = model.predict_proba(X_test_scaled)[:, 1]
        else:
            y_score = model.predict_proba(X_test)[:, 1]

        fpr, tpr, thresholds = roc_curve(y_test, y_score)
        auc_value = roc_auc_score(y_test, y_score)

        fig_roc, ax_roc = plt.subplots()
        ax_roc.plot(fpr, tpr, label=f"AUC = {auc_value:.2f}", color="blue")
        ax_roc.plot([0, 1], [0, 1], linestyle="--", color="gray")
        ax_roc.set_title("ROC Curve")
        ax_roc.set_xlabel("False Positive Rate")
        ax_roc.set_ylabel("True Positive Rate")
        ax_roc.legend(loc="lower right")
        st.pyplot(fig_roc)

        st.success(f"ROC AUC Score: {auc_value:.2f}")
    except Exception as e:
        st.error(f"ROC Curve failed: {e}")

    # 🔹 Precision-Recall Curve
    st.markdown("### 📉 Precision-Recall Curve")
    try:
        from sklearn.metrics import precision_recall_curve, average_precision_score

        if model_choice == "Logistic Regression":
            y_score = model.predict_proba(X_test_scaled)[:, 1]
        else:
            y_score = model.predict_proba(X_test)[:, 1]

        precision, recall, thresholds = precision_recall_curve(y_test, y_score)
        avg_precision = average_precision_score(y_test, y_score)

        fig_pr, ax_pr = plt.subplots()
        ax_pr.plot(recall, precision, color="green", label=f"AP = {avg_precision:.2f}")
        ax_pr.set_title("Precision-Recall Curve")
        ax_pr.set_xlabel("Recall")
        ax_pr.set_ylabel("Precision")
        ax_pr.legend(loc="lower left")
        st.pyplot(fig_pr)

        st.success(f"Average Precision Score: {avg_precision:.2f}")
    except Exception as e:
        st.error(f"Precision-Recall Curve failed: {e}")


    # Force plot
    st.markdown("### 🧑‍⚕️ Inspect Individual Prediction (force plot)")
    idx = st.number_input("Select test case index", min_value=0, max_value=len(X_used_test)-1, value=0)
    st.write("True label:", y_test.iloc[idx])
    st.write("Predicted:", predictions[idx])

    try:
        shap_values_to_use = shap_values[..., 1] if shap_values.values.ndim == 3 else shap_values
        viz = shap.plots.force(shap_values_to_use[idx])
        html = f"<head>{shap.getjs()}</head><body>{viz.html()}</body>"
        components.html(html, height=300)
    except Exception as e:
        st.error(f"Force plot failed: {e}")

    # Bar plot
    st.markdown("### 📊 Average impact per biomarker")
    try:
        fig_bar, ax_bar = plt.subplots()
        if shap_values.values.ndim == 3:
            shap.summary_plot(shap_values.values[:, :, 1], X_test, plot_type="bar", show=False)
        else:
            shap.summary_plot(shap_values.values, X_test, plot_type="bar", show=False)
        st.pyplot(fig_bar)
    except Exception as e:
        st.error(f"Bar plot failed: {e}")

    # Beeswarm plot
    st.markdown("### 🐝 Individual impact per patient (beeswarm)")
    try:
        fig_swarm, ax_swarm = plt.subplots()
        if shap_values.values.ndim == 3:
            shap.summary_plot(shap_values.values[:, :, 1], X_test, plot_type="dot", show=False)
        else:
            shap.summary_plot(shap_values.values, X_test, plot_type="dot", show=False)
        st.pyplot(fig_swarm)
    except Exception as e:
        st.error(f"Beeswarm plot failed: {e}")

    # Dependence plot
    st.markdown("### 📈 SHAP Dependence Plot")
    try:
        feature_name = st.selectbox("Select biomarker for dependence plot", X.columns)
        fig_dep, ax_dep = plt.subplots()
        if shap_values.values.ndim == 3:
            shap.dependence_plot(feature_name, shap_values.values[:, :, 1], X_test, ax=ax_dep, show=False)
        else:
            shap.dependence_plot(feature_name, shap_values.values, X_test, ax=ax_dep, show=False)
        st.pyplot(fig_dep)
    except Exception as e:
        st.error(f"Dependence plot failed: {e}")

    # Sammenligning av to pasienter
    st.markdown("### 👥 Compare Two Patients")
    idx1 = st.number_input("Select first patient index", min_value=0, max_value=len(X_used_test)-1, value=0)
    idx2 = st.number_input("Select second patient index", min_value=0, max_value=len(X_used_test)-1, value=1)
    st.write("Patient 1 - True:", y_test.iloc[idx1], "Predicted:", predictions[idx1])
    st.write("Patient 2 - True:", y_test.iloc[idx2], "Predicted:", predictions[idx2])
    try:
        shap_values_to_use = shap_values[..., 1] if shap_values.values.ndim == 3 else shap_values
        viz1 = shap.plots.force(shap_values_to_use[idx1])
        viz2 = shap.plots.force(shap_values_to_use[idx2])
        html = f"""
        <head>{shap.getjs()}</head>
        <body>
        <h4>Patient {idx1}</h4>{viz1.html()}
        <h4>Patient {idx2}</h4>{viz2.html()}
        </body>
        """
        components.html(html, height=600, scrolling=True)
    except Exception as e:
        st.error(f"Comparison failed: {e}")

    # Modell-sammenligning
    st.markdown("### ⚖️ Model Comparison (Logistic Regression vs Random Forest)")
    try:
        # Logistic Regression explainer
        scaler_lr = StandardScaler()
        X_train_lr = scaler_lr.fit_transform(X_train)
        X_test_lr = scaler_lr.transform(X_test)
        model_lr = LogisticRegression()
        model_lr.fit(X_train_lr, y_train)
        explainer_lr = shap.LinearExplainer(model_lr, X_train_lr, feature_names=X.columns)
        shap_values_lr = explainer_lr(X_test_lr)

        # Random Forest explainer
        model_rf = RandomForestClassifier(n_estimators=200, random_state=42)
        model_rf.fit(X_train, y_train)
        explainer_rf = shap.TreeExplainer(model_rf)
        shap_values_rf = explainer_rf(X_test, check_additivity=False)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Logistic Regression**")
            fig_lr, ax_lr = plt.subplots()
            shap.summary_plot(shap_values_lr.values, X_test, plot_type="bar", show=False)
            st.pyplot(fig_lr)
        with col2:
            st.markdown("**Random Forest**")
            fig_rf, ax_rf = plt.subplots()
            shap.summary_plot(shap_values_rf.values[:, :, 1], X_test, plot_type="bar", show=False)
            st.pyplot(fig_rf)
    except Exception as e:
        st.error(f"Model comparison failed: {e}")


# --- Main app entry point ---
def main():
    st.title("Gentian Predictor / ClarityPredict")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        mode = st.radio("Choose mode:", ["Prediction", "EDA"])
        if mode == "Prediction":
            run_prediction(df)
        else:
            run_eda(df, required_columns=["CRP", "Creatinine", "Albumin", "BMI"])

if __name__ == "__main__":
    main()
