-- Load data/credit_portfolio.csv into a SQL table named credit_portfolio.
-- SQL is written in broadly portable syntax; date functions may need minor
-- adjustment for PostgreSQL, SQL Server, MySQL or SQLite.

-- 1. Portfolio overview
SELECT
    COUNT(*) AS account_count,
    SUM(loan_amount_inr) AS total_originated_amount_inr,
    SUM(outstanding_balance_inr) AS total_outstanding_inr,
    AVG(default_12m * 1.0) AS synthetic_12m_default_rate
FROM credit_portfolio;

-- 2. DPD bucket monitoring
SELECT
    dpd_bucket,
    COUNT(*) AS account_count,
    SUM(outstanding_balance_inr) AS outstanding_exposure_inr,
    AVG(outstanding_balance_inr) AS average_balance_inr
FROM credit_portfolio
GROUP BY dpd_bucket
ORDER BY CASE dpd_bucket
    WHEN 'Current' THEN 1
    WHEN '1-30' THEN 2
    WHEN '31-60' THEN 3
    WHEN '61-90' THEN 4
    ELSE 5
END;

-- 3. Risk segmentation by bureau-score band
SELECT
    CASE
        WHEN bureau_score < 600 THEN '<600'
        WHEN bureau_score < 650 THEN '600-649'
        WHEN bureau_score < 700 THEN '650-699'
        WHEN bureau_score < 750 THEN '700-749'
        ELSE '750+'
    END AS bureau_score_band,
    COUNT(*) AS account_count,
    AVG(default_12m * 1.0) AS synthetic_default_rate,
    SUM(outstanding_balance_inr) AS outstanding_exposure_inr
FROM credit_portfolio
GROUP BY
    CASE
        WHEN bureau_score < 600 THEN '<600'
        WHEN bureau_score < 650 THEN '600-649'
        WHEN bureau_score < 700 THEN '650-699'
        WHEN bureau_score < 750 THEN '700-749'
        ELSE '750+'
    END
ORDER BY bureau_score_band;

-- 4. Origination vintage (calendar month)
SELECT
    SUBSTR(origination_date, 1, 7) AS origination_vintage,
    COUNT(*) AS originated_accounts,
    SUM(loan_amount_inr) AS originated_amount_inr,
    AVG(default_12m * 1.0) AS synthetic_12m_default_rate
FROM credit_portfolio
GROUP BY SUBSTR(origination_date, 1, 7)
ORDER BY origination_vintage;

-- 5. Employment-type concentration
SELECT
    employment_type,
    COUNT(*) AS account_count,
    SUM(outstanding_balance_inr) AS outstanding_exposure_inr,
    AVG(default_12m * 1.0) AS synthetic_default_rate
FROM credit_portfolio
GROUP BY employment_type
ORDER BY outstanding_exposure_inr DESC;

-- Note: default_12m is simulated. These rates are not observed bank portfolio KPIs.
