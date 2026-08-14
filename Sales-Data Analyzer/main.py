"""
main.py
Sales Data Analyzer - CLI entry point.

Loads a sales CSV, cleans it, and offers a menu to explore trends,
top products, correlations, a sales forecast, and generate a full PDF report.
"""

import os
import pandas as pd

from data_cleaning import load_data, clean_data, print_cleaning_report
from analysis import (
    filter_date_range, monthly_sales, quarterly_sales, top_n_products,
    category_breakdown, region_breakdown, correlation_matrix,
    year_over_year_growth, summary_stats,
)
from visualizations import (
    plot_monthly_trend, plot_quarterly_bar, plot_top_products_bar,
    plot_correlation_heatmap, plot_category_breakdown, plot_region_breakdown,
    plot_prediction,
)
from prediction import train_model, evaluate_model, forecast_future_months, trend_direction
from report_generator import generate_pdf_report

CHART_DIR = "outputs/charts"
REPORT_PATH = "outputs/sales_report.pdf"
CLEANED_CSV_PATH = "outputs/cleaned_sales_data.csv"


def load_and_clean(filepath):
    print(f"\nLoading data from: {filepath}")
    raw_df = load_data(filepath)
    cleaned_df, report = clean_data(raw_df)
    print_cleaning_report(report)
    os.makedirs("outputs", exist_ok=True)
    cleaned_df.to_csv(CLEANED_CSV_PATH, index=False)
    print(f"Cleaned data saved to: {CLEANED_CSV_PATH}")
    return cleaned_df, report


def get_date_range_filtered(df):
    print("\nEnter a date range to filter (format: YYYY-MM-DD), or press Enter to use all data.")
    start = input("Start date: ").strip()
    end = input("End date: ").strip()

    start = start if start else None
    end = end if end else None

    try:
        filtered = filter_date_range(df, start, end)
        if filtered.empty:
            print("No data in that range. Using full dataset instead.")
            return df
        print(f"Filtered to {len(filtered)} rows.")
        return filtered
    except (ValueError, TypeError):
        print("Invalid date format. Using full dataset instead.")
        return df


def show_monthly_quarterly(df):
    os.makedirs(CHART_DIR, exist_ok=True)
    monthly = monthly_sales(df)
    quarterly = quarterly_sales(df)

    print("\nMonthly Sales (last 6 months shown):")
    print(monthly.tail(6).apply(lambda x: f"${x:,.2f}"))

    monthly_path = f"{CHART_DIR}/monthly_trend.png"
    quarterly_path = f"{CHART_DIR}/quarterly_sales.png"
    plot_monthly_trend(monthly, monthly_path)
    plot_quarterly_bar(quarterly, quarterly_path)
    print(f"Charts saved to {monthly_path} and {quarterly_path}")


def show_top_products(df):
    os.makedirs(CHART_DIR, exist_ok=True)
    top = top_n_products(df, n=5)
    print("\nTop 5 Best-Selling Products:")
    for i, (product, sales) in enumerate(top.items(), start=1):
        print(f"  {i}. {product:<25} ${sales:,.2f}")

    path = f"{CHART_DIR}/top_products.png"
    plot_top_products_bar(top, path)
    print(f"Chart saved to {path}")


def show_correlation(df):
    os.makedirs(CHART_DIR, exist_ok=True)
    corr = correlation_matrix(df)
    print("\nCorrelation Matrix:")
    print(corr.round(2))

    path = f"{CHART_DIR}/correlation_heatmap.png"
    plot_correlation_heatmap(corr, path)
    print(f"Chart saved to {path}")


def show_prediction(df):
    os.makedirs(CHART_DIR, exist_ok=True)
    monthly = monthly_sales(df)

    if len(monthly) < 3:
        print("Not enough monthly data points to train a reliable model (need at least 3).")
        return

    model, X, y = train_model(monthly)
    metrics = evaluate_model(model, X, y)
    trend = trend_direction(model)

    while True:
        raw = input("\nHow many future months to forecast? (e.g. 3): ").strip()
        try:
            n_months = int(raw)
            if n_months <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a whole number.")

    future_dates, predictions = forecast_future_months(model, monthly, n_months=n_months)

    print(f"\nModel R\u00b2 Score : {metrics['r2_score']}")
    print(f"MAE            : ${metrics['mae']:,.2f}")
    print(f"RMSE           : ${metrics['rmse']:,.2f}")
    print(f"Trend Direction: {trend}")
    print("\nForecast:")
    for date, value in zip(future_dates, predictions):
        print(f"  {date.strftime('%B %Y')}: ${value:,.2f}")

    path = f"{CHART_DIR}/prediction.png"
    plot_prediction(monthly, future_dates, predictions, path)
    print(f"Chart saved to {path}")


def generate_full_report(df, cleaning_report):
    os.makedirs(CHART_DIR, exist_ok=True)
    print("\nGenerating full report — this may take a few seconds...")

    monthly = monthly_sales(df)
    quarterly = quarterly_sales(df)
    top = top_n_products(df, n=5)
    category = category_breakdown(df)
    region = region_breakdown(df)
    corr = correlation_matrix(df)
    yoy = year_over_year_growth(df)
    summary = summary_stats(df)

    chart_paths = {
        "monthly": f"{CHART_DIR}/monthly_trend.png",
        "quarterly": f"{CHART_DIR}/quarterly_sales.png",
        "top_products": f"{CHART_DIR}/top_products.png",
        "category": f"{CHART_DIR}/category_breakdown.png",
        "region": f"{CHART_DIR}/region_breakdown.png",
        "heatmap": f"{CHART_DIR}/correlation_heatmap.png",
        "prediction": f"{CHART_DIR}/prediction.png",
    }

    plot_monthly_trend(monthly, chart_paths["monthly"])
    plot_quarterly_bar(quarterly, chart_paths["quarterly"])
    plot_top_products_bar(top, chart_paths["top_products"])
    plot_category_breakdown(category, chart_paths["category"])
    plot_region_breakdown(region, chart_paths["region"])
    plot_correlation_heatmap(corr, chart_paths["heatmap"])

    model, X, y = train_model(monthly)
    metrics = evaluate_model(model, X, y)
    trend = trend_direction(model)
    future_dates, predictions = forecast_future_months(model, monthly, n_months=3)
    plot_prediction(monthly, future_dates, predictions, chart_paths["prediction"])

    generate_pdf_report(
        REPORT_PATH, summary, cleaning_report, top, yoy, chart_paths,
        metrics, future_dates, predictions, trend,
    )
    print(f"\nFull PDF report generated: {REPORT_PATH}")


def main():
    print("=" * 55)
    print("SALES DATA ANALYZER")
    print("=" * 55)

    default_path = "sample_data/sales_data.csv"
    path = input(f"Enter CSV path (press Enter for sample data '{default_path}'): ").strip()
    path = path if path else default_path

    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    df, cleaning_report = load_and_clean(path)
    working_df = df

    while True:
        print("\n" + "-" * 55)
        print("MENU")
        print("-" * 55)
        print("1. View Monthly & Quarterly Sales Trends")
        print("2. View Top 5 Best-Selling Products")
        print("3. View Correlation Heatmap")
        print("4. Predict Future Sales (Linear Regression)")
        print("5. Filter Data by Date Range")
        print("6. Reset to Full Dataset")
        print("7. Generate Full PDF Report")
        print("8. Exit")

        choice = input("\nChoose an option (1-8): ").strip()

        if choice == "1":
            show_monthly_quarterly(working_df)
        elif choice == "2":
            show_top_products(working_df)
        elif choice == "3":
            show_correlation(working_df)
        elif choice == "4":
            show_prediction(working_df)
        elif choice == "5":
            working_df = get_date_range_filtered(df)
        elif choice == "6":
            working_df = df
            print("Reset to full dataset.")
        elif choice == "7":
            generate_full_report(working_df, cleaning_report)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Please choose a number between 1 and 8.")


if __name__ == "__main__":
    main()
