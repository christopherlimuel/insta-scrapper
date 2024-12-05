import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from utils import login_instagram, load_cookies
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

st.title(":red[Ins]:orange[tag]:violet[ram] Comment Scraper")

if st.session_state['logged_in']:
    #====== HOME PAGE ======#
    st.success("Anda sudah login. Siap untuk scraping komentar")

    col1, col2 = st.columns(2)
    tile1 = col1.container(height=200)
    tile2 = col2.container(height=200)
    tile1.page_link("Singlepost.py", label="**Single Post**", use_container_width=True, icon=":material/draft:")
    tile1.markdown("Mengambil komentar dari 1 post")
    tile2.page_link("Multipost.py", label="**Multiple Post**", use_container_width=True, icon=":material/file_copy:")
    tile2.markdown("Mengambil komentar dari semua post dalam 1 akun")
else:
    #====== LOGIN PAGE ======#
    st.warning("Anda belum login. Silahkan login untuk pertama kali.")
    st.markdown("Anda perlu login ke akun instagram yang digunakan untuk mengakses unggahan Instagram.")
    st.caption("Username dan password hanya akan disimpan secara lokal.")

    username = st.text_input("Masukkan username Instagram")
    password = st.text_input("Masukkan password Instagram", type="password")

    if st.button("Login"):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        login_success = login_instagram(driver, username, password)

        if login_success:
            st.session_state['logged_in'] = True
            st.success("Login berhasil!")
            time.sleep(1)
            streamlit_js_eval(js_expressions="parent.window.location.reload()")
        else:
            st.error("Login gagal. Pastikan username dan password Anda benar!")