from datetime import date
from user import User
from finance_manager import FinanceManager

MENU = """
===== PERSONAL FINANCE MANAGER =====
1. Add Income
2. Add Expense
3. View Report
4. Save Data
0. Exit
"""

USER_NAME_FILE = "user_name.txt"


def get_user_name():
    """Loads the saved user name if it exists, otherwise asks for it once and saves it."""
    try:
        with open(USER_NAME_FILE, "r") as file:
            saved_name = file.read().strip()
            if saved_name:
                return saved_name
    except FileNotFoundError:
        pass

    # no saved name found (or it was blank) - ask until we get a real answer
    new_name = ""
    while not new_name:
        new_name = input("Enter your name: ").strip()
        if not new_name:
            print("Name cannot be empty. Please try again.")

    with open(USER_NAME_FILE, "w") as file:
        file.write(new_name)

    return new_name


# ----- Set up the user and load any previously saved data -----
name = get_user_name()
print(f"Welcome back, {name}!")
user = User(name)
manager = FinanceManager(user)
manager.load_from_file()

is_running = True

while is_running:
    print(MENU)
    choice = input("Enter your choice: ")

    if choice == "1" or choice == "2":
        transaction_type = "Income" if choice == "1" else "Expense"

        transaction_name = input(f"Enter {transaction_type} name/description (e.g. Electricity bill): ")

        amount_input = input(f"Enter {transaction_type} amount: ")
        try:
            amount = float(amount_input)
        except ValueError:
            print("Invalid amount. Please enter a number.")
            continue

        category = input("Enter category (e.g. Food, Travel, Bills, Salary): ")

        date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
        transaction_date = date_input if date_input else str(date.today())

        manager.add_transaction(transaction_name, transaction_date, amount, category, transaction_type)

    elif choice == "3":
        manager.generate_report()

    elif choice == "4":
        manager.save_to_file()

    elif choice == "0":
        manager.save_to_file()
        print("Goodbye!")
        is_running = False

    else:
        print("Invalid choice. Please try again.")