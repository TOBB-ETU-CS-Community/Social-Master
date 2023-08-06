import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import streamlit as st
from webdriver_manager.chrome import ChromeDriverManager
from modules.utils import add_bg_from_local, set_page_config

DELAY_TIME = 5


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://www.instagram.com/")

    def go_to_login_page(self):
        try:
            time.sleep(DELAY_TIME)
            self.driver.find_element(By.XPATH, "//a[text()='Log in']").click()
        except:
            pass
        return LoginPage(self.driver)


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        time.sleep(DELAY_TIME)
        username_input = self.driver.find_element(
            By.CSS_SELECTOR, "input[name='username']"
        )
        password_input = self.driver.find_element(
            By.CSS_SELECTOR, "input[name='password']"
        )
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.driver.execute_script("arguments[0].click();", login_button)

    def close_popups(self):
        time.sleep(DELAY_TIME)
        try:
            not_now_button = self.driver.find_element(
                By.XPATH, '//button[text()="Not Now"]'
            )  # close notifications pop-up
            not_now_button.click()
            time.sleep(DELAY_TIME)
            not_now_button = self.driver.find_element(
                By.XPATH, '//button[text()="Not Now"]'
            )  # close save login info pop-up
            not_now_button.click()
        except:
            pass

    def go_to_profile_page(self, username):
        return ProfilePage(self.driver, username)


class ProfilePage:
    def __init__(self, driver, username):
        time.sleep(DELAY_TIME)
        self.driver = driver
        self.username = username
        self.driver.get(f"https://www.instagram.com/{username}")

    def go_to_followers_window(self):
        time.sleep(DELAY_TIME)
        followers_button = self.driver.find_element(
            By.CSS_SELECTOR, f"a[href='/{self.username}/followers/']"
        )
        followers_button.click()
        return self.driver

    def follow_followers(self, max_count=100):
        time.sleep(DELAY_TIME)
        followers_dialog = self.driver.find_element(By.XPATH, "//div[@class='_aano']")
        visible_followers = len(self.driver.find_elements(By.TAG_NAME, "li"))
        for _ in range(max_count // visible_followers + 1):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                followers_dialog,
            )
            time.sleep(1)
        print("Scroll down finished")
        follow_buttons = self.driver.find_elements(By.XPATH, "//*[text()='Follow']")
        print(f"{len(follow_buttons)} profile will be followed")
        for follow_button in follow_buttons:
            self.driver.execute_script("arguments[0].click();", follow_button)
            time.sleep(1)
        print(f"{len(follow_buttons)} profile were followed")


def get_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--headless")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


def main():
    set_page_config()

    background_img_path = os.path.join("static", "background", "main-bg.png")
    sidebar_background_img_path = os.path.join("static", "background", "side-bg.png")
    page_markdown = add_bg_from_local(
        background_img_path=background_img_path,
        sidebar_background_img_path=sidebar_background_img_path,
    )
    st.markdown(page_markdown, unsafe_allow_html=True)

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 60px;'> 🤖 INSTA BOT </h1>
        <br>""",
        unsafe_allow_html=True,
    )

    username = st.text_input("Please enter your username:")
    password = st.text_input("Please enter your password:", type="password")
    influencer_username = st.text_input(
        "Please enter the username whose followers you want to follow:"
    )
    if st.button("Login"):
        try:
            container = st.empty()
            driver = get_driver()
            home_page = HomePage(driver)
            with container:
                st.success("Instagram home page opened")
            login_page = home_page.go_to_login_page()
            login_page.login(username, password)
            login_page.close_popups()
            with container:
                st.success("Instagram login successful")
            profile_page = login_page.go_to_profile_page(influencer_username)
            profile_page.go_to_followers_window()
            with container:
                st.success("Followers dialog opened")
            profile_page.follow_followers(max_count=100)
            with container:
                st.success("100 followers followed")
        except Exception as e:
            with container:
                st.error("An error occured. Please try again.")
                st.error(e)
        finally:
            driver.quit()


if __name__ == "__main__":
    main()
