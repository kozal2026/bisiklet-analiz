import streamlit as st
import requests
import json
import os
from datetime import date

# --- KONFİGÜRASYON VE AYARLAR ---
st.set_page_config(page_title="Erkoz Analiz v48.5", layout="wide", page_icon="🚴‍♂️")
CONFIG_FILE = "erkoz_settings.json"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

# 1. YEREL VERİ YÖNETİMİ (Kalıcı Ayarlar)
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return None
    return None

def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Oturum başlatma
saved_data = load_config()
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = saved_data if saved_data else {
        "ad_soyad": "İsim Soyisim", "dogum_tarihi": "1975-01-01", 
        "boy": 175, "kilo": 75.0, "bis_marka": "Model Belirtilmedi", "bis_kilosu": 10.0
    }

if 'last_km' not in st.session_state:
    st.session_state['last_km'] = 0.0

# 2. SOL PANEL (KİŞİSELLEŞTİRME)
with st.sidebar:
    st.header("⚙️ Sürücü & Ekipman")
    u_ad = st.text_input("Ad Soyad", value=st.session_state['user_data']["ad_soyad"])
    u_dt = st.date_input("Doğum Tarihi", date.fromisoformat(st.session_state['user_data']["dogum_tarihi"]))
    u_boy = st.number_input("Boy (cm)", value=int(st.session_state['user_data']["boy"]))
    u_kilo = st.number_input("Kilo (kg)", value=float(st.session_state['user_data']["kilo"]))
    st.markdown("---")
    u_bis = st.text_input("Bisiklet Modeli", value=st.session_state['user_data']["bis_marka"])
    u_biskilo = st.number_input("Donanım Ağırlığı (kg)", value=float(st.session_state['user_data']["bis_kilosu"]))

    if st.button("💾 BİLGİLERİMİ CİHAZA KAYDET"):
        new_cfg = {
            "ad_soyad": u_ad, "dogum_tarihi": str(u_dt), "boy": u_boy, 
            "kilo": u_kilo, "bis_marka": u_bis, "bis_kilosu": u_biskilo
        }
        save_config(new_cfg)
        st.session_state['user_data'] = new_cfg
        st.success("Ayarlar bu bilgisayara mühürlendi!")

    vke = round(u_kilo / ((u_boy/100)**2), 1)
    zorluk = round((u_biskilo - 10) * 2, 1)
    st.sidebar.metric("Anlık VKE", vke)

# 3. ANA EKRAN (SÜRÜŞ VERİLERİ)
st.title(f"🚀 Erkoz Performans Analiz | Hoş Geldin {u_ad}")

col1, col2 = st.columns(2)
with col1:
    km_in = st.number_input("Sürüş Mesafesi (KM)", value=0.0, step=0.1)
    ruz_in = st.number_input("Ortalama Rüzgar (km/h)", value=0.0)
with col2:
    yuk_in = st.number_input("Toplam Yükselti (m)", value=0)
    kal_in = st.number_input("Yakılan Kalori (kcal)", value=0)

# 4. HESAPLAMA VE EXCEL AKTARIMI
if st.button("📊 ANALİZİ TAMAMLA VE EXCEL'E GÖNDER"):
    if km_in <= 0:
        st.error("Lütfen önce sürüş kilometresini gir kanka!")
    elif km_in == st.session_state['last_km']:
        st.warning(f"⚠️ {km_in} KM verisi zaten gönderildi!")
    else:
        # Algoritma
        yas = date.today().year - u_dt.year
        bak = 1 + (zorluk / 100)
        puan = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / km_in) * 115, 2)
        yag = round((kal_in * 0.8) / 9, 1)

        # 🎯 EXCEL SÜTUN SIRALAMASINA TAM UYUMLU PAYLOAD (A'dan H'ye)
        payload = {
            "adSoyad": u_ad,        # A
            "bisikleti": u_bis,     # B
            "bisKilosu": u_biskilo, # C
            "surusTarihi": str(date.today()), # D
            "surusKM": km_in,       # E
            "ruzgarHizi": ruz_in,   # F
            "yukselti": yuk_in,     # G
            "puan": puan            # H
        }
        
        try:
            res = requests.post(SCRIPT_URL, json=payload, timeout=10)
            st.success(f"✅ Excel Senkronizasyonu Tamam! Skor: {puan}")
            st.session_state['last_km'] = km_in
            st.balloons()
        except:
            st.error("❌ Excel bağlantısı başarısız. İnterneti kontrol et kanka.")

        # SERTİFİKA GÖRÜNÜMÜ
        with st.container(border=True):
            st.header(f"🏆 PERFORMANS ÖZETİ")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Mesafe", f"{km_in} KM")
            m2.metric("Puan", puan)
            m3.metric("Yükselti", f"{yuk_in} m")
            m4.metric("Yağ Yakımı", f"{yag} gr")

st.caption("Erkoz Yazılım © 2026 | v48.5 - Full Sync Mode")
