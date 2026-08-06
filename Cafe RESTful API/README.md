# Cafe RESTful API

Minimal Flask-based RESTful API for a simple cafe project.

## Project Overview

- `main.py` — application entrypoint (Flask app and route definitions).
- `requirements.txt` — Python dependencies.
- `templates/` — HTML templates (includes `index.html`).
- `static/` — static assets (CSS, images, JS).
- `instance/` — configuration and instance-specific files.

This project provides a small RESTful service and a simple frontend page at the root route.

## Prerequisites

- Python 3.8 or newer
- pip

## Setup

Create a virtual environment and install dependencies:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix/macOS
source venv/bin/activate
pip install -r requirements.txt
```

## Run

Start the app:

```bash
python main.py
```

By default the Flask development server runs on http://127.0.0.1:5000/ — open that URL to view the `index.html` page.

## Project Structure

```
.
├─ main.py
├─ requirements.txt
├─ instance/
├─ static/
│  └─ css/
│     └─ style.css
└─ templates/
   └─ index.html
```

## Notes

- Check `main.py` for existing routes and API endpoints.
- Add any additional configuration to the `instance/` folder (for secret keys, DB paths, etc.).

## Contributing

Feel free to open issues or submit pull requests.

## License

This project does not include a license file. Add one if you intend to make the repository public.
