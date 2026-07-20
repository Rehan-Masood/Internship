class Transaction:
    """Represents a single income or expense entry."""

    def __init__(self, name, date, amount, category, transaction_type):
        self.name = name          # short description, e.g. "Electricity bill"
        self.date = date
        self.amount = amount
        self.category = category
        self.type = transaction_type  # "Income" or "Expense"

    def get_details(self):
        """Returns a readable string with all details of this transaction."""
        return (f"{self.date} | {self.type:<7} | {self.category:<12} | "
                f"{self.name:<20} | ${self.amount:.2f}")

    def to_line(self):
        """Converts this transaction into one CSV line for saving to a file."""
        return f"{self.name},{self.date},{self.amount},{self.category},{self.type}\n"

    @staticmethod
    def from_line(line):
        """Rebuilds a Transaction object from one CSV line read from a file."""
        name, date, amount, category, transaction_type = line.strip().split(",")
        return Transaction(name, date, float(amount), category, transaction_type)