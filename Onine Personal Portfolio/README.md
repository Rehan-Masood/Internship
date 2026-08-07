# Online Personal Portfolio

A simple Flask-based personal portfolio website that showcases featured projects, key statistics, and a contact form.

## Demo Video
<video src="https://github.com/user-attachments/assets/4832987d-c318-4ff9-bd5e-44b1a7f58b9f" controls width="600"></video>

## Features

- Responsive portfolio landing page
- Project cards with categories, descriptions, and tags
- Portfolio statistics section
- Contact form with success confirmation page

## Project Structure

- app.py: Main Flask application
- templates/: HTML templates for the homepage, base layout, and contact success page
- static/css/style.css: Stylesheet for the site
- requirements.txt: Python dependencies

## Requirements

- Python 3.8+
- Flask

## Installation

1. Clone the repository
2. Navigate to the project folder
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the App

Start the Flask development server:

```bash
python app.py
```

Then open your browser and visit:

```text
http://127.0.0.1:5000/
```

## Notes

- The contact form currently prints submissions to the terminal and shows a success page.
- The portfolio projects are defined in the app.py file and can be updated easily.
