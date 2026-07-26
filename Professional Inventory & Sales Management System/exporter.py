import pandas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.pdfgen import canvas as pdf_canvas

# ----- Brand colors used throughout every PDF -----
BRAND_DARK = colors.HexColor("#1B2A41")     # header banner background
BRAND_ACCENT = colors.HexColor("#2E7D32")   # green accent (totals, highlights)
BRAND_LIGHT_ROW = colors.HexColor("#F2F4F7")  # zebra-stripe row color
TEXT_GREY = colors.HexColor("#555555")

# ----- Company details shown in the footer of every page - edit these for your store -----
COMPANY_NAME = "YourStore Inc."
COMPANY_ADDRESS = "123 Market Street, City"
COMPANY_CONTACT = "+92-000-0000000  |  contact@yourstore.com"


class NumberedCanvas(pdf_canvas.Canvas):
    """A canvas that remembers every page so it can print 'Page X of Y' once the
    total page count is known, plus a branded company footer on every page."""

    def __init__(self, *args, **kwargs):
        pdf_canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_footer(total_pages)
            pdf_canvas.Canvas.showPage(self)
        pdf_canvas.Canvas.save(self)

    def _draw_footer(self, total_pages):
        page_width = letter[0]
        center_x = page_width / 2

        # thin divider line above the footer
        self.setStrokeColor(colors.lightgrey)
        self.setLineWidth(0.5)
        self.line(0.7 * inch, 0.62 * inch, page_width - 0.7 * inch, 0.62 * inch)

        # company name
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(BRAND_DARK)
        self.drawCentredString(center_x, 0.46 * inch, COMPANY_NAME)

        # address + contact
        self.setFont("Helvetica", 7)
        self.setFillColor(TEXT_GREY)
        self.drawCentredString(center_x, 0.34 * inch, f"{COMPANY_ADDRESS}  |  {COMPANY_CONTACT}")

        # page number
        self.setFont("Helvetica", 7.5)
        self.setFillColor(TEXT_GREY)
        self.drawCentredString(center_x, 0.20 * inch, f"Page {self._pageNumber} of {total_pages}")


def _build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="BrandTitle", fontName="Helvetica-Bold", fontSize=20,
        textColor=colors.white, alignment=1, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name="BrandSubtitle", fontName="Helvetica", fontSize=11,
        textColor=colors.white, alignment=1,
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading", fontName="Helvetica-Bold", fontSize=13,
        textColor=BRAND_DARK, spaceBefore=14, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="MetaText", fontName="Helvetica", fontSize=9,
        textColor=TEXT_GREY,
    ))
    styles.add(ParagraphStyle(
        name="FooterText", fontName="Helvetica-Oblique", fontSize=10,
        textColor=BRAND_ACCENT, alignment=1, spaceBefore=16,
    ))
    return styles


def _header_banner(styles, title, subtitle):
    """A full-width dark banner with a white title/subtitle - used at the top of every PDF."""
    banner_table = Table(
        [[Paragraph(title, styles["BrandTitle"])],
         [Paragraph(subtitle, styles["BrandSubtitle"])]],
        colWidths=[6.6 * inch],
    )
    banner_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_DARK),
        ("TOPPADDING", (0, 0), (-1, 0), 14),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 14),
    ]))
    return banner_table


def _items_table(rows, col_widths):
    """A styled table with a colored header row and alternating row colors."""
    table = Table(rows, colWidths=col_widths, repeatRows=1)

    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), BRAND_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, 0), 1, BRAND_DARK),
        ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.lightgrey),
    ]
    # zebra stripes on data rows
    for row_index in range(1, len(rows)):
        if row_index % 2 == 0:
            style_commands.append(("BACKGROUND", (0, row_index), (-1, row_index), BRAND_LIGHT_ROW))

    table.setStyle(TableStyle(style_commands))
    return table


def export_inventory_to_excel(products, filename="inventory_export.xlsx"):
    """Exports the full product list to a formatted Excel file."""
    if not products:
        print("No products to export.")
        return

    rows = [product.to_dict() for product in products]
    dataframe = pandas.DataFrame(rows)
    dataframe.to_excel(filename, index=False, sheet_name="Inventory")

    print(f"Inventory exported to '{filename}'.")


def export_daily_report_to_pdf(sales, target_date, filename="daily_sales_report.pdf"):
    """Exports a premium-styled PDF summary of all sales for a given date."""
    if not sales:
        print("No sales to export for this date.")
        return

    styles = _build_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter,
                             topMargin=0, bottomMargin=0.85 * inch,
                             leftMargin=0.7 * inch, rightMargin=0.7 * inch)
    story = []

    story.append(_header_banner(styles, "DAILY SALES REPORT",
                                 f"{target_date.strftime('%A, %d %B %Y')}"))
    story.append(Spacer(1, 18))

    grand_total = 0.0

    for sale in sales:
        story.append(Paragraph(f"Invoice #{sale.sale_id}", styles["SectionHeading"]))

        meta_line = f"Time: {sale.date_time.strftime('%H:%M')}"
        if sale.staff_name:
            meta_line += f" &nbsp;|&nbsp; Served by: {sale.staff_name}"
        story.append(Paragraph(meta_line, styles["MetaText"]))
        story.append(Spacer(1, 6))

        table_rows = [["Item", "Qty", "Unit Price", "Line Total"]]
        for item in sale.product_list:
            line_total = item["quantity"] * item["price"]
            table_rows.append([
                item["name"], str(item["quantity"]),
                f"Rs.{item['price']:.2f}", f"Rs.{line_total:.2f}",
            ])

        story.append(_items_table(table_rows, col_widths=[2.6 * inch, 0.8 * inch, 1.3 * inch, 1.3 * inch]))
        story.append(Spacer(1, 6))

        # subtotal / discount / total summary, right-aligned
        summary_rows = [["Subtotal", f"Rs.{sale.subtotal:.2f}"]]
        if sale.discount_percent > 0:
            discount_amount = sale.subtotal - sale.total_amount
            summary_rows.append([f"Discount ({sale.discount_percent:.0f}%)", f"-Rs.{discount_amount:.2f}"])
        summary_rows.append(["TOTAL", f"Rs.{sale.total_amount:.2f}"])

        summary_table = Table(summary_rows, colWidths=[5.4 * inch, 1.6 * inch])
        summary_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
            ("FONTNAME", (0, 0), (-1, -2), "Helvetica"),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, -1), (-1, -1), BRAND_ACCENT),
            ("LINEABOVE", (0, -1), (-1, -1), 0.75, BRAND_DARK),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", color=colors.lightgrey, thickness=0.5))

        grand_total += sale.total_amount

    # ----- grand total banner at the end -----
    story.append(Spacer(1, 16))
    grand_total_table = Table([["GRAND TOTAL REVENUE", f"Rs.{grand_total:.2f}"]],
                               colWidths=[5.0 * inch, 2.0 * inch])
    grand_total_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (0, 0), 12),
    ]))
    story.append(grand_total_table)

    story.append(Paragraph("Thank you for your business!", styles["FooterText"]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Daily sales report exported to '{filename}'.")


def export_invoice_to_pdf(sale, filename=None):
    """Exports a single sale as a premium-styled standalone invoice PDF."""
    filename = filename if filename else f"invoice_{sale.sale_id}.pdf"

    styles = _build_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter,
                             topMargin=0, bottomMargin=0.85 * inch,
                             leftMargin=0.7 * inch, rightMargin=0.7 * inch)
    story = []

    story.append(_header_banner(styles, "INVOICE", f"#{sale.sale_id}"))
    story.append(Spacer(1, 18))

    meta_line = f"Date: {sale.date_time.strftime('%Y-%m-%d %H:%M')}"
    if sale.staff_name:
        meta_line += f" &nbsp;|&nbsp; Served by: {sale.staff_name}"
    story.append(Paragraph(meta_line, styles["MetaText"]))
    story.append(Spacer(1, 10))

    table_rows = [["Item", "Qty", "Unit Price", "Line Total"]]
    for item in sale.product_list:
        line_total = item["quantity"] * item["price"]
        table_rows.append([
            item["name"], str(item["quantity"]),
            f"Rs.{item['price']:.2f}", f"Rs.{line_total:.2f}",
        ])

    story.append(_items_table(table_rows, col_widths=[2.6 * inch, 0.8 * inch, 1.3 * inch, 1.3 * inch]))
    story.append(Spacer(1, 10))

    summary_rows = [["Subtotal", f"Rs.{sale.subtotal:.2f}"]]
    if sale.discount_percent > 0:
        discount_amount = sale.subtotal - sale.total_amount
        summary_rows.append([f"Discount ({sale.discount_percent:.0f}%)", f"-Rs.{discount_amount:.2f}"])
    summary_rows.append(["TOTAL", f"Rs.{sale.total_amount:.2f}"])

    summary_table = Table(summary_rows, colWidths=[5.4 * inch, 1.6 * inch])
    summary_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("FONTNAME", (0, 0), (-1, -2), "Helvetica"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("TEXTCOLOR", (0, -1), (-1, -1), BRAND_ACCENT),
        ("LINEABOVE", (0, -1), (-1, -1), 0.75, BRAND_DARK),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(summary_table)

    story.append(Paragraph("Thank you for shopping with us!", styles["FooterText"]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Invoice exported to '{filename}'.")