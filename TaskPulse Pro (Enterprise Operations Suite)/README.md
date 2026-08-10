# TaskPulse Pro — Enterprise Operations Suite

A small desktop GUI for running asynchronous background tasks, monitoring live performance, and exporting audit reports. Built with `customtkinter`, `matplotlib`, and `pandas` on top of a lightweight SQLite audit store.

## Demo Video
<video src="https://github.com/user-attachments/assets/44615465-aa0e-454e-b3a0-9ce68505fe90" controls width="600"></video>

## Features

- Run quick or heavy asynchronous jobs with responsive GUI
- Live console with searchable logs and progress bar
- Embedded Matplotlib chart showing runtime per task
- Import preview for log/text files
- Export completed-task audit to SQLite (`taskpulse_enterprise.db`), Excel (`taskpulse_report.xlsx`), and CSV (`taskpulse_report.csv`)
- Simple system cleanup to clear logs and progress

## Files

- `app_gui.py` — Main application GUI and logic
- `taskpulse_enterprise.db` — SQLite audit DB (created at first run)
- `taskpulse_report.xlsx` / `taskpulse_report.csv` — Generated exports

## Requirements

- Python 3.8+
- Packages:
  - `customtkinter`
  - `matplotlib`
  - `pandas`

Install dependencies with pip:

```bash
pip install customtkinter matplotlib pandas
```

Note: On some systems you may need to install `tkinter` separately (e.g., via your OS package manager or the system Python installer).

## Running

From the project root run:

```bash
python app_gui.py
```

The GUI will initialize an SQLite DB (`taskpulse_enterprise.db`) in the current directory on the first run.

## Usage

- Click `Run Quick Task` or `Heavy Batch Engine` to start background jobs.
- Monitor progress via the progress bar, console logs, and the Live Task Performance chart.
- Use `Load Log File` to preview the first 10 lines of a log/text file.
- Click `Export Reports` to write audit data to DB, Excel, and CSV files.
- Use `Clear Logs` to reset console and progress.

## Contributing

Feel free to open issues or submit PRs. Suggestions:

- Persist completed tasks between sessions by reading/writing the DB on startup/shutdown
- Add configuration for export paths and file naming
- Add authentication or multi-user support for enterprise deployments

## Troubleshooting

- If the GUI fails to start, check that `tkinter` is available for your Python build.
- If plotting fails, ensure `matplotlib` is installed and configured for your OS backend.

## License

MIT — adapt as needed.
