# NutriFlow Enterprise

NutriFlow Enterprise is a small Flask web application for managing user authentication, viewing menus, and generating receipts.

## Demo Video
<video src="https://github.com/user-attachments/assets/0cb082d1-c113-467c-939f-d73817d6f021" controls width="600"></video>

## Features

- User registration & login
- Menu display
- Receipt generation
- Simple HTML templates under `templates/` and static assets under `static/`

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1  # PowerShell (Windows)
# or
venv\Scripts\activate.bat   # Command Prompt (Windows)
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

If there is no `requirements.txt`, install Flask manually:

```powershell
pip install Flask
```

## Running the app

You can run the app directly:

```powershell
python app.py
```

Or use Flask CLI:

```powershell
set FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000
```

## Project structure

```
app.py
static/
    css/
        style.css
    js/
        main.js
templates/
    base.html
    login.html
    menu.html
    receipt.html
    register.html
README.md
```

## Notes

- Update `requirements.txt` with any additional dependencies used by the project.
- Adjust run instructions if your `app.py` uses a factory or different entrypoint.

## Contributing

Contributions welcome — open an issue or submit a PR.

## License

Specify a license for the project if needed.
