import datetime
import json
import sqlite3
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'nutriflow_enterprise_secret_key_2026'
DB_FILE = 'database.db'


def init_db():
  """Initializes database tables and seeds menu items with image URLs."""
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image_url TEXT
        )
    """)

  cursor.execute('SELECT COUNT(*) FROM menu_items')
  if cursor.fetchone()[0] == 0:
    items = [
        (
            'Truffle Burger',
            'Mains',
            18.50,
            'Angus beef patty, black truffle aioli, aged cheddar on brioche.',
            'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80',
        ),
        (
            'Artisanal Margherita',
            'Mains',
            16.00,
            'San Marzano tomatoes, fresh mozzarella, organic basil.',
            'https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?auto=format&fit=crop&w=600&q=80',
        ),
        (
            'Pan-Seared Salmon',
            'Mains',
            24.00,
            'Atlantic salmon, asparagus, lemon-herb butter.',
            'https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=600&q=80',
        ),
        (
            'Caesar Salad',
            'Starters',
            12.00,
            'Romaine hearts, garlic croutons, parmigiano reggiano.',
            'https://images.unsplash.com/photo-1546793665-c74683f339c1?auto=format&fit=crop&w=600&q=80',
        ),
        (
            'Matcha Milk Tea',
            'Beverages',
            6.50,
            'Ceremonial grade matcha, oat milk, boba pearls.',
            'https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&w=600&q=80',
        ),
        (
            'Chocolate Lava Cake',
            'Desserts',
            9.50,
            'Warm chocolate ganache, vanilla bean gelato.',
            'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=600&q=80',
        ),
    ]
    cursor.executemany(
        'INSERT INTO menu_items (name, category, price, description, image_url)'
        ' VALUES (?, ?, ?, ?, ?)',
        items,
    )

  conn.commit()
  conn.close()


def get_db():
  conn = sqlite3.connect(DB_FILE)
  conn.row_factory = sqlite3.Row
  return conn


@app.route('/')
def index():
  if 'user_id' in session:
    return redirect(url_for('menu'))
  return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    hashed_pw = generate_password_hash(password)
    db = get_db()
    cursor = db.cursor()

    try:
      cursor.execute(
          'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
          (username, email, hashed_pw),
      )
      db.commit()
      flash('Registration successful! Please login.', 'success')
      return redirect(url_for('login'))
    except sqlite3.IntegrityError:
      flash('Username or Email already exists.', 'error')
    finally:
      db.close()

  return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    db = get_db()
    user = db.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    db.close()

    if user and check_password_hash(user['password'], password):
      session['user_id'] = user['id']
      session['username'] = user['username']
      flash('Welcome back!', 'success')
      return redirect(url_for('menu'))
    else:
      flash('Invalid credentials. Please try again.', 'error')

  return render_template('login.html')


@app.route('/logout')
def logout():
  session.clear()
  flash('Logged out successfully.', 'info')
  return redirect(url_for('login'))


@app.route('/menu')
def menu():
  if 'user_id' not in session:
    return redirect(url_for('login'))

  db = get_db()
  items = db.execute('SELECT * FROM menu_items').fetchall()
  db.close()
  return render_template('menu.html', items=items, username=session['username'])


@app.route('/checkout', methods=['POST'])
def checkout():
  if 'user_id' not in session:
    return redirect(url_for('login'))

  raw_cart = request.form.get('cart_data', '')

  if not raw_cart or raw_cart == '[]':
    flash('Your cart is empty. Please add items before checking out.', 'error')
    return redirect(url_for('menu'))

  try:
    cart_items = json.loads(raw_cart)
  except Exception:
    flash('Invalid cart submission.', 'error')
    return redirect(url_for('menu'))

  subtotal = sum(
      float(item.get('price', 0)) * int(item.get('qty', 1))
      for item in cart_items
  )
  tax = round(subtotal * 0.10, 2)
  total = round(subtotal + tax, 2)

  receipt = {
      'order_id': f'NFE-{int(datetime.datetime.now().timestamp())}',
      'date': datetime.datetime.now().strftime('%B %d, %Y - %I:%M %p'),
      'username': session['username'],
      'cart_items': cart_items,  # Avoids shadowing python dictionary method .items()
      'subtotal': f'{subtotal:.2f}',
      'tax': f'{tax:.2f}',
      'total': f'{total:.2f}',
  }

  return render_template('receipt.html', receipt=receipt)


if __name__ == '__main__':
  init_db()
  app.run(debug=True, port=5000)