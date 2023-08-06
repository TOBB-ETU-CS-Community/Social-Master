import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import streamlit as st

username = st.text_input("Please enter your username: ")
password = st.text_input("Please enter your password: ", type="password")
if st.checkbox("Are you using 2-Factor Authentication on your Instagram account?"):
    security_code = st.text_input(
        "Please enter one of your backup codes: ", type="password"
    )

if st.button("Login"):
    pass
