# Name Card Website

A minimal Flask web app that serves a simple name-card webpage.

## Features
- Serves `index.html` from the `templates/` folder
- Static assets served from `static/`

## Prerequisites
- Python 3.8 or newer
- `pip` (Python package manager)

## Setup
1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1  # PowerShell
# or for cmd.exe: venv\Scripts\activate.bat
```

2. Install dependencies:

If you have a `requirements.txt` file:

```powershell
pip install -r requirements.txt
```

Otherwise install Flask directly:

```powershell
pip install Flask
```

## Run the app

Start the server with:

```powershell
python server.py
```

Then open http://127.0.0.1:5000/ in your browser.

## Project Structure

- `server.py` — Flask application entrypoint
- `templates/index.html` — main HTML page
- `static/` — CSS, images, and other static assets

## Notes
- The app currently runs in Flask's debug mode (`app.run(debug=True)`).
  Disable debug mode or use a production WSGI server for deployment.

If you'd like, I can also add a `requirements.txt` and a short `README` badge.
