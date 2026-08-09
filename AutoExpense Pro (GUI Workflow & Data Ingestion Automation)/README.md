# AutoExpense Pro

AutoExpense Pro is a small utility for GUI-based workflow and data-ingestion automation focused on processing invoices.

## Features

- GUI dashboard for reviewing and managing invoice ingestion (`app_dashboard.py`).
- Drop-in invoice storage and sample data folder: `invoices/`.
- Designed to be extended for parsing, validation, and downstream automation.

## Project structure

- `app_dashboard.py`  main GUI entrypoint.
- `invoices/`  folder to store incoming invoice files and related data.
- `README.md`  project overview and usage instructions.

## Requirements

- Python 3.10+ recommended.
- Optional: `requirements.txt` (create and pin dependencies used by your environment).

## Setup (Windows)

1. Create a virtual environment:

```
python -m venv venv
```

2. Activate the environment:

```
venv\Scripts\activate
```

3. Install dependencies (if you have a `requirements.txt`):

```
pip install -r requirements.txt
```

## Run

Run the dashboard:

```
python app_dashboard.py
```

## Usage

- Place invoice files (PDFs, images, CSVs, etc.) into the `invoices/` folder.
- Launch the dashboard via `python app_dashboard.py` and follow the GUI to ingest, preview, and process invoices.

## Development

- Add or update dependencies and record them in `requirements.txt`.
- Extend `app_dashboard.py` or add modules for parsing, validation, and persistence.

## Contributing

Contributions are welcome. Open issues or pull requests with a clear description of proposed changes.

## License

Specify a license for the project (for example, MIT).
