from datetime import date, datetime


class Product:
    """Represents a single product in the store's inventory."""

    LOW_STOCK_THRESHOLD = 5
    EXPIRY_WARNING_DAYS = 7

    def __init__(self, product_id, name, category, price, quantity_in_stock,
                 cost_price=0.0, supplier="", expiry_date=""):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.quantity_in_stock = quantity_in_stock
        self.cost_price = cost_price      # what the store paid per unit (for profit tracking)
        self.supplier = supplier          # optional supplier name
        self.expiry_date = expiry_date    # optional, format YYYY-MM-DD, empty string if not perishable

    def display_info(self):
        """Prints a neatly formatted row with this product's details."""
        extra = ""
        if self.supplier:
            extra += f" | Supplier: {self.supplier}"
        if self.expiry_date:
            extra += f" | Expires: {self.expiry_date}"

        print(f"{self.product_id:<6} | {self.name:<18} | {self.category:<14} | "
              f"Rs.{self.price:<10.2f} | Stock: {self.quantity_in_stock:<5}{extra}")

    def update_stock(self, change):
        """Adjusts the stock level by the given amount (positive to restock, negative to sell)."""
        self.quantity_in_stock += change

    def is_low_on_stock(self):
        """Returns True if the stock has dropped below the low-stock threshold."""
        return self.quantity_in_stock < self.LOW_STOCK_THRESHOLD

    def profit_per_unit(self):
        """Returns how much profit is made from selling one unit of this product."""
        return self.price - self.cost_price

    def is_expiring_soon(self):
        """Returns True if this product has an expiry date within the warning window."""
        if not self.expiry_date:
            return False
        try:
            expiry = datetime.strptime(self.expiry_date, "%Y-%m-%d").date()
            days_left = (expiry - date.today()).days
            return 0 <= days_left <= self.EXPIRY_WARNING_DAYS
        except ValueError:
            return False

    def to_dict(self):
        """Converts this product into a dictionary ready for CSV writing."""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity_in_stock": self.quantity_in_stock,
            "cost_price": self.cost_price,
            "supplier": self.supplier,
            "expiry_date": self.expiry_date,
        }

    @staticmethod
    def from_dict(row):
        """Rebuilds a Product object from one CSV row (a dict). Missing optional fields default safely."""
        return Product(
            product_id=row["product_id"],
            name=row["name"],
            category=row["category"],
            price=float(row["price"]),
            quantity_in_stock=int(row["quantity_in_stock"]),
            cost_price=float(row.get("cost_price") or 0),
            supplier=row.get("supplier") or "",
            expiry_date=row.get("expiry_date") or "",
        )
