# ScrapeIntel Enterprise

ScrapeIntel Enterprise is a Streamlit-based dashboard for simulating and visualizing e-commerce product scraping, competitor price monitoring, and inventory insights.

## Demo Video
<video src="https://github.com/user-attachments/assets/7db5a9c5-9081-4cc7-93b1-4ea136ce83d9" controls width="600"></video>

## Overview

This project demonstrates a lightweight web scraping workflow with:

- simulated product extraction from multiple ecommerce-style pages
- competitor price comparison
- discount and stock analysis
- interactive charts and KPI metrics
- downloadable CSV export of scraped data

## Features

- Filter products by category
- Set a maximum price alert threshold
- View total products, average price, active sellers, and out-of-stock items
- Explore price distribution and discount breakdown charts
- Review stock warnings for low or unavailable inventory
- Download the cleaned dataset as a CSV file

## Tech Stack

- Python
- Streamlit
- BeautifulSoup
- NumPy
- Pandas
- Plotly
- Requests

## Installation

Install the required dependencies:

```bash
pip install streamlit beautifulsoup4 numpy pandas plotly requests
```

## Run the Application

From the project folder, run:

```bash
streamlit run app.py
```

Then open the local URL displayed in the terminal.

## Project Structure

```text
.
├── app.py
└── README.md
```

## Notes

This project currently uses a simulated scraper engine to demonstrate the full data pipeline. It is suitable for prototyping dashboards, analytics views, and competitor monitoring concepts.
