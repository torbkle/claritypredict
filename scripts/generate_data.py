import pandas as pd
import numpy as np

def generate_synthetic_data(n_samples=100, seed=42):
    np.random.seed(seed)

    data = {
        "CRP": np.round(np.random.normal(loc=4.0, scale=2.5, size=n_samples), 2),             # C-reactive protein (mg/L)
        "Creatinine": np.round(np.random.normal(loc=80, scale=15, size=n_samples), 1),        # Creatinine (µmol/L)
        "Albumin": np.round(np.random.normal(loc=40, scale=5, size=n_samples), 1),            # Albumin (g/L)
        "BMI": np.round(np.random.normal(loc=24, scale=4, size=n_samples), 1),                # Body Mass Index (kg/m²)
    }

    df = pd.DataFrame(data)
    df.to_csv("data/example.csv", index=False)
    print("✅ Synthetic data saved to data/example.csv")

if __name__ == "__main__":
    generate_synthetic_data()
