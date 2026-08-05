# Templating Flask Application

A small Flask example demonstrating Jinja2 templates and static assets.

## Demo Video
<video src="" controls width="600"></video>

## Project structure

- main.py — Flask app entry point
- post.py — post-related logic
- templates/ — Jinja2 templates (`index.html`, `post.html`)
- static/ — static files (CSS, images)

## Prerequisites

- Python 3.8+ installed
- pip

## Install

Install Flask (and any other dependencies you add):

```powershell
pip install Flask
```

Optionally create a `requirements.txt` later with `pip freeze > requirements.txt`.

## Run

Option 1 — run directly (if `main.py` calls `app.run()`):

```powershell
python main.py
```

Option 2 — use the Flask CLI:

PowerShell:

```powershell
$env:FLASK_APP = "main.py"
flask run
```

CMD (Windows):

```cmd
set FLASK_APP=main.py
flask run
```

Then open http://127.0.0.1:5000 in your browser.

## Notes

- Templates are in the `templates/` folder; CSS lives in `static/css/styles.css`.
- `post.py` contains example logic for handling posts.

## Next steps

- Add a `requirements.txt` if you want reproducible installs.
- Add a short CONTRIBUTING or license if needed.

