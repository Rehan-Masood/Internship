"""
analysis.py
Exploratory analysis functions: monthly/quarterly aggregation, top
products, category/region breakdowns, correlation matrix, YoY growth.
"""

import pandas as pd


def filter_date_range(df, start_date=None, end_date=None):
    """Filters the DataFrame to only rows within [start_date, end_date]."""
    filtered = df.copy()
    if start_date:
        filtered = filtered[filtered["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        filtered = filtered[filtered["Date"] <= pd.to_datetime(end_date)]
    return filtered


def monthly_sales(df):
    """Returns total Sales grouped by month (as a Period-indexed Series)."""
    monthly = df.set_index("Date").resample("ME")["Sales"].sum()
    return monthly


def quarterly_sales(df):
    """Returns total Sales grouped by quarter."""
    quarterly = df.set_index("Date").resample("QE")["Sales"].sum()
    return quarterly


def top_n_products(df, n=5):
    """Returns the top N products by total Sales."""
    top = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(n)
    return top


def category_breakdown(df):
    """Returns total Sales grouped by Category."""
    return df.groupby("Category")["Sales"].sum().sort_values(ascending=False)


def region_breakdown(df):
    """Returns total Sales grouped by Region."""
    return df.groupby("Region")["Sales"].sum().sort_values(ascending=False)


def correlation_matrix(df):
    """Returns the correlation matrix of numeric sales-related columns."""
    numeric_cols = ["Quantity", "UnitPrice", "Sales"]
    return df[numeric_cols].corr()


def year_over_year_growth(df):
    """
    Returns a DataFrame of total sales per year and the year-over-year
    percentage growth compared to the previous year.
    """
    yearly = df.set_index("Date").resample("YE")["Sales"].sum()
    yearly_df = yearly.to_frame(name="TotalSales")
    yearly_df["YoY Growth %"] = yearly_df["TotalSales"].pct_change() * 100
    yearly_df.index = yearly_df.index.year
    return yearly_df.round(2)


def summary_stats(df):
    """Returns headline summary statistics for the report."""
    return {
        "total_sales": round(df["Sales"].sum(), 2),
        "total_orders": len(df),
        "avg_order_value": round(df["Sales"].mean(), 2),
        "date_range": f"{df['Date'].min().date()} to {df['Date'].max().date()}",
        "total_products": df["Product"].nunique(),
        "total_categories": df["Category"].nunique(),
    }
