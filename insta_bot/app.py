import streamlit as st
from instabot import Bot

st.write("hello")

username = st.text_input("Please enter your username: ")
password = st.text_input("Please enter your password: ", type="password")
if st.checkbox("Are you using 2-Factor Authentication on your Instagram account?"):
    security_code = st.text_input(
        "Please enter one of your backup codes: ", type="password"
    )

if st.button("Login"):
    bot = Bot()
    bot.login(username=username, password=password)
