from datetime import date, datetime, timedelta
from product import Product

SLOW_MOVING_DAYS = 30  # a product not sold in this many days is considered "slow-moving"


class ReportGenerator:
    """Handles business analytics: sales reports, product rankings, stock alerts, profit."""

    def __init__(self, inventory_manager):
        self.inventory_manager = inventory_manager

    # ----- Daily & monthly sales -----
    def daily_sales_report(self, target_date=None):
        """Prints all sales and total revenue for a given date (defaults to today)."""
        target_date = target_date if target_date else date.today()

        matching_sales = [s for s in self.inventory_manager.sales if s.date_time.date() == target_date]

        print(f"\n----- Daily Sales Report: {target_date} -----")
        if not matching_sales:
            print("No sales recorded for this date.")
            return

        total_revenue = 0.0
        for sale in matching_sales:
            print(f"{sale.sale_id} | {sale.date_time.strftime('%H:%M')} | Rs.{sale.total_amount:.2f}")
            total_revenue += sale.total_amount

        print("-" * 40)
        print(f"Total Sales: {len(matching_sales)}")
        print(f"Total Revenue: Rs.{total_revenue:.2f}")

    def monthly_sales_report(self, year=None, month=None):
        """Prints total revenue and sale count for a given month (defaults to this month)."""
        today = date.today()
        year = year if year else today.year
        month = month if month else today.month

        matching_sales = [
            s for s in self.inventory_manager.sales
            if s.date_time.year == year and s.date_time.month == month
        ]

        print(f"\n----- Monthly Sales Report: {year}-{month:02d} -----")
        if not matching_sales:
            print("No sales recorded for this month.")
            return

        total_revenue = sum(s.total_amount for s in matching_sales)
        total_profit = sum(s.calculate_profit() for s in matching_sales)

        print(f"Total Sales: {len(matching_sales)}")
        print(f"Total Revenue: Rs.{total_revenue:.2f}")
        print(f"Total Profit: Rs.{total_profit:.2f}")

    # ----- Product rankings -----
    def top_selling_products(self, top_n=5):
        """Prints the top N products ranked by total quantity sold."""
        quantity_sold = {}
        for sale in self.inventory_manager.sales:
            for item in sale.product_list:
                quantity_sold[item["name"]] = quantity_sold.get(item["name"], 0) + item["quantity"]

        if not quantity_sold:
            print("\nNo sales data available yet.")
            return

        ranked = sorted(quantity_sold.items(), key=lambda entry: entry[1], reverse=True)

        print(f"\n----- Top {top_n} Selling Products -----")
        for rank, (name, quantity) in enumerate(ranked[:top_n], start=1):
            print(f"{rank}. {name} - {quantity} unit(s) sold")

    def category_wise_sales(self):
        """Prints total revenue earned per product category."""
        revenue_by_category = {}

        for sale in self.inventory_manager.sales:
            for item in sale.product_list:
                product = self.inventory_manager.find_product_by_id(item["product_id"])
                category = product.category if product else "Unknown"
                line_total = item["quantity"] * item["price"]
                revenue_by_category[category] = revenue_by_category.get(category, 0) + line_total

        print("\n----- Category-wise Sales -----")
        if not revenue_by_category:
            print("No sales data available yet.")
            return

        ranked = sorted(revenue_by_category.items(), key=lambda entry: entry[1], reverse=True)
        for category, revenue in ranked:
            print(f"{category:<15} | Rs.{revenue:.2f}")

    def slow_moving_products(self, days_threshold=SLOW_MOVING_DAYS):
        """Prints products that haven't sold at all within the given number of days."""
        cutoff = datetime.now() - timedelta(days=days_threshold)

        recently_sold_ids = set()
        for sale in self.inventory_manager.sales:
            if sale.date_time >= cutoff:
                for item in sale.product_list:
                    recently_sold_ids.add(item["product_id"])

        slow_movers = [p for p in self.inventory_manager.products if p.product_id not in recently_sold_ids]

        print(f"\n----- Slow-Moving Stock (no sales in {days_threshold} days) -----")
        if not slow_movers:
            print("All products have recent sales activity.")
            return

        for product in slow_movers:
            print(f"{product.product_id} | {product.name:<18} | Stock: {product.quantity_in_stock}")

    # ----- Stock & expiry alerts -----
    def low_stock_alert(self):
        """Prints every product that has fallen below the low-stock threshold."""
        low_stock_products = [p for p in self.inventory_manager.products if p.is_low_on_stock()]

        print(f"\n----- Low Stock Alert (below {Product.LOW_STOCK_THRESHOLD} units) -----")
        if not low_stock_products:
            print("All products are sufficiently stocked.")
            return

        for product in low_stock_products:
            print(f"WARNING: '{product.name}' has only {product.quantity_in_stock} unit(s) left! Restock needed.")

    def expiry_alert(self):
        """Prints every product that is expiring within the warning window."""
        expiring_products = self.inventory_manager.expiring_soon_products()

        print(f"\n----- Expiry Alert (within {Product.EXPIRY_WARNING_DAYS} days) -----")
        if not expiring_products:
            print("No products are expiring soon.")
            return

        for product in expiring_products:
            print(f"WARNING: '{product.name}' expires on {product.expiry_date}!")

    # ----- Profit -----
    def profit_report(self):
        """Prints total profit earned across all recorded sales."""
        if not self.inventory_manager.sales:
            print("\nNo sales data available yet.")
            return

        total_profit = sum(sale.calculate_profit() for sale in self.inventory_manager.sales)
        total_revenue = sum(sale.total_amount for sale in self.inventory_manager.sales)

        print("\n----- Overall Profit Report -----")
        print(f"Total Revenue: Rs.{total_revenue:.2f}")
        print(f"Total Profit:  Rs.{total_profit:.2f}")

    # ----- Revenue trend chart -----
    def revenue_trend_chart(self, filename="revenue_trend.png"):
        """Generates a line chart of daily revenue over time and saves it as an image."""
        import matplotlib
        matplotlib.use("Agg")  # renders to a file, no GUI window needed
        import matplotlib.pyplot as plt

        if not self.inventory_manager.sales:
            print("\nNo sales data available yet to chart.")
            return

        revenue_by_day = {}
        for sale in self.inventory_manager.sales:
            day = sale.date_time.date()
            revenue_by_day[day] = revenue_by_day.get(day, 0) + sale.total_amount

        sorted_days = sorted(revenue_by_day.keys())
        revenues = [revenue_by_day[day] for day in sorted_days]

        plt.figure(figsize=(8, 4))
        plt.plot(sorted_days, revenues, marker="o", color="#2e7d32")
        plt.title("Daily Revenue Trend")
        plt.xlabel("Date")
        plt.ylabel("Revenue (Rs.)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()

        print(f"\nRevenue trend chart saved to '{filename}'.")
