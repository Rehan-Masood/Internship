import time
import speedtest
import pyautogui

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    StaleElementReferenceException,
    WebDriverException,
)

from webdriver_manager.chrome import ChromeDriverManager

from credentials import LINKEDIN_EMAIL, LINKEDIN_PASSWORD


# ============================================================
# SETTINGS
# ============================================================

PROMISED_DOWN = 150
PROMISED_UP = 10

PROVIDER_NAME = "@MyInternetProvider"


# ============================================================
# BOT
# ============================================================

class SpeedLinkedInBot:

    def __init__(self):

        self.driver = None
        self.wait = None

        self.down = 0.0
        self.up = 0.0

        self.post_message = ""

    # ========================================================
    # START BROWSER
    # ========================================================

    def start_browser(self):

        print("🌐 Starting Chrome...")

        options = webdriver.ChromeOptions()

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )

        self.driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            ),
            options=options
        )

        self.wait = WebDriverWait(
            self.driver,
            20
        )

    # ========================================================
    # SPEED TEST
    # ========================================================

    def get_internet_speed(self):

        print(
            "🌐 Measuring internet speed via speedtest-cli "
            "(takes ~15-30 seconds)..."
        )

        try:

            st = speedtest.Speedtest()

            print("🔎 Finding the best speedtest server...")
            st.get_best_server()

            print("⬇️ Testing download speed...")
            download_bps = st.download()

            print("⬆️ Testing upload speed...")
            upload_bps = st.upload()

            self.down = round(
                download_bps / 1_000_000,
                2
            )

            self.up = round(
                upload_bps / 1_000_000,
                2
            )

        except Exception as e:

            print(
                f"❌ Speed test failed: {e}"
            )

            return False

        print("\n📊 Speed Results:")

        print(
            f"   Download: {self.down} Mbps "
            f"(Promised: {PROMISED_DOWN} Mbps)"
        )

        print(
            f"   Upload:   {self.up} Mbps "
            f"(Promised: {PROMISED_UP} Mbps)"
        )

        print()

        return True

    # ========================================================
    # COOKIE POPUP
    # ========================================================

    def dismiss_cookie_banner(self):

        try:

            buttons = self.driver.find_elements(
                By.TAG_NAME,
                "button"
            )

            for button in buttons:

                try:

                    if not button.is_displayed():
                        continue

                    text = button.text.strip().lower()

                    if text in (
                        "accept",
                        "accept cookies",
                        "agree",
                        "reject",
                        "reject all",
                    ):

                        self.driver.execute_script(
                            "arguments[0].click();",
                            button
                        )

                        time.sleep(1)

                        return

                except Exception:
                    continue

        except Exception:
            pass

    # ========================================================
    # LOGIN
    # ========================================================

    def login_linkedin(self):

        print(
            "🔐 Opening LinkedIn login page..."
        )

        self.driver.get(
            "https://www.linkedin.com/checkpoint/"
            "rm/sign-in-another-account"
        )

        time.sleep(3)

        self.dismiss_cookie_banner()

        try:

            email = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//input[@id='username' "
                        "or @id='session_key' "
                        "or @name='session_key' "
                        "or @type='email']"
                    )
                )
            )

            email.clear()
            email.send_keys(
                LINKEDIN_EMAIL
            )

            password = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//input[@type='password']"
                    )
                )
            )

            password.clear()
            password.send_keys(
                LINKEDIN_PASSWORD
            )

            password.send_keys(
                Keys.ENTER
            )

        except Exception as e:

            print(
                f"⚠️ Login auto-fill issue: {e}"
            )

        print(
            "⏳ Login submitted..."
        )

        input(
            "\n👉 Solve any CAPTCHA/Verification in Chrome "
            "(if shown), then press ENTER here in VS Code "
            "to continue...\n"
        )

    # ========================================================
    # FIND START A POST
    # ========================================================

    def find_start_post(self):

        selectors = [

            (
                By.CSS_SELECTOR,
                "button.share-box-feed-entry__trigger"
            ),

            (
                By.XPATH,
                "//button[contains(., 'Start a post')]"
            ),

            (
                By.XPATH,
                "//*[normalize-space()='Start a post']"
            ),

            (
                By.XPATH,
                "//*[@aria-label='Start a post']"
            ),

        ]

        for by, selector in selectors:

            try:

                elements = self.driver.find_elements(
                    by,
                    selector
                )

                for element in elements:

                    try:

                        if element.is_displayed():
                            return element

                    except Exception:
                        continue

            except Exception:
                continue

        return None

    # ========================================================
    # OPEN POST COMPOSER
    # ========================================================

    def open_post_composer(self):

        print(
            "🌐 Opening LinkedIn feed..."
        )

        self.driver.get(
            "https://www.linkedin.com/feed/"
        )

        time.sleep(4)

        self.driver.execute_script(
            "window.scrollTo(0, 0);"
        )

        time.sleep(2)

        print(
            "✅ LinkedIn feed loaded."
        )

        print(
            "✍️ Opening LinkedIn post creation modal..."
        )

        start_post = self.find_start_post()

        if not start_post:

            print(
                "❌ 'Start a post' button not found."
            )

            return False

        print(
            "✅ 'Start a post' button found."
        )

        try:

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'center'
                });
                """,
                start_post
            )

            time.sleep(0.5)

            try:

                start_post.click()

            except Exception:

                self.driver.execute_script(
                    "arguments[0].click();",
                    start_post
                )

        except Exception as e:

            print(
                f"❌ Could not click Start a post: {e}"
            )

            return False

        time.sleep(3)

        print(
            "✅ Post composer is open."
        )

        return True

    # ========================================================
    # FIND EDITOR
    # ========================================================

    def find_editor(self):

        selectors = [

            (
                By.CSS_SELECTOR,
                "div.ql-editor[contenteditable='true']"
            ),

            (
                By.CSS_SELECTOR,
                "[contenteditable='true']"
                "[data-placeholder='What do you want to talk about?']"
            ),

            (
                By.CSS_SELECTOR,
                "[contenteditable='true']"
                "[aria-label='Text editor for creating content']"
            ),

            (
                By.CSS_SELECTOR,
                "[contenteditable='true']"
                "[role='textbox']"
            ),

            (
                By.CSS_SELECTOR,
                "[contenteditable='true']"
            ),

        ]

        for by, selector in selectors:

            try:

                elements = self.driver.find_elements(
                    by,
                    selector
                )

                for element in elements:

                    try:

                        if element.is_displayed():
                            return element

                    except Exception:
                        continue

            except Exception:
                continue

        return None

    # ========================================================
    # WRITE WITH SELENIUM
    # ========================================================

    def write_using_selenium(self):

        editor = self.find_editor()

        if not editor:

            return False

        print(
            "✅ LinkedIn editor detected."
        )

        try:

            self.driver.execute_script(
                """
                arguments[0].scrollIntoView({
                    block: 'center',
                    inline: 'center'
                });
                """,
                editor
            )

            time.sleep(0.5)

            editor.click()

            time.sleep(0.3)

            editor.send_keys(
                Keys.CONTROL,
                "a"
            )

            time.sleep(0.2)

            editor.send_keys(
                self.post_message
            )

            time.sleep(2)

            text = self.driver.execute_script(
                """
                return (
                    arguments[0].innerText ||
                    arguments[0].textContent ||
                    ''
                );
                """,
                editor
            )

            if self.post_message in text:

                print(
                    "✅ Complaint written successfully."
                )

                return True

            if (
                str(self.down) in text
                and
                str(self.up) in text
            ):

                print(
                    "✅ Complaint text detected."
                )

                return True

        except Exception as e:

            print(
                f"⚠️ Selenium editor typing failed: {e}"
            )

        return False

    # ========================================================
    # VISUAL WRITE
    # ========================================================

    def write_using_visual(self):

        print(
            "🖱️ Using visible LinkedIn composer..."
        )

        try:

            screen_width, screen_height = (
                pyautogui.size()
            )

            # ------------------------------------------------
            # Based on the screenshot you provided:
            #
            # LinkedIn composer occupies the center.
            # The writing area begins around 20%-40%
            # from the top.
            #
            # We click well inside the text area.
            # ------------------------------------------------

            x = int(
                screen_width * 0.30
            )

            y = int(
                screen_height * 0.27
            )

            print(
                f"🖱️ Clicking editor at "
                f"({x}, {y})..."
            )

            pyautogui.click(
                x,
                y
            )

            time.sleep(0.7)

            pyautogui.hotkey(
                "ctrl",
                "a"
            )

            time.sleep(0.2)

            pyautogui.write(
                self.post_message,
                interval=0.01
            )

            time.sleep(2)

            print(
                "✅ Complaint text sent to LinkedIn composer."
            )

            return True

        except Exception as e:

            print(
                f"❌ Visual writing failed: {e}"
            )

            return False

    # ========================================================
    # WRITE COMPLAINT
    # ========================================================

    def write_complaint(self):

        self.post_message = (
            f"Hey {PROVIDER_NAME}, why is my internet speed "
            f"{self.down} Mbps down / {self.up} Mbps up "
            f"when I pay for {PROMISED_DOWN} Mbps down / "
            f"{PROMISED_UP} Mbps up? #SpeedTest"
        )

        print(
            "📝 Typing complaint message..."
        )

        if self.write_using_selenium():

            return True

        return self.write_using_visual()

    # ========================================================
    # FIND POST BUTTON WITH JAVASCRIPT
    # ========================================================

    def find_post_button_javascript(self):

        try:

            result = self.driver.execute_script(
                """
                const buttons = Array.from(
                    document.querySelectorAll("button")
                );

                for (const button of buttons) {

                    const text = (
                        button.innerText ||
                        button.textContent ||
                        ""
                    ).trim();

                    const rect =
                        button.getBoundingClientRect();

                    const style =
                        window.getComputedStyle(button);

                    const disabled =
                        button.disabled ||
                        button.getAttribute(
                            "aria-disabled"
                        ) === "true";

                    if (
                        text === "Post" &&
                        rect.width > 0 &&
                        rect.height > 0 &&
                        style.display !== "none" &&
                        style.visibility !== "hidden" &&
                        !disabled
                    ) {

                        return button;
                    }
                }

                return null;
                """
            )

            return result

        except Exception:

            return None

    # ========================================================
    # FIND POST BUTTON USING SELENIUM
    # ========================================================

    def find_post_button_selenium(self):

        selectors = [

            (
                By.CSS_SELECTOR,
                "button.share-actions__primary-action"
            ),

            (
                By.XPATH,
                "//button[contains("
                "@class,"
                "'share-actions__primary-action'"
                ") and contains(normalize-space(.), 'Post')]"
            ),

            (
                By.XPATH,
                "//button[.//span[contains("
                "@class,"
                "'artdeco-button__text'"
                ") and normalize-space()='Post']]"
            ),

            (
                By.XPATH,
                "//button[normalize-space(.)='Post']"
            ),

        ]

        for by, selector in selectors:

            try:

                elements = self.driver.find_elements(
                    by,
                    selector
                )

                for button in elements:

                    try:

                        if not button.is_displayed():
                            continue

                        text = button.text.strip()

                        if text != "Post":
                            continue

                        if button.get_attribute(
                            "disabled"
                        ) is not None:

                            continue

                        if button.get_attribute(
                            "aria-disabled"
                        ) == "true":

                            continue

                        return button

                    except StaleElementReferenceException:

                        continue

            except Exception:

                continue

        return None

    # ========================================================
    # CLICK POST USING SELENIUM
    # ========================================================

    def click_post_selenium(self):

        print(
            "🔎 Searching LinkedIn DOM for Post button..."
        )

        end_time = time.time() + 20

        while time.time() < end_time:

            button = self.find_post_button_selenium()

            if button:

                print(
                    "✅ Post button found in LinkedIn DOM."
                )

                try:

                    self.driver.execute_script(
                        """
                        arguments[0].scrollIntoView({
                            block: 'center',
                            inline: 'center'
                        });
                        """,
                        button
                    )

                    time.sleep(0.5)

                    button.click()

                    print(
                        "🎉 Post clicked with Selenium."
                    )

                    return True

                except Exception as e:

                    print(
                        f"⚠️ Selenium click failed: {e}"
                    )

                    try:

                        button = (
                            self.find_post_button_selenium()
                        )

                        if button:

                            self.driver.execute_script(
                                "arguments[0].click();",
                                button
                            )

                            print(
                                "🎉 Post clicked with JavaScript."
                            )

                            return True

                    except Exception:
                        pass

            time.sleep(0.5)

        return False

    # ========================================================
    # FIND BLUE POST BUTTON ON SCREEN
    # ========================================================

    def find_blue_post_on_screen(self):

        """
        Final visual fallback.

        Instead of guessing one coordinate, inspect the
        screenshot and search the lower-right part of the
        LinkedIn composer for a blue clickable button.

        This fixes the previous incorrect coordinate:
        (972, 511)
        """

        try:

            screenshot = pyautogui.screenshot()

            width, height = screenshot.size

            # ------------------------------------------------
            # Only inspect the lower-right portion of the
            # screen where the LinkedIn composer Post button
            # appears in your screenshot.
            # ------------------------------------------------

            left = int(width * 0.65)
            right = int(width * 0.95)

            top = int(height * 0.50)
            bottom = int(height * 0.90)

            blue_points = []

            for y in range(
                top,
                bottom,
                3
            ):

                for x in range(
                    left,
                    right,
                    3
                ):

                    r, g, b = screenshot.getpixel(
                        (x, y)
                    )

                    # LinkedIn blue / blue-like pixels.
                    if (
                        b > 120
                        and
                        b > r * 1.25
                        and
                        b > g * 1.05
                        and
                        r < 100
                    ):

                        blue_points.append(
                            (x, y)
                        )

            if not blue_points:

                return None

            # ------------------------------------------------
            # Calculate bounding box of blue pixels.
            # ------------------------------------------------

            xs = [
                point[0]
                for point in blue_points
            ]

            ys = [
                point[1]
                for point in blue_points
            ]

            min_x = min(xs)
            max_x = max(xs)

            min_y = min(ys)
            max_y = max(ys)

            detected_width = max_x - min_x
            detected_height = max_y - min_y

            # ------------------------------------------------
            # Ignore huge blue areas. We want a button,
            # not a background/banner.
            # ------------------------------------------------

            if detected_width > width * 0.25:
                return None

            if detected_height > height * 0.20:
                return None

            center_x = (
                min_x + max_x
            ) // 2

            center_y = (
                min_y + max_y
            ) // 2

            print(
                f"🔵 Blue button detected around "
                f"({center_x}, {center_y})."
            )

            return (
                center_x,
                center_y
            )

        except Exception as e:

            print(
                f"⚠️ Screen button detection failed: {e}"
            )

            return None

    # ========================================================
    # FINAL VISUAL POST CLICK
    # ========================================================

    def click_post_visual(self):

        print(
            "🖱️ Selenium could not access Post."
        )

        print(
            "🔍 Searching screen for the actual "
            "blue Post button..."
        )

        position = self.find_blue_post_on_screen()

        if position:

            x, y = position

            print(
                f"🖱️ Clicking detected Post button "
                f"at ({x}, {y})..."
            )

            pyautogui.click(
                x,
                y
            )

            time.sleep(5)

            return True

        # ----------------------------------------------------
        # If color detection doesn't find it, use the actual
        # screen geometry from your screenshot.
        #
        # IMPORTANT:
        # This is based on FULL SCREEN dimensions,
        # NOT Selenium's viewport coordinates.
        # ----------------------------------------------------

        try:

            screen_width, screen_height = (
                pyautogui.size()
            )

            # Your screenshot places Post at approximately
            # 76.5% screen width and 70% screen height.

            x = int(
                screen_width * 0.765
            )

            y = int(
                screen_height * 0.70
            )

            print(
                f"🖱️ Using final screen fallback: "
                f"({x}, {y})"
            )

            pyautogui.click(
                x,
                y
            )

            time.sleep(5)

            return True

        except Exception as e:

            print(
                f"❌ Final visual click failed: {e}"
            )

            return False

    # ========================================================
    # VERIFY POST WAS SUBMITTED
    # ========================================================

    def verify_post_submitted(self):

        print(
            "🔍 Verifying that LinkedIn submitted the post..."
        )

        # Give LinkedIn time to close composer.
        time.sleep(2)

        end_time = time.time() + 10

        while time.time() < end_time:

            # If Post button disappears, that's a good sign.
            button = self.find_post_button_selenium()

            if not button:

                # Also check for composer editor.
                editor = self.find_editor()

                if not editor:

                    print(
                        "✅ LinkedIn composer closed."
                    )

                    print(
                        "✅ Post submission appears successful."
                    )

                    return True

            time.sleep(0.5)

        # ----------------------------------------------------
        # If the page still contains the composer, don't lie
        # to the user and don't open Recent Activity.
        # ----------------------------------------------------

        print(
            "⚠️ LinkedIn composer is still open."
        )

        print(
            "⚠️ Post submission could not be verified."
        )

        return False

    # ========================================================
    # CLICK POST
    # ========================================================

    def click_post_button(self):

        print(
            "🔎 Looking for blue 'Post' button..."
        )

        # ----------------------------------------------------
        # Method 1: Selenium.
        # ----------------------------------------------------

        if self.click_post_selenium():

            if self.verify_post_submitted():

                return True

        # ----------------------------------------------------
        # Method 2: Screen detection.
        # ----------------------------------------------------

        if self.click_post_visual():

            if self.verify_post_submitted():

                return True

        print(
            "❌ Post was NOT submitted."
        )

        return False

    # ========================================================
    # SHOW RECENT ACTIVITY
    # ========================================================

    def show_recent_activity(self):

        print(
            "\n👀 Opening your Recent Activity..."
        )

        try:

            self.driver.get(
                "https://www.linkedin.com/in/me/"
                "recent-activity/all/"
            )

            time.sleep(5)

            print(
                "✨ Recent Activity opened."
            )

            print(
                "✨ Your published post should be visible."
            )

        except Exception as e:

            print(
                f"⚠️ Could not open Recent Activity: {e}"
            )

    # ========================================================
    # MAIN LINKEDIN PROCESS
    # ========================================================

    def post_to_linkedin(self):

        # ----------------------------------------------------
        # Speed condition
        # ----------------------------------------------------

        if (
            self.down >= PROMISED_DOWN
            and
            self.up >= PROMISED_UP
        ):

            print(
                "✅ Internet speed meets expectations."
            )

            print(
                "✅ No LinkedIn complaint post needed!"
            )

            return

        print(
            "🚨 Speed is below promised limit! "
            "Opening Chrome to post..."
        )

        # ----------------------------------------------------
        # Start browser
        # ----------------------------------------------------

        self.start_browser()

        # ----------------------------------------------------
        # Login
        # ----------------------------------------------------

        self.login_linkedin()

        # ----------------------------------------------------
        # Open composer
        # ----------------------------------------------------

        if not self.open_post_composer():

            print(
                "❌ Could not open LinkedIn post composer."
            )

            return

        # ----------------------------------------------------
        # Write
        # ----------------------------------------------------

        if not self.write_complaint():

            print(
                "❌ Complaint could not be written."
            )

            return

        # ----------------------------------------------------
        # Wait for LinkedIn to process the text.
        # ----------------------------------------------------

        time.sleep(2)

        # ----------------------------------------------------
        # Click Post
        # ----------------------------------------------------

        if not self.click_post_button():

            print(
                "❌ Post was NOT submitted."
            )

            return

        # ----------------------------------------------------
        # ONLY NOW open Recent Activity.
        # ----------------------------------------------------

        self.show_recent_activity()

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        if not self.driver:
            return

        print(
            "\n🔍 Chrome is being kept open for inspection."
        )

        try:

            input(
                "👉 Press ENTER in VS Code when you want "
                "to close Chrome..."
            )

        except KeyboardInterrupt:

            pass

        try:

            self.driver.quit()

        except Exception:
            pass

        print(
            "🏁 Session finished."
        )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    bot = SpeedLinkedInBot()

    try:

        if bot.get_internet_speed():

            bot.post_to_linkedin()

    except Exception as e:

        print(
            f"\n❌ Unexpected error: {e}"
        )

    finally:

        bot.close()
