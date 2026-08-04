# LinkedIn Speed Complaint Bot

Automates a quick LinkedIn post when your measured internet speed is below the promised provider speeds. The script measures download/upload speeds (using speedtest), and if results fall short it opens Chrome, logs into LinkedIn, composes a short complaint post mentioning the provider, and submits it (requires brief manual verification if LinkedIn shows a CAPTCHA).

## Demo Video
<video src="https://github.com/user-attachments/assets/402e9fe7-6507-4440-8762-7278639a8baa" controls width="600"></video>

## LinkedIn-Speed-Complaint Bot
   ![LinkedIn-Speed-Complaint Bot.](./LinkedIn-Speed-Complaint%20Bot.jpg)

**Files**
- `main.py`: main script that measures speed and posts to LinkedIn.
- `credentials.py`: stores `LINKEDIN_EMAIL` and `LINKEDIN_PASSWORD` used for login (see Security).

**Features**
- Measures real internet speed using `speedtest`.
- Uses Selenium + `webdriver-manager` to control Chrome.
- Uses `pyautogui` for reliable typing/clicking in the post modal.
- Promised speed thresholds are configurable at the top of `main.py`.

Prerequisites
- Python 3.8+ (Windows recommended for `pyautogui` GUI interactions).
- Google Chrome installed (Chromedriver is installed automatically by `webdriver-manager`).

Install dependencies

Run these commands in a virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# or Command Prompt
.venv\Scripts\activate

pip install --upgrade pip
pip install speedtest-cli pyautogui selenium webdriver-manager
```

Quickstart

1. Edit `credentials.py` and replace the placeholders with your LinkedIn login credentials, or modify the script to read from environment variables.
2. (Optional) Adjust `PROMISED_DOWN`, `PROMISED_UP`, and `PROVIDER_NAME` at the top of `main.py`.
3. Run the script:

```bash
python main.py
```

4. When Chrome opens and LinkedIn asks for CAPTCHA or other verification, complete it in the browser and then press ENTER in the terminal to let the script continue.

Security & Privacy
- Do NOT commit real credentials into the repository. `credentials.py` currently contains plaintext credentials — replace/remove them and add `credentials.py` to `.gitignore` or use environment variables.
- Using automation for social posting may violate LinkedIn's terms of service. Use this script responsibly and at your own risk.

Notes & Troubleshooting
- The script requires an interactive desktop environment because `pyautogui` simulates keyboard/mouse input.
- If Selenium fails to find buttons due to DOM changes, the script falls back to `pyautogui` keyboard navigation.
- If `speedtest` fails, `main.py` uses fallback measured values so the flow continues.

License
- No license provided. Add one if you plan to share the project publicly.

---

If you want, I can also:
- Add a `requirements.txt`.
- Replace `credentials.py` with a secure environment-variable loader.
- Add `.gitignore` entries to avoid committing credentials.
