import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from utils import *

st.title(":red[Ins]:orange[tag]:violet[ram] Comment Scraper Test & Repair")
account_url = "https://www.instagram.com/instagram/"
post_url = "https://www.instagram.com/p/C_Le3j9pG52/"

testtab, repairtab, helptab = st.tabs(["Test", "Repair", "Help"])

with testtab:
    st.markdown("Uji apakah setiap elemen dapat ditemukan oleh program.")
    if st.button("Jalankan tes", icon=":material/frame_inspect:"):
        try:
            with open("selectors.json", "r") as file:
                selectors = json.load(file)
        except FileNotFoundError:
            st.error("File selectors.json tidak ditemukan")
            st.stop()

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        load_cookies(driver)

        # Test post_elements
        driver.get(account_url)
        time.sleep(3)
        try:
            post_elements = driver.find_elements(By.CSS_SELECTOR, selectors["post_elements"])
            if len(post_elements) > 0:
                try:
                    post_text = post_elements[0].get_attribute("href")
                    st.success(f"Elemen post_elements ditemukan")
                except Exception as e:
                    post_text = "https://www.instagram.com/p/C_Le3j9pG52/"
                    st.warning(f"Atribut href pada post_elements tidak ditemukan: {e}")
            else:
                st.error(f"Elemen post_elements tidak ditemukan")
        except Exception as e:
            st.error(f"Elemen post_elements tidak ditemukan: {e}")

        # Test comment_container
        driver.get(post_url)
        time.sleep(3)
        try:
            comment_container = driver.find_elements(By.CSS_SELECTOR, selectors["comment_container"])
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", comment_container)
            if len(comment_container) > 0:
                st.success("Elemen comment_container ditemukan")
            else:
                st.error(f'Elemen comment_container tidak ditemukan')
        except Exception as e:
            st.error(f'Elemen comment_container tidak ditemukan: {e}')

        # Test comment_elements
        try:
            comment_elements = driver.find_elements(By.CSS_SELECTOR, selectors["comment_elements"])
            if len(comment_elements) > 0:
                st.success("Elemen comment_elements ditemukan")
            else:
                st.error('Elemen comment_elements tidak ditemukan')
        except Exception as e:
            st.error(f'Elemen comment_elements tidak ditemukan: {e}')

        # Test username_elements
        try:
            username_elements = driver.find_elements(By.CSS_SELECTOR, selectors["username_elements"])
            if len(username_elements) > 0:
                st.success("Elemen username_elements ditemukan")
            else:
                st.error('Elemen username_elements tidak ditemukan')
        except Exception as e:
            st.error(f'Elemen username_elements tidak ditemukan: {e}')

        # Test datetime_elements
        try:
            datetime_elements = driver.find_elements(By.CSS_SELECTOR, selectors["datetime_elements"])
            if len(datetime_elements) > 0:
                st.success("Elemen datetime_elements ditemukan")
            else:
                st.error('Elemen datetime_elements tidak ditemukan')
        except Exception as e:
            st.error(f'Elemen datetime_elements tidak ditemukan: {e}')
        
        # Test view_replies_button
        try:
            view_replies_button = driver.find_elements(By.XPATH, selectors["view_replies_button"])
            st.success("Elemen view_replies_button ditemukan")
            try:
                driver.execute_script("arguments[0].click();", view_replies_button[0])
                time.sleep(1)
            except Exception as e:
                st.error(f"Error clicking view replies button: {e}")
        except Exception as e:
            st.error(f'Elemen view_replies_button tidak ditemukan: {e}')

with repairtab:
    st.markdown("Mengubah CSS Selector program jika elemen tertentu tidak dapat ditemukan.")
    
    try:
        with open("selectors.json", "r") as file:
            selectors = json.load(file)
    except FileNotFoundError:
        st.error("File selectors.json tidak ditemukan")
        st.stop()

    for key, value in selectors.items():
        # Menyimpan input pengguna ke dalam variabel selector
        selectors[key] = st.text_input(f"{key}", value)

    @st.dialog("Konfirmasi Perubahan")
    def popover_confirm(data):
        st.write("Yakin ingin menyimpan perubahan?")
        st.write("Perubahan akan disimpan secara permanen")
        if st.button("Konfirmasi"):
            with open("selectors.json", "w") as file:
                json.dump(data, file, indent=4)
            st.success("Perubahan berhasil disimpan.")


    if st.button("Simpan perubahan"):
        popover_confirm(selectors)

with helptab:
    st.markdown("Bantuan untuk menemukan CSS Selector.")
    with st.expander("post_elements"):
        st.markdown("1. Buka menu inspect pada halaman Instagram")
        st.markdown("2. Gunakan select element (pojok kiri atas menu inspect), pilih salah satu unggahan")
        st.image("assets/Post1.png")
        st.markdown("3. Lihat pada menu inspect, kita ingin mengambil atribut href yang berisi link unggahan tersebut")
        st.markdown("4. Klik kanan pada elemen <a> yang mengandung atribut href, dan copy Selector")
        st.image("assets/Post2.png")
        st.markdown("5. Selector ini merujuk pada unggahan spesifik yang kita pilih, kita ingin selector yang lebih umum (merujuk pada setiap unggahan)")
        st.markdown("6. Untuk itu, ambil atribut class dari elemen <div> di atas <a> yang kita copy tadi")
        st.image("assets/Post3.png")
        st.markdown("7. Modifikasi CSS Selector seperti berikut")
        post_code = '''
    # Selector awal:
        #mount_0_0_K7 > div > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div:nth-child(2) > div > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y.x8vgawa > section > main > div > div:nth-child(4) > div > div:nth-child(1) > div:nth-child(1) > a
    # div class:
        x1lliihq x1n2onr6 xh8yej3 x4gyw5p x1ntc13c x9i3mqj x11i5rnm x2pgyrj
    # Hasil selector:
        div.x1lliihq.x1n2onr6.xh8yej3.x4gyw5p.x1ntc13c.x9i3mqj.x11i5rnm.x2pgyrj > a
    #   div.[class div (ganti semua spasi dengan titik)] > a'''
        st.code(post_code, language='html')
        st.markdown("8. Uji selector dengan mencari selector pada halaman inspect. Pastikan selector hanya merujuk pada unggahan dan semua unggahan dapat ditemukan. Anda dapat bereksperimen dengan selector untuk mendapatkan selector yang benar.")
        st.image("assets/Post4.png")
    with st.expander("comment_container"):
        st.markdown("1. Buka menu inspect pada halaman unggahan Instagram (pastikan tautan berbentuk instagram.com/p/ABCDEFGHIJK/)")
        st.markdown("2. Gunakan select element (pojok kiri atas menu inspect), pilih scrollbar kolom komentar hingga terlihat seperti ini")
        st.image("assets/Container1.png")
        st.markdown("3. Elemen yang benar memiliki value \"scroll\", klik kanan pada elemen di menu inspect dan copy Selector")
        st.image("assets/Container2.png")
    with st.expander("comment_elements"):
        st.markdown("1. Buka menu inspect pada halaman unggahan Instagram (pastikan tautan berbentuk instagram.com/p/ABCDEFGHIJK/)")
        st.markdown("2. Gunakan select element (pojok kiri atas menu inspect), pilih teks komentar (bukan caption)")
        st.markdown("3. Klik kanan pada elemen di menu inspect, dan copy Selector")
        st.image("assets/Comment1.png")
        st.markdown("4. Selector ini merujuk pada komentar spesifik yang kita pilih, kita ingin selector yang lebih umum (merujuk pada setiap komentar)\nUntuk itu, modifikasi selector seperti berikut")
        comment_code ='''
    # Selector awal:
        #mount_0_0_4N > div > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y.x8vgawa > section > main > div > div.x6s0dn4.x78zum5.xdt5ytf.xdj266r.xkrivgy.xat24cr.x1gryazu.x1n2onr6.xh8yej3 > div > div.x4h1yfo > div > div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6 > div > div.x78zum5.xdt5ytf.x1iyjqo2 > div:nth-child(1) > div:nth-child(1) > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(1) > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1cy8zhl.x1oa3qoh.x1nhvcw1 > span
    # Hasil selektor:
        div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1cy8zhl.x1oa3qoh.x1nhvcw1 > span
    #   #mount > div > div > ... > div.[class] > span -->> div.[class] > span
    #   (hanya ambil div > span paling belakang)'''
        st.code(comment_code, language='html')
    with st.expander("username_elements"):
        st.markdown("1. Buka menu inspect pada halaman unggahan Instagram (pastikan tautan berbentuk instagram.com/p/ABCDEFGHIJK/)")
        st.markdown("2. Gunakan select element (pojok kiri atas menu inspect), pilih teks username")
        st.markdown("3. Klik kanan pada elemen di menu inspect, dan copy Selector")
        st.image("assets/Username1.png")
        st.markdown("4. Selector ini merujuk pada username spesifik yang kita pilih, kita ingin selector yang lebih umum (merujuk pada setiap username)\nUntuk itu, modifikasi selector seperti berikut")
        username_code ='''
    # Selector awal:
        #mount_0_0_4N > div > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y.x8vgawa > section > main > div > div.x6s0dn4.x78zum5.xdt5ytf.xdj266r.xkrivgy.xat24cr.x1gryazu.x1n2onr6.xh8yej3 > div > div.x4h1yfo > div > div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6 > div > div.x78zum5.xdt5ytf.x1iyjqo2 > div:nth-child(1) > div:nth-child(1) > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(1) > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj > span > div > a > div > div > span
    # Hasil selektor:
        span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj > span > div > a > div > div > span
    #   #mount > div > div > ... > span.[class] > span > div > a > div > div > span -->> span.[class] > span > div > a > div > div > span
    #   (hanya ambil elemen dibawah span yang disebutkan classnya)'''
        st.code(username_code, language='html')
    with st.expander("datetime_elements"):
        st.markdown("1. Buka menu inspect pada halaman unggahan Instagram (pastikan tautan berbentuk instagram.com/p/ABCDEFGHIJK/)")
        st.markdown("2. Gunakan select element (pojok kiri atas menu inspect), pilih teks waktu di sebelah username")
        st.markdown("3. Klik kanan pada elemen di menu inspect, dan copy Selector")
        st.image("assets/Datetime1.png")
        st.markdown("4. Selector ini merujuk pada datetime komentar spesifik yang kita pilih, kita ingin selector yang lebih umum (merujuk pada setiap datetime komentar)\nUntuk itu, modifikasi selector seperti berikut")
        datetime_code ='''
    # Selector awal:
        #mount_0_0_Cb > div > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y.x8vgawa > section > main > div > div.x6s0dn4.x78zum5.xdt5ytf.xdj266r.xkrivgy.xat24cr.x1gryazu.x1n2onr6.xh8yej3 > div > div.x4h1yfo > div > div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6 > div > div.x78zum5.xdt5ytf.x1iyjqo2 > div:nth-child(1) > div:nth-child(1) > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div:nth-child(1) > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj > a > time
    # Hasil selektor:
        span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x1ji0vk5.x18bv5gf.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x1roi4f4.x10wh9bi.x1wdrske.x8viiok.x18hxmgj > a > time
    #   #mount > div > div > ... > span.[class] > a > time -->> span.[class] > a > time
    #   (hanya ambil span > a > div paling belakang)'''
        st.code(datetime_code, language='html')
    with st.expander("view_replies_button"):
        st.markdown("Selector untuk view_replies_button bekerja dengan mencari elemen yang mengandung elemen teks tertentu")
        st.markdown("Jika website menggunakan bahasa Inggris, biasanya teks dari tombol ini adalah \"View all replies\", jadi selector dapat dibuat untuk mencari teks \"View\"")
        st.image("assets/Replies1.png")
        st.markdown("Teks pada tombol bisa berubah jika menggunakan pengaturan bahasa yang berbeda. Sesuaikan selector sesuai teks yang dimiliki button")
        replies_code='''
//span[contains(text(), '<Teks button>')]
        '''
        st.code(replies_code, language='html')
