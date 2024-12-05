import streamlit as st
import os
import time
from streamlit_js_eval import streamlit_js_eval

# Initiate logged_in state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = os.path.exists("cookies.pkl")

# Place Logout button on sidebar if logged in
# Hide sidebar if not logged in
def set_sidebar(state):
    if state == True:
        sidebar_position = "sidebar"
        if st.sidebar.button("Logout", icon=":material/logout:"):
            os.remove("cookies.pkl")
            st.session_state['logged_in'] = False
            st.success("Logout berhasil. Silahkan login kembali.")
            time.sleep(1)
            streamlit_js_eval(js_expressions="parent.window.location.reload()")
    else:
        sidebar_position = "hidden"
    return sidebar_position

st.set_page_config(page_title="Instagram Comment Scraper", page_icon=":material/forum:")

pg = st.navigation([st.Page("Home.py", title="Home", icon=":material/home:"),
                    st.Page("Singlepost.py", title="Single Post", icon=":material/draft:"),
                    st.Page("Multipost.py", title = 'Multiple Post', icon=":material/file_copy:"),
                    st.Page("Test.py", title = 'Test & Repair', icon=":material/construction:")],
                    position=set_sidebar(st.session_state['logged_in']))

pg.run()