# Loan Applicant Data - Exploratory Data Analysis

## 🎯 Objective

The goal of this project is to perform an exploratory data analysis (EDA) on a
loan applicant dataset. The analysis covers:

- Loading and inspecting the dataset structure
- Generating summary statistics for numeric columns
- Computing the mean, median and standard deviation of a key numeric
  variable
- Visualizing the relationship between two numeric features
- Visualizing correlation between all numeric features via a heatmap

> **Note on the "price" column:** The task template refers to a `price`
> column, but this dataset (`loan.csv`) is a loan-applicant dataset and has
> no such column. The nearest equivalent, the numeric value that varies per
> record and drives the loan, is **`loan_amnt`** (the requested loan
> amount) so that column is used wherever "price" was specified.

## 🛠 Libraries Used

| Library | Purpose |
|---|---|
| `pandas` | Loading and manipulating the dataset |
| `matplotlib` | Base plotting engine |
| `seaborn` | Statistical visualizations (scatter plot, heatmap) |
| `os` | Managing output file paths |

Install dependencies with:

```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
loan-data-analysis/
├── analysis.py              # Main analysis script (run this)
├── data/
│   └── loan.csv              # Dataset
├── outputs/
│   ├── relationship_scatter.png
│   └── correlation_heatmap.png
├── requirements.txt
└── README.md
```

## ▶️ How to Run

```bash
python analysis.py
```

The script will print inspection details and summary statistics to the
console and save two plots to the `outputs/` folder.

## 📊 Dataset Overview

- **Rows:** 45,015
- **Columns:** 12 (6 numeric, 5 categorical/text, 1 binary target)
- **Target-like column:** `loan_status` (0 = not defaulted, 1 = defaulted)
- **Key columns:** `loan_amnt`, `loan_int_rate`, `loan_percent_income`,
  `person_income`, `cb_person_cred_hist_length`, `loan_intent`,
  `person_education`, `person_home_ownership`

Missing values are minimal, only 1–2 rows are missing values in a few
columns out of 45,015 total rows.

## 🔢 `loan_amnt` Central Tendency & Spread

| Statistic | Value |
|---|---|
| Mean | 65,120.40 |
| Median | 8,000.00 |
| Std. Deviation | 8,496,802.40 |

**Important finding:** the mean and standard deviation are wildly distorted
by a tiny number of corrupted rows — two records list a `loan_amnt` of
**1,000,000,000** and **1,500,000,000**, far outside any realistic loan size
(typical values in the dataset range from $500 to ~$35,000). A similar issue
appears in `cb_person_cred_hist_length`, where one row has a value of
500,000 (years of credit history). These are almost certainly data-entry
errors.

Because of this, the **median ($8,000)** is a far more reliable measure of
the "typical" loan amount than the mean. In a production analysis, these
outlier rows should be investigated and likely removed or corrected before
modeling.

## 📈 Relationship Between Two Numerical Features

`person_income` vs. `loan_amnt` is plotted as a scatter plot
(`outputs/relationship_scatter.png`). Because of the extreme outliers
described above, points are shown at the 99th-percentile range for
readability (outliers are kept in all statistical calculations, only
excluded from this one plot).

**Observation:** loan amount rises with income at the lower end but plateaus
—most applicants, regardless of income, request loans clustered at common
"round number" amounts (e.g. $5,000, $10,000, $15,000, $20,000, $25,000),
visible as horizontal bands in the plot. Income alone does not appear to be
a strong predictor of loan size.

## 🔥 Correlation Heatmap

`outputs/correlation_heatmap.png` shows pairwise correlation between all
numeric features. **Spearman (rank-based) correlation is used instead of the
default Pearson method**, because Pearson correlation is highly sensitive to
outliers — with the billion-dollar `loan_amnt` rows included, Pearson
correlations collapse to near-zero everywhere and hide the real
relationships in the data.

Key relationships observed:
- `loan_amnt` and `loan_percent_income` are strongly positively correlated
  (**ρ ≈ 0.67**) - larger loans naturally represent a larger share of the
  applicant's income.
- `loan_percent_income` and `person_income` are moderately negatively
  correlated (**ρ ≈ -0.35**) - higher earners request loans that make up a
  smaller fraction of their income.
- `loan_int_rate` and `loan_percent_income` are both positively correlated
  with `loan_status` (default), suggesting higher interest rates and a
  larger loan-to-income ratio are both associated with a higher chance of
  default.
- `person_income` is negatively correlated with `loan_status`
  (**ρ ≈ -0.27**), higher-income applicants default less often.

## 📝 Summary

Overall default rate in this dataset is about **22.2%**. The analysis
suggests loan-to-income ratio and interest rate are more informative signals
of default risk than raw loan amount or income alone, a useful direction
for any follow-up predictive modeling work.
