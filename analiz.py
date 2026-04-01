import streamlit as st
import requests
import json
import os
from datetime import date
from streamlit_local_storage import LocalStorage

# --- 1. KONFİGÜRASYON VE HAFIZA ---
st.set_page_config(page_title="Erkoz Analiz v48.7", layout="wide", page_icon="🚴‍♂️")

# Tarayıcı yerel hafızası için araç (Her telefonun kendi hafızası)
local_storage = LocalStorage()
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

# --- 2. KİŞİSEL VERİLERİ ÇEKME ---
# Tarayıcıda 'erkoz_user_data' anahtarıyla kayıtlı veri var mı bakıyoruz
saved_user = local_storage.getItem("erkoz_user_data")

if 'user_data' not in st.session_state:
    if saved_user:
        # Eğer tarayıcıda kayıtlıysa onu yükle
        st.session_state['user_data'] = json.loads(saved_user)
    else:
        # Kayıt yoksa tertemiz varsayılan değerler
        st.session_state['user_data'] = {
            "ad_soyad": "İsim Soyisim", 
            "dogum_tarihi": "1985-01-01", 
            "boy": 175, 
            "kilo": 75.0, 
            "bis_marka": "Model Girilmedi", 
            "bis_kilosu": 10.0
        }

if 'last_km' not in st.session_state:
    st.session_state['last_km'] = 0.0

# --- 3. SOL PANEL (KİŞİSEL AYARLAR) ---
with st.sidebar:
    st.header("⚙️ Sürücü Profili")
    st.info("Bilgilerini bir kez gir ve 'CİHAZA SABİTLE' butonuna bas kanka.")
    
    u_ad = st.text_input("Ad Soyad", value=st.session_state['user_data']["ad_soyad"])
    
    # Genişletilmiş yaş aralığı (1920'den bugüne)
    u_dt = st.date_input(
        "Doğum Tarihi", 
        value=date.fromisoformat(st.session_state['user_data']["dogum_tarihi"]),
        min_value=date(1920, 1, 1),
        max_value=date.today()
    )
    
    u_boy = st.number_input("Boy (cm)", value=int(st.session_state['user_data']["boy"]))
    u_kilo = st.number_input("Kilo (kg)", value=float(st.session_state['user_data']["kilo"]))
    
    st.markdown("---")
    u_bis = st.text_input("Bisiklet Modeli", value=st.session_state['user_data']["bis_marka"])
    u_biskilo = st.number_input("Donanım Ağırlığı (kg)", value=float(st.session_state['user_data']["bis_kilosu"]))

    # 💾 KRİTİK BUTON: Veriyi sadece o telefonun hafızasına yazar
    if st.button("💾 BİLGİLERİMİ BU CİHAZA SABİTLE"):
        user_info = {
            "ad_soyad": u_ad, "dogum_tarihi": str(u_dt), "boy": u_boy, 
            "kilo": u_kilo, "bis_marka": u_bis, "bis_kilosu": u_biskilo
        }
        local_storage.setItem("erkoz_user_data", json.dumps(user_info))
        st.session_state['user_data'] = user_info
        st.success("✅ Bilgiler sadece SİZİN cihazınıza mühürlendi!")

    # Anlık hesaplamalar
    vke = round(u_kilo / ((u_boy/100)**2), 1)
    zorluk = round((u_biskilo - 10) * 2, 1)
    st.sidebar.metric("Anlık VKE", vke)
    st.sidebar.metric("Zorluk Katsayısı", f"%{zorluk}")

# --- 4. ANA EKRAN (SÜRÜŞ GİRİŞİ) ---
st.title(f"🚀 Erkoz Performans Analiz")
st.subheader(f"Hoş Geldin, {u_ad}")

col1, col2 = st.columns(2)
with col1:
    km_in = st.number_input("Sürüş Mesafesi (KM)", value=0.0, step=0.1)
    ruz_in = st.number_input("Ortalama Rüzgar (km/h)", value=0.0)
with col2:
    yuk_in = st.number_input("Toplam Yükselti (m)", value=0)
    kal_in = st.number_input("Yakılan Kalori (kcal)", value=0)

# --- 5. ANALİZ VE EXCEL GÖNDERİM ---
if st.button("📊 ANALİZİ TAMAMLA VE EXCEL'E UÇUR"):
    if km_in <= 0:
        st.error("KM girmeden analiz yapamayız Erdal abi!")
    elif km_in == st.session_state['last_km']:
        st.warning(f"⚠️ {km_in} KM verisi zaten az önce gönderildi!")
    else:
        # Algoritma v48.7
        yas = date.today().year - u_dt.year
        bak = 1 + (zorluk / 100)
        # Sürüş puanı hesabı
        puan = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / km_in) * 115, 2)
        yag_gr = round((kal_in * 0.8) / 9, 1)

        # 🎯 EXCEL SÜTUN SIRALAMASI (A'dan H'ye)
        payload = {
            "adSoyad": u_ad,        # A: Ad Soyad
            "bisikleti": u_bis,     # B: Bisikleti
            "bisKilosu": u_biskilo, # C: Bisiklet Kilosu
            "surusTarihi": str(date.today()), # D: Tarih
            "surusKM": km_in,       # E: KM
            "ruzgarHizi": ruz_in,   # F: Rüzgar
            "yukselti": yuk_in,     # G: Yükselti
            "puan": puan            # H: Skor
        }
        
        try:
            # Google Apps Script'e JSON verisini gönderiyoruz
            res = requests.post(SCRIPT_URL, json=payload, timeout=10)
            if res.status_code == 200:
                st.success(f"✅ Excel Senkronizasyonu Başarılı! Skorun: {puan}")
                st.session_state['last_km'] = km_in
                st.balloons()
            else:
                st.error("❌ Sunucu hatası! Veri Excel'e yazılmadı.")
        except:
            st.error("❌ Excel bağlantısı başarısız. İnterneti kontrol et kanka.")

        # --- GÖRSEL SERTİFİKA ---
        st.divider()
        with st.container(border=True):
            st.header(f"🏆 BAŞARI SERTİFİKASI: {u_ad}")
            st.write(f"🚲 Ekipman: {u_bis} | 👤 Yaş: {yas} | 👤 VKE: {vke}")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Mesafe", f"{km_in} KM")
            m2.metric("Puan", puan)
            m3.metric("Yükselti", f"{yuk_in} m")
            m4.metric("Yağ Yakımı", f"{yag_gr} gr")

st.caption("Erkoz Yazılım © 2026 | v48.7 - Private Local Storage Mode")
