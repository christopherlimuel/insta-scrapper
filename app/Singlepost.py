import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from utils import *

# Redirect to home page if not logged in
if 'logged_in' not in st.session_state:
    st.switch_page("Home.py")
else:
    if st.session_state['logged_in'] == False:
        st.switch_page("Home.py")

st.title(":red[Ins]:orange[tag]:violet[ram] Comment Scraper")

post_url = st.text_input("Masukkan URL Post Instagram", placeholder="https://www.instagram.com/p/ABCDEFGHIJK/")
file_format = st.selectbox("Pilih format file:", ['.xlsx', '.csv'])

# Scraping button
if st.button("Scrape komentar", icon=":material/frame_inspect:"):
    # Checking URL validity
    valid_url = False
    if len(post_url) == 40:
        if post_url[0:28] == 'https://www.instagram.com/p/' and post_url[-1] == '/':
            valid_url = True
    elif len(post_url) == 32:
        if post_url[0:20] == 'www.instagram.com/p/' and post_url[-1] == '/':
            valid_url = True

    if valid_url == True:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        load_cookies(driver)
        SHORTCODE = post_url.split('/')[-2]
        status = st.empty()
        status.markdown("Sedang memuat komentar, mohon tunggu...")
        comment_data = scrape_comments(driver, post_url)
        status.markdown(f'{len(comment_data)} komentar berhasil diambil!')

        # Download file
        file_path = save_to_file(comment_data, file_format, SHORTCODE)
        st.download_button(f"Download {SHORTCODE}{file_format}", data = open(file_path, "rb"), file_name=file_path, icon=":material/file_save:")
        st.success(f'Data disimpan sebagai {SHORTCODE}{file_format}')
        st.table(pd.DataFrame(comment_data))
    else:
        st.error("URL Post Instagram tidak valid.")