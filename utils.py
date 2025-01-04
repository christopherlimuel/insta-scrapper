from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.core.os_manager import ChromeType
import time
import csv
import pickle
import streamlit as st
import pandas as pd
import os
import glob
from datetime import datetime
import json

try:
    with open("selectors.json", "r") as file:
        selectors = json.load(file)
except FileNotFoundError:
    st.error("File .json tidak ditemukan")
    st.stop()

# Inisialisasi driver
def get_driver():
    # options = Options()
    # options.add_argument("--disable-gpu")
    # options.add_argument("--headless")
    # return webdriver.Chrome(
    #     service=ChromeService(
    #         ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    #     ),
    #     options=options,
    # )
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(username)
    time.sleep(1)
    password_input.send_keys(password)
    time.sleep(1)
    password_input.submit()
    time.sleep(6)

    if driver.current_url == "https://www.instagram.com/accounts/login/":
        return False

    # Save cookies
    with open("cookies.pkl", 'wb') as file:
        pickle.dump(driver.get_cookies(), file)
    driver.quit()
    return True

def load_cookies(driver):
    driver.get('https://www.instagram.com')
    with open("cookies.pkl", "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()

def click_view_replies(driver):
    while True:
        try:
            view_replies_button = driver.find_elements(By.XPATH, "//span[contains(text(), 'View all')]")
            if len(view_replies_button) == 0:
                break

            for button in view_replies_button:
                try:
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(1)
                except Exception as e:
                    st.error(f"Error clicking view replies button: {e}")
        except Exception as e:
            st.error(f"Error finding view replies buttons: {e}")
            break

def scroll_to_buttom(driver):
    try:
        comment_container = driver.find_element(By.CSS_SELECTOR, selectors["comment_container"])
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comment_container)
    except NoSuchElementException as e:
        st.error(f'Kolom komentar tidak ditemukan (Pastikan URL sudah benar): {e}')
        # st.stop()

def scrape_comments(driver, post_url):
    driver.get(post_url)
    time.sleep(1)
        
    # Storing comments
    comment_data = []
    previous_comment_count = 0
    
    # Start scraping comments from post
    while True:
        scroll_to_buttom(driver)
        time.sleep(1)
        click_view_replies(driver)

        comment_elements = driver.find_elements(By.CSS_SELECTOR, "div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1cy8zhl.x1oa3qoh.x1nhvcw1 > span")
        username_elements = driver.find_elements(By.CSS_SELECTOR, 'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj > span > div > a > div > div > span._ap3a._aaco._aacw._aacx._aad7._aade')
        datetime_elements = driver.find_elements(By.CSS_SELECTOR, 'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj > a > time')

        # Take found comments
        for i in range(len(comment_elements)):
            comment_text = comment_elements[i].text
            username_text = username_elements[i].text
            datetime_html = datetime_elements[i].get_attribute("datetime")
            datetime_parsed = datetime.strptime(datetime_html, "%Y-%m-%dT%H:%M:%S.%fZ")
            datetime_text = datetime_parsed.strftime("%Y-%m-%d %H:%M:%S")
        
            # Only add data if not yet exists (prevent duplicate)
            keyvaluepair = {
                'Username':username_text, 
                'Comment':comment_text, 
                'Time Posted':datetime_text,
                'Post URL':post_url
                }
            if keyvaluepair not in comment_data:
                comment_data.append(keyvaluepair)
    
        # Counting comment
        current_comment_count = len(comment_data)
        if current_comment_count == previous_comment_count:
            break
        previous_comment_count = current_comment_count
    return comment_data

def scrape_posts(driver, account_url):
    driver.get(account_url)
    time.sleep(1)

    # Storing found post URLs
    post_data = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        
        post_elements = driver.find_elements(By.CSS_SELECTOR, "div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x1ntc13c.x9i3mqj.x11i5rnm.x2pgyrj > a")
        
        # Find post URLs
        for post in post_elements:
            post_text = post.get_attribute("href")
            if "reel" in post_text:
                post_text = post_text.replace("reel", 'p')
            account_name = post_text.split('/')[-4]
            post_text = post_text.replace(f"/{account_name}", "")
            if post_text not in post_data:
                post_data.append(post_text)

        # Scroll until reaches the buttom of account page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    return post_data

def save_to_file(data, file_format, file_name):
    df = pd.DataFrame(data)
    if file_format == '.csv':
        df.to_csv(f'{file_name}.csv', index=False)
        return f'{file_name}.csv'
    elif file_format == '.xlsx':
        df.to_excel(f'{file_name}.xlsx', index=False)
        return f'{file_name}.xlsx'