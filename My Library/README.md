# My Library

A small Flask app to track books and ratings using SQLite and SQLAlchemy.

## Features
- Add, edit (rating), and delete books
- Persistent storage with SQLite (`books.db`)
- Simple HTML templates for listing and forms

## Prerequisites
- Python 3.8+
- `pip` for installing dependencies

## Install
1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# Windows (cmd)
.\.venv\Scripts\activate.bat
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run
The app runs on port `5002` by default in development mode.

```bash
# Run directly
python main.py

# Or use flask (if FLASK_APP is desired):
# set FLASK_APP=main.py
# flask run --port 5002
```

After starting, open http://127.0.0.1:5002/ in your browser.

## Project layout
- `main.py` — Flask application and routes
- `requirements.txt` — Python dependencies
- `templates/` — HTML templates used by the app
  - `index.html` — book list
  - `add.html` — add book form
  - `edit_rating.html` — edit rating form
- `books.db` — SQLite database (created at runtime)

## Notes
- The app uses `Flask`, `flask_sqlalchemy`, and `SQLAlchemy`.
- Database tables are created automatically on first run.

## License
Choose a license for your project (e.g., MIT) and add a `LICENSE` file.

---
If you want, I can also add a minimal `README` badge, a `LICENSE` file, or a short `CONTRIBUTING.md`.
