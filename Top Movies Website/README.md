# Top Movies Website

A simple Flask web app to search, add, rate, review, and manage a personal movies list using The Movie Database (TMDb) API.

## Demo Video
<video src="" controls width="600"></video>

## Features
- Search movies via TMDb and add them to a local SQLite database
- Rate and review movies
- Automatic ranking by rating
- Edit and delete movie entries

## Tech stack / Dependencies
- Python 3.10+
- Flask
- Flask-WTF
- Flask-Bootstrap (Bootstrap-Flask)
- Flask-SQLAlchemy / SQLAlchemy
- WTForms
- Requests

See full dependency list: [requirements.txt](requirements.txt)

## Quick setup
1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Or on bash/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration
- The TMDb API key is currently defined in the source at [main.py](main.py#L1-L20) as `MOVIE_DB_API_KEY`.
- The app uses an SQLite database file `movies.db` created automatically in the project folder.

Tip: For production or security, remove the hard-coded API key and read it from an environment variable.

## Run
Start the app with:

```bash
python main.py
```

Then open http://127.0.0.1:5003/ in your browser.

## Project structure
- `main.py` — Flask application and routes
- `requirements.txt` — Python dependencies
- `templates/` — HTML templates (index, add, edit, select)
- `static/` — CSS and static assets
- `instance/` — (optional) runtime files

## Usage
- Add a movie: click "Add", search by title, choose a result, then rate and review.
- Edit a movie: click "Edit" next to an entry to update rating/review.
- Delete a movie: click "Delete" to remove it from the database.

## Notes
- The app listens on port `5003` by default (see `main.py`).
- The SQLite DB and uploaded data remain local to this project folder.

If you'd like, I can: run the app, remove the hard-coded API key, or add a sample `.env` configuration—which would you prefer?
