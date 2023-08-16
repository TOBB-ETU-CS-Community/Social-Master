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
from PIL import Image

# from webdriver_manager.chrome import ChromeDriverManager
from modules.utils import add_bg_from_local, set_page_config
from selenium.webdriver.support import expected_conditions as EC
from chromedriver_py import binary_path


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

    def like_and_comment_tags(self, hashtags, like_count=5):
        comments = [
            "Great 🤩",
            "Amazing 😍",
            "Love it ❤️",
            "Looks nice 👌",
            "WoW 🤯",
            "Unbelievable 🙀",
            "Impressive 👏" "Fantastic 🌟",
            "Incredible 🚀",
            "Mind-blowing 🤯",
            "Brilliant 💡",
            "Astonishing 🌈",
            "Exceptional 💪",
            "Outstanding 🏆",
        ]
        for hashtag in hashtags:
            try:
                self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
                get_random_delay()
                posts = self.wait.until(
                    EC.visibility_of_any_elements_located(
                        (By.XPATH, "//div[@class='_aagu']")
                    )
                )
                placeholder = st.empty()
                for i in range(len(posts)):
                    try:
                        get_random_delay()
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
                        with placeholder.container():
                            st.success(f"{i+1} posts liked for {hashtag} hashtag")
                        print("like finished")
                        comment_button = buttons[3]
                        self.driver.execute_script(
                            "arguments[0].click();", comment_button
                        )
                        print("comment button clicked")
                        get_random_delay()
                        textarea = self.wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//div[@class='_akhn']//textarea")
                            )
                        )
                        self.driver.execute_script("arguments[0].click();", textarea)
                        print("comment textarea clicked")
                        get_random_delay()
                        print("render emojis")
                        self.driver.execute_script(
                            "arguments[0].innerHTML = '{}'".format(
                                random.choice(comments)
                            ),
                            textarea,
                        )
                        print("send keys")
                        textarea.send_keys(" ")
                        textarea.send_keys(Keys.ENTER)
                        print("comment finished")
                        get_random_delay()
                    except:
                        with placeholder.container():
                            st.error(f"This post cannot be commented on")
                        continue
                with placeholder.container():
                    st.success(f"{i+1} posts liked for {hashtag} hashtag in total")
            except:
                st.error(f"There is no explore page for hashtag: {hashtag}")


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

    def unfollow_following(self, count=50):
        try:
            st.write("method")
            st.session_state.driver.get_screenshot_as_file("exception.png")
            image = Image.open("exception.png")
            st.image(image)
            get_random_delay()
            st.write("after delay")
            st.session_state.driver.get_screenshot_as_file("exception.png")
            image = Image.open("exception.png")
            st.image(image)
            dialog_window = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='_aano']"))
            )
            st.write("dialog clicked")
            for _ in range(count // 4 + 1):
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                    dialog_window,
                )
            st.write("dialog scrolled")
            get_random_delay()
            unfollow_buttons = self.wait.until(
                EC.visibility_of_any_elements_located(
                    (By.XPATH, "//button[@class='_acan _acap _acat _aj1-']")
                )
            )
            st.write("buttons selected")
            placeholder = st.empty()
            for i in range(len(unfollow_buttons)):
                try:
                    unfollow_button1 = unfollow_buttons[i]
                    self.driver.execute_script(
                        "arguments[0].click();", unfollow_button1
                    )
                    st.write("unfollow 1")
                    get_random_delay()
                    unfollow_button2 = self.wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//*[text()='Unfollow']")
                        )
                    )
                    self.driver.execute_script(
                        "arguments[0].click();", unfollow_button2
                    )
                    st.write("unfollow 2")
                    with placeholder.container():
                        st.success(f"{i+1} profile unfollowed")
                    get_random_delay()
                    if i == count:
                        break
                except Exception as e:
                    print(e)
                    continue
            with placeholder.container():
                st.success(f"{i+1} profile unfollowed in total")
            close_button = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//button[@class='_abl-']"))
            )
            self.driver.execute_script("arguments[0].click();", close_button)
            return i + 1
        except Exception as e:
            st.write(e)
            st.session_state.driver.get_screenshot_as_file("exception.png")

    def follow_followers(self, count=50):
        get_random_delay()
        dialog_window = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='_aano']"))
        )
        for _ in range(count // 5 + 1):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;",
                dialog_window,
            )
        get_random_delay()
        follow_buttons = self.wait.until(
            EC.visibility_of_any_elements_located(
                (By.XPATH, "//button[@class='_acan _acap _acas _aj1-']")
            )
        )
        placeholder = st.empty()
        for i in range(1, len(follow_buttons)):
            try:
                follow_button = follow_buttons[i]
                self.driver.execute_script("arguments[0].click();", follow_button)
                with placeholder.container():
                    st.success(f"{i} profile followed")
                get_random_delay()
                if i == count:
                    break
            except Exception as e:
                print(e)
                continue
        with placeholder.container():
            st.success(f"{i} profile followed in total")
        close_button = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//button[@class='_abl-']"))
        )
        self.driver.execute_script("arguments[0].click();", close_button)
        return i


def get_driver(headful, incognito, ignore):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=720x720")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    if not headful:
        options.add_argument("--headless")
    if ignore:
        options.add_argument("--ignore-certificate-errors")
    if incognito:
        options.add_argument("--incognito")

    service = Service(executable_path=binary_path)

    driver = webdriver.Chrome(
        service=service,
        options=options,
        # service=Service(ChromeDriverManager().install()), options=options
    )
    driver.implicitly_wait(10)
    return driver


def login_button_callback():
    st.session_state.login_button_clicked = True


def start_automation(headful, incognito, ignore):
    error = None
    try:
        driver = get_driver(headful, incognito, ignore)
        st.session_state.driver = driver
        wait = WebDriverWait(driver, 20)
        home_page = HomePage(driver, wait)
        st.session_state.home_page = home_page
        login_page = home_page.go_to_login_page()
        st.session_state.login_page = login_page
        login_page.login(st.session_state.username.lower(), st.session_state.password)
        st.session_state.login = True
    except Exception as e:
        print(e)
        error = e
        st.session_state.login = False
    finally:
        return [st.session_state.login, error]


def get_random_delay(
    delays: list[float] = [
        0.5,
        0.75,
        1,
        1.25,
        1.5,
        1.75,
        2,
    ]
):
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
        with st.expander("Extra Configurations for the Bot"):
            headful = st.checkbox("Headful")
            incognito = st.checkbox("Incognito")
            ignore = st.checkbox("Ignore certificate errors")
        button = st.button("Login Account", on_click=login_button_callback)
        if button:
            login_status, error = start_automation(headful, incognito, ignore)
            get_random_delay()
            placeholder = st.sidebar.empty()
            if login_status:
                with placeholder.container():
                    st.success("Instagram login successful")
                st.session_state.driver.get_screenshot_as_file("exception.png")
                image = Image.open("exception.png")
                st.image(image)
            else:
                with placeholder.container():
                    st.error("An error occured. Please try again to login.")
                    st.error(error)
    if st.session_state.login:
        try:
            get_random_delay()
            _, center_col, _ = st.columns([1, 3, 1])
            operation = center_col.selectbox(
                "Please select the operation you want",
                ["<Select>", "Follow", "Like & Comment", "Unfollow"],
            )
            if operation == "Follow":
                center_col.text_input(
                    "Please enter the username whose followers you want to follow:",
                    key="influencer_username",
                )
                center_col.number_input(
                    "Please enter the number of followers you want to follow:",
                    min_value=10,
                    max_value=200,
                    value=50,
                    step=10,
                    key="number_of_follow",
                )
            elif operation == "Like & Comment":
                center_col.text_input(
                    "Please write the hashtags that you want to like and comment, separated by space:",
                    key="hashtags",
                )
            elif operation == "Unfollow":
                center_col.number_input(
                    "Please enter the number of following you want to unfollow:",
                    min_value=10,
                    max_value=200,
                    value=50,
                    step=10,
                    key="number_of_unfollow",
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
                followed_number = 0
                while followed_number < st.session_state.number_of_follow:
                    followed_number += profile_page.follow_followers(
                        count=st.session_state.number_of_follow
                    )
                with placeholder.container():
                    st.success("Following operation completed")
            elif start and operation == "Like & Comment":
                login_page = st.session_state.login_page
                explore_page = login_page.go_to_explore_page()
                hashtags = st.session_state.hashtags.split(" ")
                explore_page.like_and_comment_tags(hashtags)
            elif start and operation == "Unfollow":
                login_page = st.session_state.login_page
                profile_page = login_page.go_to_profile_page()
                profile_page.go_to_following_window(st.session_state.username.lower())
                with placeholder.container():
                    st.success("Following dialog opened")
                unfollowed_number = 0
                while unfollowed_number < st.session_state.number_of_unfollow:
                    unfollowed_number += profile_page.unfollow_following(
                        count=st.session_state.number_of_unfollow
                    )
                with placeholder.container():
                    st.success("Unfollowing operation completed")
        except Exception as e:
            with placeholder.container():
                st.error("An exception occured. Please try again.")
                st.error(e)
                st.session_state.driver.get_screenshot_as_file("exception.png")
    else:
        st.warning(body="Please login first.", icon="⚠️")


if __name__ == "__main__":
    main()
