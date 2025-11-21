import shap

def get_explainer(model, X_train, model_type="rf", feature_names=None):
    if model_type == "lr":
        return shap.LinearExplainer(model, X_train, feature_names=feature_names)
    else:
        return shap.TreeExplainer(model)

def get_shap_values(explainer, X_test, model_type="rf"):
    if model_type == "rf":
        return explainer(X_test, check_additivity=False)
    else:
        return explainer(X_test)
