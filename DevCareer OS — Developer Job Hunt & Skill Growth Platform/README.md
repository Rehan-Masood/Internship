# DevCareer OS — Developer Job Hunt & Skill Growth Platform

Simple Flask app to track developer job applications and practice skills.

## Project Structure

- [app.py](app.py) — Flask application entrypoint.
- [requirements.txt](requirements.txt) — Python dependencies.
- [schema.sql](schema.sql) — Database schema (SQLite).
- [templates/](templates/) — HTML templates (index, add_job, flashcards, base).
- [static/](static/) — CSS and other static assets.

## Features

- Add and list job applications.
- Simple flashcards interface for study/practice.
- Minimal, easy-to-extend Flask codebase.

## Requirements

- Python 3.10+ (recommended)
- See `[requirements.txt](requirements.txt)` for packages.

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the database (SQLite):

```bash
# Create a SQLite database file and apply schema
sqlite3 devcareer.db < schema.sql
```

If you don't have `sqlite3` CLI, open your favorite DB client and run the SQL in [schema.sql](schema.sql).

## Running

Start the app with:

```bash
python app.py
# or, if using Flask CLI
set FLASK_APP=app.py
flask run
```

Open http://127.0.0.1:5000/ in your browser.

## Development Notes

- Templates are in the [templates/](templates/) folder.
- Static CSS is in [static/css/style.css](static/css/style.css).
- To add features, extend routes in `app.py` and corresponding templates.

## Contributing

Feel free to open issues or submit PRs. For quick help, ask the maintainer.

## License

This project does not include a license file. Add one if you plan to publish.
