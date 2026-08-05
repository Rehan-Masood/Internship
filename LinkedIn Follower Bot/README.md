# LinkedIn Follower Bot

A small automation script that opens Chrome, logs into LinkedIn, and attempts to follow a target company page.

## Features
- Uses Selenium + webdriver-manager to drive Chrome.
- Uses `pyautogui` and `pyperclip` for clipboard-based credential entry and fallback clicking.
- Navigates to a target company page and clicks the Follow button.

## Requirements
- Python 3.8+
- Chrome browser installed (matching ChromeDriver installed automatically)
- Packages: `selenium`, `webdriver-manager`, `pyautogui`, `pyperclip`

Install packages with:

```powershell
pip install selenium webdriver-manager pyautogui pyperclip
```

## Configuration
- The project reads credentials from `credentials.py`. Example contents:

```python
LINKEDIN_EMAIL = "your-email@example.com"
LINKEDIN_PASSWORD = "your-password"
```

WARNING: Do NOT commit real credentials to version control. Replace the values above with environment-variable-based loading or add `credentials.py` to `.gitignore` before committing.

## Usage
1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install the required packages (see Requirements).
3. Edit `credentials.py` to add your LinkedIn login.
4. Run the bot:

```powershell
python main.py
```

Notes:
- The script will open a Chrome window. Complete any CAPTCHA or 2FA manually in the browser when prompted, then return to the terminal and press ENTER to continue.
- `webdriver-manager` automatically downloads a compatible ChromeDriver, but ensure your Chrome installation is up to date.
- `pyautogui` performs screen clicks if DOM-based clicks fail; avoid moving the mouse while the bot runs.

## Limitations & Safety
- Automating interactions on LinkedIn may violate their terms of service. Use this code only for personal learning and with accounts you own.
- Be careful with login automation — LinkedIn may block or restrict accounts that show automated behaviour.

## License
This repository has no license specified. Add a `LICENSE` file if you want to share it publicly.
