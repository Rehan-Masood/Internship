# Advanced BLOG Capstone Project

A simple Flask-based blogging application built as a capstone project. It includes user authentication, post creation, and template-driven pages using the `templates/` and `static/` folders.

## Demo Video
<video src="" controls width="600"></video>

## Features

- User registration and login
- Create, edit, and view posts
- Static assets served from `static/`
- Templates in `templates/` for page structure

## Prerequisites

- Python 3.10 or newer
- Git (optional)

## Installation (Windows)

1. Create a virtual environment:

```powershell
python -m venv venv
```

2. Activate the virtual environment (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the App

Start the app with:

```powershell
python main.py
```

Open a browser and go to http://127.0.0.1:5000/ (or the host/port printed by the app).

## Project Structure

Top-level files:

- `main.py` — application entry point
- `forms.py` — form definitions (WTForms or similar)
- `requirements.txt` — Python dependencies
- `README.md` — this file
- `instance/` — optional runtime configuration, DB, or uploads

Folders:

- `templates/` — HTML templates (index.html, post.html, login.html, etc.)
- `static/` — static assets (css, js, images)

Example template files included:

- `templates/index.html`
- `templates/post.html`
- `templates/make-post.html`
- `templates/register.html`
- `templates/login.html`

## Notes

- If the app uses a database, check `main.py` or `instance/` for DB configuration and migration steps.
- Adjust environment variables or config files as needed for production deployment.

## Contributing

Feel free to open issues or submit pull requests. Keep changes small and focused.

## License

Add a license file if you intend to publish this project. Otherwise assume private/institutional use.

## Contact

For questions, open an issue or contact the project owner.
