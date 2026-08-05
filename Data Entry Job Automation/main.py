import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

ZILLOW_CLONE_URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSc-te2Hr5X4pE30Lfbdf7uYcr8bnqdZgLJ5KDYbuASB2nU3Lg/viewform"
MAX_LISTINGS = 8  


class DataEntryAutomation:
    def __init__(self):
        self.links = []
        self.prices = []
        self.addresses = []

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 15)

    def scrape_zillow_data(self):
        """Scrapes property addresses, prices, and links using BeautifulSoup."""
        print("🌐 Scraping property data from Zillow Clone...")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }

        response = requests.get(ZILLOW_CLONE_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        link_elements = soup.select(".StyledPropertyCardDataWrapper a")[:MAX_LISTINGS]
        self.links = [link["href"] for link in link_elements]

        price_elements = soup.select(".PropertyCardWrapper span")
        for price in price_elements:
            if len(self.prices) >= MAX_LISTINGS:
                break
            price_text = price.get_text()
            if "$" in price_text:
                clean_price = price_text.split("+")[0].split("/")[0].strip()
                self.prices.append(clean_price)

        # 3. Scrape Addresses (sliced to MAX_LISTINGS)
        address_elements = soup.select(".StyledPropertyCardDataWrapper address")[:MAX_LISTINGS]
        self.addresses = [addr.get_text().replace("|", "").strip() for addr in address_elements]

        print(f"✅ Found {len(self.links)} listings to process (limited to {MAX_LISTINGS}).")

    def fill_google_form(self):
        """Submits the scraped property listings into the Google Form."""
        print(f"📝 Submitting {len(self.links)} listings into Google Form...")

        for i in range(len(self.links)):
            self.driver.get(GOOGLE_FORM_URL)
            time.sleep(2)

            try:
                # Locate text input fields in the Google Form
                inputs = self.wait.until(
                    EC.presence_of_all_elements_located((
                        By.XPATH, 
                        '//input[@jsname="YPqf1c"] | //input[@type="text"]'
                    ))
                )

                # Question 1: Address, Question 2: Price, Question 3: Link
                inputs[0].clear()
                inputs[0].send_keys(self.addresses[i])
                time.sleep(0.3)

                inputs[1].clear()
                inputs[1].send_keys(self.prices[i])
                time.sleep(0.3)

                inputs[2].clear()
                inputs[2].send_keys(self.links[i])
                time.sleep(0.3)

                # Submit Form
                submit_btn = self.driver.find_element(
                    By.XPATH, 
                    '//div[@role="button" and .//span[text()="Submit"]] | //span[text()="Submit"]/ancestor::div[@role="button"]'
                )
                self.driver.execute_script("arguments[0].click();", submit_btn)

                print(f"➡️ Submitted listing #{i + 1}/{len(self.links)}: {self.addresses[i]}")
                time.sleep(1)

            except Exception as e:
                print(f"⚠️ Failed to submit listing #{i + 1}: {e}")

        print(f"\n🎉 Successfully submitted all {len(self.links)} listings!")

    def close(self):
        """Closes browser session cleanly."""
        time.sleep(3)
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
        print("🏁 Session finished.")


# ==================== RUN BOT ====================
if __name__ == "__main__":
    bot = DataEntryAutomation()
    try:
        bot.scrape_zillow_data()
        bot.fill_google_form()
    finally:
        bot.close()