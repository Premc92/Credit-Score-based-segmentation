"""Generate a reproducible synthetic Indian retail-loan portfolio.

All data is fictional. The target is simulated for learning and is not a
representation of actual bank default experience.
"""
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_FILE = DATA_DIR / "credit_portfolio.csv"


def generate_portfolio(n_rows: int = 5000, random_state: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_state)

    age = rng.integers(21, 66, n_rows)
    monthly_income = np.clip(rng.lognormal(mean=10.7, sigma=0.55, size=n_rows), 12000, 500000)
    employment_type = rng.choice(
        ["Salaried", "Self-employed", "Business"], n_rows, p=[0.62, 0.25, 0.13]
    )
    bureau_score = np.clip(rng.normal(710, 55, n_rows), 450, 900).round().astype(int)
    credit_utilisation = np.clip(rng.beta(2.2, 3.0, n_rows), 0.01, 0.99)
    prior_delinquency = rng.binomial(1, 0.18, n_rows)
    open_loan_count = rng.poisson(2.0, n_rows)
    loan_amount = np.clip(monthly_income * rng.uniform(5, 30, n_rows), 50000, 5000000)
    interest_rate = np.clip(
        10.5 + (720 - bureau_score) * 0.025 + rng.normal(0, 1.1, n_rows), 8, 26
    )
    tenure_months = rng.choice([12, 24, 36, 48, 60, 72, 84], n_rows)
    loan_purpose = rng.choice(
        ["Personal", "Home Improvement", "Vehicle", "Business", "Education"],
        n_rows,
        p=[0.32, 0.12, 0.22, 0.22, 0.12],
    )

    # Synthetic log-odds: deliberately create plausible directional signals.
    log_odds = (
        -2.35
        + 0.95 * prior_delinquency
        + 1.15 * credit_utilisation
        + 0.22 * open_loan_count
        - 0.010 * (bureau_score - 700)
        + 0.00000012 * (loan_amount / np.maximum(monthly_income, 1))
        + 0.012 * (interest_rate - 12)
        + 0.18 * (employment_type != "Salaried")
        - 0.008 * (age - 40)
    )
    probability = 1 / (1 + np.exp(-log_odds))
    default_12m = rng.binomial(1, probability)

    start = pd.Timestamp("2022-01-01")
    month_offsets = rng.integers(0, 48, n_rows)
    origination_date = start + pd.to_timedelta(month_offsets * 30, unit="D")

    # Monitoring values are synthetic snapshots and are not model features.
    current_dpd = np.where(
        default_12m == 1,
        rng.choice([30, 60, 90, 120, 180], n_rows, p=[0.12, 0.15, 0.28, 0.25, 0.20]),
        rng.choice([0, 5, 15, 30, 60], n_rows, p=[0.72, 0.10, 0.08, 0.07, 0.03]),
    )
    outstanding_balance = np.round(
        loan_amount * rng.uniform(0.15, 0.95, n_rows), 2
    )
    dpd_bucket = pd.cut(
        current_dpd,
        bins=[-1, 0, 30, 60, 90, np.inf],
        labels=["Current", "1-30", "31-60", "61-90", "90+"],
    ).astype(str)

    df = pd.DataFrame(
        {
            "account_id": [f"SYN{i:06d}" for i in range(1, n_rows + 1)],
            "origination_date": pd.to_datetime(origination_date).strftime("%Y-%m-%d"),
            "age": age,
            "monthly_income_inr": monthly_income.round(2),
            "employment_type": employment_type,
            "bureau_score": bureau_score,
            "credit_utilisation": credit_utilisation.round(4),
            "prior_delinquency_12m": prior_delinquency,
            "open_loan_count": open_loan_count,
            "loan_amount_inr": loan_amount.round(2),
            "interest_rate_pct": interest_rate.round(2),
            "tenure_months": tenure_months,
            "loan_purpose": loan_purpose,
            "default_12m": default_12m,
            "current_dpd": current_dpd,
            "dpd_bucket": dpd_bucket,
            "outstanding_balance_inr": outstanding_balance,
            "data_label": "SYNTHETIC",
        }
    )
    return df


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    portfolio = generate_portfolio()
    portfolio.to_csv(OUTPUT_FILE, index=False)
    print(f"Created {len(portfolio):,} synthetic accounts: {OUTPUT_FILE}")
    print(f"12-month default rate: {portfolio['default_12m'].mean():.2%}")
