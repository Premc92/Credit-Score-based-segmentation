"""Create descriptive portfolio and vintage monitoring summaries."""
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "credit_portfolio.csv"
OUTPUT_DIR = ROOT / "outputs"


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Dataset not found. Run: python src/generate_synthetic_data.py"
        )

    df = pd.read_csv(DATA_FILE, parse_dates=["origination_date"])
    df["origination_month"] = df["origination_date"].dt.to_period("M").astype(str)
    df["dpd_30_plus"] = (df["current_dpd"] >= 30).astype(int)
    df["dpd_90_plus"] = (df["current_dpd"] >= 90).astype(int)

    monthly = (
        df.groupby("origination_month", as_index=False)
        .agg(
            account_count=("account_id", "count"),
            outstanding_exposure_inr=("outstanding_balance_inr", "sum"),
            dpd_30_plus_accounts=("dpd_30_plus", "sum"),
            dpd_90_plus_accounts=("dpd_90_plus", "sum"),
            synthetic_defaults=("default_12m", "sum"),
        )
    )
    monthly["dpd_30_plus_rate"] = (
        monthly["dpd_30_plus_accounts"] / monthly["account_count"]
    )
    monthly["dpd_90_plus_rate"] = (
        monthly["dpd_90_plus_accounts"] / monthly["account_count"]
    )
    monthly["synthetic_default_rate"] = (
        monthly["synthetic_defaults"] / monthly["account_count"]
    )

    vintage = (
        df.groupby("origination_month", as_index=False)
        .agg(
            originated_accounts=("account_id", "count"),
            originated_amount_inr=("loan_amount_inr", "sum"),
            synthetic_default_rate=("default_12m", "mean"),
        )
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    monthly.to_csv(OUTPUT_DIR / "monthly_portfolio_summary.csv", index=False)
    vintage.to_csv(OUTPUT_DIR / "vintage_summary.csv", index=False)

    print("Monthly portfolio summary (synthetic snapshot):")
    print(monthly.head(12).to_string(index=False))
    print("\nVintage summary:")
    print(vintage.head(12).to_string(index=False))
    print("\nOutputs saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
