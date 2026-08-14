# Inkwell — Flask Blog Platform

A full-stack blogging platform built with Flask. Users can register, log in, publish articles, edit or delete their own posts, comment on articles, and upload a profile picture. Guests can read everything but need an account to write or comment.

**🔗 Live Demo :** [Inkwell — Flask Blog Platform](https://internship-racj-fq7yu2i7z-rehan-web.vercel.app)

## Demo Video
<video src="https://github.com/user-attachments/assets/ccefa95a-a307-42f2-9efd-441577a1f042" controls width="600"></video>

## Features

- **Authentication** — Register, log in, log out. Passwords are hashed with Werkzeug's `generate_password_hash` (never stored in plain text).
- **Full CRUD for articles** — Create, read, update, delete. Only the original author can edit or delete their own post (enforced server-side, returns `403 Forbidden` otherwise).
- **Comments** — Any logged-in user can comment on any article. Guests are prompted to log in.
- **Profile pictures** — Upload and resize (via Pillow) a profile picture. Users without one get an auto-generated initials avatar instead, so there's no broken-image fallback.
- **Cover images** — Optional cover image per article, shown on the homepage and article page.
- **Database relationships** — `User → Posts` and `User/Post → Comments`, using SQLAlchemy `relationship()` with cascading deletes (deleting a post removes its comments; deleting a user removes their posts and comments).
- **Pagination** — Homepage paginates articles, 6 per page.
- **Custom error pages** — 403, 404, and 500 all use the site's own design instead of Flask's default error screen.
- **Responsive design** — Works down to mobile, with a collapsing nav menu.

## Design

The interface uses a custom "editorial" design system (not default Bootstrap look):

- **Colors** — deep ink navy for the header/footer, a cool mist-grey page background, white content cards, with a muted antique gold and muted teal as accent colors.
- **Typography** — Fraunces (serif) for headlines, Inter for body/UI text, JetBrains Mono for meta text like dates and bylines.
- **Signature detail** — an animated hand-drawn "ink underline" that brushes in under links and titles on hover.

All of this lives in `app/static/css/style.css` as CSS custom properties (`:root` variables) at the top of the file, so colors and fonts can be swapped project-wide by editing a handful of lines.

## Project Structure

```
flask_blog/
├── run.py                  # Entry point
├── config.py                # App configuration (secret key, DB path, upload settings)
├── requirements.txt
├── app/
│   ├── __init__.py          # App factory, registers blueprints
│   ├── models.py            # User, Post, Comment (SQLAlchemy models)
│   ├── forms.py              # WTForms: registration, login, post, comment, account forms
│   ├── utils.py              # Image save/resize/delete helpers
│   ├── auth/routes.py        # /register, /login, /logout
│   ├── posts/routes.py       # /post/new, /post/<id>, /post/<id>/update, /post/<id>/delete
│   ├── users/routes.py       # /account, /author/<username>
│   ├── main/routes.py        # / (homepage), /about
│   ├── errors/handlers.py    # 403 / 404 / 500 handlers
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   ├── profile_pics/     # uploaded profile pictures land here
│   │   └── post_covers/      # uploaded article cover images land here
│   └── templates/            # Jinja2 templates
```

## Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set a real secret key** before running for real — open `config.py` and replace:
   ```python
   SECRET_KEY = "change-this-to-a-random-secret-key-before-deploying"
   ```
   You can generate one with:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Run the app:**
   ```bash
   python run.py
   ```
   The database (`app/site.db`) is created automatically on first run — no manual migration step needed for this project's scope.

5. Open **http://127.0.0.1:5000** in your browser.

## How to Use

1. Click **Sign Up**, create an account.
2. Click **Write** in the nav to publish your first article (title, optional excerpt, optional cover image, content).
3. Anyone logged in can comment on any article.
4. Only you can edit/delete your own articles — visit any of your articles and you'll see **Edit** / **Delete** buttons that don't appear for other users.
5. Visit **Account** to update your username, email, bio, or upload a profile picture.
6. Visit any author's name to see their public profile page listing all their articles.

## Deployment Notes

This project uses Flask's built-in development server (`app.run()`), which is fine for local testing but not for production. Before deploying (e.g. to Render or Heroku):

- Swap the dev server for a production WSGI server like **Gunicorn**
- Move `SECRET_KEY` and any sensitive config into environment variables instead of hardcoding them in `config.py`
- Consider switching from SQLite to PostgreSQL for a real deployment, since SQLite's file-based storage doesn't play well with most cloud platforms' ephemeral filesystems
- Set `debug=False` in `run.py`

## Tech Stack

Flask · Flask-SQLAlchemy · Flask-Login · Flask-WTF · WTForms · Pillow · SQLite
