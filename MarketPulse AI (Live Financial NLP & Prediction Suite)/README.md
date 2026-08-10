# MarketPulse AI — Live Financial NLP & Prediction Suite
> sentiment with time-series price prediction (Random Forest).

## Demo Video
<video src="https://github.com/user-attachments/assets/e9e9050f-e5fd-453d-9dfc-7619980ae780" controls width="600"></video>

## Project Overview

MarketPulse AI is a lightweight demo that fetches 1 year of historical
price data for a selected ticker using `yfinance`, applies simple
technical indicators, simulates news headlines, scores those headlines
with NLTK VADER sentiment, and trains a Random Forest to predict the
next-day close. The app is delivered as an interactive Streamlit
dashboard in `app.py`.

## Features

- Select from example tickers (NVDA, AAPL, MSFT, TSLA, AMZN)
- Fetches 1 year of historical prices via `yfinance`
- Calculates 10- and 30-day SMA technical indicators
- Simulates financial headlines and scores sentiment with VADER
- Trains a `RandomForestRegressor` and shows actual vs predicted
- Interactive plots using Plotly and a full dataset table

## Requirements

- Python 3.8+
- Packages: `streamlit`, `yfinance`, `nltk`, `numpy`, `pandas`,
  `plotly`, `scikit-learn`

You can install the required packages directly:

```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate
pip install streamlit yfinance nltk numpy pandas plotly scikit-learn
```

Note: `app.py` calls `nltk.download('vader_lexicon')` at startup, so
the VADER lexicon will be fetched automatically when you first run the
app. If you prefer to download manually, run:

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

## Run the app

Start the Streamlit dashboard from the project root:

```bash
streamlit run app.py
```

Then open the provided local URL in your browser (Streamlit prints it
to the console).

## Files

- `app.py` — main Streamlit dashboard and data/model pipeline

## Notes & Limitations

- Headlines are simulated for demo purposes; replace with real news
  ingestion for production uses.
- The model and features are intended as an educational capstone and
  not for live trading decisions.

## Next steps (ideas)

- Add persistent storage or scheduled data refresh
- Replace simulated headlines with live news or RSS feeds
- Experiment with different ML models or expanded feature sets

---
If you want I can also add a `requirements.txt` or create a small
Dockerfile for reproducible runs—tell me which you prefer.
