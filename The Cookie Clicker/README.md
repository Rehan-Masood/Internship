# The Cookie Clicker — Automation Script

Small Selenium automation that plays the Cookie Clicker experiment
available at http://orteil.dashnet.org/experiments/cookie/.

## Demo Video
<video src="https://github.com/user-attachments/assets/9ff40451-fe3b-4f12-a4ac-195af7e0e5cc" controls width="600"></video>

## Features
- Automates clicking the big cookie repeatedly.
- Parses available store items and purchases the most expensive affordable upgrade every 5 seconds.
- Runs for 5 minutes and prints final cookies-per-second (CPS).

## Requirements
- Python 3.8+
- Google Chrome
- ChromeDriver compatible with your Chrome version
- Python packages: `selenium`

Install dependencies:

```bash
pip install selenium
```

## Usage
1. Ensure `chromedriver` is on your PATH or placed next to your Python executable.
2. Open a terminal in the project folder.
3. Run the script:

```bash
python main.py
```

The script will open a Chrome window, start clicking, buy upgrades automatically, and after
5 minutes will print the final CPS value.

## Notes
- The script uses `chrome_options.experimental_option("detach", True)` so the
  browser stays open after the script finishes.
- If you see errors about ChromeDriver, download the matching driver from
  https://chromedriver.chromium.org/ and place it on your PATH.

## License
This repository contains a small personal script — feel free to adapt it.
