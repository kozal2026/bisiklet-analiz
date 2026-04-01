import streamlit as st
import requests
import json
import os
from datetime import date

# --- AYARLAR ---
st.set_page_config(page_title="Erkoz Analiz v48.6", layout="wide", page_icon="🚴‍♂️")
CONFIG_FILE = "erkoz_settings.json"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

# 1. YEREL VERİ YÖNETİMİ
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

saved_data = load_config()
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = saved_data if saved_data else {
        "ad_soyad": "İsim Soyisim", "dogum_tarihi": "2000-01-01", # Varsayılanı gençleştirdik
        "boy": 175, "kilo": 75.0, "bis_marka": "Model Girilmedi", "bis_kilosu": 10.0
    }

if 'last_km' not in st.session_state:
    st.session_state['last_km'] = 0.0

# 2. SOL PANEL
with st.sidebar:
    st.header("⚙️ Sürücü & Ekipman")
    u_ad = st.text_input("Ad Soyad", value=st.session_state['user_data']["ad_soyad"])
    
    # 🛠️ DÜZELTME BURADA: 1920 ile Bugün arasını açtık
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

    if st.button("💾 BİLGİLERİMİ CİHAZA KAYDET"):
        new_cfg = {
            "ad_soyad": u_ad, "dogum_tarihi": str(u_dt), "boy": u_boy, 
            "kilo": u_kilo, "bis_marka": u_bis, "bis_kilosu": u_biskilo
        }
        save_config(new_cfg)
        st.session_state['user_data'] = new_cfg
        st.success("Bilgiler mühürlendi kanka!")

    vke = round(u_kilo / ((u_boy/100)**2), 1)
    zorluk = round((u_biskilo - 10) * 2, 1)
    st.sidebar.metric("Anlık VKE", vke)

# 3. ANA EKRAN
st.title(f"🚀 Erkoz Performans Analiz | Sürücü: {u_ad}")

col1, col2 = st.columns(2)
with col1:
    km_in = st.number_input("Sürüş Mesafesi (KM)", value=0.0, step=0.1)
    ruz_in = st.number_input("Ortalama Rüzgar (km/h)", value=0.0)
with col2:
    yuk_in = st.number_input("Toplam Yükselti (m)", value=0)
    kal_in = st.number_input("Yakılan Kalori (kcal)", value=0)

# 4. ANALİZ VE GÖNDERİM
if st.button("📊 ANALİZİ TAMAMLA VE EXCEL'E GÖNDER"):
    if km_in <= 0:
        st.error("KM girmeden analiz olmaz abi!")
    elif km_in == st.session_state['last_km']:
        st.warning(f"⚠️ {km_in} KM zaten gönderildi.")
    else:
        # Yaş hesabı ve skor
        yas = date.today().year - u_dt.year
        bak = 1 + (zorluk / 100)
        puan = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / km_in) * 115, 2)
        yag = round((kal_in * 0.8) / 9, 1)

        payload = {
            "adSoyad": u_ad, "bisikleti": u_bis, "bisKilosu": u_biskilo,
            "surusTarihi": str(date.today()), "surusKM": km_in, 
            "ruzgarHizi": ruz_in, "yukselti": yuk_in, "puan": puan
        }
        
        try:
            requests.post(SCRIPT_URL, json=payload, timeout=10)
            st.success(f"✅ Excel Senkronizasyonu Başarılı! Puan: {puan}")
            st.session_state['last_km'] = km_in
            st.balloons()
        except:
            st.error("❌ Bağlantı hatası!")

        # SERTİFİKA
        with st.container(border=True):
            st.header(f"🏆 TUR SONUÇLARI")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Mesafe", f"{km_in} KM")
            m2.metric("Puan", puan)
            m3.metric("Yükselti", f"{yuk_in} m")
            m4.metric("Yağ", f"{yag} gr")

st.caption("Erkoz Yazılım © 2026 | v48.6 - Multi-Generation Support")
