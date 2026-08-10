# WeConnect Innovation Studio

WeConnect Innovation Studio is a lightweight Flask app for practicing coding problems in a LeetCode-style workflow. It includes a problem browser, an in-browser editor, local code execution against test cases, note taking, and submission history, all backed by SQLite.

## Demo Video
<video src="https://github.com/user-attachments/assets/09b24616-3892-46d0-a5b7-7a61ca4318ca" controls width="600"></video>

## Features

- Browse seeded practice problems from the home page
- Open an individual problem page with starter code and test cases
- Run Python solutions against predefined test cases with `/api/run_code`
- Save personal notes for each problem with `/api/save_note`
- View submission history at `/history`
- Generate a random problem through the external LeetCode API and Gemini-powered content generation

## Requirements

- Python 3.8 or newer
- A Gemini API key in the environment for the random problem generation flow
- Packages listed in `requirements.txt`

## Setup

1. Clone or copy the project into a local folder.
2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create a `.env` file if you want random problem generation to work:

```powershell
GEMINI_API_KEY=your_api_key_here
```

## Database

The app uses SQLite and stores data in `devprep.db`.

On first run, `app.py` creates the database from `schema.sql` and seeds a few sample problems if the table is empty.

To reset the database manually:

```powershell
Remove-Item .\devprep.db -Force
python app.py
```

## Run

Start the development server with:

```powershell
python app.py
```

The app runs at `http://127.0.0.1:5000/` with Flask debug mode enabled.

## API Endpoints

- `GET /` - Home page with the problem list
- `GET /problem/<id>` - Individual problem page
- `GET /api/fetch_next_random_problem` - Fetches or generates a random problem and redirects to it
- `POST /api/run_code` - Runs submitted Python code against the problem test cases
- `POST /api/save_note` - Saves a note for a problem
- `GET /history` - Submission history page

## Project Structure

- `app.py` - Flask application, database setup, and API routes
- `schema.sql` - SQLite schema for problems, submissions, and notes
- `requirements.txt` - Python dependencies
- `templates/` - Jinja2 templates for the UI
- `static/` - CSS and JavaScript assets

## Notes

- Submitted code is executed with Python `exec()`, so this project is intended for local development and practice only.
- If the external API or Gemini generation fails, the app falls back to the local problem bank.

## License

Add your preferred license here.
