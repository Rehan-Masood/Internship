"""
report_generator.py
Builds a professional multi-page PDF report combining summary stats,
the data cleaning log, all charts, top products, and the sales forecast.
"""

from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
)


def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="ReportTitle", fontSize=26, leading=32, spaceAfter=6,
        textColor=colors.HexColor("#14182b"), fontName="Helvetica-Bold"
    ))
    styles.add(ParagraphStyle(
        name="ReportSubtitle", fontSize=12, leading=16,
        textColor=colors.HexColor("#5b6270"), spaceAfter=24
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading", fontSize=16, leading=20, spaceBefore=18, spaceAfter=10,
        textColor=colors.HexColor("#14182b"), fontName="Helvetica-Bold"
    ))
    return styles


def _summary_table(summary, styles):
    data = [
        ["Total Sales", f"${summary['total_sales']:,.2f}"],
        ["Total Orders", f"{summary['total_orders']:,}"],
        ["Average Order Value", f"${summary['avg_order_value']:,.2f}"],
        ["Date Range", summary["date_range"]],
        ["Products Tracked", str(summary["total_products"])],
        ["Categories", str(summary["total_categories"])],
    ]
    table = Table(data, colWidths=[220, 260])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#14182b")),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#1c1f2e")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe4")),
    ]))
    return table


def _cleaning_table(report, styles):
    data = [
        ["Metric", "Value"],
        ["Rows before cleaning", str(report["rows_before"])],
        ["Rows dropped (bad date)", str(report["rows_dropped_bad_date"])],
        ["Duplicate rows removed", str(report["duplicates_removed"])],
        ["UnitPrice values filled", str(report["unit_price_filled"])],
        ["Quantity values filled", str(report["quantity_filled"])],
        ["Sales values recomputed", str(report["sales_recomputed"])],
        ["Outlier Sales values capped", str(report["outliers_capped"])],
        ["Rows after cleaning", str(report["rows_after"])],
    ]
    table = Table(data, colWidths=[280, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#14182b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f5f7")]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe4")),
    ]))
    return table


def _top_products_table(top_products, styles):
    data = [["Rank", "Product", "Total Sales"]]
    for i, (product, sales) in enumerate(top_products.items(), start=1):
        data.append([str(i), product, f"${sales:,.2f}"])
    table = Table(data, colWidths=[50, 280, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#b8912f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f5f7")]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe4")),
    ]))
    return table


def _yoy_table(yoy_df, styles):
    data = [["Year", "Total Sales", "YoY Growth"]]
    for year, row in yoy_df.iterrows():
        growth = row["YoY Growth %"]
        growth_str = "N/A" if pd_isna(growth) else f"{growth:+.1f}%"
        data.append([str(year), f"${row['TotalSales']:,.2f}", growth_str])
    table = Table(data, colWidths=[80, 220, 180])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2f6e73")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f5f7")]),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe4")),
    ]))
    return table


def pd_isna(value):
    import pandas as pd
    return pd.isna(value)


def generate_pdf_report(
    output_path, summary, cleaning_report, top_products, yoy_df,
    chart_paths, model_metrics, forecast_dates, forecast_values, trend_label,
):
    """Builds the full PDF report and saves it to output_path."""
    styles = _styles()
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        topMargin=50, bottomMargin=50, leftMargin=50, rightMargin=50,
    )
    story = []

    # --- Title page ---
    story.append(Spacer(1, 60))
    story.append(Paragraph("Sales Data Analysis Report", styles["ReportTitle"]))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}",
        styles["ReportSubtitle"]
    ))
    story.append(Spacer(1, 20))
    story.append(_summary_table(summary, styles))
    story.append(PageBreak())

    # --- Data cleaning report ---
    story.append(Paragraph("Data Cleaning Summary", styles["SectionHeading"]))
    story.append(_cleaning_table(cleaning_report, styles))
    story.append(PageBreak())

    # --- Monthly & Quarterly trends ---
    story.append(Paragraph("Monthly Sales Trend", styles["SectionHeading"]))
    story.append(Image(chart_paths["monthly"], width=6.5 * inch, height=3.25 * inch))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Quarterly Sales", styles["SectionHeading"]))
    story.append(Image(chart_paths["quarterly"], width=6.5 * inch, height=3.25 * inch))
    story.append(PageBreak())

    # --- Top products ---
    story.append(Paragraph("Top 5 Best-Selling Products", styles["SectionHeading"]))
    story.append(Image(chart_paths["top_products"], width=6.5 * inch, height=3.25 * inch))
    story.append(Spacer(1, 14))
    story.append(_top_products_table(top_products, styles))
    story.append(PageBreak())

    # --- Category & Region breakdown ---
    story.append(Paragraph("Sales by Category", styles["SectionHeading"]))
    story.append(Image(chart_paths["category"], width=6.5 * inch, height=3.25 * inch))
    story.append(Spacer(1, 16))
    story.append(Paragraph("Sales Share by Region", styles["SectionHeading"]))
    story.append(Image(chart_paths["region"], width=4 * inch, height=3.25 * inch))
    story.append(PageBreak())

    # --- Correlation heatmap ---
    story.append(Paragraph("Correlation Between Sales Metrics", styles["SectionHeading"]))
    story.append(Image(chart_paths["heatmap"], width=4.5 * inch, height=3.7 * inch))
    story.append(PageBreak())

    # --- Year over year growth ---
    story.append(Paragraph("Year-over-Year Growth", styles["SectionHeading"]))
    story.append(_yoy_table(yoy_df, styles))
    story.append(PageBreak())

    # --- Prediction ---
    story.append(Paragraph("Sales Forecast (Linear Regression)", styles["SectionHeading"]))
    story.append(Image(chart_paths["prediction"], width=6.5 * inch, height=3.25 * inch))
    story.append(Spacer(1, 14))

    metrics_data = [
        ["Model R-squared Score", str(model_metrics["r2_score"])],
        ["Mean Absolute Error (MAE)", f"${model_metrics['mae']:,.2f}"],
        ["Root Mean Squared Error (RMSE)", f"${model_metrics['rmse']:,.2f}"],
        ["Trend Direction", trend_label],
    ]
    for date, value in zip(forecast_dates, forecast_values):
        metrics_data.append([f"Forecast: {date.strftime('%B %Y')}", f"${value:,.2f}"])

    metrics_table = Table(metrics_data, colWidths=[260, 220])
    metrics_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#dcdfe4")),
    ]))
    story.append(metrics_table)

    doc.build(story)
    return output_path
