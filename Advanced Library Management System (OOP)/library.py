from datetime import date, timedelta
from transaction import Transaction

BORROW_PERIOD_DAYS = 14   # how many days a member can keep a book
FINE_PER_DAY = 1.0        # late fine charged per day, in dollars


class Library:
    """Main controller class that manages all books, members, and transactions."""

    def __init__(self):
        self.books = []
        self.members = []
        self.transactions = []
        self.next_transaction_id = 1

    # ----- Adding books and members -----
    def add_book(self, book):
        self.books.append(book)
        print(f"Book added: {book.title}")

    def add_member(self, member):
        self.members.append(member)
        print(f"Member added: {member.name}")

    # ----- Searching -----
    def search_book_by_title(self, title):
        """Returns a list of books whose title contains the search text."""
        results = []
        for book in self.books:
            if title.lower() in book.title.lower():
                results.append(book)
        return results

    def search_book_by_author(self, author):
        """Returns a list of books whose author contains the search text."""
        results = []
        for book in self.books:
            if author.lower() in book.author.lower():
                results.append(book)
        return results

    # ----- Displaying -----
    def display_all_books(self):
        if not self.books:
            print("No books in the library yet.")
            return
        for book in self.books:
            print(book.get_details())

    def display_all_members(self):
        if not self.members:
            print("No members registered yet.")
            return
        for member in self.members:
            print(member.get_details())

    # ----- Helper lookups -----
    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def find_member_by_id(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    # ----- Core borrow/return logic -----
    def borrow_book(self, member_id, book_id):
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_id(book_id)

        if member is None:
            print("Member not found.")
            return
        if book is None:
            print("Book not found.")
            return
        if book.is_borrowed:
            print(f"Sorry, '{book.title}' is already borrowed.")
            return

        borrow_date = date.today()
        due_date = borrow_date + timedelta(days=BORROW_PERIOD_DAYS)

        book.mark_borrowed(member_id, due_date)
        member.borrow_book(book)

        transaction = Transaction(self.next_transaction_id, member_id, book_id, borrow_date)
        self.transactions.append(transaction)
        self.next_transaction_id += 1

        print(f"'{book.title}' borrowed successfully by {member.name}. Due date: {due_date}")

    def return_book(self, member_id, book_id):
        member = self.find_member_by_id(member_id)
        book = self.find_book_by_id(book_id)

        if member is None:
            print("Member not found.")
            return
        if book is None:
            print("Book not found.")
            return
        if not book.is_borrowed or book not in member.borrowed_books:
            print(f"'{book.title}' was not borrowed by this member.")
            return

        return_date = date.today()
        fine = self.calculate_late_fine(book.due_date, return_date)

        # find the open transaction for this book and member
        transaction = self.find_open_transaction(member_id, book_id)
        if transaction:
            transaction.mark_returned(return_date, fine)

        book.mark_returned()
        member.return_book(book)

        if fine > 0:
            print(f"'{book.title}' returned late. Fine: ${fine:.2f}")
        else:
            print(f"'{book.title}' returned on time. No fine.")

    def find_open_transaction(self, member_id, book_id):
        """Finds the most recent transaction for this member/book that hasn't been returned yet."""
        for transaction in reversed(self.transactions):
            if (transaction.member_id == member_id
                    and transaction.book_id == book_id
                    and transaction.return_date is None):
                return transaction
        return None

    @staticmethod
    def calculate_late_fine(due_date, return_date):
        """Calculates the fine based on how many days late the book is."""
        if return_date > due_date:
            days_late = (return_date - due_date).days
            return days_late * FINE_PER_DAY
        return 0.0

    def display_all_transactions(self):
        if not self.transactions:
            print("No transactions yet.")
            return
        for transaction in self.transactions:
            print(transaction.get_details())
