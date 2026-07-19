class Member:
    """Represents a library member who can borrow and return books."""

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []  # list of Book objects currently held

    def borrow_book(self, book):
        """Adds a book to this member's borrowed list."""
        self.borrowed_books.append(book)

    def return_book(self, book):
        """Removes a book from this member's borrowed list."""
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def get_borrowed_count(self):
        """Returns how many books this member currently has."""
        return len(self.borrowed_books)

    def get_details(self):
        """Returns a readable string with this member's details."""
        return f"[{self.member_id}] {self.name} - Books borrowed: {self.get_borrowed_count()}"
