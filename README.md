# Credit Scoring & Borrower Segmentation

## Professional focus
A credit-risk analytics project exploring borrower profiling, credit characteristics and risk segmentation using Python. The business context is retail/MSME lending: support consistent borrower assessment, portfolio monitoring and risk-based decision support.

## Business questions
- What borrower characteristics and loan attributes are present in the dataset?
- How do credit utilisation, payment-history fields and loan characteristics vary across segments?
- Can borrowers be grouped into interpretable risk or behaviour segments?
- What additional outcome data would be required to build a defensible Probability of Default (PD) model?

## Dataset and modelling limitation
The supplied `credit_scoring.csv` contains 1,000 records and 12 fields, including age, employment status, credit utilisation, payment history, credit-account count, loan amount, interest rate, loan term and loan type. The currently identified schema does **not** contain an explicit default, delinquency or bad-loan outcome.

Therefore:
- Treat this dataset as suitable for data quality review, exploratory analysis and descriptive segmentation.
- Do not describe an unsupervised segment or an arbitrary proxy as a validated PD model.
- Before supervised credit scoring, define a target such as 90+ days past due/default within a stated performance window, with a clear observation date and outcome definition.
- Confirm the meaning and provenance of `Payment History` before using it as a predictor or target.

## Planned analytical workflow
1. Data audit: schema, missing values, duplicates, ranges and category consistency.
2. Exploratory analysis: borrower profile, utilisation, loan size, pricing and term.
3. Segmentation: interpretable borrower groups and business descriptions.
4. If a valid outcome becomes available: train/test split before preprocessing; WOE/IV, logistic regression and score scaling; compare with a baseline.
5. Validation: ROC-AUC, KS, Gini, confusion matrix, calibration and stability checks where appropriate.
6. Business interpretation: risk drivers, limitations and responsible-use considerations.

## Tools
Python, pandas, NumPy, scikit-learn, Matplotlib/Seaborn (as applicable).

## Repository contents
- `Credit Scoring and Segmentation using Python.ipynb` — original analysis notebook.
- `credit_scoring.csv` — dataset used by the notebook.

## Next improvements
- Add a reproducible data dictionary and data-quality report.
- Separate descriptive segmentation from supervised default prediction.
- Add a synthetic, clearly labelled default-outcome dataset only if a modelling demonstration is needed; never present synthetic outcomes as actual bank performance.
- Add tests and a requirements file as the project is refactored.

## Disclaimer
This is an educational portfolio project, not a production credit decision system. No real customer data or confidential bank information should be uploaded.
