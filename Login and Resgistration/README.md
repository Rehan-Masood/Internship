# Login and Registration

Simple Flask-based login and registration example app.

## Project Overview

This repository contains a small web application that demonstrates user login and registration flows using Flask. It includes HTML templates, static assets, and a minimal Python entrypoint.

## Features

- User registration
- User login
- Protected `secrets` page (requires login)
- HTML templates under `templates/` and static assets under `static/`

## Requirements

- Python 3.8+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup (recommended)

Create and activate a virtual environment, then install requirements:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Running

Start the app (the project uses `main.py` as the entrypoint):

```bash
python main.py
```

Open a browser at http://127.0.0.1:5000 to view the app.

## Project Structure

- `main.py` — application entrypoint
- `requirements.txt` — Python dependencies
- `templates/` — HTML templates (includes `index.html`, `login.html`, `register.html`, `secrets.html`, `base.html`)
- `static/` — static files (CSS under `static/css/styles.css`)
- `instance/` — (optional) runtime instance files

## Notes

- If the app uses a configuration or secret keys, ensure you set them securely (for development use environment variables or `instance/` files).
- This README assumes the app is a Flask app with `main.py`. If the entrypoint differs, adjust the run command accordingly.

## Contributing

Contributions and improvements are welcome. Please open an issue or submit a pull request.

## License

Specify a license for the project or add one to the repository root.
