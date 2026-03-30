import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v27.6 - EKSİKSİZ TAM SÜRÜM
st.set_page_config(page_title="Erkoz Analiz v27.6", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (GİZLİ HESAPLAMA VERİLERİ) ---
st.sidebar.header("👤 Profil Ayarları")
st.sidebar.info("Buradaki veriler puanınızı etkiler ama Excel'e gitmez.")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

st.sidebar.markdown("---")
st.sidebar.header("🔑 Yönetici Girişi")
sifre = st.sidebar.text_input("Şifre", type="password")
if st.sidebar.button("Giriş"):
    if sifre == "erkoz":
        st.session_state.is_admin = True
        st.sidebar.success("Yönetici Yetkisi Verildi!")
    else:
        st.sidebar.error("Hatalı Şifre!")

# --- ANA EKRAN (GİRİŞ ALANLARI) ---
st.title("🚴‍♂️ Erkoz Yazılım - Grup Performans Terminali")
st.markdown("---")

# Eğer yöneticiyse Excel linkini göster
if st.session_state.is_admin:
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:45px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">📊 EXCEL LİSTESİNİ AÇ</button></a>', unsafe_allow_html=True)
    st.markdown("---")

st.subheader("🏁 Sürüş Bilgilerini Girin")
col1, col2 = st.columns(2)

with col1:
    surus_km = st.number_input("Yapılan Mesafe (KM)", value=157.0, step=0.1)
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0, step=0.5)
    bisiklet_markasi = st.text_input("Bisiklet Markası", value="Mosso Black Edition")

with col2:
    yukselti = st.number_input("Toplam Yükselti (m)", value=1049, step=1)
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    bisiklet_kilosu = st.number_input("Bisiklet Ağırlığı (kg)", value=10.5, step=0.1)

st.markdown("---")

# --- HESAPLAMA VE GÖNDERME ---
if st.button("🚀 SÜRÜŞÜ ANALİZ ET VE EXCEL'E KAYDET"):
    # Arka Plan Puan Motoru
    yas = date.today().year - dogum_tarihi.year
    vke = round(kilo / ((boy/100)**2), 1)
    
    # Performans Formülü
    std_puan = round(((yas + 20) / 100) * 3 + (vke / 5), 3)
    km_p = round((std_puan / surus_km) * 100, 3)
    rz_p = round((km_p / 10) * (2 if ruzgar_hizi > 15 else 1), 3)
    yk_p = round((yukselti / 1000 * 0.3) + 1, 3)
    final_puan = round(km_p + rz_p + yk_p, 3)

    # Excel'e gidecek 8 sütunluk paket
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
        with st.spinner('Veriler Google Tabloya işleniyor...'):
            response = requests.post(SCRIPT_URL, json=payload, timeout=15)
        
        if response.status_code == 200:
            st.balloons()
            st.success("✅ BAŞARILI! Veriler Excel'e milimetrik olarak işlendi.")
            
            # Sonuç Kartı
            st.markdown(f"""
            <div style="background:#0E1117; border:3px solid #FF4B4B; padding:20px; border-radius:15px; color:white; text-align:center;">
                <h2 style="color:#FF4B4B; margin:0;">🏆 PERFORMANS SKORU</h2>
                <h1 style="font-size:60px; margin:10px 0;">{final_puan}</h1>
                <p style="font-size:18px;">{ad_soyad} | {surus_km} KM | {yukselti} M</p>
                <p style="color:#888;">{bisiklet_markasi} ({bisiklet_kilosu} kg)</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ Hata Oluştu: {response.status_code}")
            
    except Exception as e:
        st.error(f"❌ Bağlantı Kesildi: {e}")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir Ar-Ge")
