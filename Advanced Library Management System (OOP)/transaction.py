class Transaction:
    """Represents one borrow/return event in the library."""

    def __init__(self, transaction_id, member_id, book_id, borrow_date):
        self.transaction_id = transaction_id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.return_date = None  # stays None until the book is returned
        self.fine = 0.0

    def mark_returned(self, return_date, fine=0.0):
        """Records the return date and any late fine for this transaction."""
        self.return_date = return_date
        self.fine = fine

    def get_details(self):
        """Returns a readable string with this transaction's details."""
        status = f"Returned on {self.return_date}" if self.return_date else "Not returned yet"
        details = (f"Transaction #{self.transaction_id} - Member {self.member_id}, "
                   f"Book {self.book_id}, Borrowed: {self.borrow_date}, {status}")
        if self.fine > 0:
            details += f", Fine: ${self.fine:.2f}"
        return details
