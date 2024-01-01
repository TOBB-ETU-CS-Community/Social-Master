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

# --- Setup Chrome Driver ---
def setup_chrome_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    return driver

# --- Main Function for finding and clapping articles ---
def find_articles_and_clap(medium_page_url: str, last_n_articles=-1) -> None:
    
    driver = setup_chrome_driver()
    # --- Input medium account email ---
    signin_email = input("Enter your email: ")
    
    driver.get(medium_page_url) # Go to the medium profile page
    time.sleep(1)
    
    # --- Sign In Part ---
    signin_button = WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-testid='headerSignInButton']"))) # Get sign in button
    # signin_button = driver.find_element(By.CSS_SELECTOR,"a[data-testid='headerSignInButton']")
    driver.get(signin_button.get_property("href")) # Click sign in button href
    time.sleep(1)
    # This part down here is for getting Sign In with Email button, since there is no id or distinct class or etc. on it.
    buttons = WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button")))
    for b in buttons:
        try:
            if "email" in b.find_element(by=By.CSS_SELECTOR, value="div").text:
                b.click()
        except:
            pass

    # --- Entering Email for confirmation ---
    input_space = WebDriverWait(driver=driver, timeout=10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input"))) # Get input space for the email for sending confirmation mail
    input_space.send_keys(signin_email)
    time.sleep(0.02)
    input_space.send_keys(Keys.ENTER)

    confirmation_link = input("Enter the sign in to medium confirmation link that must have been sent to the email you provided: ") # Input confirmation link from the mail that has been sent to the email user provided
    driver.get(confirmation_link)

    a = 0
    while True:

        # --- Clicking Article Part ---
        print("Article number: ",(a+1))
        search : list = WebDriverWait(driver=driver, timeout=10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR,"article"))
        ) # Wait and get the list of articles
        href = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"a"))
        ) # Wait until the articles are clickable
        href = search[a].find_element(by=By.CSS_SELECTOR, value = "a") # Get the next article to be clicked
        href.click() # click the article
        
        # --- Clapping Part ---
        clap_button = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-testid='headerClapButton']"))) # Wait for the page to load and get clapping button
        for _ in range(50):
            clap_button.click() # click the clapping button 50 times
        time.sleep(1)

        # --- Commenting Part ---
        standard_comments = ["Great 🤩",
            "Amazing 😍",
            "Love it ❤️",
            "Looks nice 👌",
            "WoW 🤯",
            "Unbelievable 🙀",
            "Impressive 👏", 
            "Fantastic 🌟",
            "Incredible 🚀",
            "Mind-blowing 🤯",
            "Brilliant 💡",
            "Astonishing 🌈",
            "Exceptional 💪",
            "Outstanding 🏆",]

        comment_button = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='responses']"))) # Wait for the html to load and get comment button
        comment_button.click() # click the comment button

        comment_textbox_div = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[role='textbox']"))) # Wait for the html to load and get textBox div for writing comments
        
        # This part is for entering the comment into the textbox, since send_keys() function in selenium cannot send non-BMP unicode chars like emojis, I had to do something like copy and pasting it.
        chosen_comment = random.choice(standard_comments)
        pyperclip.copy(chosen_comment)
        act = ActionChains(driver)
        act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
        print("copy-paste comment: "+chosen_comment)

        time.sleep(0.05)
        try:
            respond_button = WebDriverWait(driver=driver, timeout=2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='ResponseRespondButton']"))) # Wait for the html to load and get respond button
        except:
            respond_button = WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-testid='ResponseRespondButton']"))) # Wait for the html to load and get respond button
        respond_button.click() # click respond button
        print("respond button clicked")
        time.sleep(0.2)
        driver.back() # go back
        a+=1 
        if last_n_articles == -1 and len(search)==a: # If all articles are clapped
            break
        if a == last_n_articles:
            break

    time.sleep(1)
    driver.quit()
