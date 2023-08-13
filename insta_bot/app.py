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
from selenium.webdriver.support import expected_conditions as EC


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


class HomePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def go_to_login_page(self):
        try:
            self.driver.get("https://www.instagram.com/")
            goto_login_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[text()='Log in']"))
            )
            self.driver.execute_script("arguments[0].click();", goto_login_button)
        except:
            pass
        return LoginPage(self.driver, self.wait)


class LoginPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def login(self, username, password):
        username_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='username']")
            )
        )
        password_input = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='password']")
            )
        )
        username_input.clear()
        password_input.clear()
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))
        )
        self.driver.execute_script("arguments[0].click();", login_button)

    def go_to_profile_page(self):
        return ProfilePage(self.driver, self.wait)

    def go_to_explore_page(self):
        return ExplorePage(self.driver, self.wait)


class ExplorePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def like_tags(self, hashtags, like_count=5):
        for hashtag in hashtags:
            self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
            get_random_delay()
            posts = self.wait.until(
                EC.visibility_of_any_elements_located(
                    (By.XPATH, "//div[@class='_aagu']")
                )
            )
            for i in range(len(posts)):
                post = posts[i]
                self.driver.execute_script("arguments[0].click();", post)
                get_random_delay()
                buttons = self.wait.until(
                    EC.visibility_of_any_elements_located(
                        (
                            By.XPATH,
                            "//div[@class='x6s0dn4 x78zum5 xdt5ytf xl56j7k']",
                        )
                    )
                )
                like_button = buttons[2]
                self.driver.execute_script("arguments[0].click();", like_button)
                get_random_delay()


class ProfilePage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def go_to_followers_window(self, username):
        get_random_delay()
        self.driver.get(f"https://www.instagram.com/{username}/followers/")

    def go_to_following_window(self, username):
        get_random_delay()
        self.driver.get(f"https://www.instagram.com/{username}/following/")

    def unfollow_following(self, max_count=100):
        get_random_delay()
        dialog_window = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='_aano']"))
        )
        for _ in range(max_count // 5 + 1):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                dialog_window,
            )
        unfollow_buttons = self.wait.until(
            EC.visibility_of_any_elements_located((By.XPATH, "//*[text()='Following']"))
        )
        for i in range(1, len(unfollow_buttons)):
            unfollow_button1 = unfollow_buttons[i]
            self.driver.execute_script("arguments[0].click();", unfollow_button1)
            get_random_delay()
            unfollow_button2 = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='Unfollow']"))
            )
            self.driver.execute_script("arguments[0].click();", unfollow_button2)
            get_random_delay()
        close_button = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='_abl-']"))
        )
        self.driver.execute_script("arguments[0].click();", close_button)
        return len(unfollow_buttons) - 1

    def follow_followers(self, max_count=100):
        get_random_delay()
        dialog_window = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='_aano']"))
        )
        for _ in range(max_count // 5 + 1):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                dialog_window,
            )
        follow_buttons = self.wait.until(
            EC.visibility_of_any_elements_located((By.XPATH, "//*[text()='Follow']"))
        )
        for i in range(1, len(follow_buttons)):
            follow_button = follow_buttons[i]
            self.driver.execute_script("arguments[0].click();", follow_button)
            get_random_delay()
        close_button = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='_abl-']"))
        )
        self.driver.execute_script("arguments[0].click();", close_button)
        return len(follow_buttons) - 1


def get_driver(headless, incognito, ignore):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=720x720")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    if headless:
        options.add_argument("--headless")
    if ignore:
        options.add_argument("--ignore-certificate-errors")
    if incognito:
        options.add_argument("--incognito")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.implicitly_wait(10)
    return driver


def login_button_callback():
    st.session_state.login_button_clicked = True


def start_automation(headless, incognito, ignore):
    try:
        driver = get_driver(headless, incognito, ignore)
        st.session_state.driver = driver
        wait = WebDriverWait(driver, 10)
        home_page = HomePage(driver, wait)
        st.session_state.home_page = home_page
        login_page = home_page.go_to_login_page()
        st.session_state.login_page = login_page
        login_page.login(st.session_state.username.lower(), st.session_state.password)
        st.session_state.login = True
    except Exception as e:
        print(e)
        st.session_state.login = False
    finally:
        return st.session_state.login


def get_random_delay(delays: list[float] = [1, 1.5, 2, 2.5, 3]):
    delay = random.choice(delays)
    time.sleep(delay)


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

    with st.sidebar:
        st.text_input("Please enter your username:", key="username")
        st.text_input("Please enter your password:", type="password", key="password")
        # headless, incognito, ignore = [False] * 3
        with st.expander("Extra Configurations for the Bot"):
            headless = st.checkbox("Headless")
            incognito = st.checkbox("Incognito")
            ignore = st.checkbox("Ignore certificate errors")
        button = st.button("Login Account", on_click=login_button_callback)
        if button:
            login_status = start_automation(headless, incognito, ignore)
            placeholder = st.sidebar.empty()
            if login_status:
                with placeholder.container():
                    st.success("Instagram login successful")
            else:
                with placeholder.container():
                    st.error("An error occured. Please try again to login.")
    if st.session_state.login:
        try:
            get_random_delay()
            _, center_col, _ = st.columns([1, 3, 1])
            operation = center_col.selectbox(
                "Please select the operation you want",
                ["<Select>", "Follow", "Like", "Unfollow"],
            )
            if operation == "Follow":
                center_col.text_input(
                    "Please enter the username whose followers you want to follow:",
                    key="influencer_username",
                )
            elif operation == "Like":
                center_col.text_input(
                    "Please write the hashtags that you want to like, separated by space:",
                    key="hashtags",
                )
            _, center_col, _ = st.columns([4, 5, 2])
            start = center_col.button("Start the automation")
            placeholder = st.empty()
            if start and operation == "Follow":
                login_page = st.session_state.login_page
                profile_page = login_page.go_to_profile_page()
                profile_page.go_to_followers_window(
                    st.session_state.influencer_username
                )
                with placeholder.container():
                    st.success("Followers dialog opened")
                followed_number = profile_page.follow_followers(max_count=100)
                with placeholder.container():
                    st.success(f"{followed_number} followers followed")
            elif start and operation == "Like":
                login_page = st.session_state.login_page
                explore_page = login_page.go_to_explore_page()
                hashtags = st.session_state.hashtags.split(" ")
                explore_page.like_tags(hashtags)
            elif start and operation == "Unfollow":
                login_page = st.session_state.login_page
                profile_page = login_page.go_to_profile_page()
                profile_page.go_to_following_window(st.session_state.username.lower())
                with placeholder.container():
                    st.success("Following dialog opened")
                unfollowed_number = profile_page.unfollow_following(max_count=100)
                with placeholder.container():
                    st.success(f"{unfollowed_number} followings unfollowed")
        except Exception as e:
            with placeholder.container():
                st.error("An exception occured. Please try again.")
                st.error(e)
                st.session_state.driver.get_screenshot_as_file("exception.png")
    else:
        st.warning("Please login first.")


if __name__ == "__main__":
    main()
