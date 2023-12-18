import os

import streamlit as st
from modules.utils import add_bg_from_local, set_page_config
from st_pages import Page, show_pages


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
        """<h1 style='text-align: center; color: black; font-size: 60px;'> Social Media Manager 📱 </h1>
        <br>""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
