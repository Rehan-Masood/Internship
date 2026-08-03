# Auto-Tinder Bot — BBC Top News Scraper

A small utility that scrapes top BBC News headlines and saves them to a CSV file. The repository currently contains `main.py`, which uses Selenium and webdriver-manager to open BBC News and collect the top headlines (default: top 10).

**Features**
- Opens BBC News (`https://www.bbc.com/news`) with Chrome
- Extracts up to 10 unique headlines and their article URLs
- Writes results to `bbc_top_news.csv`

**Prerequisites**
- Python 3.8 or newer
- Google Chrome installed on the system
- Internet access

**Install**
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # PowerShell
# or: .\.venv\Scripts\activate   # cmd.exe
```

2. Install dependencies:

```powershell
pip install selenium webdriver-manager
```

(Optionally create `requirements.txt` with `pip freeze > requirements.txt`.)

**Run**

```powershell
python main.py
```

The script will launch Chrome, visit BBC News, and save the top headlines to `bbc_top_news.csv` in the repository root.

**Configuration & Tips**
- `CSV_FILE_NAME` and `BBC_URL` are defined in `main.py` and can be changed for alternate targets or output file names.
- If you want the scraper to run without opening a visible window, add a headless flag to the Chrome options in `main.py`:

```python
chrome_options.add_argument("--headless=new")  # or "--headless" for older Chrome
```

- `webdriver-manager` automatically downloads the compatible ChromeDriver version, but Chrome must be installed and reasonably up-to-date.

**Caveats & Legal**
- Use this script responsibly. Respect BBC's terms of service and robots.txt. Don't run scraping loops at high frequency.

**Next steps**
- Add `requirements.txt`
- Add error logging and retry/backoff logic
- Add tests or a small CLI wrapper for configuration

**License**
- MIT (adjust as needed)
