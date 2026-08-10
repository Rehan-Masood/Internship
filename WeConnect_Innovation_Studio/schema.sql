CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    description TEXT NOT NULL,
    starter_code TEXT NOT NULL,
    reference_solution TEXT,
    test_cases TEXT NOT NULL,
    complexity TEXT
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id INTEGER NOT NULL,
    code TEXT NOT NULL,
    status TEXT NOT NULL,
    output TEXT,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (problem_id) REFERENCES problems (id)
);

CREATE TABLE IF NOT EXISTS user_notes (
    problem_id INTEGER PRIMARY KEY,
    note_text TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);