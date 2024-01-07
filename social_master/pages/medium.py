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


def get_random_delay(delay_range: list[float] = [1, 5]):
    delay = random.uniform(*delay_range)
    time.sleep(delay)


def show_screenshot(driver: st.session_state.driver or None):
    driver.get_screenshot_as_file("exception.png")
    image = Image.open("exception.png")
    st.image(image)


# --- Find the path of a folder using part of a directory ---
def find_path(name: str, path: str) -> str:
    for root, dirs, files in os.walk(path):
        for d in dirs:
            dir = os.path.join(root, d)
            nameparts = []
            nameparts.append(os.path.join(path, name).split("\\")[-1])
            for p in os.path.join(path, name).split("\\")[:-1]:
                if p not in dir.split("\\"):
                    nameparts.append(p)
            nm = "\\".join(nameparts)
            if os.path.join(root, nm) == dir:
                return os.path.join(root, nm)
    return "None"


# --- Find Chrome User Data, search it through C and D drives. Works for Windows ---
def find_chrome_user_data() -> str:
    drives = ["C:\\", "D:\\"]
    for drive in range(len(drives)):
        USER_DATA_PATH = find_path("Google\\Chrome\\User Data", drives[drive])
        if USER_DATA_PATH != "None":
            print("Found Chrome User Data Path: " + USER_DATA_PATH)
            return USER_DATA_PATH
    return "None"


def get_driver(headful: bool = True):
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
    USER_DATA_PATH = (
        "C:\\Users\\NEO\\AppData\\Local\\Google\\Chrome\\User Data"
    )
    options.add_argument(f"--user-data-dir={USER_DATA_PATH}")

    service = Service(executable_path=binary_path)

    driver = webdriver.Chrome(
        service=service,
        options=options,
    )
    driver.implicitly_wait(5)
    return driver


def find_articles_and_clap(medium_page_url: str, last_n_articles=-1) -> None:
    driver = get_driver()
    driver.get(medium_page_url)  # Go to the medium profile page
    """
    while True:
        print("Article number: ", (a + 1))
        search: list = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
        )  # Wait and get the list of articles
        href = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a"))
        )  # Wait until the articles are clickable
        href = search[a].find_element(
            by=By.CSS_SELECTOR, value="a"
        )  # Get the next article to be clicked
        href.click()  # click the article
        clap_button = WebDriverWait(driver=driver, timeout=10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button[data-testid='headerClapButton']")
            )
        )  # Wait for the page to load and get clapping button
        for _ in range(50):
            clap_button.click()  # click the clapping button 50 times
        time.sleep(1)
        driver.back()  # go back
        a += 1
        if last_n_articles == -1 and len(search) == a:  # If all articles are clapped
            break
        if a == last_n_articles:
            break
    """
    driver.quit()


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
        st.text_input(
            "Please enter your passcode sent to your email:", key="passcode"
        )
        with st.expander("Extra Configurations"):
            st.checkbox("Headful")
        button = st.button("Login Account")
        if button:
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

    if st.button("clap"):
        find_articles_and_clap(
            medium_page_url="https://medium.com/@aifastcash",
            last_n_articles=10,
        )


if __name__ == "__main__":
    main()
