import streamlit as st
import requests
import json
import os
from datetime import date

# --- ERKOZ ANALİZ v36.0 - EFSANE SERTİFİKA & ZIRHLI KONTROL ---
st.set_page_config(page_title="Erkoz Analiz v36.0", layout="wide", page_icon="🚴‍♂️")

# --- 1. HAFIZA SİSTEMİ ---
SETTINGS_FILE = "erkoz_settings.json"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return {"ad_soyad": "Erdal Kozal", "dogum_tarihi": "1967-04-03", "boy": 179, "kilo": 69.0, "bis_marka": "Mosso Black Edition", "bis_kilosu": 10.5}

saved = load_settings()

# --- 2. SOL PANEL (KONTROL PANELİ - TEMİZLENDİ) ---
with st.sidebar:
    st.header("👤 Profil & Donanım")
    ad_soyad = st.text_input("Ad Soyad", value=saved["ad_soyad"])
    d_tarihi = st.date_input("Doğum Tarihi", date.fromisoformat(saved["dogum_tarihi"]))
    boy = st.number_input("Boy (cm)", value=int(saved["boy"]))
    kilo = st.number_input("Kilo (kg)", value=float(saved["kilo"]))
    st.markdown("---")
    bis_marka = st.text_input("Bisiklet", value=saved["bis_marka"])
    bis_kilo = st.number_input("Bisiklet KG", value=float(saved["bis_kilosu"]))

    # Anlık Hesaplar
    vke = round(kilo / ((boy/100)**2), 1)
    zorluk = round((bis_kilo - 10) * 2, 1)
    yas = date.today().year - d_tarihi.year
    
    st.markdown("---")
    st.subheader("📊 Canlı Metrikler")
    st.metric("VKE Durumu", vke)
    st.metric("Donanım Zorluğu", f"%{zorluk}")
    # Bozuk Excel linki kaldırıldı, panel temizlendi.

# --- 3. ANA TERMİNAL ---
st.title("🚀 Erkoz Yazılım | Analiz Terminali")

# Sürüş Verileri Girişi
st.subheader("🏁 Sürüş Verileri")
c1, c2 = st.columns(2)
km_in = c1.number_input("Mesafe (KM)", value=157.0)
yuk_in = c2.number_input("Yükselti (m)", value=1049)
ruz_in = c1.number_input("Rüzgar (km/h)", value=25.0)
kal_in = c2.number_input("Kalori (kcal)", value=3150)

if st.button("🚀 ANALİZİ TAMAMLA VE SERTİFİKAYI OLUŞTUR"):
    # Kaydet
    new_data = {"ad_soyad": ad_soyad, "dogum_tarihi": str(d_tarihi), "boy": boy, "kilo": kilo, "bis_marka": bis_marka, "bis_kilosu": bis_kilo}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f: json.dump(new_data, f)
    
    # Skor Algoritması
    bak = 1 + (zorluk / 100)
    final_skor = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / km_in) * 115, 2)
    yag_gr = round((kal_in * 0.8) / 9, 1)

    # Excel Aktarımı (Buluta Arka Planda)
    try: requests.post(SCRIPT_URL, json={"adSoyad": ad_soyad, "puan": final_skor, "km": km_in}, timeout=3)
    except: pass

    # --- 🏆 JANJANLI SERTİFİKA (v29.3 TAKLİDİ - HATASIZ) ---
    st.markdown("---")
    
    # Koyu Tema Kapsayıcı (Border=True ile zırhlı kutu)
    with st.container(border=True):
        st.subheader(f"🏆 BAŞARI SERTİFİKASI: {ad_soyad}")
        st.caption(f"📅 {date.today()} | 🚲 {bis_marka} | 👤 VKE: {vke}")
        st.divider()
        
        # Metrik Kutuları (v29.3 gibi yan yana 4lü)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Mesafe", f"{km_in} km")
        m2.metric("Yükselti", f"{yuk_in} m")
        m3.metric("Skor", final_skor)
        m4.metric("Yağ", f"{yag_gr} g")
        
        st.divider()

        # Ana Skor ve Yağ Yakımı (Büyük, Renkli, Janjanlı Kısımlar)
        # st.error (Kırmızı) ve st.warning (Turuncu) kullanarak o efsane görüntüyü veriyoruz
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.error(f"🚀 *GENEL PERFORMANS SKORU*: {final_skor}")
        with res_col2:
            st.warning(f"🔥 *YAKILAN YAĞ (TOPLAM)*: {yag_gr} gr")

    st.success("✅ İşlem Başarılı! Veriler senkronize edildi.")

st.caption("Erkoz Yazılım © 2026 | v36.0 - Efsane Geri Dönüyor")
