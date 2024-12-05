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

tab1, tab2 = st.tabs(["Scrape Unggahan", "Scrape Komentar"])

with tab1:
    st.subheader("Scrape Unggahan")
    with st.form("Post"):
        account_url = st.text_input("Masukkan URL Akun Instagram", placeholder="https://www.instagram.com/<username>")
        batch_size = st.number_input("Masukkan jumlah post per batch", min_value=1, step=10, value=100)

        if st.form_submit_button("Scrape unggahan", icon=":material/frame_inspect:"):
        # Checking URL validity
            valid_url = False
            if account_url[0:3] == 'htt':
                if account_url[0:26] == 'https://www.instagram.com/' and account_url[-1] == '/':
                    valid_url = True
            elif account_url[0:3] =='www':
                if account_url[0:18] == 'www.instagram.com/' and account_url[-1] == '/':
                    valid_url = True
            
            if valid_url == True:
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                load_cookies(driver)    
                SHORTCODE = account_url.split('/')[-2]
                status = st.empty()
                status.markdown("Sedang memuat unggahan, mohon tunggu...")
                post_data = scrape_posts(driver, account_url)
                status.markdown(f"{len(post_data)} unggahan ditemukan")

                # Simpan link unggahan dalam file csv (dalam batch @100 post)
                # batch_size = 100
                for i in range(0, len(post_data), batch_size):
                    df = pd.DataFrame(post_data[i:i+batch_size], columns=["Post URL"])
                    file_path = f'{SHORTCODE}_posts_{i//batch_size}.csv'
                    df.to_csv(file_path, index=False)
                st.success(f"Data tautan unggahan disimpan sebagai {SHORTCODE}_posts dalam {len(post_data)//batch_size + 1} batch")
            else:
                st.error("URL Akun Instagram tidak valid")

with tab2:
    st.subheader("Scrape Komentar")

    # Muat semua file csv berisi URL unggahan akun 
    csv_account = glob.glob("*_posts*")
    # csv_account = [os.path.basename(f).split("_")[0] for f in csv_files]

    with st.form("Comment"):
        files_in_directory = os.listdir(os.getcwd())
        account = None
        upload_account = None
        account_name = None

        if csv_account:
            selectbox_account = st.selectbox("Pilih file tautan unggahan untuk diambil komentarnya", csv_account)
            st.markdown(':grey[atau]')
        
        upload_account = st.file_uploader("Upload file CSV berisi tautan unggahan (opsional):", type=["csv"])

        file_format = st.selectbox("Pilih format file:", ['.xlsx', '.csv'])

        # Utamakan file yang diupload jika ada
        if upload_account is None:
            if csv_account:
                account = selectbox_account
                account_name = selectbox_account
        else:
            account = upload_account
            account_name = upload_account.name
        
        # Disable submit button jika belum memilih akun
        if account_name == None:
            st.warning("Pilih file CSV berisi tautan unggahan akun")
            submit_disable = True
        else:
            submit_disable = False        

        submitted = st.form_submit_button(f"Scrape komentar dari {account_name}", icon=":material/frame_inspect:", disabled=submit_disable)

        if submitted:
            if account is not None:
                # # Akses data dari file csv
                # if isinstance(account, str):
                #     df_posts = pd.read_csv(account)
                # elif account is not None:
                #     df_posts = pd.read_csv(account)
                df_posts = pd.read_csv(account)
                if 'Post URL' not in df_posts.columns:
                    st.error("File CSV harus memiliki kolom 'Post URL'")
                else:
                    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                    load_cookies(driver)
                    
                    post_data = df_posts['Post URL'].tolist()
                    all_comment_data = []
                    progress = st.empty()
                    for post_url in post_data:
                        progress.markdown(f"Memuat komentar unggahan {post_data.index(post_url)+1}/{len(post_data)}")
                        comment_data = scrape_comments(driver, post_url)
                        for comment in comment_data:
                            all_comment_data.append(comment)
                    progress.markdown(f'{len(all_comment_data)} komentar berhasil diambil dari {len(post_data)} unggahan!')
                    file_name = account_name.replace('_posts', '')
                    file_name = file_name.replace('.csv', '')
                    file_path = save_to_file(all_comment_data, file_format, file_name)
                    st.success(f'Data disimpan sebagai {file_name}{file_format}')
                    st.table(pd.DataFrame(all_comment_data))
            else:
                st.error("Pilih atau upload file CSV terlebih dahulu")