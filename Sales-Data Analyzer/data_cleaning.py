"""
data_cleaning.py
Loads raw sales data and cleans it: parses dates, removes duplicates,
fills missing values sensibly, and caps extreme outliers.
"""

import pandas as pd
import numpy as np


def load_data(filepath):
    """Loads a CSV file into a DataFrame."""
    df = pd.read_csv(filepath)
    return df


def clean_data(df):
    """
    Cleans the raw sales DataFrame.

    Steps:
    - Parse Date column, drop rows where it can't be parsed
    - Remove exact duplicate rows
    - Fill missing UnitPrice/Quantity using the per-product median
    - Recompute missing Sales as Quantity * UnitPrice where possible
    - Fill missing Region/Category with 'Unknown'
    - Cap extreme Sales outliers using the IQR method

    Returns (cleaned_df, report_dict) where report_dict summarizes
    what was changed, for display in the CLI and the PDF report.
    """
    report = {}
    df = df.copy()
    report["rows_before"] = len(df)

    # --- Parse dates ---
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    bad_dates = df["Date"].isna().sum()
    df = df.dropna(subset=["Date"])
    report["rows_dropped_bad_date"] = int(bad_dates)

    # --- Remove duplicates ---
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()
    report["duplicates_removed"] = int(duplicates)

    # --- Fill missing UnitPrice / Quantity using per-product median ---
    missing_price_before = df["UnitPrice"].isna().sum()
    df["UnitPrice"] = df.groupby("Product")["UnitPrice"].transform(
        lambda x: x.fillna(x.median())
    )
    df["UnitPrice"] = df["UnitPrice"].fillna(df["UnitPrice"].median())

    missing_qty_before = df["Quantity"].isna().sum()
    df["Quantity"] = df.groupby("Product")["Quantity"].transform(
        lambda x: x.fillna(x.median())
    )
    df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())

    report["unit_price_filled"] = int(missing_price_before)
    report["quantity_filled"] = int(missing_qty_before)

    # --- Recompute missing Sales where possible ---
    missing_sales_before = df["Sales"].isna().sum()
    recomputed_mask = df["Sales"].isna()
    df.loc[recomputed_mask, "Sales"] = (
        df.loc[recomputed_mask, "Quantity"] * df.loc[recomputed_mask, "UnitPrice"]
    )
    report["sales_recomputed"] = int(missing_sales_before)

    # --- Fill missing categorical fields ---
    for col in ["Region", "Category"]:
        if col in df.columns:
            missing_before = df[col].isna().sum()
            df[col] = df[col].fillna("Unknown")
            report[f"{col.lower()}_filled_unknown"] = int(missing_before)

    # --- Cap outliers in Sales using IQR method ---
    q1 = df["Sales"].quantile(0.25)
    q3 = df["Sales"].quantile(0.75)
    iqr = q3 - q1
    upper_bound = q3 + 1.5 * iqr
    lower_bound = max(0, q1 - 1.5 * iqr)

    outliers_capped = int(((df["Sales"] > upper_bound) | (df["Sales"] < lower_bound)).sum())
    df["Sales"] = df["Sales"].clip(lower=lower_bound, upper=upper_bound)
    report["outliers_capped"] = outliers_capped
    report["outlier_upper_bound"] = round(upper_bound, 2)

    df = df.sort_values("Date").reset_index(drop=True)
    report["rows_after"] = len(df)

    return df, report


def print_cleaning_report(report):
    """Prints a readable summary of the cleaning steps performed."""
    print("\n" + "=" * 55)
    print("DATA CLEANING REPORT")
    print("=" * 55)
    print(f"Rows before cleaning      : {report['rows_before']}")
    print(f"Rows with unparseable date: {report['rows_dropped_bad_date']} (dropped)")
    print(f"Duplicate rows removed    : {report['duplicates_removed']}")
    print(f"UnitPrice values filled   : {report['unit_price_filled']}")
    print(f"Quantity values filled    : {report['quantity_filled']}")
    print(f"Sales values recomputed   : {report['sales_recomputed']}")
    print(f"Region filled 'Unknown'   : {report.get('region_filled_unknown', 0)}")
    print(f"Category filled 'Unknown' : {report.get('category_filled_unknown', 0)}")
    print(f"Outlier Sales values capped: {report['outliers_capped']} (cap = {report['outlier_upper_bound']})")
    print(f"Rows after cleaning       : {report['rows_after']}")
    print("=" * 55)
