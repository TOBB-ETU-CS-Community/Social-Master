import base64

import streamlit as st

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import SessionNotCreatedException

from webdriver_manager.chrome import ChromeDriverManager

import time
import os


@st.cache_data
def add_bg_from_local(background_img_path, sidebar_background_img_path):
    with open(background_img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    with open(sidebar_background_img_path, "rb") as image_file:
        sidebar_encoded_string = base64.b64encode(image_file.read())

    return f"""<style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
        }}

        section[data-testid="stSidebar"] {{
            background-image: url(data:image/png;base64,{sidebar_encoded_string.decode()});
            background-size: cover;
        }}
        div[class="stChatFloatingInputContainer css-90vs21 ehod42b2"]
            {{
                background: url(data:image/png;base64,{encoded_string.decode()});
                background-size: cover;
                z-index: 1;
            }}
    </style>"""


def set_page_config():
    st.set_page_config(
        page_title="INSTA BOT",
        page_icon="🤖",
        # layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/olympian-21",
            "Report a bug": "https://github.com/olympian-21",
            "About": """
            Welcome to the Instagram Bot, a tool designed to automate various social media management tasks on Instagram.
             This bot is developed to assist social media managers, influencers, and businesses in efficiently handling their
              Instagram accounts.
            """,
        },
    )


def local_css(file_name):
    # with open(file_name) as f:
    #    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    style = """<style>
        .row-widget.stButton {
            text-align: center;
            position: fixed;
            bottom: 0;
            z-index: 2;
            }
    </style>"""
    st.markdown(style, unsafe_allow_html=True)


# --- Find the path of a folder using part of a directory ---
def find_path(name: str, path: str) -> str:
    for root , dirs, files in os.walk(path):
        for d in dirs:
            dir = os.path.join(root,d)
            nameparts = []
            nameparts.append(os.path.join(path,name).split("\\")[-1])
            for p in os.path.join(path,name).split("\\")[:-1]:
                if p not in dir.split("\\"):
                    nameparts.append(p)
            nm = "\\".join(nameparts)
            if(os.path.join(root,nm) == dir):
                return os.path.join(root,nm)
    return "None"

# --- Find Chrome User Data, search it through C and D drives. Works for Windows ---
def find_chrome_user_data() -> str:
    drives = ["C:\\","D:\\"]
    for drive in range(len(drives)):
        USER_DATA_PATH = find_path("Google\\Chrome\\User Data",drives[drive])
        if USER_DATA_PATH != "None":
            print("Found Chrome User Data Path: "+USER_DATA_PATH)
            return USER_DATA_PATH
    return "None"

# --- Setup Chrome Driver ---
def setup_chrome_driver() -> webdriver.Chrome:
    USER_DATA_PATH : str = find_chrome_user_data()
    assert USER_DATA_PATH != "None", "Google Chrome User Data not found"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument(f"--user-data-dir={USER_DATA_PATH}") #e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    return driver

# --- Main Function for finding and clapping articles ---
def find_articles_and_clap(medium_page_url: str, last_n_articles=-1) -> None:
    try:
        driver = setup_chrome_driver()
    except SessionNotCreatedException as error:
        print("This program works when all current chrome sessions/pages are closed, you have open chrome sessions, please run the program again after closing them.")
        return
    driver.get(medium_page_url) # Go to the medium profile page
    a = 0
    while True:
        print("Article number: ",(a+1))
        search : list = WebDriverWait(driver=driver, timeout=10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR,"article"))
        ) # Wait and get the list of articles
        href = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"a"))
        ) # Wait until the articles are clickable
        href = search[a].find_element(by=By.CSS_SELECTOR, value = "a") # Get the next article to be clicked
        href.click() # click the article
        clap_button = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-testid='headerClapButton']"))) # Wait for the page to load and get clapping button
        for _ in range(50):
            clap_button.click() # click the clapping button 50 times
        time.sleep(1)
        driver.back() # go back
        a+=1 
        if last_n_articles == -1 and len(search)==a: # If all articles are clapped
            break
        if a == last_n_articles:
            break

    time.sleep(1)
    driver.quit()
