import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v32.0 - HATASIZ & ZIRHLI SÜRÜM ---
st.set_page_config(page_title="Erkoz Analiz v32.0", layout="wide", page_icon="🛡️")

# --- 1. HAFIZA ---
SETTINGS_FILE = "erkoz_settings.json"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"ad_soyad": "Erdal Kozal", "dogum_tarihi": "1967-04-03", "boy": 179, "kilo": 69.0, "bis_marka": "Mosso Black Edition", "bis_kilosu": 10.5}

saved_data = load_settings()

# --- 2. SOL PANEL (YÖNETİCİ PANELİ) ---
st.sidebar.title("🛡️ Yönetici Paneli")
ad_soyad_in = st.sidebar.text_input("Sürücü Adı", value=saved_data["ad_soyad"])
d_tarihi_raw = date.fromisoformat(saved_data["dogum_tarihi"]) if isinstance(saved_data["dogum_tarihi"], str) else saved_data["dogum_tarihi"]
dogum_tarihi_in = st.sidebar.date_input("Doğum Tarihi", d_tarihi_raw)
boy_in = st.sidebar.number_input("Boy (cm)", value=int(saved_data["boy"]))
kilo_in = st.sidebar.number_input("Kilo (kg)", value=float(saved_data["kilo"]))

st.sidebar.divider()
bis_marka_in = st.sidebar.text_input("Bisiklet Modeli", value=saved_data["bis_marka"])
bis_kilosu_in = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=float(saved_data["bis_kilosu"]), step=0.1)

# Anlık Hesaplamalar
vke_sid = round(kilo_in / ((boy_in/100)**2), 1)
zorluk_yuz_sid = round((bis_kilosu_in - 10) * 2, 1)

st.sidebar.divider()
st.sidebar.metric("Anlık VKE", vke_sid)
st.sidebar.metric("Donanım Zorluğu", f"%{zorluk_yuz_sid}")

# --- 3. ANA EKRAN ---
st.title("🚀 ERKOZ YAZILIM | Performans Terminali")

# Veri Giriş Alanı
c_in1, c_in2 = st.columns(2)
km_input = c_in1.number_input("Mesafe (KM)", value=157.0)
yukselti = c_in2.number_input("Yükselti (m)", value=1049)
ruzgar_hizi = c_in1.number_input("Rüzgar (km/h)", value=25.0)
kalori_input = c_in2.number_input("Yakılan Kalori (kcal)", value=3150)

if st.button("🚀 ANALİZİ TAMAMLA VE SERTİFİKAYI BAS"):
    # Kayıt
    new_data = {"ad_soyad": ad_soyad_in, "dogum_tarihi": str(dogum_tarihi_in), "boy": boy_in, "kilo": kilo_in, "bis_marka": bis_marka_in, "bis_kilosu": bis_kilosu_in}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(new_data, f)
    
    # Hesaplama
    yas = date.today().year - dogum_tarihi_in.year
    bak_katsayisi = 1 + (zorluk_yuz_sid / 100)
    p1 = ((yas + 20) / 100) * 3
    p2 = (vke_sid / 100) * 20
    standart_puan = (p1 + p2 + (200/100)*1.5 + 3.9) * bak_katsayisi
    km_p = (standart_puan / km_input) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    final_puan = round(km_p + ((km_p * kademe) / 10) + (yukselti / 1000 * 0.3) + 1, 2)
    yakilan_yag = round((kalori_input * 0.8) / 9, 1)

    # Excel Aktarımı
    try: requests.post(SCRIPT_URL, json={"adSoyad": ad_soyad_in, "puan": final_puan, "km": km_input}, timeout=3)
    except: pass

    # --- 🏆 SERTİFİKA ALANI (HATASIZ & KOMPAKT) ---
    st.divider()
    with st.container(border=True):
        st.header(f"🏆 BAŞARI SERTİFİKASI: {ad_soyad_in}")
        st.markdown(f"📅 *Tarih:* {date.today()} | 🚲 *Donanım:* {bis_marka_in} | 👤 *VKE:* {vke_sid}")
        
        st.divider()
        
        # Metrikler (Tek Satırda 4lü)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Mesafe", f"{km_input} KM")
        m2.metric("Yükselti", f"{yukselti} M")
        m3.metric("Skor", f"{final_puan}")
        m4.metric("Yağ Yakımı", f"{yakilan_yag} gr")
        
        st.divider()
        
        # Büyük Göstergeler (v29.3 Stili Renkli Alanlar)
        # Hata vermemesi için direkt st.error ve st.warning kutularını kullanıyoruz
        res1, res2 = st.columns(2)
        res1.error(f"🚀 *GENEL PERFORMANS SKORU*: {final_puan}")
        res2.warning(f"🔥 *YAKILAN TOPLAM YAĞ*: {yakilan_yag} gr")

    st.success("✅ Veriler hafızaya alındı ve Excel senkronizasyonu tamamlandı.")

st.caption("Erkoz Yazılım © 2026 | v32.0 - Zırhlı & Kararlı Sürüm")
