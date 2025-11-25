import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import shap
import streamlit.components.v1 as components

from app.icons import show_icon
from app.eda import run_eda
from models.train import split_data, train_logistic_regression, train_random_forest
from models.predict import safe_predict
from models.explainer import get_explainer, get_shap_values

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score
)

def run_prediction(df: pd.DataFrame):
    st.markdown("---")
    show_icon("search", "Run Prediction", size=32)

    required_columns = ["CRP", "Creatinine", "Albumin", "BMI"]
    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        st.error(f"Missing required columns: {missing}")
        st.write(list(df.columns))
        return

    # Dummy target
    df["target"] = (df["CRP"] > 5).astype(int)

    # 📊 Diagnostikk: vis klassefordeling
    st.write("Class distribution before split:", df["target"].value_counts().to_dict())

    # Split data
    X_train, X_test, y_train, y_test = split_data(df, required_columns)

    # --- Nytt: sjekk antall klasser ---
    if len(y_train.unique()) < 2:
        st.error("⚠️ Training data contains only one class. Cannot train model.")
        st.write("Class distribution:", y_train.value_counts().to_dict())
        return

    # Modellvalg
    model_choice = st.radio("Select model:", ["Logistic Regression", "Random Forest"])

    try:
        if model_choice == "Logistic Regression":
            model, scaler = train_logistic_regression(X_train, y_train)
            predictions = safe_predict(model, X_test, scaler=scaler)
            X_test_final = scaler.transform(X_test)
            explainer = get_explainer(model, scaler.transform(X_train), model_type="lr", feature_names=X_train.columns)
            shap_values = get_shap_values(explainer, X_test_final, model_type="lr")
        else:
            model = train_random_forest(X_train, y_train)
            predictions = safe_predict(model, X_test)
            X_test_final = X_test
            explainer = get_explainer(model, X_train, model_type="rf")
            shap_values = get_shap_values(explainer, X_test_final, model_type="rf")
    except Exception as e:
        st.error(f"Model training failed: {e}")
        return

    # Resultater
    df_result = X_test.copy()
    df_result["Prediction"] = predictions
    df_result["True Label"] = y_test.values
    st.success("✅ Prediction completed!")
    st.dataframe(df_result)

    # 📊 Classification Report
    show_icon("chart", "Classification Report", size=32)
    try:
        st.text(classification_report(y_test, predictions))
    except Exception as e:
        st.error(f"Classification report failed: {e}")

    # 🧩 Confusion Matrix
    st.markdown("### 🧩 Confusion Matrix")
    try:
        cm = confusion_matrix(y_test, predictions)
        st.write(pd.DataFrame(cm, index=["True 0","True 1"], columns=["Pred 0","Pred 1"]))
    except Exception as e:
        st.error(f"Confusion matrix failed: {e}")

    # 📈 ROC Curve & AUC
    st.markdown("### 📈 ROC Curve & AUC")
    try:
        y_score = model.predict_proba(X_test_final)[:, 1]
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

    # 📉 Precision-Recall Curve
    st.markdown("### 📉 Precision-Recall Curve")
    try:
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

    # 🧑‍⚕️ Inspect Individual Prediction
    st.markdown("### 🧑‍⚕️ Inspect Individual Prediction (force plot)")
    if len(X_test_final) > 0:
        idx = st.number_input("Select test case index", min_value=0, max_value=len(X_test_final)-1, value=0)
        st.write("True label:", y_test.iloc[idx])
        st.write("Predicted:", predictions[idx])

        try:
            shap_values_to_use = shap_values[..., 1] if hasattr(shap_values, "values") and shap_values.values.ndim == 3 else shap_values
            viz = shap.plots.force(shap_values_to_use[idx])
            html = f"<head>{shap.getjs()}</head><body>{viz.html()}</body>"
            components.html(html, height=300)
        except Exception as e:
            st.error(f"Force plot failed: {e}")

    # TODO: Juster SHAP-plot størrelse og stil ved sluttpuss
    show_icon("chart", "SHAP Summary Plot", size=32)
    try:
        st.write(f"SHAP summary for model: {model.__class__.__name__}")

        if model.__class__.__name__ == "RandomForestClassifier":
            shap.summary_plot(
                shap_values.values if hasattr(shap_values, "values") else shap_values,
                X_test,
                plot_type="bar",
                max_display=10,
                show=False
            )
            fig = plt.gcf()  # hent figuren SHAP faktisk tegnet på
            fig.set_size_inches(8, 4)  # juster størrelse
            st.pyplot(fig)
        else:
            shap.summary_plot(
                shap_values.values if hasattr(shap_values, "values") else shap_values,
                X_test,
                plot_type="dot",
                show=False
            )
            fig = plt.gcf()
            fig.set_size_inches(10, 6)
            st.pyplot(fig)
    except Exception as e:
        st.error(f"SHAP summary failed: {e}")
