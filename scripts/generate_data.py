import pandas as pd
import numpy as np

def generate_synthetic_data(n_samples=100, seed=42):
    np.random.seed(seed)

    # Demografi
    age = np.random.randint(18, 90, size=n_samples)
    sex = np.random.choice(["Male", "Female"], size=n_samples)

    # Biomarkører
    crp = np.clip(np.random.normal(loc=4.0, scale=3.0, size=n_samples), 0, 100)
    creatinine = np.clip(np.random.normal(loc=80, scale=15, size=n_samples), 40, 150)
    egfr = np.clip(120 - 0.8 * creatinine + np.random.normal(0, 5, size=n_samples), 15, 120)
    albumin = np.clip(np.random.normal(loc=40, scale=4, size=n_samples), 25, 50)
    ntprobnp = np.clip(np.random.lognormal(mean=6, sigma=0.5, size=n_samples), 50, 5000)
    bmi = np.clip(np.random.normal(loc=24, scale=4, size=n_samples), 16, 40)

    # Diagnose
    diagnosis = np.where(
        crp > 20, "Infection",
        np.where(egfr < 60, "CKD",
        np.where(ntprobnp > 1000, "Heart Failure", "Healthy"))
    )

    df = pd.DataFrame({
        "Age": age,
        "Sex": sex,
        "CRP": np.round(crp, 2),
        "Creatinine": np.round(creatinine, 1),
        "eGFR": np.round(egfr, 1),
        "Albumin": np.round(albumin, 1),
        "NT_proBNP": np.round(ntprobnp, 1),
        "BMI": np.round(bmi, 1),
        "Diagnosis": diagnosis
    })

    # --- Lag target ---
    df["target"] = (
        (df["CRP"] > 5) |
        (df["eGFR"] < 60) |
        (df["NT_proBNP"] > 1000)
    ).astype(int)

    # --- Garanter 50/50 balanse ---
    half = n_samples // 2
    df.loc[:half-1, "target"] = 0
    df.loc[half:, "target"] = 1

    return df
