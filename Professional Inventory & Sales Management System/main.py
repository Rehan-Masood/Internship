import sys
from inventory_manager import InventoryManager
from report_generator import ReportGenerator
from exporter import export_inventory_to_excel, export_daily_report_to_pdf
from utils import (
    get_valid_text, get_valid_price, get_valid_quantity, get_optional_float,
    paginate_products, print_success, print_error, print_warning, print_info, print_heading,
)
from datetime import date

# Force UTF-8 output so special characters never crash on Windows terminals
sys.stdout.reconfigure(encoding="utf-8")

MAIN_MENU = """
========================================
   PROFESSIONAL INVENTORY & SALES MANAGER
========================================
1. Add Product
2. Sell Product(s)
3. Restock Product
4. Search Product
5. View All Products
6. Update Product
7. Delete Product
8. Reports & Analytics
9. Data Export
10. Undo Last Action
11. Save Data
0. Exit
"""

REPORTS_MENU = """
----- Reports & Analytics -----
1. Daily Sales Report
2. Monthly Sales Report
3. Top Selling Products
4. Category-wise Sales
5. Slow-Moving Stock
6. Low Stock Alert
7. Expiry Alert
8. Profit Report
9. Revenue Trend Chart
0. Back to Main Menu
"""

EXPORT_MENU = """
----- Data Export -----
1. Export Inventory to Excel
2. Export Daily Sales Report to PDF
0. Back to Main Menu
"""

inventory = InventoryManager()
inventory.load_data()
report = ReportGenerator(inventory)

print_heading("Welcome to your Inventory & Sales Manager!")


def handle_reports_menu():
    while True:
        print(REPORTS_MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            report.daily_sales_report()
        elif choice == "2":
            report.monthly_sales_report()
        elif choice == "3":
            report.top_selling_products()
        elif choice == "4":
            report.category_wise_sales()
        elif choice == "5":
            report.slow_moving_products()
        elif choice == "6":
            report.low_stock_alert()
        elif choice == "7":
            report.expiry_alert()
        elif choice == "8":
            report.profit_report()
        elif choice == "9":
            report.revenue_trend_chart()
        elif choice == "0":
            break
        else:
            print_error("Invalid choice. Please try again.")


def handle_export_menu():
    while True:
        print(EXPORT_MENU)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            export_inventory_to_excel(inventory.products)
        elif choice == "2":
            export_daily_report_to_pdf(
                [s for s in inventory.sales if s.date_time.date() == date.today()],
                date.today(),
            )
        elif choice == "0":
            break
        else:
            print_error("Invalid choice. Please try again.")


is_running = True

while is_running:
    print(MAIN_MENU)
    choice = input("Enter your choice: ").strip()

    # ----- 1. Add Product -----
    if choice == "1":
        name = get_valid_text("Enter product name: ")
        category = get_valid_text("Enter category: ")
        price = get_valid_price("Enter selling price: ")
        quantity = get_valid_quantity("Enter starting stock quantity: ")
        cost_price = get_optional_float("Enter cost price (optional, for profit tracking): ", default=0.0)
        supplier = input("Enter supplier name (optional): ").strip()
        expiry_date = input("Enter expiry date YYYY-MM-DD (optional, leave blank if none): ").strip()

        inventory.add_product(name, category, price, quantity, cost_price, supplier, expiry_date)
        print_success(f"'{name}' added to inventory.")

    # ----- 2. Sell Product(s) -----
    elif choice == "2":
        cart_items = []

        while True:
            product_id = input("Enter Product ID to sell (or 'done' to finish): ").strip()
            if product_id.lower() == "done":
                break

            product = inventory.find_product_by_id(product_id)
            if product is None:
                print_error(f"No product found with ID '{product_id}'. Please try again.")
                continue

            quantity = get_valid_quantity(f"Enter quantity of '{product.name}' to sell: ")

            if quantity > product.quantity_in_stock:
                print_error(f"Insufficient stock! Only {product.quantity_in_stock} unit(s) of "
                            f"'{product.name}' available.")
                continue

            cart_items.append((product, quantity))
            print_success(f"Added {quantity}x {product.name} to the cart.")

        if not cart_items:
            print_warning("Sale cancelled - no items were added.")
        else:
            # ----- confirmation summary before finalizing -----
            subtotal = sum(product.price * quantity for product, quantity in cart_items)
            print_heading("\n----- Order Summary -----")
            for product, quantity in cart_items:
                print(f"{quantity}x {product.name} @ Rs.{product.price:.2f} = Rs.{product.price * quantity:.2f}")
            print(f"Subtotal: Rs.{subtotal:.2f}")

            discount_percent = get_optional_float("Enter discount % (optional, leave blank for none): ", default=0.0)
            staff_name = input("Enter staff name (optional): ").strip()

            estimated_total = subtotal * (1 - discount_percent / 100)
            print(f"Estimated Total: Rs.{estimated_total:.2f}")

            confirm = input("Confirm this sale? (y/n): ").strip().lower()
            if confirm != "y":
                print_warning("Sale cancelled. No stock was deducted.")
            else:
                sale = inventory.sell_items(cart_items, staff_name, discount_percent)
                sale.print_invoice()

                for product, _ in cart_items:
                    if product.is_low_on_stock():
                        print_warning(f"WARNING: '{product.name}' stock is now only "
                                      f"{product.quantity_in_stock} unit(s)! Restock needed.")

    # ----- 3. Restock Product -----
    elif choice == "3":
        product_id = get_valid_text("Enter Product ID to restock: ")
        quantity = get_valid_quantity("Enter quantity to add: ")
        inventory.restock_product(product_id, quantity)

    # ----- 4. Search Product -----
    elif choice == "4":
        search_choice = input("Search by (1) Name or (2) Category? Enter 1 or 2: ").strip()
        search_by = "name" if search_choice == "1" else "category"
        keyword = get_valid_text(f"Enter {search_by} to search for: ")

        results = inventory.search_product(keyword, search_by)
        if not results:
            print_error("Product not found.")
        else:
            print_heading(f"\n----- Search Results ({len(results)} found) -----")
            for product in results:
                product.display_info()

    # ----- 5. View All Products (paginated) -----
    elif choice == "5":
        paginate_products(inventory.products, page_size=10)

    # ----- 6. Update Product -----
    elif choice == "6":
        product_id = get_valid_text("Enter Product ID to update: ")
        product = inventory.find_product_by_id(product_id)

        if product is None:
            print_error(f"No product found with ID '{product_id}'.")
        else:
            print(f"Current details: {product.name}, {product.category}, Rs.{product.price:.2f}, "
                  f"Stock: {product.quantity_in_stock}")
            print("Leave a field blank to keep its current value.")

            name_input = input(f"New name [{product.name}]: ").strip()
            category_input = input(f"New category [{product.category}]: ").strip()
            price_input = input(f"New price [{product.price}]: ").strip()
            quantity_input = input(f"New quantity [{product.quantity_in_stock}]: ").strip()

            new_price = None
            if price_input:
                try:
                    new_price = float(price_input)
                except ValueError:
                    print_error(f"'{price_input}' is not a valid price. Price left unchanged.")

            new_quantity = None
            if quantity_input:
                try:
                    new_quantity = int(quantity_input)
                except ValueError:
                    print_error(f"'{quantity_input}' is not a valid quantity. Quantity left unchanged.")

            inventory.update_product(
                product_id,
                name=name_input if name_input else None,
                category=category_input if category_input else None,
                price=new_price,
                quantity=new_quantity,
            )
            print_success(f"Product '{product_id}' updated.")

    # ----- 7. Delete Product -----
    elif choice == "7":
        product_id = get_valid_text("Enter Product ID to delete: ")
        confirm = input(f"Are you sure you want to delete '{product_id}'? (y/n): ").strip().lower()
        if confirm == "y":
            inventory.delete_product(product_id)
        else:
            print_warning("Delete cancelled.")

    # ----- 8. Reports & Analytics -----
    elif choice == "8":
        handle_reports_menu()

    # ----- 9. Data Export -----
    elif choice == "9":
        handle_export_menu()

    # ----- 10. Undo Last Action -----
    elif choice == "10":
        inventory.undo_last_action()

    # ----- 11. Save Data -----
    elif choice == "11":
        inventory.save_data()

    # ----- 0. Exit -----
    elif choice == "0":
        inventory.save_data()
        print_success("Goodbye!")
        is_running = False

    else:
        print_error("Invalid choice. Please select an option from the menu.")
