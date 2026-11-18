"""Train and evaluate an illustrative 12-month PD logistic regression model.

Only application-time variables are used as predictors. Outcome and
post-origination monitoring fields are explicitly excluded.
"""
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "credit_portfolio.csv"
OUTPUT_DIR = ROOT / "outputs"
MODEL_FILE = OUTPUT_DIR / "pd_logistic_pipeline.joblib"
PREDICTIONS_FILE = OUTPUT_DIR / "test_predictions.csv"
ROC_FILE = OUTPUT_DIR / "roc_curve.png"

TARGET = "default_12m"
NUMERIC_FEATURES = [
    "age",
    "monthly_income_inr",
    "bureau_score",
    "credit_utilisation",
    "prior_delinquency_12m",
    "open_loan_count",
    "loan_amount_inr",
    "interest_rate_pct",
    "tenure_months",
]
CATEGORICAL_FEATURES = ["employment_type", "loan_purpose"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def calculate_ks(y_true: pd.Series, probabilities: np.ndarray) -> float:
    """Return the maximum absolute separation of good/bad cumulative rates."""
    frame = pd.DataFrame({"actual": y_true.to_numpy(), "pd": probabilities})
    frame = frame.sort_values("pd", ascending=False)
    total_bad = (frame["actual"] == 1).sum()
    total_good = (frame["actual"] == 0).sum()
    if total_bad == 0 or total_good == 0:
        return float("nan")
    frame["cum_bad"] = (frame["actual"] == 1).cumsum() / total_bad
    frame["cum_good"] = (frame["actual"] == 0).cumsum() / total_good
    return float((frame["cum_bad"] - frame["cum_good"]).abs().max())


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Dataset not found. Run: python src/generate_synthetic_data.py"
        )

    df = pd.read_csv(DATA_FILE)
    required = FEATURES + [TARGET]
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    X = df[FEATURES].copy()
    y = df[TARGET].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessing = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("classifier", LogisticRegression(max_iter=2000, random_state=42)),
        ]
    )
    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.50).astype(int)

    roc_auc = roc_auc_score(y_test, probabilities)
    gini = 2 * roc_auc - 1
    ks = calculate_ks(y_test, probabilities)
    pr_auc = average_precision_score(y_test, probabilities)
    brier = brier_score_loss(y_test, probabilities)

    print("\n=== HOLDOUT TEST RESULTS (SYNTHETIC DATA) ===")
    print(f"Test accounts: {len(y_test):,}")
    print(f"Observed synthetic default rate: {y_test.mean():.2%}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"Gini: {gini:.4f}")
    print(f"KS: {ks:.4f}")
    print(f"PR-AUC / Average Precision: {pr_auc:.4f}")
    print(f"Brier score: {brier:.4f}")
    print("\nConfusion matrix at illustrative 0.50 threshold:")
    print(confusion_matrix(y_test, predictions))
    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prediction_output = X_test.copy()
    prediction_output["actual_default_12m"] = y_test.to_numpy()
    prediction_output["predicted_pd_12m"] = probabilities
    prediction_output["predicted_default_at_50pct"] = predictions
    prediction_output.to_csv(PREDICTIONS_FILE, index=False)
    joblib.dump(model, MODEL_FILE)

    fpr, tpr, _ = roc_curve(y_test, probabilities)
    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, label=f"Logistic regression (AUC={roc_auc:.3f})")
    plt.plot([0, 1], [0, 1], linestyle="--", label="Random baseline")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve — Synthetic Holdout Sample")
    plt.legend()
    plt.tight_layout()
    plt.savefig(ROC_FILE, dpi=150)
    plt.close()

    print(f"\nSaved model: {MODEL_FILE}")
    print(f"Saved predictions: {PREDICTIONS_FILE}")
    print(f"Saved ROC plot: {ROC_FILE}")
    print("\nReminder: synthetic demonstration only; validate calibration and stability on real, representative data.")


if __name__ == "__main__":
    main()
