import os
import random
import time

import streamlit as st
from chromedriver_py import binary_path
from modules.utils import add_bg_from_local, set_page_config
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from st_pages import Page, show_pages

if "login" not in st.session_state:
    st.session_state.login = False
if "login_button_clicked" not in st.session_state:
    st.session_state.login_button_clicked = False
if "driver" not in st.session_state:
    st.session_state.driver = None
if "home_page" not in st.session_state:
    st.session_state.home_page = None
if "login_page" not in st.session_state:
    st.session_state.login_page = None
if "profile_page" not in st.session_state:
    st.session_state.profile_page = None
if "mail_auth" not in st.session_state:
    st.session_state.mail_auth = False


class HomePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def go_to_login_page(self):
        try:
            self.driver.get("https://medium.com/m/signin")
            goto_email_login_button = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[text()='Sign in with email']",
                    )
                )
            )
            self.driver.execute_script(
                "arguments[0].click();", goto_email_login_button
            )
        except Exception as e:
            print(e)
        return LoginPage(self.driver, self.wait)


class LoginPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def email_login(self, email):
        try:
            email_input = self.wait.until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "input[aria-label='email']")
                )
            )
            email_input.clear()
            email_input.send_keys(email)
            continue_button = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//button[text()='Continue']")
                )
            )
            self.driver.execute_script(
                "arguments[0].click();", continue_button
            )
            return True
        except Exception as e:
            print(e)
            return False

    def sign_in(self, link):
        try:
            self.driver.get(link)
            return True
        except Exception as e:
            print(e)
            return False

    def check_login(self):
        get_random_delay([5, 10])
        try:
            login_button = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//button[@type='submit']/div[text()='Log in']")
                )
            )
            self.driver.execute_script("arguments[0].click();", login_button)
            return False
        except Exception as e:
            print(e)
            return True


def get_random_delay(delay_range: list[float] = [1, 5]):
    delay = random.uniform(*delay_range)
    time.sleep(delay)


def show_screenshot(driver: st.session_state.driver or None):
    driver.get_screenshot_as_file("exception.png")
    image = Image.open("exception.png")
    st.image(image)


def get_driver(headful):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=720x720")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    if not headful:
        options.add_argument("--headless")

    service = Service(executable_path=binary_path)

    driver = webdriver.Chrome(
        service=service,
        options=options,
    )
    driver.implicitly_wait(5)
    return driver


def start_automation(headful):
    error = None
    login = False
    try:
        driver = get_driver(headful)
        st.session_state.driver = driver
        wait = WebDriverWait(driver, 5)
        home_page = HomePage(driver, wait)
        st.session_state.home_page = home_page
        login_page = home_page.go_to_login_page()
        st.session_state.login_page = login_page
        if login_page.email_login(st.session_state.email.lower()):
            st.session_state.mail_auth = True
        # login = login_page.check_login()
    except Exception as e:
        print(e)
        error = e

    finally:
        return [login, error]


def main():
    set_page_config()

    background_img_path = os.path.join("static", "background", "main-bg.png")
    sidebar_background_img_path = os.path.join(
        "static", "background", "side-bg.png"
    )
    page_markdown = add_bg_from_local(
        background_img_path=background_img_path,
        sidebar_background_img_path=sidebar_background_img_path,
    )
    st.markdown(page_markdown, unsafe_allow_html=True)

    show_pages(
        [
            Page("social_master/app.py", "Social Media Manager", "📱"),
            Page("social_master/pages/instagram.py", "Instagram Manager", "📸"),
            Page("social_master/pages/medium.py", "Medium Manager", "📰"),
        ]
    )

    st.markdown(
        """<h1 style='text-align: center; color: black; font-size: 60px;'> Medium Manager 📰 </h1>
        <br>""",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.text_input("Please enter your email:", key="email")
        if st.session_state.mail_auth:
            st.text_input(
                "Please paste your sign in link sent to your email:",
                key="signin_link",
            )
        with st.expander("Extra Configurations"):
            st.checkbox("Headful")
        if not st.session_state.mail_auth:
            button = st.button("Send Sign in Link to Email")
            if button:
                st.session_state.login, error = start_automation(headful=True)
                if error:
                    st.error(error)
                placeholder = st.sidebar.empty()
        else:
            button = st.button("Sign in using Email Link")
            if button:
                st.session_state.login = st.session_state.login_page.sign_in(
                    st.session_state.signin_link
                )

            placeholder = st.sidebar.empty()

            if st.session_state.login:
                with placeholder.container():
                    st.success("Medium login successful")
            else:
                with placeholder.container():
                    st.error("An error occured. Please try again to login.")
    if st.session_state.login:
        try:
            get_random_delay()
            _, center_col, _ = st.columns([1, 3, 1])
            operation = center_col.selectbox(
                "Please select the operation you want",
                ["<Select>", "Clap & Comment"],
            )
            if operation == "Clap & Comment":
                center_col.text_input(
                    "Please write the accounts which you want to clap and comment its stories, separated by space:",
                    key="accounts",
                )
                center_col.number_input(
                    "Please enter the number of stories you want to clap and comment:",
                    min_value=10,
                    max_value=200,
                    value=50,
                    step=10,
                    key="number_of_stories",
                )
            _, center_col, _ = st.columns([4, 5, 2])
            start = center_col.button("Start the automation")
            placeholder = st.empty()
            if start and operation == "Clap & Comment":
                pass
        except Exception as e:
            with placeholder.container():
                st.error("An exception occured. Please try again.")
                st.error(e)
                show_screenshot()
    else:
        st.warning(body="Please login first.", icon="⚠️")


if __name__ == "__main__":
    main()
