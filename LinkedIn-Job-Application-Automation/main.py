import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, 
    ElementClickInterceptedException, 
    StaleElementReferenceException,
    TimeoutException
)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ACCOUNT_EMAIL = "YOUR_LINKEDIN_EMAIL@example.com"
ACCOUNT_PASSWORD = "YOUR_LINKEDIN_PASSWORD"
PHONE = "1234567890"

SEARCH_URL = (
    "https://www.linkedin.com/jobs/search/?"
    "keywords=python&location=Milton%20Keynes"
)


def abort_application(driver):
    """Closes and discards complex multi-page job application modals safely."""
    try:
        close_button = driver.find_element(By.CLASS_NAME, value="artdeco-modal__dismiss")
        driver.execute_script("arguments[0].click();", close_button)
        time.sleep(1)

        discard_button = driver.find_element(
            By.XPATH, 
            value="//button[contains(@data-control-name, 'discard_application') or contains(., 'Discard')]"
        )
        driver.execute_script("arguments[0].click();", discard_button)
        time.sleep(1)
    except Exception:
        pass  


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 15)

try:
    print("🔑 Navigating to LinkedIn Login...")
    driver.get("https://www.linkedin.com/checkpoint/rm/sign-in-another-account")

    try:
        email_field = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
    except TimeoutException:
        email_field = wait.until(
            EC.presence_of_element_located((By.ID, "session_key"))
        )

    email_field.clear()
    email_field.send_keys(ACCOUNT_EMAIL)

    try:
        password_field = driver.find_element(By.ID, value="password")
    except NoSuchElementException:
        password_field = driver.find_element(By.ID, value="session_password")

    password_field.clear()
    password_field.send_keys(ACCOUNT_PASSWORD)
    password_field.send_keys(Keys.ENTER)

    print("\n⏳ Login submitted...")
    input("👉 Solve any CAPTCHA/Verification in Chrome (if shown), then press ENTER here in VS Code to continue...\n")

    print("🔍 Opening job search page...")
    driver.get(SEARCH_URL)
    time.sleep(5)

    all_listings = driver.find_elements(By.CSS_SELECTOR, value=".job-card-container--clickable")
    print(f"📋 Found {len(all_listings)} job listings on page.")

    for index, listing in enumerate(all_listings, start=1):
        print(f"\n[{index}/{len(all_listings)}] Checking job...")
        
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", listing)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", listing)
            time.sleep(2)

            apply_button = driver.find_element(By.CSS_SELECTOR, value=".jobs-s-apply button")
            driver.execute_script("arguments[0].click();", apply_button)
            time.sleep(2)

            try:
                phone_field = driver.find_element(By.CSS_SELECTOR, value="input[id*='phoneNumber']")
                if phone_field.get_attribute("value") == "":
                    phone_field.send_keys(PHONE)
            except NoSuchElementException:
                pass

            submit_button = driver.find_element(By.CSS_SELECTOR, value="footer button")
            data_control = submit_button.get_attribute("data-control-name")

            if data_control == "continue_unify":
                print("➡️ Multi-step application required. Skipping.")
                abort_application(driver)
            else:
                print("🚀 Submitting Easy Apply application!")
                driver.execute_script("arguments[0].click();", submit_button)
                time.sleep(2)

                close_button = driver.find_element(By.CLASS_NAME, value="artdeco-modal__dismiss")
                driver.execute_script("arguments[0].click();", close_button)

        except NoSuchElementException:
            print("⚠️ No 'Easy Apply' button found. Skipping.")
            abort_application(driver)
            continue
        except Exception as e:
            print(f"⚠️ Skipping this listing: {e}")
            abort_application(driver)
            continue

    print("\n✅ Completed processing all listings on this page!")

except Exception as err:
    print(f"\n❌ Script error: {err}")