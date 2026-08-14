"""
visualizations.py
Generates and saves all charts as PNG files: monthly trend line,
quarterly bar chart, top products bar chart, correlation heatmap,
category/region breakdowns, and the prediction chart.
"""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend, safe for scripts/servers
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid")
PALETTE = "crest"


def plot_monthly_trend(monthly_series, save_path):
    """Line chart of monthly sales over time."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(monthly_series.index, monthly_series.values, marker="o", color="#2f6e73", linewidth=2)
    ax.fill_between(monthly_series.index, monthly_series.values, alpha=0.1, color="#2f6e73")
    ax.set_title("Monthly Sales Trend", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def plot_quarterly_bar(quarterly_series, save_path):
    """Bar chart of quarterly sales."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    labels = [f"{d.year} Q{d.quarter}" for d in quarterly_series.index]
    ax.bar(labels, quarterly_series.values, color="#b8912f")
    ax.set_title("Quarterly Sales", fontsize=14, fontweight="bold")
    ax.set_ylabel("Total Sales")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def plot_top_products_bar(top_products, save_path):
    """Horizontal bar chart of the top N products by sales."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sorted_products = top_products.sort_values()
    ax.barh(sorted_products.index, sorted_products.values, color="#2f6e73")
    ax.set_title(f"Top {len(top_products)} Best-Selling Products", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Sales")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def plot_correlation_heatmap(corr_matrix, save_path):
    """Heatmap of correlations between numeric sales columns."""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    sns.heatmap(corr_matrix, annot=True, cmap="crest", fmt=".2f", ax=ax, vmin=-1, vmax=1)
    ax.set_title("Correlation Heatmap", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def plot_category_breakdown(category_series, save_path):
    """Bar chart of total sales by product category."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(category_series.index, category_series.values, color="#8a6fb0")
    ax.set_title("Sales by Category", fontsize=14, fontweight="bold")
    ax.set_ylabel("Total Sales")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def plot_region_breakdown(region_series, save_path):
    """Pie chart of total sales by region."""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    colors = sns.color_palette("crest", len(region_series))
    ax.pie(region_series.values, labels=region_series.index, autopct="%1.1f%%",
           colors=colors, startangle=90)
    ax.set_title("Sales Share by Region", fontsize=14, fontweight="bold")
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def plot_prediction(monthly_series, future_index, future_predictions, save_path):
    """Line chart showing historical monthly sales plus the forecasted months."""
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(monthly_series.index, monthly_series.values, marker="o",
            color="#2f6e73", linewidth=2, label="Actual")
    ax.plot(future_index, future_predictions, marker="o", linestyle="--",
            color="#b3432f", linewidth=2, label="Forecast")
    ax.axvline(x=monthly_series.index[-1], color="gray", linestyle=":", linewidth=1)
    ax.set_title("Sales Forecast (Linear Regression)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)
