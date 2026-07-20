class User:
    """Represents the person using the app, and keeps track of their transactions and balance."""

    def __init__(self, name):
        self.name = name
        self.transactions = []
        self.balance = 0.0

    def add_transaction(self, transaction):
        """Adds a transaction to this user's history and updates their balance."""
        self.transactions.append(transaction)
        if transaction.type == "Income":
            self.balance += transaction.amount
        else:
            self.balance -= transaction.amount

    def get_total_income(self):
        """Returns the sum of all income transactions."""
        total = 0.0
        for transaction in self.transactions:
            if transaction.type == "Income":
                total += transaction.amount
        return total

    def get_total_expense(self):
        """Returns the sum of all expense transactions."""
        total = 0.0
        for transaction in self.transactions:
            if transaction.type == "Expense":
                total += transaction.amount
        return total