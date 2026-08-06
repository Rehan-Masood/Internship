# Coffee and Wifi

Simple Flask app to list and add cafes with Wi‑Fi info.

## Features
- View a list of cafes
- Add a cafe via a form

## Prerequisites
- Python 3.8+ 
- See dependencies: [requirements.txt](requirements.txt)

## Install
1. Create a virtual environment (recommended):

   python -m venv venv

2. Activate it and install dependencies:

Windows (PowerShell):

```powershell
.\\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## Run
Start the app:

```powershell
python main.py
```

Open http://127.0.0.1:5000/ in your browser.

## Project structure
- [cafe-data.csv](cafe-data.csv)
- [main.py](main.py)
- [requirements.txt](requirements.txt)
- [static/css/styles.css](static/css/styles.css)
- templates:
  - [templates/add.html](templates/add.html)
  - [templates/base.html](templates/base.html)
  - [templates/cafes.html](templates/cafes.html)
  - [templates/index.html](templates/index.html)

## Notes
- If the app uses Flask environment variables, consult `main.py` for details.
- Want me to add a short README badge, example screenshot, or run a quick test? Ask and I will.
