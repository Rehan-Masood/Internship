class Book:
    """Represents a single book in the library."""

    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.borrowed_by = None   # member_id of the borrower
        self.due_date = None      # date the book must be returned by

    def get_details(self):
        """Returns a readable string with all details of the book."""
        status = "Borrowed" if self.is_borrowed else "Available"
        details = f"[{self.book_id}] '{self.title}' by {self.author} - {status}"
        if self.is_borrowed:
            details += f" (Borrowed by Member {self.borrowed_by}, Due: {self.due_date})"
        return details

    def mark_borrowed(self, member_id, due_date):
        """Marks this book as borrowed by a specific member."""
        self.is_borrowed = True
        self.borrowed_by = member_id
        self.due_date = due_date

    def mark_returned(self):
        """Marks this book as returned and available again."""
        self.is_borrowed = False
        self.borrowed_by = None
        self.due_date = None
