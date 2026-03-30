import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v27.0 - YENİ KÖPRÜ VE TAM HİZALAMA
st.set_page_config(page_title="Erkoz Analiz v27.0", layout="wide", page_icon="🚴‍♂️")

# --- YENİ URL ENTEGRE EDİLDİ ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzUZvqPnAzqiFfdUFGuKmvHQKPjsNC3gDHNYO5KO0yOgIq_737ST5_5yEDa5UNz7guobg/exec"

# --- PANEL & HESAPLAMA ---
st.sidebar.header("👤 Gizli Hesaplama Verileri")
st.sidebar.info("Boy, kilo ve yaş verileri sadece puan hesaplar, Excel'e gönderilmez.")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)
st.sidebar.markdown("---")
bisiklet_markasi = st.sidebar.text_input("Bisiklet Markası", value="Mosso Black Edition")
bisiklet_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5)
haftalik_km = st.sidebar.number_input("Haftalık KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme (1-3)", [1, 2, 3], index=2)

st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Grup Terminali")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Sürüş Detayları")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=157.0)
    kalori = st.number_input("Yakılan Kalori (kcal)", value=3150)
with col2:
    st.subheader("🌤️ Koşullar")
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    yukselti = st.number_input("Tırmanış (m)", value=1049)

if st.button("🚀 KAYDI TAMAMLA VE TABLOYU GÜNCELLE"):
    # Arka Plan Hesaplama Motoru (Erkoz Ar-Ge)
    yas = date.today().year - dogum_tarihi.year
    vke = round(kilo / ((boy/100)**2), 1)
    std_puan = round(((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + (vke / 5), 3)
    km_p = round((std_puan / surus_km) * 100, 3)
    rz_p = round((km_p / 10) * kademe, 3)
    yk_p = round((yukselti / 1000 * 0.3) + 1, 3)
    final_puan = round(km_p + rz_p + yk_p, 3)

    # --- TAM HİZALANMIŞ 8 SÜTUNLU PAKET (A-H ARASI) ---
    payload = {
        "adSoyad": ad_soyad, 
        "bisikleti": bisiklet_markasi, 
        "bisKilosu": bisiklet_kilosu,
        "surusTarihi": str(surus_tarihi), 
        "surusKM": surus_km, 
        "ruzgarHizi": ruzgar_hizi,
        "yukselti": yukselti, 
        "puan": final_puan
    }
    
    try:
        # Veriyi Google Apps Script'e gönder
        requests.post(SCRIPT_URL, json=payload)
        st.balloons()
        
        # --- BAŞARI BELGESİ (GÖRSEL) ---
        st.markdown(f"""
        <div style="background:#0E1117; border:5px double #FF4B4B; padding:20px; border-radius:15px; color:white; text-align:center;">
            <h2 style="color:#FF4B4B; margin-top:0;">🏆 ERKOZ BAŞARI BELGESİ</h2>
            <p style="font-size:18px;"><b>{ad_soyad}</b></p>
            <p style="color:#888;">{surus_tarihi} | {bisiklet_markasi}</p>
            <hr style="border:0.5px solid #333;">
            <div style="display:flex; justify-content:space-around; margin:15px 0;">
                <div><small style="color:#888;">Mesafe</small><br><b>{surus_km} KM</b></div>
                <div><small style="color:#888;">Yükselti</small><br><b>{yukselti} M</b></div>
                <div><small style="color:#888;">Rüzgar</small><br><b>{ruzgar_hizi} km/h</b></div>
            </div>
            <div style="background:#1F2937; padding:15px; border-radius:10px; border:2px solid #FF4B4B;">
                <small style="color:#888;">GENEL PERFORMANS SKORU</small>
                <h1 style="color:#FF4B4B; font-size:60px; margin:0;">{final_puan}</h1>
            </div>
            <p style="margin-top:15px; font-style:italic; color:#555;">Erkoz Yazılım Ar-Ge Onaylıdır.</p>
        </div>
        """, unsafe_allow_html=True)
        st.success("Kanka veriler yeni köprü üzerinden milimetrik olarak Excel'e işlendi!")
    except:
        st.error("Bağlantı hatası! Yeni URL'yi veya interneti kontrol et kanka.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")
