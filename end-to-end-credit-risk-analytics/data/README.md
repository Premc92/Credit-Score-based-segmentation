# Data

The CSV is generated locally by `../src/generate_synthetic_data.py`.

Do not commit generated customer-level files or real banking/customer data. The generator is deterministic when the random seed is unchanged. All rows are synthetic and must be labelled as such in any presentation.

## Main field groups

**Application-time predictors:** age, monthly income, employment type, bureau score, credit utilisation, prior delinquency indicator, open loan count, loan amount, interest rate, tenure and loan purpose.

**Outcome/monitoring fields:** default_12m, origination_date, current_dpd, dpd_bucket and outstanding_balance.

The outcome and monitoring fields are intentionally excluded from the PD model's predictor matrix.
