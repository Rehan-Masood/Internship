# ScrapePulse

ScrapePulse is a lightweight real-time job and tech-stack intelligence engine that scrapes remote job listings, extracts demanded technologies, and stores results in a local SQLite database. It provides a simple Streamlit dashboard for triggering scrapes and viewing analytics.

## Features

- Scrapes job postings from RemoteOK (top results) and extracts common tech keywords
- Stores job posts in a local SQLite database (`scrapepulse.db`)
- Streamlit dashboard for running scrapes, viewing metrics and simple visualizations

## Requirements

- Python 3.8+
- Packages listed in `requirements.txt` (or install manually): `streamlit`, `requests`, `beautifulsoup4`, `pandas`, `plotly`

## Installation

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install streamlit requests beautifulsoup4 pandas plotly
```

## Running the app

Start the Streamlit dashboard from the repository root:

```bash
streamlit run app.py
```

The UI exposes a button to trigger the live scraping engine. Scraped job postings are persisted to `scrapepulse.db`.

## Database

- The app uses a local SQLite file named `scrapepulse.db` and creates a table `job_postings` automatically on first run.
- Stored fields include `title`, `company`, `location`, `tech_stack`, `source`, and `scraped_at`.

## How scraping works

- The included `JobScraperEngine` fetches a RemoteOK page, parses job rows, and matches tech keywords (e.g., Python, React, Docker) using simple regex word-boundary checks.
- To add or customize keywords, update the `tech_keywords` list in `app.py`.

## Contributing

- Feel free to open issues or submit pull requests to improve scraping robustness, add more sources, or enhance analytics.

## License

This project is provided as-is. Add a license file if you wish to apply one.

---

Created for quick evaluation and iterative development.
