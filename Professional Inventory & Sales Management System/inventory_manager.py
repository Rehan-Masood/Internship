import csv
import os
from datetime import datetime
from product import Product
from sale import Sale

PRODUCTS_FILE = "products.csv"
SALES_FILE = "sales.csv"

PRODUCT_FIELDS = ["product_id", "name", "category", "price", "quantity_in_stock",
                   "cost_price", "supplier", "expiry_date"]
SALE_FIELDS = ["sale_id", "date_time", "product_id", "name", "quantity", "price",
               "cost_price", "staff_name", "discount_percent"]


class InventoryManager:
    """Main controller: manages all products and sales, and handles saving/loading."""

    def __init__(self):
        self.products = []
        self.sales = []
        self.next_product_number = 1
        self.next_sale_number = 1
        self.undo_stack = []  # keeps recent actions so the last one can be undone

    # ----- ID generation -----
    def generate_product_id(self):
        product_id = f"P{self.next_product_number:03d}"
        self.next_product_number += 1
        return product_id

    def generate_sale_id(self):
        sale_id = f"S{self.next_sale_number:03d}"
        self.next_sale_number += 1
        return sale_id

    # ----- Undo support -----
    def _record_undo(self, action_type, data):
        """Stores enough information to reverse the most recent action."""
        self.undo_stack.append({"type": action_type, "data": data})

    def undo_last_action(self):
        """Reverses the most recent add / delete / restock / update / sell action."""
        if not self.undo_stack:
            print("Nothing to undo.")
            return

        action = self.undo_stack.pop()
        action_type = action["type"]
        data = action["data"]

        if action_type == "add_product":
            product = self.find_product_by_id(data["product_id"])
            if product:
                self.products.remove(product)
            print(f"Undo: removed newly added product '{data['product_id']}'.")

        elif action_type == "delete_product":
            self.products.append(data["product"])
            print(f"Undo: restored deleted product '{data['product'].product_id}'.")

        elif action_type == "restock_product":
            product = self.find_product_by_id(data["product_id"])
            if product:
                product.update_stock(-data["quantity"])
            print(f"Undo: reversed restock of {data['quantity']} unit(s) for '{data['product_id']}'.")

        elif action_type == "update_product":
            product = self.find_product_by_id(data["product_id"])
            if product:
                product.name = data["previous"]["name"]
                product.category = data["previous"]["category"]
                product.price = data["previous"]["price"]
                product.quantity_in_stock = data["previous"]["quantity_in_stock"]
                product.cost_price = data["previous"]["cost_price"]
                product.supplier = data["previous"]["supplier"]
                product.expiry_date = data["previous"]["expiry_date"]
            print(f"Undo: reverted changes to product '{data['product_id']}'.")

        elif action_type == "sell_items":
            # restore stock for every item in the sale, then remove the sale record
            sale = data["sale"]
            for item in sale.product_list:
                product = self.find_product_by_id(item["product_id"])
                if product:
                    product.update_stock(item["quantity"])
            if sale in self.sales:
                self.sales.remove(sale)
            print(f"Undo: reversed sale '{sale.sale_id}' and restored stock.")

    # ----- Product management -----
    def add_product(self, name, category, price, quantity, cost_price=0.0, supplier="", expiry_date=""):
        product_id = self.generate_product_id()
        product = Product(product_id, name, category, price, quantity, cost_price, supplier, expiry_date)
        self.products.append(product)
        self._record_undo("add_product", {"product_id": product_id})
        print(f"Product added successfully: {product_id} - {name}")
        return product

    def find_product_by_id(self, product_id):
        for product in self.products:
            if product.product_id.lower() == product_id.lower():
                return product
        return None

    def search_product(self, keyword, search_by="name"):
        """Returns a list of products matching the keyword, by name or category."""
        results = []
        for product in self.products:
            field = product.name if search_by == "name" else product.category
            if keyword.lower() in field.lower():
                results.append(product)
        return results

    def restock_product(self, product_id, quantity):
        product = self.find_product_by_id(product_id)
        if product is None:
            print(f"No product found with ID '{product_id}'.")
            return
        product.update_stock(quantity)
        self._record_undo("restock_product", {"product_id": product_id, "quantity": quantity})
        print(f"Restocked {quantity} unit(s) of '{product.name}'. New stock: {product.quantity_in_stock}")

    def update_product(self, product_id, name=None, category=None, price=None,
                        quantity=None, cost_price=None, supplier=None, expiry_date=None):
        """Updates any given fields of an existing product. Pass None to leave a field unchanged."""
        product = self.find_product_by_id(product_id)
        if product is None:
            print(f"No product found with ID '{product_id}'.")
            return False

        previous = {
            "name": product.name, "category": product.category, "price": product.price,
            "quantity_in_stock": product.quantity_in_stock, "cost_price": product.cost_price,
            "supplier": product.supplier, "expiry_date": product.expiry_date,
        }

        if name is not None:
            product.name = name
        if category is not None:
            product.category = category
        if price is not None:
            product.price = price
        if quantity is not None:
            product.quantity_in_stock = quantity
        if cost_price is not None:
            product.cost_price = cost_price
        if supplier is not None:
            product.supplier = supplier
        if expiry_date is not None:
            product.expiry_date = expiry_date

        self._record_undo("update_product", {"product_id": product_id, "previous": previous})
        print(f"Product '{product_id}' updated successfully.")
        return True

    def delete_product(self, product_id):
        """Removes a product from the inventory entirely."""
        product = self.find_product_by_id(product_id)
        if product is None:
            print(f"No product found with ID '{product_id}'.")
            return False

        self.products.remove(product)
        self._record_undo("delete_product", {"product": product})
        print(f"Product '{product_id} - {product.name}' has been deleted.")
        return True

    def expiring_soon_products(self):
        """Returns all products whose expiry date is within the warning window."""
        return [p for p in self.products if p.is_expiring_soon()]

    # ----- Selling -----
    def sell_items(self, cart_items, staff_name="", discount_percent=0.0):
        """Finalizes a sale for a list of (product, quantity) pairs already validated by the caller.
        Deducts stock, creates a Sale record, and returns it."""
        sale_id = self.generate_sale_id()
        product_list = []

        for product, quantity in cart_items:
            product.update_stock(-quantity)
            product_list.append({
                "product_id": product.product_id,
                "name": product.name,
                "quantity": quantity,
                "price": product.price,
                "cost_price": product.cost_price,
            })

        sale = Sale(sale_id, product_list, datetime.now(), staff_name, discount_percent)
        self.sales.append(sale)
        self._record_undo("sell_items", {"sale": sale})
        return sale

    # ----- File persistence -----
    def save_data(self):
        """Saves the full current state of products and sales to their CSV files."""
        with open(PRODUCTS_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=PRODUCT_FIELDS)
            writer.writeheader()
            for product in self.products:
                writer.writerow(product.to_dict())

        with open(SALES_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=SALE_FIELDS)
            writer.writeheader()
            for sale in self.sales:
                for row in sale.to_rows():
                    writer.writerow(row)

        print("Data saved successfully.")

    def load_data(self):
        """Loads products and sales from their CSV files, if they exist."""
        self._load_products()
        self._load_sales()

    def _load_products(self):
        if not os.path.exists(PRODUCTS_FILE):
            return

        with open(PRODUCTS_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row:
                    self.products.append(Product.from_dict(row))

        # make sure the next auto-generated ID continues after the highest loaded one
        if self.products:
            highest_number = max(int(p.product_id[1:]) for p in self.products)
            self.next_product_number = highest_number + 1

    def _load_sales(self):
        if not os.path.exists(SALES_FILE):
            return

        sales_by_id = {}

        with open(SALES_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row:
                    continue
                sale_id = row["sale_id"]
                item = {
                    "product_id": row["product_id"],
                    "name": row["name"],
                    "quantity": int(row["quantity"]),
                    "price": float(row["price"]),
                    "cost_price": float(row.get("cost_price") or 0),
                }
                if sale_id not in sales_by_id:
                    sales_by_id[sale_id] = {
                        "date_time": row["date_time"],
                        "staff_name": row.get("staff_name") or "",
                        "discount_percent": float(row.get("discount_percent") or 0),
                        "items": [],
                    }
                sales_by_id[sale_id]["items"].append(item)

        for sale_id, sale_info in sales_by_id.items():
            date_time = datetime.strptime(sale_info["date_time"], "%Y-%m-%d %H:%M:%S")
            sale = Sale(sale_id, sale_info["items"], date_time,
                        sale_info["staff_name"], sale_info["discount_percent"])
            self.sales.append(sale)

        if self.sales:
            highest_number = max(int(s.sale_id[1:]) for s in self.sales)
            self.next_sale_number = highest_number + 1
