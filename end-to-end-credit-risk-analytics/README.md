# End-to-End Credit Risk Analytics
## PD Modelling, Credit Scorecard & Portfolio Monitoring

**Portfolio project | Synthetic Indian retail-loan data | Python + SQL + Tableau**

This project demonstrates an end-to-end credit-risk workflow similar to analytical work performed by a bank or NBFC risk team. It covers borrower-level data generation, data-quality checks, exploratory analysis, Probability of Default (PD) modelling, model validation, score scaling, portfolio monitoring and dashboard design.

> **Data and model disclaimer:** All records are synthetically generated for education and demonstration. They are not real borrowers, bank records or observed default outcomes. Model metrics are illustrative and must not be interpreted as evidence of production performance or used for lending decisions.

## 1. Business problem

A lender wants to understand borrower risk at origination and monitor the loan portfolio over time. The analytical objectives are to:

1. Estimate a 12-month default probability using information available at the time of application.
2. Rank borrowers by estimated risk and translate model outputs into an illustrative score.
3. Evaluate discrimination and calibration on an untouched test sample.
4. Monitor delinquency, outstanding exposure and vintage performance.
5. Communicate risk trends through a Tableau dashboard.

## 2. Project architecture

```text
end-to-end-credit-risk-analytics/
├── README.md
├── requirements.txt
├── data/
│   └── README.md
├── src/
│   ├── generate_synthetic_data.py
│   ├── train_pd_model.py
│   └── portfolio_monitoring.py
├── sql/
│   └── portfolio_risk_queries.sql
└── dashboard/
    └── tableau_dashboard_guide.md
```

## 3. Dataset design

The generator creates a reproducible synthetic portfolio with application-time fields such as age, income, employment type, bureau score, utilisation, prior delinquency, loan amount, interest rate and tenure.

It also creates outcome/monitoring fields such as the 12-month default flag, current DPD bucket and outstanding balance. **Outcome and monitoring fields are not model predictors.** The PD model uses only application-time variables to avoid target leakage.

Run the generator:

```bash
python src/generate_synthetic_data.py
```

It creates `data/credit_portfolio.csv`.

## 4. Run the PD model

```bash
pip install -r requirements.txt
python src/train_pd_model.py
```

The training script:
- separates the target from application-time predictors;
- creates a stratified train/test split;
- fits imputation, scaling and one-hot encoding inside a scikit-learn pipeline;
- trains a logistic regression model;
- reports ROC-AUC, Gini, KS, PR-AUC, Brier score and confusion matrix;
- saves test-set predictions and model artefacts under `outputs/`.

The test set is held out from model fitting. Metrics should be read together: discrimination metrics assess ranking, while Brier score and calibration plots assess probability quality.

## 5. Portfolio monitoring

Run:

```bash
python src/portfolio_monitoring.py
```

The script produces a monthly summary of account count, outstanding exposure, 30+ DPD rate, 90+ DPD rate and observed synthetic default rate. It also produces vintage summaries. These are descriptive monitoring views, not causal analyses.

## 6. SQL analysis

Open `sql/portfolio_risk_queries.sql` and run the queries against the generated CSV after loading it into a SQL database/table named `credit_portfolio`. Queries cover DPD buckets, portfolio exposure, vintage and concentration.

## 7. Tableau dashboard

Follow `dashboard/tableau_dashboard_guide.md` to connect Tableau Public to `data/credit_portfolio.csv` and build:
- Portfolio overview
- Delinquency and risk trends
- Vintage performance
- Risk segmentation and concentration

Do not publish real customer-level or confidential bank data to Tableau Public.

## 8. Key credit-risk concepts demonstrated

| Concept | Meaning |
|---|---|
| PD | Probability that a borrower defaults within a defined horizon |
| DPD | Days past due, used to monitor delinquency |
| ROC-AUC | Ranking/discrimination across thresholds |
| Gini | (2 \times ROC\text{-}AUC - 1) |
| KS | Maximum separation between good and bad cumulative distributions |
| PR-AUC | Precision-recall performance, useful with class imbalance |
| Brier score | Mean squared error of predicted probabilities |
| Vintage | Performance of accounts grouped by origination period |

## 9. Important limitations and next steps

- Synthetic target generation creates a known illustrative relationship; real-world performance will be different.
- A production PD model needs a formally approved default definition, observation date, performance window, representative historical data and out-of-time validation.
- Add WOE/IV binning and a traditional scorecard comparison after the baseline pipeline is understood.
- Add calibration, stability (PSI), reject inference considerations, fairness review and independent model validation before any production use.
- Extend to LGD, EAD and IFRS 9 ECL only with appropriate workout, recovery, exposure and scenario data.

## 10. Learning outcomes

By completing this project, you should be able to explain the business objective, target definition, leakage controls, train/test methodology, logistic regression, probability outputs, validation metrics, portfolio indicators and dashboard interpretation in a Credit Risk Analyst interview.
