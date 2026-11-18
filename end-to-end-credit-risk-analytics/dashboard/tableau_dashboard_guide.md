# Tableau Public — Credit Risk Dashboard Build Guide

## Data connection
1. Run `python src/generate_synthetic_data.py`.
2. Open Tableau Public and connect to the generated `data/credit_portfolio.csv`.
3. Confirm `origination_date` is Date and amount/income fields are numeric.
4. Keep a visible note on every dashboard: **Synthetic educational data — not actual bank performance.**

## Calculated fields

**DPD 30+ Flag**
```tableau
IF [current_dpd] >= 30 THEN 1 ELSE 0 END
```

**DPD 90+ Flag**
```tableau
IF [current_dpd] >= 90 THEN 1 ELSE 0 END
```

**Synthetic Default Flag**
Use `default_12m` as supplied. Do not rename it as actual or observed bank default.

**Bureau Score Band**
```tableau
IF [bureau_score] < 600 THEN "<600"
ELSEIF [bureau_score] < 650 THEN "600-649"
ELSEIF [bureau_score] < 700 THEN "650-699"
ELSEIF [bureau_score] < 750 THEN "700-749"
ELSE "750+"
END
```

## Dashboard 1 — Portfolio Overview
- KPI cards: account count, total outstanding exposure, average loan amount, synthetic 12-month default rate.
- Bar chart: outstanding exposure by employment type.
- Donut or bar chart: account distribution by loan purpose.
- Filters: origination month, employment type, loan purpose.

## Dashboard 2 — Delinquency Monitoring
- Bar chart: account count by DPD bucket.
- KPI: DPD 30+ account rate and DPD 90+ account rate.
- Bar chart: outstanding exposure by DPD bucket.
- Segment by employment type and bureau-score band.

## Dashboard 3 — Vintage & Risk Segmentation
- Trend: synthetic default rate by origination month.
- Heatmap: bureau-score band by employment type.
- Bar chart: outstanding exposure by bureau-score band.
- Add a tooltip explaining that the outcome is simulated.

## Suggested interview narrative
"This dashboard demonstrates how I would structure a retail credit portfolio monitoring pack: exposure, delinquency, vintage and borrower-segment views. The underlying data is synthetic, so I use it to demonstrate the analytical workflow rather than claim actual portfolio results."

## Publishing and privacy
Only publish this synthetic dataset. Never upload identifiable borrower data, account numbers, bank statements or confidential portfolio extracts to Tableau Public.
