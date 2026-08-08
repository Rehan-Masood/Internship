import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_FILE = 'dev_career.db'


def get_db_connection():
    """Establishes a connection to the local SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes database tables and seeds sample interview cards."""
    conn = get_db_connection()
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM interview_cards")
    if cursor.fetchone()[0] == 0:
        sample_cards = [
            ("Python", "What is the difference between list.sort() and sorted()?", 
             "list.sort() mutates the list in place and returns None. sorted() returns a new sorted list without modifying the original."),
            ("Flask", "How do request contexts work in Flask?", 
             "Flask uses thread-local objects (like request and session) to make incoming HTTP payload data accessible globally within the thread handling the request."),
            ("System Design", "What is database indexing?", 
             "Indexing creates a data structure (usually B-Tree) that improves data retrieval speed at the cost of additional storage and slower writes.")
        ]
        cursor.executemany(
            "INSERT INTO interview_cards (topic, question, answer) VALUES (?, ?, ?)",
            sample_cards
        )
        conn.commit()
    conn.close()


# -------------------------------------------------------------
# Routes
# -------------------------------------------------------------

@app.route('/')
def index():
    """Displays job applications dashboard and status summary metrics."""
    conn = get_db_connection()
    jobs = conn.execute("SELECT * FROM job_applications ORDER BY applied_date DESC").fetchall()
    
    # Calculate stats
    total = len(jobs)
    interviewing = sum(1 for j in jobs if j['status'] == 'Interviewing')
    offers = sum(1 for j in jobs if j['status'] == 'Offer')
    applied = sum(1 for j in jobs if j['status'] == 'Applied')
    
    conn.close()
    return render_template('index.html', jobs=jobs, total=total, interviewing=interviewing, offers=offers, applied=applied)


@app.route('/job/add', methods=['GET', 'POST'])
def add_job():
    """Adds a new job application entry to the tracker."""
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        status = request.form['status']
        salary = request.form.get('salary', '')
        applied_date = request.form.get('applied_date', datetime.today().strftime('%Y-%m-%d'))
        interview_date = request.form.get('interview_date', '')
        notes = request.form.get('notes', '')

        conn = get_db_connection()
        conn.execute(
            """INSERT INTO job_applications 
               (company, position, status, salary, applied_date, interview_date, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (company, position, status, salary, applied_date, interview_date, notes)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_job.html')


@app.route('/job/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    """Deletes a job application record."""
    conn = get_db_connection()
    conn.execute("DELETE FROM job_applications WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/flashcards', methods=['GET', 'POST'])
def flashcards():
    """Tech interview flashcard study hub."""
    conn = get_db_connection()

    if request.method == 'POST':
        topic = request.form['topic']
        question = request.form['question']
        answer = request.form['answer']

        conn.execute(
            "INSERT INTO interview_cards (topic, question, answer) VALUES (?, ?, ?)",
            (topic, question, answer)
        )
        conn.commit()

    cards = conn.execute("SELECT * FROM interview_cards ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('flashcards.html', cards=cards)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)