# Stock News Monitoring Project

This Python project monitors a stock's daily price movement and sends WhatsApp alerts with related news headlines when the change is significant.

## Demo Video
<video src="https://github.com/user-attachments/assets/68b92043-3759-47df-a905-23a78ff483dd" controls width="600"></video>

## Message-Received for testing
   ![Message-Received for testing.](./Message-Received%20for%20testing.jpg)

## Real-Time Working
   ![Real-Time Working.](./Real-Time%20Working.jpg)

## What it does

The script:
- fetches daily stock price data from Alpha Vantage
- compares yesterday's close with the day before
- checks whether the price moved by more than 5%
- fetches recent news articles for the company from NewsAPI
- sends the results to your WhatsApp number through Twilio

## Features

- Tracks a configurable stock symbol
- Sends alerts for significant price movement
- Includes a test mode for sending alerts without the 5% threshold check
- Uses Twilio WhatsApp sandbox integration

## Requirements

- Python 3.8 or newer
- Internet access
- Accounts for:
  - Alpha Vantage
  - NewsAPI
  - Twilio

## Installation

1. Clone or open the project folder.
2. Create and activate a virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install requests twilio
```

## Configuration

Open [main.py](main.py) and update the following values:

- `TWILIO_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_NUMBER`
- `MY_WHATSAPP_NUMBER`
- `STOCK_NAME`
- `COMPANY_NAME`
- `STOCK_API_KEY`
- `NEWS_API_KEY`

You can also set `TEST_MODE = True` to bypass the 5% threshold and send alerts during testing.

## Usage

Run the script with:

```bash
python main.py
```

The script will print the stock movement and, if conditions are met, send WhatsApp messages with the latest news headlines.

## Notes

- For Twilio WhatsApp alerts, your phone number must be verified and joined to the Twilio sandbox.
- Keep API keys private and do not commit them to public repositories.
- If you are using free-tier API keys, be aware of request limits.

## Project Files

- [main.py](main.py) - Main script for fetching stock data, news, and sending WhatsApp alerts
