import pandas as pd
import numpy as np

def generate_synthetic_data(n_samples=100, seed=42):
    np.random.seed(seed)

    # Demografi
    age = np.random.randint(18, 90, size=n_samples)
    sex = np.random.choice(["Male", "Female"], size=n_samples)

    # Biomarkører og labverdier
    crp = np.clip(np.random.normal(loc=4.0, scale=3.0, size=n_samples), 0, 100)
    cystatin_c = np.clip(np.random.normal(loc=0.95, scale=0.2, size=n_samples), 0.5, 2.5)
    creatinine = np.clip(np.random.normal(loc=80, scale=15, size=n_samples), 40, 150)
    albumin = np.clip(np.random.normal(loc=40, scale=4, size=n_samples), 25, 50)
    egfr = np.clip(120 - 0.8 * creatinine + np.random.normal(0, 5, size=n_samples), 15, 120)
    urea = np.clip(np.random.normal(loc=5.5, scale=1.5, size=n_samples), 2, 15)
    hemoglobin = np.where(
        sex == "Male",
        np.random.normal(loc=15.0, scale=1.0, size=n_samples),
        np.random.normal(loc=13.5, scale=1.0, size=n_samples)
    )
    wbc = np.clip(np.random.normal(loc=6.5, scale=1.5, size=n_samples), 3, 15)
    bmi = np.clip(np.random.normal(loc=24, scale=4, size=n_samples), 16, 40)

    # Diagnoser basert på CRP og eGFR
    diagnosis = np.where(
        crp > 20, "Infection",
        np.where(egfr < 60, "CKD", "Healthy")
    )

    df = pd.DataFrame({
        "Age": age,
        "Sex": sex,
        "CRP": np.round(crp, 2),
        "Cystatin_C": np.round(cystatin_c, 2),
        "Creatinine": np.round(creatinine, 1),
        "eGFR": np.round(egfr, 1),
        "Albumin": np.round(albumin, 1),
        "Urea": np.round(urea, 1),
        "Hemoglobin": np.round(hemoglobin, 1),
        "WBC": np.round(wbc, 1),
        "BMI": np.round(bmi, 1),
        "Diagnosis": diagnosis
    })

    if __name__ == "__main__":
        df.to_csv("data/example.csv", index=False)
        print("✅ Synthetic data saved to data/example.csv")

    return df
