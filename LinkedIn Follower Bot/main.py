import time
import pyautogui
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from credentials import LINKEDIN_EMAIL, LINKEDIN_PASSWORD

TARGET_URL = "https://www.linkedin.com/company/google/"


class LinkedInFollowerBot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 20)

    def dismiss_cookies(self):
        """Dismisses any cookie consent banners if shown."""
        try:
            cookie_btn = self.driver.find_element(
                By.XPATH, 
                '//button[contains(., "Accept") or contains(., "Agree") or contains(., "Reject")]'
            )
            self.driver.execute_script("arguments[0].click();", cookie_btn)
            time.sleep(1)
        except Exception:
            pass

    def login(self):
        """Logs into LinkedIn cleanly using explicit waits and clipboard pasting."""
        print("🌐 Opening LinkedIn login page...")
        self.driver.get("https://www.linkedin.com/checkpoint/rm/sign-in-another-account")
        time.sleep(3)
        self.dismiss_cookies()

        print("📝 Auto-filling login credentials...")
        try:
            email_field = self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    '//input[@id="username" or @id="session_key" or @name="session_key"]'
                ))
            )
            email_field.click()
            time.sleep(0.5)

            pyperclip.copy(LINKEDIN_EMAIL)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)

            password_field = self.driver.find_element(By.XPATH, '//input[@type="password"]')
            password_field.click()
            time.sleep(0.5)

            pyperclip.copy(LINKEDIN_PASSWORD)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)

            password_field.send_keys(Keys.ENTER)
            print("⏳ Login submitted...")
            time.sleep(3)

        except Exception as e:
            print(f"⚠️ Auto-fill notice: {e}")

        print("\n" + "=" * 65)
        input("👉 Complete any CAPTCHA/Verification in Chrome (if shown), then press ENTER here in VS Code to continue...\n" + "=" * 65 + "\n")

    def follow_target_page(self):
        """Navigates to the target page and clicks the Follow button."""
        print(f"🎯 Navigating to target page: {TARGET_URL}")
        self.driver.get(TARGET_URL)
        time.sleep(4)

        self.driver.execute_script("window.scrollTo(0, 200);")
        time.sleep(2)

        print("🔍 Locating '+ Follow' button...")
        follow_clicked = False

        follow_locators = [
            '//button[contains(@class, "follow")]',
            '//button[.//span[text()="+ Follow"] or .//span[text()="Follow"] or contains(., "Follow")]',
            '//button[contains(@aria-label, "Follow")]'
        ]

        for locator in follow_locators:
            try:
                buttons = self.driver.find_elements(By.XPATH, locator)
                for btn in buttons:
                    if btn.is_displayed():
                        self.driver.execute_script("arguments[0].click();", btn)
                        follow_clicked = True
                        print("🎉 Successfully clicked '+ Follow' button!")
                        time.sleep(3)
                        break
                if follow_clicked:
                    break
            except Exception:
                continue

        if not follow_clicked:
            print("⚠️ Button click via DOM missed, attempting focused screen click...")
            screen_w, screen_h = pyautogui.size()
            pyautogui.click(x=screen_w // 2, y=screen_h // 3)
            time.sleep(2)

        print("✨ Task completed! Check the browser to confirm page follow status.")

    def close(self):
        """Closes browser session cleanly after delay."""
        time.sleep(5)
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
        print("🏁 Session finished.")

if __name__ == "__main__":
    bot = LinkedInFollowerBot()
    try:
        bot.login()
        bot.follow_target_page()
    finally:
        bot.close()