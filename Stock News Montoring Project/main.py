import requests
from twilio.rest import Client

TWILIO_SID = "your_twilio_account_sid_here"         
TWILIO_AUTH_TOKEN = "your_twilio_auth_token_here"  
TWILIO_WHATSAPP_NUMBER = "whatsapp:+1234567890"                
MY_WHATSAPP_NUMBER = "whatsapp:+9232345678976"                  

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "QCU31YH2LHEK85SQ"     
NEWS_API_KEY = "9dea02d58ad34bc98fb07aad83697d7b"      

TEST_MODE = False 

def get_stock_price_change():
    """Fetches yesterday's and the day before's closing price, returns (up_down_symbol, diff_percent)."""
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK_NAME,
        "apikey": STOCK_API_KEY,
    }

    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]

    yesterday_data = data_list[0]
    yesterday_closing_price = float(yesterday_data["4. close"])

    day_before_yesterday_data = data_list[1]
    day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

    difference = yesterday_closing_price - day_before_yesterday_closing_price
    up_down = "🔺" if difference > 0 else "🔻"
    diff_percent = round((difference / yesterday_closing_price) * 100, 2)

    print(f"Yesterday's close: {yesterday_closing_price}")
    print(f"Day before's close: {day_before_yesterday_closing_price}")
    print(f"Change: {up_down} {diff_percent}%")

    return up_down, diff_percent


def get_news_articles():
    """Fetches the first 3 news articles about the company."""
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]

    return articles[:3]


def send_whatsapp_alerts(formatted_articles):
    """Sends each formatted article as a separate WhatsApp message via Twilio."""
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=MY_WHATSAPP_NUMBER,
        )
        print(f"Sent. Status: {message.status}")


up_down, diff_percent = get_stock_price_change()

if TEST_MODE or abs(diff_percent) > 5:
    print("Significant move detected (or TEST_MODE) — fetching news...")
    three_articles = get_news_articles()

    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}.\nBrief: {article['description']}"
        for article in three_articles
    ]

    send_whatsapp_alerts(formatted_articles)
    print("Done! Check your WhatsApp.")
else:
    print(f"No significant move ({diff_percent}% change). No alert sent.")