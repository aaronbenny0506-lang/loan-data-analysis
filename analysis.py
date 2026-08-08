"""
analysis.py
-----------
Exploratory Data Analysis (EDA) on a Loan Applicant dataset.

Tasks performed:
1. Load the dataset using pandas.
2. Inspect the dataset structure (shape, dtypes, missing values, sample rows).
3. Generate summary statistics of all numeric columns.
4. Find the mean, median, and standard deviation of the 'loan_amnt' column
   (this dataset has no 'price' column, so loan_amnt — the size of the
   requested loan — is used as the closest numeric equivalent).
5. Plot the relationship between two numerical features
   (person_income vs. loan_amnt).
6. Visualize correlation between numeric features using a heatmap.

All generated plots are saved to the repo root as PNG files.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
DATA_PATH = "loan.csv"
OUTPUT_DIR = "."

sns.set_theme(style="whitegrid")


def load_data(path: str) -> pd.DataFrame:
    """Step 1: Load the dataset using pandas."""
    df = pd.read_csv(path)
    print(f"Dataset loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns\n")
    return df


def inspect_data(df: pd.DataFrame) -> None:
    """Step 2: Inspect the dataset structure."""
    print("=" * 70)
    print("DATASET STRUCTURE")
    print("=" * 70)

    print("\n--- First 5 rows ---")
    print(df.head())

    print("\n--- Shape (rows, columns) ---")
    print(df.shape)

    print("\n--- Column info (dtypes & non-null counts) ---")
    print(df.info())

    print("\n--- Missing values per column ---")
    print(df.isnull().sum())


def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Step 3: Generate summary statistics of all numeric columns."""
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS (numeric columns)")
    print("=" * 70)
    numeric_df = df.select_dtypes(include="number")
    stats = numeric_df.describe()
    print(stats)
    return stats


def loan_amount_stats(df: pd.DataFrame, column: str = "loan_amnt") -> dict:
    """
    Step 4: Find the mean, median, and standard deviation of the target
    numeric column. The task asks for a 'price' column; this dataset does
    not contain one, so 'loan_amnt' (the requested loan amount) is used
    as the nearest equivalent.
    """
    print("\n" + "=" * 70)
    print(f"CENTRAL TENDENCY & SPREAD: '{column}'")
    print("=" * 70)

    mean_val = df[column].mean()
    median_val = df[column].median()
    std_val = df[column].std()

    print(f"Mean   : {mean_val:,.2f}")
    print(f"Median : {median_val:,.2f}")
    print(f"Std Dev: {std_val:,.2f}")

    return {"mean": mean_val, "median": median_val, "std": std_val}


def plot_relationship(df: pd.DataFrame, x: str = "person_income",
                       y: str = "loan_amnt") -> None:
    """
    Step 5: Plot the relationship between two numerical features.

    Note: both 'person_income' and 'loan_amnt' contain a handful of extreme
    data-entry outliers (e.g. loan amounts in the billions) that compress
    the entire plot into an unreadable line. For a readable visual, points
    are clipped to below the 99th percentile of each axis; the presence of
    these outliers is reported separately in the printed output / README.
    """
    x_cap = df[x].quantile(0.99)
    y_cap = df[y].quantile(0.99)
    plot_df = df[(df[x] <= x_cap) & (df[y] <= y_cap)]

    n_dropped = len(df) - len(plot_df)
    print(f"\n[Note] {n_dropped} extreme outlier rows excluded from the "
          f"scatter plot only (kept in all statistics) for readability.")

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=plot_df, x=x, y=y, alpha=0.3, s=15, color="teal")
    plt.title(f"Relationship between {x} and {y} (99th-percentile view)")
    plt.xlabel(x.replace("_", " ").title())
    plt.ylabel(y.replace("_", " ").title())
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "relationship_scatter.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Scatter plot saved to: {out_path}")


def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    """
    Step 6: Visualize correlation using a heatmap.

    Note: a few rows contain extreme data-entry outliers (e.g. loan_amnt in
    the billions, a credit history length of 500,000 years). Pearson
    correlation is highly sensitive to such outliers and, if left in, drags
    almost every correlation to ~0.00, hiding the real relationships.
    Spearman (rank-based) correlation is used instead, which is robust to
    these extreme values.
    """
    numeric_df = df.select_dtypes(include="number").drop(columns=["ID"], errors="ignore")
    corr = numeric_df.corr(method="spearman")

    plt.figure(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True,
                linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title("Correlation Heatmap of Numeric Features (Spearman)")
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "correlation_heatmap.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Correlation heatmap saved to: {out_path}")


def main():
    df = load_data(DATA_PATH)
    inspect_data(df)
    summary_statistics(df)
    loan_amount_stats(df, column="loan_amnt")
    plot_relationship(df, x="person_income", y="loan_amnt")
    plot_correlation_heatmap(df)
    print("\nAnalysis complete. Check the repo root for saved plots.")


if __name__ == "__main__":
    main()
