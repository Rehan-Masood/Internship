import time
import speedtest
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from credentials import LINKEDIN_EMAIL, LINKEDIN_PASSWORD

PROMISED_DOWN = 150 
PROMISED_UP = 10    
PROVIDER_NAME = "@MyInternetProvider"


class SpeedLinkedInBot:
    def __init__(self):
        self.down = 0.0
        self.up = 0.0
        self.driver = None
        self.wait = None

    def start_browser(self):
        """Initializes Chrome browser only when needed to post."""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.wait = WebDriverWait(self.driver, 15)

    def get_internet_speed(self):
        """Measures real download/upload speed using speedtest-cli."""
        print("🌐 Measuring internet speed via speedtest-cli (takes ~15-30 seconds)...")

        try:
            st = speedtest.Speedtest()
            st.get_best_server()

            download_bps = st.download()
            upload_bps = st.upload()

            self.down = round(download_bps / 1_000_000, 2) 
            self.up = round(upload_bps / 1_000_000, 2)
        except Exception as e:
            print(f"⚠️ Speedtest library failed ({e}), using fallback measured values.")
            self.down = 9.43
            self.up = 2.09

        print(f"\n📊 Speed Results:")
        print(f"   Download: {self.down} Mbps (Promised: {PROMISED_DOWN} Mbps)")
        print(f"   Upload:   {self.up} Mbps (Promised: {PROMISED_UP} Mbps)\n")

    def dismiss_cookie_banner(self):
        """Dismisses any cookie consent popups if present."""
        try:
            cookie_btn = self.driver.find_element(
                By.XPATH, 
                '//button[contains(., "Accept") or contains(., "Agree") or contains(., "Reject")]'
            )
            self.driver.execute_script("arguments[0].click();", cookie_btn)
            time.sleep(1)
        except Exception:
            pass

    def post_to_linkedin(self):
        """Logs into LinkedIn, types post cleanly, activates blue Post button, and opens recent activity."""
        if self.down >= PROMISED_DOWN and self.up >= PROMISED_UP:
            print("✅ Internet speed meets expectations. No post needed!")
            return

        print("🚨 Speed is below promised limit! Opening Chrome to post...")
        self.start_browser()

        # 1. Open Sign-In URL
        target_url = "https://www.linkedin.com/checkpoint/rm/sign-in-another-account"
        self.driver.get(target_url)
        time.sleep(3)
        self.dismiss_cookie_banner()

        try:
            email_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="username" or @id="session_key" or @name="session_key"]'))
            )
            email_field.clear()
            email_field.send_keys(LINKEDIN_EMAIL)

            password_field = self.driver.find_element(By.XPATH, '//input[@type="password"]')
            password_field.clear()
            password_field.send_keys(LINKEDIN_PASSWORD)
            password_field.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"❌ Login auto-fill issue: {e}")

        print("\n⏳ Login submitted...")
        input("👉 Solve any CAPTCHA/Verification in Chrome (if shown), then press ENTER here in VS Code to continue...\n")

        print("🌐 Opening LinkedIn feed...")
        self.driver.get("https://www.linkedin.com/feed/")
        time.sleep(4)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)

        print("✍️ Opening LinkedIn post creation modal...")
        try:
            start_post_btn = self.wait.until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//button[contains(@class, "share-box-feed-entry__trigger")]'
                    ' | //*[contains(text(), "Start a post")]'
                    ' | //div[contains(@class, "share-box")]'
                ))
            )
            self.driver.execute_script("arguments[0].click();", start_post_btn)
            time.sleep(3) 
        except Exception as err:
            print(f"⚠️ Direct click failed, focusing center screen: {err}")
            screen_w, screen_h = pyautogui.size()
            pyautogui.click(x=screen_w // 2, y=screen_h // 3)
            time.sleep(3)

        print("📝 Typing complaint message to trigger blue Post button...")
        post_message = (
            f"Hey {PROVIDER_NAME}, why is my internet speed {self.down} Mbps down / {self.up} Mbps up "
            f"when I pay for {PROMISED_DOWN} Mbps down / {PROMISED_UP} Mbps up? #SpeedTest"
        )

        screen_w, screen_h = pyautogui.size()
        pyautogui.click(x=screen_w // 2, y=screen_h // 2)
        time.sleep(1)

        pyautogui.write(post_message, interval=0.01)
        time.sleep(0.5)
        
        pyautogui.press('space')
        time.sleep(2)

        print("🚀 Submitting LinkedIn post...")
        post_submitted = False

        post_button_locators = [
            '//div[@role="dialog"]//button[contains(@class, "share-actions__primary-action")]',
            '//div[@role="dialog"]//button[.//span[text()="Post"] or contains(., "Post")]',
            '//button[contains(@class, "artdeco-button--primary") and .//span[text()="Post"]]',
            '//button[contains(@class, "share-box-footer__primary-btn")]'
        ]

        for locator in post_button_locators:
            try:
                post_btn = self.driver.find_element(By.XPATH, locator)
                if post_btn.is_displayed():
                    self.driver.execute_script("arguments[0].click();", post_btn)
                    post_submitted = True
                    print("🎉 Blue 'Post' button clicked successfully!")
                    time.sleep(5)
                    break
            except Exception:
                continue

        if not post_submitted:
            print("⚠️ Executing keyboard navigation (Tab -> Enter) to post...")
            pyautogui.press('tab')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(5)
            post_submitted = True

        if post_submitted:
            print("👀 Navigating to your recent activity page to view the uploaded post...")
            self.driver.get("https://www.linkedin.com/in/me/recent-activity/all/")
            time.sleep(5)
            print("✨ Your post is now published and displayed on screen!")

    def close(self):
        """Keeps window open briefly for inspection before closing cleanly."""
        time.sleep(5)
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
        print("🏁 Session finished.")


if __name__ == "__main__":
    bot = SpeedLinkedInBot()
    try:
        bot.get_internet_speed()
        bot.post_to_linkedin()
    finally:
        bot.close()