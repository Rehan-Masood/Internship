# WeatherPulse Lite

Lightweight Python script for auditing live weather data and exporting reports.

Project: WeatherPulse Lite (Live REST API & Environmental Auditor)

Overview
- Fetches current weather metrics for a configurable list of cities using the Open-Meteo REST API.
- Logs entries to a local SQLite database and exports an Excel audit report.

Key files
- `weather_pulse.py`: main script that initializes the DB, fetches data, saves to SQLite, and exports an Excel report.

Features
- Simple, dependency-light Python utility
- Uses Open-Meteo (no API key required)
- Persists results to `weather_audit.db` and `weather_report.xlsx`

Requirements
- Python 3.8+
- Packages: `pandas`, `requests`, and an Excel writer engine (pandas will use `openpyxl` by default).

Install dependencies

```bash
python -m pip install --upgrade pip
pip install pandas requests openpyxl
```

Usage

Run the script from the repository root:

```bash
python weather_pulse.py
```

Observed outputs
- `weather_audit.db` — SQLite database containing the `weather_logs` table.
- `weather_report.xlsx` — Excel export of the latest fetched metrics.

Configuration
- Edit the `CITIES` constant at the top of `weather_pulse.py` to change which cities are queried.
- `DB_FILE` and `EXCEL_FILE` can be changed in `weather_pulse.py` to alter output filenames/paths.

Notes
- The script uses the Open-Meteo public API for current weather; check their terms if you plan heavy usage.

Contributing
- Open an issue or submit a pull request for improvements.

License
- MIT License (feel free to change if you prefer another license).

Contact
- Project owner: local workspace repository (no remote set).
