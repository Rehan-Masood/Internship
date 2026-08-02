import smtplib
import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.com/dp/B0D18VS397"

BUY_PRICE = 6000.0 

MY_EMAIL = "jrehan590@gmail.com"
MY_PASSWORD = "sqpcxcgeggmnvpty" 
RECIPIENT_EMAIL = "jrehan590@gmail.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def main():
    try:
        response = requests.get(URL, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        title_element = soup.find(id="productTitle")
        if title_element:
            title = title_element.get_text().strip()
        else:
            title = "Amazon Product"

        price_element = None
        price_selectors = [
            {"class_": "a-offscreen"},
            {"id": "priceblock_ourprice"},
            {"id": "priceblock_dealprice"},
            {"class_": "a-price-whole"},
            {"id": "price_inside_buybox"}
        ]

        for selector in price_selectors:
            found = soup.find(**selector)
            if found and found.get_text().strip():
                price_element = found
                break

        if not price_element:
            raise ValueError("Could not locate a valid price element on the page.")

        price_text = price_element.get_text()

        clean_price = (
            price_text.replace("PKR", "")
            .replace("$", "")
            .replace(",", "")
            .strip()
        )

        price_as_float = float(clean_price)

        print(f"📦 Product: {title}")
        print(f"💰 Current Price: {price_as_float}")

        if price_as_float < BUY_PRICE:
            message = f"Subject: Amazon Price Alert!\n\n{title} is now available for ${price_as_float}!\n\nBuy now: {URL}"
            
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=RECIPIENT_EMAIL,
                    msg=message.encode("utf-8")
                )
                print("📧 Price drop detected! Alert email sent successfully.")
        else:
            print(f"ℹ️ Current price ({price_as_float}) is above target ({BUY_PRICE}). No email sent.")

    except requests.exceptions.HTTPError as err:
        print(f"❌ HTTP Error: {err}")
    except ValueError as err:
        print(f"❌ Parsing Error: {err}")
    except Exception as err:
        print(f"❌ Unexpected Error: {err}")

if __name__ == "__main__":
    main()