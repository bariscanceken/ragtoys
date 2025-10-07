import streamlit as st
from PIL import Image
import sqlite3
import bcrypt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from streamlit_drawable_canvas import st_canvas
import io
import time
import base64
import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
load_dotenv()
from graph.graph import app 
  

con = sqlite3.connect("C:\\Users\\baris\\OneDrive\\Masaüstü\\önemli\\ragtoys.db")
c = con.cursor()

def check_login(input_username, input_password):
    
    c.execute("SELECT password FROM users WHERE username = ?", (input_username,))
    result = c.fetchone()
    if result:
        stored_hash = result[0]
        if bcrypt.checkpw(input_password.encode('utf-8'), stored_hash):
            st.query_params["page"] = "main"
            st.rerun()
        else:
            st.warning("Hatalı Deneme!")
    else:
        st.warning("Hatalı Deneme!")

def response_generator():
    try:
        response = str(app.invoke(input={"question": prompt}).get("generation") or "(Yanıt bulunamadı)")
    except:
        response = "(Yanıt bulunamadı)"
    
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def mail_nt_r(input_name, input_email):
    try:
        sender_email = "bariscancekenx@gmail.com"
        sender_password = "gqmh rbeq ohdv vjqv"

        verification_code = ''.join(random.choices(string.digits, k=6))
        st.session_state.verification_code = verification_code

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = input_email
        message["Subject"] = "ragtoys - E-posta Doğrulama Kodu"

        body = f"""
        Merhaba {input_name},

        ragtoys için aşağıdaki doğrulama kodunu kullanın:

        {verification_code}

        Bu kod 1 saat geçerlidir.

        Saygılarımızla,
        ragtoys Ekibi
        """

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        st.success("Doğrulama kodu e-posta adresinize gönderildi!")
        return True
        
    except Exception as e:
        st.error(f"E-posta gönderilirken hata oluştu: {str(e)}")
        return False

def reset_password_email(input_email):
    try:
        conn = sqlite3.connect("C:\\Users\\baris\\OneDrive\\Masaüstü\\önemli\\ragtoys.db", timeout=30)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (input_email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            sender_email = "bariscancekenx@gmail.com"
            sender_password = "gqmh rbeq ohdv vjqv"

            # Şifre sıfırlama kodu oluştur
            reset_code = ''.join(random.choices(string.digits, k=6))
            st.session_state.reset_code = reset_code
            st.session_state.reset_email = input_email

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = input_email
            message["Subject"] = "ragtoys - Şifre Sıfırlama Kodu"

            body = f"""
            Merhaba,

            ragtoys hesabınız için şifre sıfırlama kodunuz:

            {reset_code}

            Bu kod 1 saat geçerlidir.

            Saygılarımızla,
            ragtoys Ekibi
            """

            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            st.success("Şifre sıfırlama kodu e-posta adresinize gönderildi!")
            return True
        else:
            st.error("Bu e-posta adresi ile kayıtlı kullanıcı bulunamadı!")
            return False
            
    except Exception as e:
        st.error(f"E-posta gönderilirken hata oluştu: {str(e)}")
        return False

def register(input_name,input_surname,input_username_r,input_email,input_password_r,input_password_r2,checkbox_privacy):
    c.execute("SELECT * FROM users WHERE email = ?", (input_email,))
    e_mail = c.fetchone()
    c.execute("SELECT * FROM users WHERE username = ?", (input_username_r,))
    e_username = c.fetchone()

    if e_mail is None and input_email:
        if input_name and input_surname:
            if (input_password_r == input_password_r2) and input_password_r:
                if checkbox_privacy == 1: 
                    if e_username is None and input_username_r:
                        # Kullanıcı bilgilerini session state'e kaydet
                        st.session_state.input_name = input_name
                        st.session_state.input_surname = input_surname
                        st.session_state.input_username_r = input_username_r
                        st.session_state.input_email = input_email
                        st.session_state.input_password_r = bcrypt.hashpw(input_password_r.encode('utf-8'), bcrypt.gensalt())
                        st.session_state.checkbox_privacy = checkbox_privacy
                        
                        if mail_nt_r(input_name, input_email):
                            st.query_params["page"] = "verify"
                            st.rerun()
                    else:
                        st.warning("Böyle Bir Kullanıcı Zaten Var!")
                else:
                    st.warning("Sözleşme kabul edilmeli!")
            else:
                st.warning("Şifreler Eşleşmiyor!")
        else:
            st.warning("Bir İsim Girilmedi!")
    else:
        st.warning("Bu Mail Zaten Kullanılmış!")

    

page = st.query_params.get("page", "login")

if page == 'login':
    st.set_page_config(layout="wide", page_title="ragtoys login page")

    st.markdown(
        """
        <style>
        .stApp {
            color: #d4ff00;  /* tüm yazı rengi */
        }

        /* Input ve buton yazıları */
        .stTextInput>div>div>input {
            color: #d4ff00;
        }
        .stButton>button {
            color: #d4ff00;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    logo = Image.open("C:\\Users\\baris\\OneDrive\\Masaüstü\\ragtoys\\logo.jpeg")
    with st.container():
        st.image(logo, width=200)
        st.markdown(
            "<h1 style='margin:0;text-align:center'>ragtoys</h1>"
            "<p style='margin-top:4px;color:#64748B;text-align:center'>Oyuncaklar, Çocuklar ve Gelecek</p>",
            unsafe_allow_html=True)
        

    left_col, center_col, right_col = st.columns([1, 1, 1])

    with center_col:
        
        st.write("") 
        st.write("")
        st.write("") 
        st.write("")
        input_username = st.text_input("Kullanıcı adınızı giriniz.")
        st.session_state['input_username'] = input_username
        input_password = st.text_input("Şifrenizi giriniz.", type="password")
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        st.write("")
        st.write("")

        with col1:
            if st.button("Giriş Yap"):
                check_login(input_username=input_username,input_password=input_password)
            
        with col2:
            st.write("")
        with col3:
            if st.button("Unuttum"):
                st.query_params["page"] = "forget"
                st.rerun()
        with col4:
            st.write("")
        with col5:
            if st.button("Kayıt Olun!"):
                st.query_params["page"] = "register"
                st.rerun()


if page == 'forget':
    st.set_page_config(layout="wide", page_title="ragtoys forget page")

    st.markdown(
        """
        <style>
        .stApp {
            color: #d4ff00;  /* tüm yazı rengi */
        }

        /* Input ve buton yazıları */
        .stTextInput>div>div>input {
            color: #d4ff00;
        }
        .stButton>button {
            color: #d4ff00;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    logo = Image.open("C:\\Users\\baris\\OneDrive\\Masaüstü\\ragtoys\\logo.jpeg")
    with st.container():
        st.image(logo, width=200)
        st.markdown(
            "<h1 style='margin:0;text-align:center'>ragtoys</h1>"
            "<p style='margin-top:4px;color:#64748B;text-align:center'>Oyuncaklar, Çocuklar ve Gelecek</p>",
            unsafe_allow_html=True)
        
    left_col, center_col, right_col = st.columns([1, 1, 1])

    with center_col:
        st.write("") 
        st.write("")
        st.write("") 
        st.write("")
        input_email = st.text_input("E-posta Adresinizi Giriniz.")
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            if st.button("Geri Dön"):
                st.query_params["page"] = "login"
                st.rerun()
        with col2:
            st.write("")
        with col3:
            if st.button("Sıfırlayın"):
                if input_email:
                    if reset_password_email(input_email):
                        st.query_params["page"] = "reset_password"
                        st.rerun()
                else:
                    st.warning("Lütfen e-posta adresinizi giriniz!")
        with col4:
            st.write("")
        with col5:
            st.write("")
    
if page == 'register':
    st.set_page_config(layout="wide", page_title="ragtoys register page")

    st.markdown(
        """
        <style>
        .stApp {
            color: #d4ff00;  /* tüm yazı rengi */
        }

        /* Input ve buton yazıları */
        .stTextInput>div>div>input {
            color: #d4ff00;
        }
        .stButton>button {
            color: #d4ff00;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    logo = Image.open("C:\\Users\\baris\\OneDrive\\Masaüstü\\ragtoys\\logo.jpeg")
    with st.container():
        st.image(logo, width=200)
        st.markdown(
            "<h1 style='margin:0;text-align:center'>ragtoys</h1>"
            "<p style='margin-top:4px;color:#64748B;text-align:center'>Oyuncaklar, Çocuklar ve Gelecek</p>",
            unsafe_allow_html=True)
        
    left_col, center_col, right_col = st.columns([1, 1, 1])

    with center_col:
        st.write("") 
        st.write("")
        st.write("") 
        st.write("")
        input_name = st.text_input("Adınızı Giriniz.")
        input_surname = st.text_input("Soyadınızı Giriniz.")
        input_username_r = st.text_input("Kullanıcı Adı Giriniz.")
        input_email = st.text_input("Mail Adresinizi Giriniz.")
        input_password_r = st.text_input("Şifrenizi Seçiniz.", type="password")
        input_password_r2 = st.text_input("Seçtiğiniz Şifrenizi Tekrar Giriniz.", type="password")
        with st.expander("**:blue[Gizlilik Sözleşmesini Oku]**"):
            st.markdown("""
            Gizlilik Sözleşmesi

            1. Kişisel Verilerin Toplanması
            Kullanıcılarımızdan, hizmetlerimizi sağlamak ve deneyiminizi iyileştirmek amacıyla bazı kişisel bilgiler (isim, e-posta, kullanım tercihleri vb.) toplanabilir.

            2. Kişisel Verilerin Kullanımı
            Toplanan bilgiler, yalnızca:

            Hizmetlerin doğru çalışmasını sağlamak,

            Kullanıcı taleplerine yanıt vermek,

            İyileştirme ve analiz yapmak amacıyla kullanılacaktır.

            3. Kişisel Verilerin Paylaşımı
            Kullanıcı bilgileriniz, üçüncü kişilerle paylaşılmaz; yalnızca yasal zorunluluklar çerçevesinde yetkili mercilerle paylaşılabilir.

            4. Çerezler ve Takip Teknolojileri
            Web sitemiz/uygulamamız, deneyiminizi geliştirmek için çerez ve benzeri teknolojiler kullanabilir. Kullanıcı, tarayıcı ayarları ile çerezleri yönetebilir.

            5. Güvenlik
            Kişisel bilgileriniz, güvenli sunucular ve şifreleme yöntemleriyle korunmaktadır. Yetkisiz erişimlere karşı azami önlem alınmıştır.

            6. Kullanıcı Hakları
            Kullanıcılar, kişisel verilerine erişim, düzeltme veya silme hakkına sahiptir. Bu hakları kullanmak için bizimle iletişime geçebilirsiniz.

            7. Onay
            Hizmetlerimizi kullanmaya devam ederek, bu gizlilik sözleşmesini okuduğunuzu ve kabul ettiğinizi onaylamış olursunuz.
            """)
        checkbox_privacy = st.checkbox("Gizlilik Sözleşmesini Onaylıyorum.")
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            if st.button("Geri Dön"):
                st.query_params["page"] = "login"
                st.rerun()
        with col2:
            st.write("")
        with col3:
            st.write("")
        with col4:
            st.write("")
        with col5:
            if st.button("Kayıt Olun!"):
                register(input_name,input_surname,input_username_r,input_email,input_password_r,input_password_r2,checkbox_privacy)
    

if page == 'verify':
        st.set_page_config(layout="wide", page_title="ragtoys login page")

        st.markdown(
            """
            <style>
            .stApp {
                color: #d4ff00;  /* tüm yazı rengi */
            }

            /* Input ve buton yazıları */
            .stTextInput>div>div>input {
                color: #d4ff00;
            }
            .stButton>button {
                color: #d4ff00;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


        logo = Image.open("C:\\Users\\baris\\OneDrive\\Masaüstü\\ragtoys\\logo.jpeg")
        with st.container():
            st.image(logo, width=200)
            st.markdown(
                "<h1 style='margin:0;text-align:center'>ragtoys</h1>"
                "<p style='margin-top:4px;color:#64748B;text-align:center'>Oyuncaklar, Çocuklar ve Gelecek</p>",
                unsafe_allow_html=True)
            

        left_col, center_col, right_col = st.columns([1, 1, 1])

        with center_col:
            
            st.write("") 
            st.write("")
            st.write("") 
            st.write("")
            input_verify = st.text_input("Doğrulama Kodunu Giriniz:")
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
            st.write("")
            st.write("")

            if "a" not in st.session_state:
                st.session_state.a = False

            if "verification_code" not in st.session_state:
                st.session_state.verification_code = ""

            if "input_verify" not in st.session_state:
                st.session_state.input_verify = ""

            with col1:
                if st.button("Doğrula"):
                    if st.session_state.verification_code == input_verify:
                        c.execute("INSERT INTO users (name,surname,username,email,password,applied_privacy) values (?,?,?,?,?,?)",
                        (st.session_state.input_name, st.session_state.input_surname, st.session_state.input_username_r, 
                         st.session_state.input_email, st.session_state.input_password_r, st.session_state.checkbox_privacy))   
                        con.commit()
                        st.success("Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz.")
                        st.query_params["page"] = "login"
                        st.rerun()
                    else:
                         st.error("Doğrulama kodu hatalı!")

if page == 'reset_password':
    st.set_page_config(layout="wide", page_title="ragtoys reset password page")

    st.markdown(
        """
        <style>
        .stApp {
            color: #d4ff00;  /* tüm yazı rengi */
        }

        /* Input ve buton yazıları */
        .stTextInput>div>div>input {
            color: #d4ff00;
        }
        .stButton>button {
            color: #d4ff00;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    logo = Image.open("C:\\Users\\baris\\OneDrive\\Masaüstü\\ragtoys\\logo.jpeg")
    with st.container():
        st.image(logo, width=200)
        st.markdown(
            "<h1 style='margin:0;text-align:center'>ragtoys</h1>"
            "<p style='margin-top:4px;color:#64748B;text-align:center'>Şifre Sıfırlama</p>",
            unsafe_allow_html=True)
        
    left_col, center_col, right_col = st.columns([1, 1, 1])

    with center_col:
        st.write("") 
        st.write("")
        st.write("") 
        st.write("")
        input_reset_code = st.text_input("Sıfırlama Kodunu Giriniz:")
        input_new_password = st.text_input("Yeni Şifrenizi Giriniz:", type="password")
        input_new_password2 = st.text_input("Yeni Şifrenizi Tekrar Giriniz:", type="password")
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            if st.button("Geri Dön"):
                st.query_params["page"] = "login"
                st.rerun()
        with col2:
            st.write("")
        with col3:
            if st.button("Şifreyi Sıfırla"):
                if input_reset_code == st.session_state.reset_code:
                    if input_new_password == input_new_password2 and input_new_password:
                        # Şifreyi güncelle
                        conn = sqlite3.connect("C:\\Users\\baris\\OneDrive\\Masaüstü\\önemli\\ragtoys.db", timeout=30)
                        cursor = conn.cursor()
                        hashed_password = bcrypt.hashpw(input_new_password.encode('utf-8'), bcrypt.gensalt())
                        cursor.execute("UPDATE users SET password = ? WHERE email = ?", 
                                     (hashed_password, st.session_state.reset_email))
                        conn.commit()
                        conn.close()
                        st.success("Şifreniz başarıyla güncellendi! Giriş sayfasına yönlendiriliyorsunuz.")
                        st.query_params["page"] = "login"
                        st.rerun()
                    else:
                        st.error("Şifreler eşleşmiyor!")
                else:
                    st.error("Sıfırlama kodu hatalı!")
        with col4:
            st.write("")
        with col5:
            st.write("")

if page == 'main':
    st.set_page_config(layout="wide", page_title="ragtoys main page")

    st.markdown(
        """
        <style>
        .stApp {
            color: #d4ff00;  /* tüm yazı rengi */
        }

        /* Input ve buton yazıları */
        .stTextInput>div>div>input {
            color: #d4ff00;
        }
        .stButton>button {
            color: #d4ff00;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    logo = Image.open("C:\\Users\\baris\\OneDrive\\Masaüstü\\ragtoys\\logo.jpeg")
    with st.container():
        st.image(logo, width=200)
        st.markdown(
            "<h1 style='margin:0;text-align:center'>ragtoys</h1>"
            "<p style='margin-top:4px;color:#64748B;text-align:center'>Oyuncaklar, Çocuklar ve Gelecek</p>",
            unsafe_allow_html=True)
        

    left_col, right_col = st.columns([3 , 1])

    with st.sidebar:
        st.header("Ayarlar")
        stroke_width = st.slider("Çizgi Kalınlığı", 1, 50, 4)
        stroke_color = st.color_picker("Çizgi Rengi", "#000000")
        bg_color = st.color_picker("Arkaplan Rengi", "#ffffff")
        realtime = st.checkbox("Gerçek zamanlı göster", True)
        save_btn = st.button("Çizimi Kaydet")
        send_btn = st.button("Çizimi Gönder")
        if st.button("Çıkış"):
            st.query_params["page"] = "login"
            st.rerun()
        if st.button("Son kaydedilen tuvali göster"):
            username = st.session_state.get('input_username')
            if not username:
                st.warning("Önce kullanıcı adıyla giriş yapın.")
            else:
                c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
                user_row = c.fetchone()
                if not user_row:
                    st.warning("Kullanıcı bulunamadı!")
                else:
                    uid = user_row[0]
                    c.execute("SELECT tuval_durum FROM canvas WHERE user_id = ? ORDER BY id DESC LIMIT 1", (uid,))
                    row = c.fetchone()
                    if row:
                        img_data = row[0]
                        st.image(io.BytesIO(img_data))
                    else:
                        st.warning("Kayıt bulunamadı!")
        
        # Gönderme işlemi mantığı aşağıda, canvas oluşturulduktan sonra çalıştırılacak

    with left_col:
        canvas_result = st_canvas(
            fill_color="rgba(0,0,0,0)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            height=600,
            width=900,
            drawing_mode="freedraw",
            key="canvas",
            display_toolbar=True,
            )
    c.execute("select user_id from users where username = ?", (st.session_state.get('input_username', ''),))
    user_id_k = c.fetchone()
    if user_id_k:
        user_id_k = user_id_k[0]

    if save_btn:
        if not user_id_k:
            st.warning("Kullanıcı bulunamadı; önce giriş yapın.")
        elif canvas_result.image_data is not None:
            # Pillow ile resmi dönüştür
            img = Image.fromarray((canvas_result.image_data).astype("uint8"))
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_data = buffer.getvalue()
            c.execute(
                "INSERT INTO canvas (user_id, tuval_durum) VALUES (?, ?)",
                (user_id_k, img_data)
            )
            con.commit()
            st.success("Tuval başarıyla kaydedildi!")

    # Çizimi Gönder: Önce mevcut tuvali al, yoksa son kaydı kullan
    if send_btn:
        username = st.session_state.get('input_username')
        if not username:
            st.warning("Önce kullanıcı adıyla giriş yapın.")
        else:
            c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            user_row = c.fetchone()
            if not user_row:
                st.warning("Kullanıcı bulunamadı!")
            else:
                uid = user_row[0]
                img_bytes_to_send = None
                # Öncelik: o anki tuval
                if canvas_result.image_data is not None:
                    try:
                        current_img = Image.fromarray((canvas_result.image_data).astype("uint8"))
                        buf = io.BytesIO()
                        current_img.save(buf, format="PNG")
                        img_bytes_to_send = buf.getvalue()
                    except Exception:
                        img_bytes_to_send = None
                # Yedek: son kaydedilen tuval
                if img_bytes_to_send is None:
                    c.execute("SELECT tuval_durum FROM canvas WHERE user_id = ? ORDER BY id DESC LIMIT 1", (uid,))
                    last_row = c.fetchone()
                    if last_row:
                        img_bytes_to_send = last_row[0]
                if img_bytes_to_send is None:
                    st.warning("Gönderilecek bir tuval bulunamadı. Lütfen çizimi kaydedin veya yeni bir çizim yapın.")
                else:
                    c.execute("INSERT INTO sent (user_id, tuval) VALUES (?, ?)", (uid, img_bytes_to_send))
                    con.commit()
                    st.success("Tuval başarıyla gönderildi!")
                    st.image(io.BytesIO(img_bytes_to_send))

    with right_col:

        # Sohbet alanı için sabit yüksekliğe sahip konteyner
        chat_area = st.container(height=500, border=True)

        # Mesaj geçmişini hazırla (ilk mesaj bot tarafından gelsin)
        if "messages" not in st.session_state or not st.session_state.messages:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hoşgeldin! yarışmanın konsepti sadece resmederek bize anlatman. Unutma tek gayemiz mutlu bir nesil!",
                }
            ]

        # Mesajları konteyner içinde göster (her çizimde)
        with chat_area:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Kullanıcı girişini al (her çizimde)
        if prompt := st.chat_input("Bizim hakkımızda soru sor!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_area:
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    response = st.write_stream(response_generator())
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Son asistan mesajını ElevenLabs ile seslendir
            try:
                api_key = os.getenv("ELEVEN_API_KEY")
                if api_key and response and isinstance(response, str):
                    client = ElevenLabs(api_key=api_key)
                    audio_stream = client.text_to_speech.convert(
                        voice_id="21m00Tcm4TlvDq8ikWAM",  # varsayılan: Rachel
                        optimize_streaming_latency="0",
                        output_format="mp3_44100_128",
                        model_id="eleven_multilingual_v2",
                        text=response,
                    )
                    audio_bytes = io.BytesIO()
                    for chunk in audio_stream:
                        if chunk:
                            audio_bytes.write(chunk)
                    audio_bytes.seek(0)
                    audio_b64 = base64.b64encode(audio_bytes.getvalue()).decode("ascii")
                    st.markdown(
                        f"""
<audio autoplay style=\"display:none\" src=\"data:audio/mpeg;base64,{audio_b64}\"></audio>
""",
                        unsafe_allow_html=True,
                    )
            except Exception:
                pass
