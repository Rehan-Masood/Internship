# Amazon Price Tracker

A simple Python project to track product prices on Amazon and notify you of price changes.

## Overview

This repository contains a small script (`main.py`) that can be used as the basis for tracking item prices on Amazon. It fetches product pages, extracts prices, and can be extended to send notifications when prices drop.

## Features

- Fetch product pages and parse prices
- Compare current price to historical price
- Easily extended to send email or push notifications

## Requirements

- Python 3.10 or newer
- Typical libraries (adjust if your code uses different ones):
  - `requests`
  - `beautifulsoup4`

If your project uses a `requirements.txt`, install dependencies with:

```bash
pip install -r requirements.txt
```

## Quick Start

1. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

2. Install dependencies (if any):

```bash
pip install -r requirements.txt
```

3. Run the tracker:

```bash
python main.py
```

Replace or update `main.py` with your desired tracking logic and configuration.

## Configuration

You can add a configuration file (for example `config.json`) to list product URLs, thresholds, and notification settings. The exact format depends on how you extend `main.py`.

## Example

A minimal example flow:

- Add product URLs to a config file.
- Run `main.py` to fetch current prices.
- Compare prices and log changes or send notifications.

## Contributing

Contributions are welcome. Open an issue or submit a pull request with improvements, bug fixes, or new features.

## License

This project is provided under the MIT License. See `LICENSE` for details, or replace with your preferred license.

---

Created to support the `main.py` tracker script in this workspace.
