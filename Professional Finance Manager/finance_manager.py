from transaction import Transaction
from budget_alert import BudgetAlert

DATA_FILE = "finance_data.txt"


class FinanceManager:
    """Main controller: manages all transactions for a user, and handles saving/loading."""

    def __init__(self, user):
        self.user = user

    def add_transaction(self, name, date, amount, category, transaction_type):
        """Creates a new transaction, adds it to the user, and checks the budget alert.
        Blocks the transaction if it's an expense that exceeds the current balance."""

        if transaction_type == "Expense" and amount > self.user.balance:
            print(f"Insufficient balance! Your current balance is ${self.user.balance:.2f}, "
                  f"but this expense is ${amount:.2f}. Transaction not added.")
            return

        transaction = Transaction(name, date, amount, category, transaction_type)
        self.user.add_transaction(transaction)
        print(f"Transaction added: {transaction.get_details()}")

        BudgetAlert.check_alert(self.user.get_total_income(), self.user.get_total_expense())

    def generate_report(self):
        """Prints a summary report of all transactions and totals."""
        if not self.user.transactions:
            print("No transactions recorded yet.")
            return

        print("\n----- Transaction History -----")
        for transaction in self.user.transactions:
            print(transaction.get_details())

        print("\n----- Summary -----")
        print(f"Total Income:  ${self.user.get_total_income():.2f}")
        print(f"Total Expense: ${self.user.get_total_expense():.2f}")
        print(f"Balance:       ${self.user.balance:.2f}")

    def save_to_file(self, filename=DATA_FILE):
        """Saves every transaction to a text file so data isn't lost when the program closes."""
        with open(filename, "w") as file:
            for transaction in self.user.transactions:
                file.write(transaction.to_line())
        print(f"Data saved to {filename}.")

    def load_from_file(self, filename=DATA_FILE):
        """Loads previously saved transactions from a text file, if it exists."""
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("No saved data found. Starting fresh.")
            return

        for line in lines:
            if line.strip():
                transaction = Transaction.from_line(line)
                self.user.add_transaction(transaction)

        print(f"Loaded {len(lines)} transaction(s) from {filename}.")