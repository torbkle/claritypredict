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

    # Split data
    X_train, X_test, y_train, y_test = split_data(df, required_columns)

    # Modellvalg
    model_choice = st.radio("Select model:", ["Logistic Regression", "Random Forest"])

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

    # Resultater
    df_result = X_test.copy()
    df_result["Prediction"] = predictions
    df_result["True Label"] = y_test.values
    st.success("✅ Prediction completed!")
    st.dataframe(df_result)

    # 📊 Classification Report
    st.markdown("### 📊 Classification Report")
    st.text(classification_report(y_test, predictions))

    # 🧩 Confusion Matrix
    st.markdown("### 🧩 Confusion Matrix")
    cm = confusion_matrix(y_test, predictions)
    st.write(pd.DataFrame(cm, index=["True 0","True 1"], columns=["Pred 0","Pred 1"]))

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

    # 🧑‍⚕️ Force plot
    st.markdown("### 🧑‍⚕️ Inspect Individual Prediction (force plot)")
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

    # 📊 SHAP Summary Plot
    st.markdown("### 📊 SHAP Summary Plot")
    try:
        shap.summary_plot(
            shap_values.values if hasattr(shap_values, "values") else shap_values,
            X_test,
            plot_type="dot",
            show=False
        )
        plt.tight_layout()
        st.pyplot(plt.gcf())
    except Exception as e:
        st.error(f"SHAP summary failed: {e}")

    # ⚖️ Model Comparison
    st.markdown("### ⚖️ Model Comparison (Logistic Regression vs Random Forest)")
    try:
        # Logistic Regression
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        scaler_lr = StandardScaler()
        X_train_lr = scaler_lr.fit_transform(X_train)
        X_test_lr = scaler_lr.transform(X_test)
        model_lr = LogisticRegression()
        model_lr.fit(X_train_lr, y_train)
        explainer_lr = shap.LinearExplainer(model_lr, X_train_lr, feature_names=X_train.columns)
        shap_values_lr = explainer_lr(X_test_lr)

        # Random Forest
        from sklearn.ensemble import RandomForestClassifier
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
