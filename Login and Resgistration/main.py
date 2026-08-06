from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-change-this-in-production'

# CREATE DATABASE SETUP
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CONFIGURE FLASK-LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, int(user_id))

# DATABASE USER MODEL
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)

with app.app_context():
    db.create_all()

# ------------------- ROUTES -------------------

@app.route('/')
def home():
    """Home landing page route."""
    return render_template("index.html", logged_in=current_user.is_authenticated)

@app.route('/register', methods=["GET", "POST"])
def register():
    """User registration route with email duplication check."""
    if current_user.is_authenticated:
        return redirect(url_for('secrets'))

    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # Check if user email already exists
        result = db.session.execute(db.select(User).where(User.email == email))
        existing_user = result.scalar()

        if existing_user:
            flash("An account with that email already exists. Please log in instead.", "warning")
            return redirect(url_for('login'))

        # Secure password hashing with salt
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            email=email,
            name=name,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        # Log in newly created user immediately
        login_user(new_user)
        flash("Welcome aboard! Your account has been created successfully.", "success")
        return redirect(url_for("secrets"))

    return render_template("register.html", logged_in=current_user.is_authenticated)

@app.route('/login', methods=["GET", "POST"])
def login():
    """User login route with credential verification."""
    if current_user.is_authenticated:
        return redirect(url_for('secrets'))

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()

        if not user:
            flash("That email address does not exist. Please check and try again.", "danger")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for('login'))
        else:
            login_user(user)
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for('secrets'))

    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/secrets')
@login_required
def secrets():
    """Protected user dashboard."""
    return render_template("secrets.html", name=current_user.name, logged_in=True)

@app.route('/logout')
@login_required
def logout():
    """Session destruction route."""
    logout_user()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('home'))

@app.route('/download')
@login_required
def download():
    """Protected file download route."""
    return send_from_directory('static', path="files/cheat_sheet.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)