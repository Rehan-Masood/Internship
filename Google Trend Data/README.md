# Google Trend Data

This repository contains scripts and CSV data for exploring relationships between Google Search Trends and time-series data (prices, rates).

Project contents
- main.py — primary script to load and analyze CSV files.
- requirements.txt — Python dependencies.
- Bitcoin Search Trend.csv — Google Trends data for Bitcoin.
- Daily Bitcoin Price.csv — Bitcoin price data.
- TESLA Search Trend vs Price.csv — Tesla search trends and price data.
- UE Benefits Search vs UE Rate 2004-19.csv — unemployment benefits search vs unemployment rate (2004-2019).
- UE Benefits Search vs UE Rate 2004-20.csv — unemployment benefits search vs unemployment rate (2004-2020).

Quick start

1. Create a virtual environment (recommended):

```powershell
python -m venv .venv
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the main script:

```powershell
python main.py
```

Notes
- `main.py` expects the CSV files to be in the repository root. Adjust paths inside the script if you keep data elsewhere.
- Inspect and preprocess the CSV files if column names or formats differ before running analyses.

If you'd like, I can:
- add usage examples and sample outputs,
- document expected CSV column names and formats,
- or add a small wrapper to run analyses for a specific dataset.
