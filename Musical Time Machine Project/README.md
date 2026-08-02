# Musical Time Machine

A tiny utility that scrapes the Billboard Hot 100 for a given date and produces a plain-text playlist with Spotify search links.

## Demo Video
<video src="https://github.com/user-attachments/assets/91acb36c-0d01-4c22-bd40-3c68fad76e34" controls width="600"></video>

## What it does
- Prompts for a date in `YYYY-MM-DD` format.
- Fetches the Billboard Hot 100 chart for that date.
- Extracts song titles and writes `playlist_<DATE>.txt` with each song and a clickable Spotify search link.

## Files
- `main.py` — the script that performs the scrape and writes the playlist file.
- `playlist_2003-05-23.txt` — an example output created by the script.

## Requirements
- Python 3.8 or newer
- `requests` and `beautifulsoup4`

Install dependencies with pip:

```bash
pip install requests beautifulsoup4
```

## Usage
1. Run the script:

```bash
python main.py
```

2. When prompted, enter a date in the format `YYYY-MM-DD` (for example: `2003-05-23`).
3. The script will create a file named `playlist_<DATE>.txt` (for example `playlist_2003-05-23.txt`) in the project directory.

## Notes & Troubleshooting
- The script scrapes Billboard's website. If the Billboard page structure changes, the scraper may stop finding songs and will print an error.
- If the request fails, check your network and ensure the date is valid and formatted correctly.
- Respect website terms of service and avoid rapid repeated requests.

## Example
After running and entering `2003-05-23` the script created `playlist_2003-05-23.txt` with entries like:

```
1. Get Busy
   Listen: https://open.spotify.com/search/Get%20Busy

2. 21 Questions
   Listen: https://open.spotify.com/search/21%20Questions
```

---
If you want, I can also add a `requirements.txt`, Dockerfile, or make the script take the date as a CLI argument.
