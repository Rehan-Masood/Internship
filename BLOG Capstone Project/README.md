# BLOG Capstone Project

A Flask-based blog application with article publishing, editing, deleting, detailed post pages, an about page, and a contact form. The app uses SQLite for persistence and CKEditor for rich-text post content.

## Demo Video
<video src="" controls width="600"></video>

## Features

- View all blog posts on the homepage
- Create new posts
- Edit existing posts
- Delete posts
- Read individual post pages
- About page
- Contact form
- Rich text editing with CKEditor
- SQLite database for local storage

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Bootstrap
- Flask-CKEditor
- SQLite
- WTForms

## Project Structure

```text
main.py
requirements.txt
templates/
  about.html
  contact.html
  footer.html
  header.html
  index.html
  make-post.html
  post.html
static/
  assets/
    img/
  css/
    styles.css
  js/
    scripts.js
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

4. Open the app in your browser at:

```text
http://127.0.0.1:5002/
```

## Notes

- The app creates the SQLite database file automatically on first run.
- Blog post data is stored in `posts.db`.
- Background images used by the templates are served from the Flask static folder.

## Routes

- `/` - Home page with all posts
- `/post/<int:post_id>` - Post detail page
- `/new-post` - Create a new post
- `/edit-post/<int:post_id>` - Edit a post
- `/delete/<int:post_id>` - Delete a post
- `/about` - About page
- `/contact` - Contact page

## License

No license has been specified for this project.
