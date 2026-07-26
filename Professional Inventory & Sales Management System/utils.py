from colorama import init, Fore, Style

init(autoreset=True)  # so colors don't bleed into the next print statement


# ----- Colored output helpers -----
def print_success(message):
    print(Fore.GREEN + message)


def print_error(message):
    print(Fore.RED + message)


def print_warning(message):
    print(Fore.YELLOW + message)


def print_info(message):
    print(Fore.CYAN + message)


def print_heading(message):
    print(Style.BRIGHT + Fore.MAGENTA + message)


# ----- Input validation helpers -----
def get_valid_text(prompt):
    """Keeps asking until the user enters some non-empty text."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print_error("This field cannot be empty. Please try again.")


def get_valid_price(prompt):
    """Keeps asking until the user enters a valid positive price."""
    while True:
        raw_value = input(prompt).strip()
        try:
            price = float(raw_value)
            if price <= 0:
                print_error("Price must be greater than 0. Please try again.")
                continue
            return price
        except ValueError:
            print_error(f"'{raw_value}' is not a valid number. Please enter a price like 20 or 49.99.")


def get_valid_quantity(prompt):
    """Keeps asking until the user enters a valid positive whole number."""
    while True:
        raw_value = input(prompt).strip()
        try:
            quantity = int(raw_value)
            if quantity <= 0:
                print_error("Quantity must be a positive number. Please try again.")
                continue
            return quantity
        except ValueError:
            print_error(f"'{raw_value}' is not a valid whole number. Please try again.")


def get_optional_float(prompt, default=0.0):
    """Asks for a number but allows leaving it blank to use the default."""
    raw_value = input(prompt).strip()
    if not raw_value:
        return default
    try:
        return float(raw_value)
    except ValueError:
        print_error(f"'{raw_value}' is not a valid number. Using default: {default}")
        return default


# ----- Pagination helper -----
def paginate_products(products, page_size=10):
    """Displays a list of products one page at a time."""
    total = len(products)
    if total == 0:
        print_info("No products to display.")
        return

    start = 0
    while start < total:
        page = products[start:start + page_size]
        page_number = (start // page_size) + 1
        total_pages = (total + page_size - 1) // page_size

        print_heading(f"\n----- Products (Page {page_number}/{total_pages}) -----")
        for product in page:
            product.display_info()

        start += page_size
        if start < total:
            choice = input("\nPress Enter for next page, or type 'q' to stop: ").strip().lower()
            if choice == "q":
                break
