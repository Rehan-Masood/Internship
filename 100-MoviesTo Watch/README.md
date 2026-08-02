# 100 Movies To Watch

This project uses BeautifulSoup to scrape Empire's list of the 100 greatest movies from the Internet Archive and writes the titles to `movies.txt`.

## What it does

- Fetches the archived Empire movie list page.
- Extracts each movie title from the page.
- Reverses the order so the titles are written from first to last.
- Saves the results to `movies.txt`, one title per line.

## Requirements

- Python 3
- `requests`
- `beautifulsoup4`

Install the dependencies with:

```bash
pip install requests beautifulsoup4
```

## Run It

From the project folder, run:

```bash
python main.py
```

After the script finishes, open `movies.txt` to see the generated list.

## Data Source

The script uses the Internet Archive copy of the Empire article below so the page structure stays stable over time:

```python
https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/
```

## Output Format

The current script writes each movie title on its own line in `movies.txt`.

If you want numbered output such as `1. Title`, `2. Title`, the script in `main.py` can be adjusted easily.