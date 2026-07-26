from datetime import datetime


class Sale:
    """Represents one completed sale transaction, which can include multiple items."""

    def __init__(self, sale_id, product_list, date_time=None, staff_name="", discount_percent=0.0):
        self.sale_id = sale_id
        self.product_list = product_list  # list of dicts: product_id, name, quantity, price, cost_price
        self.date_time = date_time if date_time else datetime.now()
        self.staff_name = staff_name
        self.discount_percent = discount_percent
        self.subtotal = self.calculate_subtotal()
        self.total_amount = self.calculate_total()

    def calculate_subtotal(self):
        """Adds up quantity * price across every item, before any discount."""
        total = 0.0
        for item in self.product_list:
            total += item["quantity"] * item["price"]
        return total

    def calculate_total(self):
        """Applies the discount percentage to the subtotal to get the final bill."""
        discount_amount = self.subtotal * (self.discount_percent / 100)
        return self.subtotal - discount_amount

    def calculate_profit(self):
        """Returns the profit made on this sale (total after discount, minus cost of goods sold)."""
        total_cost = sum(item["quantity"] * item.get("cost_price", 0) for item in self.product_list)
        return self.total_amount - total_cost

    def print_invoice(self):
        """Prints a clean, receipt-style invoice for this sale."""
        print("-" * 44)
        print(f"INVOICE #{self.sale_id}")
        print(f"Date: {self.date_time.strftime('%Y-%m-%d %H:%M')}")
        if self.staff_name:
            print(f"Served by: {self.staff_name}")
        print("-" * 44)

        for item in self.product_list:
            line_total = item["quantity"] * item["price"]
            print(f"Item: {item['quantity']}x {item['name']} @ Rs.{item['price']:.2f} = Rs.{line_total:.2f}")

        print("-" * 44)
        print(f"Subtotal: Rs.{self.subtotal:.2f}")

        if self.discount_percent > 0:
            discount_amount = self.subtotal - self.total_amount
            print(f"Discount ({self.discount_percent:.0f}%): -Rs.{discount_amount:.2f}")

        print(f"Total Bill: Rs.{self.total_amount:.2f}")
        print("Thank you!")
        print("-" * 44)

    def to_rows(self):
        """Converts this sale into a list of CSV-ready dicts (one row per item, sharing the same sale_id)."""
        rows = []
        for item in self.product_list:
            rows.append({
                "sale_id": self.sale_id,
                "date_time": self.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                "product_id": item["product_id"],
                "name": item["name"],
                "quantity": item["quantity"],
                "price": item["price"],
                "cost_price": item.get("cost_price", 0),
                "staff_name": self.staff_name,
                "discount_percent": self.discount_percent,
            })
        return rows
