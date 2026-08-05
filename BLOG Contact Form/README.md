# BLOG Contact Form

Simple Flask blog with a contact form that emails form submissions.

## Demo Video
<video src="https://github.com/user-attachments/assets/e8fb2f90-822e-4dc5-a32b-90e1339704f5" controls width="600"></video>

## Features

- Static blog pages rendered from a remote JSON (npoint) in `main.py`
- Contact form that sends an email using SMTP
- Templates in `templates/` and assets in `static/`

## Prerequisites

- Python 3.8+
- Internet access (fetches posts from a remote npoint URL)

## Installation

1. Create a virtual environment and activate it:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Configuration

Before running the app, update `main.py` with your own values:

- Replace the npoint URL used to fetch posts (the `requests.get(...)` call).
- Set `OWN_EMAIL` and `OWN_PASSWORD` to an email account you control.

Security note: storing credentials directly in source is unsafe for production. Prefer environment variables or a `.env` file and use a library like `python-dotenv`.

Example using environment variables (recommended):

```python
import os
OWN_EMAIL = os.environ.get('OWN_EMAIL')
OWN_PASSWORD = os.environ.get('OWN_PASSWORD')
```

Then set them in PowerShell before running:

```powershell
$env:OWN_EMAIL = "you@example.com"
$env:OWN_PASSWORD = "your-password"
```

## Run

Start the app locally:

```powershell
python main.py
```

Open http://127.0.0.1:5000 in your browser.

## Project Structure

- `main.py` - Flask application
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `static/` - CSS, JS and image assets

## Notes

- The contact form uses Gmail SMTP in `send_email()`; if you use Gmail you may need an app password or to enable less secure access depending on your account settings.
- Replace hardcoded secrets before sharing the repo.

---

If you want, I can update `main.py` to read credentials from environment variables and add a `.env` example file.
