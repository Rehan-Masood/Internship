# Flask Advance Form

A simple Flask web application that demonstrates a login form with validation using Flask-WTF, WTForms, and Bootstrap.

## Demo Video
<video src="https://github.com/user-attachments/assets/7bfe9e5d-79b4-482f-a600-8990f2a32b66" controls width="600"></video>

## Features

- Home page with a welcome screen
- Login form with client-side and server-side validation
- Success page for valid credentials
- Denied page for invalid credentials
- Bootstrap-styled templates

## Project Structure

- `main.py` - Main Flask application
- `templates/` - HTML templates for the app
  - `index.html`
  - `login.html`
  - `success.html`
  - `denied.html`
  - `base.html`

## Requirements

The project uses the following Python packages:

- Flask
- Flask-WTF
- WTForms
- Flask-Bootstrap
- Werkzeug

## Installation

1. Clone or open the project folder.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

Start the Flask app with:

```bash
python main.py
```

Then open your browser and go to:

- http://127.0.0.1:5001/

## Login Credentials

Use the following credentials to see the success page:

- Email: `admin@email.com`
- Password: `12345678`

## Notes

This project is intended for learning purposes and shows how to build a basic Flask form application with validation and templating.
