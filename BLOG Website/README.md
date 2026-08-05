# BLOG Website

A small Flask-based blog demo that fetches posts from an external JSON endpoint and renders them using the templates in the `templates/` folder.

## Features
- Lists blog posts on the homepage
- Individual post pages using `post.html`
- About and Contact pages
- Static assets served from the `static/` folder

## Prerequisites
- Python 3.8 or newer
- `pip`

## Setup
1. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS / Linux
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Then open http://127.0.0.1:5001/ in your browser (the app runs on port 5001 by default).

## Configuration
- The sample posts are loaded from an `npoint` JSON URL defined near the top of `main.py`. Replace that URL with your own JSON endpoint if you want custom posts.

## Project structure

- main.py — application entry
- requirements.txt — Python dependencies
- templates/ — HTML templates (`index.html`, `post.html`, `about.html`, `contact.html`, `header.html`, `footer.html`)
- static/ — static assets (CSS, JS, images)

## Contributing
- Open issues or submit pull requests with improvements or bug fixes.

## License
This project is provided as-is. Add a license file if you want to apply an open-source license.
