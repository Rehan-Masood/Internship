import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'library-secret-key-9876'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    """Renders the library dashboard with all books sorted by rating."""
    all_books = Book.query.order_by(Book.rating.desc()).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    """Handles adding a new book to the database."""
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"].strip(),
            author=request.form["author"].strip(),
            rating=float(request.form["rating"])
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    """Handles updating the rating of an existing book."""
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db.session.get(Book, book_id)
        if book_to_update:
            book_to_update.rating = float(request.form["rating"])
            db.session.commit()
        return redirect(url_for('home'))

    book_id = request.args.get('id')
    book_selected = db.session.get(Book, book_id)
    return render_template("edit_rating.html", book=book_selected)


@app.route("/delete")
def delete():
    """Deletes a book from the database by ID."""
    book_id = request.args.get('id')
    book_to_delete = db.session.get(Book, book_id)
    if book_to_delete:
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=5002)