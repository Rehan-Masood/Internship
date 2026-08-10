# LogSentinel Pro (Enterprise Desktop Log Auditor)

> Lightweight desktop tool for auditing and inspecting logs (GUI).

## Demo Video
<video src="https://github.com/user-attachments/assets/f5fcf815-697e-474b-ad78-2b32bef6b1ed" controls width="600"></video>

## Overview

This repository contains a simple GUI application, `app_gui.py`, intended as the entry point for the LogSentinel Pro desktop auditor. The GUI presents logs, supports basic filtering, and can be extended to integrate with enterprise log sources.

## Requirements

- Python 3.8 or newer
- Any GUI toolkit dependencies (if used) should be installed; check `requirements.txt` if present.

## Installation

1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies if a `requirements.txt` file exists:

```powershell
pip install -r requirements.txt
```

## Running

Run the GUI application with:

```powershell
python app_gui.py
```

If the project uses a GUI framework (PyQt, Tkinter, etc.), ensure the corresponding packages are installed.

## Extending

- Add logging backends or parsers under a `backends/` or `parsers/` folder.
- Add configuration options in a `config/` folder or via environment variables.

## Development

- Keep dependencies in `requirements.txt` or `pyproject.toml`.
- Run linting and tests (if added) before committing changes.

## Files

- `app_gui.py` — main GUI entry point.

## License

Add a license to this repository (e.g., MIT, Apache-2.0) by placing a `LICENSE` file in the project root.

## Contact

For questions or contributions, open an issue or reach out to the project maintainer.
