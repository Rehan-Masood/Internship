from library import Library
from book import Book
from member import Member

library = Library()

library.add_book(Book("B1", "The Hobbit", "J.R.R. Tolkien"))
library.add_book(Book("B2", "1984", "George Orwell"))
library.add_book(Book("B3", "Clean Code", "Robert C. Martin"))
library.add_member(Member("M1", "Alice"))
library.add_member(Member("M2", "Bob"))

MENU = """
===== LIBRARY MANAGEMENT SYSTEM =====
1. Add Book
2. Add Member
3. Display All Books
4. Display All Members
5. Search Book by Title
6. Search Book by Author
7. Borrow Book
8. Return Book
9. Display All Transactions
0. Exit
"""

is_running = True

while is_running:
    print(MENU)
    choice = input("Enter your choice: ")

    if choice == "1":
        book_id = input("Enter Book ID: ")
        title = input("Enter Title: ")
        author = input("Enter Author: ")
        library.add_book(Book(book_id, title, author))

    elif choice == "2":
        member_id = input("Enter Member ID: ")
        name = input("Enter Name: ")
        library.add_member(Member(member_id, name))

    elif choice == "3":
        library.display_all_books()

    elif choice == "4":
        library.display_all_members()

    elif choice == "5":
        title = input("Enter title to search: ")
        results = library.search_book_by_title(title)
        if results:
            for book in results:
                print(book.get_details())
        else:
            print("No books found with that title.")

    elif choice == "6":
        author = input("Enter author to search: ")
        results = library.search_book_by_author(author)
        if results:
            for book in results:
                print(book.get_details())
        else:
            print("No books found by that author.")

    elif choice == "7":
        member_id = input("Enter Member ID: ")
        book_id = input("Enter Book ID: ")
        library.borrow_book(member_id, book_id)

    elif choice == "8":
        member_id = input("Enter Member ID: ")
        book_id = input("Enter Book ID: ")
        library.return_book(member_id, book_id)

    elif choice == "9":
        library.display_all_transactions()

    elif choice == "0":
        print("Goodbye!")
        is_running = False

    else:
        print("Invalid choice. Please try again.")
