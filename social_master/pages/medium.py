import os

import streamlit as st
from chromedriver_py import binary_path
from modules.utils import add_bg_from_local, set_page_config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from st_pages import Page, show_pages


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
    if st.button("clap"):
        find_articles_and_clap(
            medium_page_url="https://medium.com/@aifastcash",
            last_n_articles=10,
        )


if __name__ == "__main__":
    main()
