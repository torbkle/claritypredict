import pandas as pd
import numpy as np

def generate_synthetic_data(n_samples=100, seed=42):
    np.random.seed(seed)

    data = {
        "CRP": np.round(np.random.normal(loc=4.0, scale=2.5, size=n_samples), 2),
        "Creatinine": np.round(np.random.normal(loc=80, scale=15, size=n_samples), 1),
        "Albumin": np.round(np.random.normal(loc=40, scale=5, size=n_samples), 1),
        "BMI": np.round(np.random.normal(loc=24, scale=4, size=n_samples), 1),
    }

    df = pd.DataFrame(data)

    # Bare lagre til fil hvis funksjonen kjøres direkte
    if __name__ == "__main__":
        df.to_csv("data/example.csv", index=False)
        print("✅ Synthetic data saved to data/example.csv")

    return df

