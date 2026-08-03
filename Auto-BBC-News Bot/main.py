import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BBC_URL = "https://www.bbc.com/news"
CSV_FILE_NAME = "bbc_top_news.csv"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    print("🌐 Opening BBC News...")
    driver.get(BBC_URL)
    time.sleep(4)  

    try:
        cookie_btn = driver.find_element(
            By.XPATH, 
            '//button[contains(., "Consent") or contains(., "Agree")]'
        )
        cookie_btn.click()
        time.sleep(1)
    except Exception:
        pass 

    headlines = driver.find_elements(By.CSS_SELECTOR, value='[data-testid="card-headline"]')
    
    scraped_data = []
    seen_titles = set()

    print("\n📰 Extracting BBC Top News...")

    for item in headlines:
        title = item.text.strip()
        
        if title and title not in seen_titles:
            seen_titles.add(title)
            
            try:
                parent_a = item.find_element(By.XPATH, "./ancestor::a")
                link = parent_a.get_attribute("href")
            except Exception:
                link = "N/A"
                
            scraped_data.append({"Headline": title, "URL": link})
            
            if len(scraped_data) >= 10:
                break

    with open(CSV_FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Headline", "URL"])
        
        writer.writeheader()
        
        writer.writerows(scraped_data)

    print(f"💾 Successfully saved {len(scraped_data)} headlines to '{CSV_FILE_NAME}'!")

except Exception as err:
    print(f"❌ Error during execution: {err}")

finally:
    time.sleep(2)
    driver.quit()
    print("🏁 Browser closed cleanly.")