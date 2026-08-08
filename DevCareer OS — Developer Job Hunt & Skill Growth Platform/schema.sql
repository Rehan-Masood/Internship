CREATE TABLE IF NOT EXISTS job_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    position TEXT NOT NULL,
    status TEXT NOT NULL,
    salary TEXT,
    applied_date DATE NOT NULL,
    interview_date DATE,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS interview_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);