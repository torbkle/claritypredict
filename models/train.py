from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def split_data(df, features, target="target", test_size=0.2, random_state=42):
    X = df[features]
    y = df[target]

    # Prøv stratify først
    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
    except ValueError:
        # Fallback: ingen stratify
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

    # Hvis treningssettet har bare én klasse → bruk hele datasettet som trening
    if y_train.nunique() < 2:
        return X, X, y, y

    return X_train, X_test, y_train, y_test

def train_logistic_regression(X_train, y_train):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_scaled, y_train)
    return model, scaler

def train_random_forest(X_train, y_train, n_estimators=200, random_state=42):
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)
    return model
