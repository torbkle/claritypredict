import pytest
import pandas as pd
import numpy as np

from models.train import split_data, train_logistic_regression, train_random_forest
from models.predict import safe_predict
from models.explainer import get_explainer, get_shap_values

# Dummy datasett for testing
@pytest.fixture
def dummy_df():
    data = {
        "CRP": [1.0, 10.0, 3.5, 7.2],
        "Creatinine": [90, 110, 85, 130],
        "Albumin": [40, 35, 42, 38],
        "BMI": [22, 28, 25, 30],
    }
    df = pd.DataFrame(data)
    df["target"] = (df["CRP"] > 5).astype(int)
    return df

def test_logistic_regression_pipeline(dummy_df):
    X_train, X_test, y_train, y_test = split_data(dummy_df, ["CRP","Creatinine","Albumin","BMI"])
    model, scaler = train_logistic_regression(X_train, y_train)
    preds = safe_predict(model, X_test, scaler=scaler)
    assert len(preds) == len(y_test)
    explainer = get_explainer(model, scaler.transform(X_train), model_type="lr", feature_names=X_train.columns)
    shap_values = get_shap_values(explainer, scaler.transform(X_test), model_type="lr")
    assert shap_values is not None

def test_random_forest_pipeline(dummy_df):
    X_train, X_test, y_train, y_test = split_data(dummy_df, ["CRP","Creatinine","Albumin","BMI"])
    model = train_random_forest(X_train, y_train)
    preds = safe_predict(model, X_test)
    assert len(preds) == len(y_test)
    explainer = get_explainer(model, X_train, model_type="rf")
    shap_values = get_shap_values(explainer, X_test, model_type="rf")
    assert shap_values is not None
