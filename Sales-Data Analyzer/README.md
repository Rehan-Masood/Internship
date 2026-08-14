# Sales Data Analyzer

A CLI-based Python tool that cleans messy retail sales data, explores trends, predicts future sales, and generates a full professional PDF report.

## Demo Video
<video src="https://github.com/user-attachments/assets/179ac0e7-48dc-41d6-b125-c51d69583b19" controls width="600"></video>

## Features

**Core requirements:**
- Data cleaning: missing value handling, duplicate removal
- Monthly & Quarterly sales trend charts
- Correlation heatmap (Quantity, UnitPrice, Sales)
- Top 5 best-selling products
- Linear regression sales forecast
- CLI menu with date range filtering

**Added on top of the original spec:**
- Outlier detection & capping (IQR method) as part of cleaning
- Category & Region sales breakdowns (own charts)
- Year-over-Year growth % table
- Model evaluation metrics (R², MAE, RMSE) alongside the forecast, not just a bare number
- Multi-month forecast (choose how many months ahead, not just one)
- Auto-generated realistic 5-year sample dataset included, so it runs immediately with no setup
- Modular file structure (cleaning / analysis / visualization / prediction / reporting are separate files)
- Cleaned dataset export to its own CSV

## Project Structure

```
sales_analyzer/
├── main.py                    # CLI entry point
├── data_cleaning.py           # missing values, duplicates, outliers
├── analysis.py                # monthly/quarterly/top products/correlation/YoY
├── visualizations.py          # all chart generation (matplotlib/seaborn)
├── prediction.py              # linear regression forecast
├── report_generator.py        # PDF report (reportlab)
├── generate_sample_data.py    # creates the sample dataset
├── requirements.txt
├── sample_data/
│   └── sales_data.csv         # 5-year sample dataset (intentionally messy)
└── outputs/                   # generated charts, cleaned CSV, and PDF report land here
```

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Press Enter when asked for a CSV path to use the included sample dataset, or provide your own CSV path. Your CSV needs these columns: `Date, Product, Category, Region, Quantity, UnitPrice, Sales`.

## Menu Options

1. View Monthly & Quarterly Sales Trends
2. View Top 5 Best-Selling Products
3. View Correlation Heatmap
4. Predict Future Sales (Linear Regression) — choose how many months ahead
5. Filter Data by Date Range
6. Reset to Full Dataset
7. Generate Full PDF Report (all charts, tables, and forecast in one document)
8. Exit

## Regenerating the Sample Dataset

```bash
python generate_sample_data.py
```

This creates a new `sample_data/sales_data.csv` with ~4,500 rows across 5 years, 15 products, 5 categories, and 4 regions — with realistic seasonal spikes (Nov/Dec), year-over-year growth, and intentionally injected missing values, duplicates, and outliers so the cleaning step has real problems to solve.

## Notes

- The prediction model is a simple linear regression on monthly totals — it captures the overall trend direction well but won't catch seasonal spikes (e.g. December surges). The R² score in the generated report reflects this honestly.
- All charts are saved as PNG files in `outputs/charts/` in addition to being embedded in the PDF report.
