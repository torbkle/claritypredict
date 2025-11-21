import numpy as np
import streamlit as st

def safe_predict(model, X, scaler=None):
    try:
        if scaler is not None:
            X = scaler.transform(X)
        return model.predict(X)
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        return np.zeros(len(X))
