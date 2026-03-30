import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v28.3 - VKE GÖSTERGESİ VE TAM PROFİL ENTEGRASYONU
st.set_page_config(page_title="Erkoz Analiz v28.3", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (TAM PROFİL & VKE HESAPLAMA) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

# Anlık VKE Hesaplama ve Sidebar Gösterimi
vke_hesap = round(kilo / ((boy/100)**2), 1)
st.sidebar.metric("Vücut Kitle İndeksi (VKE)", vke_hesap)

st.sidebar.markdown("---")
st.sidebar.header("🚲 Donanım & Alışkanlık")
bisiklet_markasi = st.sidebar.text_input("Bisiklet Markası", value="Mosso Black Edition")
bisiklet_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5)
haftalik_km = st.sidebar.number_input("Haftalık Ortalama KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme Düzeyi (1-3)", [1, 2, 3], index=2)

st.sidebar.markdown("---")
st.sidebar.header("🔑 Yönetici Girişi")
sifre = st.sidebar.text_input("Şifre", type="password")
if st.sidebar.button("Yönetici Panelini Aç"):
    if sifre == "erkoz":
        st.session_state.is_admin = True
        st.sidebar.success("Panel Aktif!")
    else:
        st.sidebar.error("Hatalı!")

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Grup Terminali")

if st.session_state.is_admin:
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:50px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold; font-size:16px;">📊 GÜNCEL EXCEL TABLOSUNU AÇ</button></a>', unsafe_allow_html=True)
    st.markdown("---")

st.subheader("🚀 Yeni Sürüş Analizi")
col1, col2 = st.columns(2)

with col1:
    surus_km = st.number_input("Yapılan Mesafe (KM)", value=157.0, step=0.1)
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    kalori = st.number_input("Yakılan Toplam Kalori", value=3150)

with col2:
    yukselti = st.number_input("Toplam Yükselti (m)", value=1049)
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    st.info(f"Profil: {ad_soyad} | VKE: {vke_hesap}")

st.markdown("---")

# --- ANALİZ VE KAYIT ---
if st.button("🏁 ANALİZİ TAMAMLA VE EXCEL'E GÖNDER"):
    # --- PUAN HESAPLAMA MOTORU ---
    yas = date.today().year - dogum_tarihi.year
    
    # Efsane yüksek puan katsayıları
    std_puan = ((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + (vke_hesap / 5)
    km_puani = (std_puan / surus_km) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    ruzgar_katkisi = (km_puani / 10) * kademe
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    kalori_bonusu = (kalori / 1000) * 1.5
    
    final_puan = round(km_puani + ruzgar_katkisi + yukselti_puani + kalori_bonusu, 3)
    yakilan_yag = round((kalori * 0.8) / 9, 1)

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
        response = requests.post(SCRIPT_URL, json=payload, timeout=15)
        if response.status_code == 200:
            
            # BAŞARI BELGESİ (VKE DAHİL)
            st.markdown(f"""
            <div style="background-color:#0E1117; border:5px solid #FF4B4B; padding:25px; border-radius:20px; color:white; text-align:center; font-family:sans-serif;">
                <h1 style="color:#FF4B4B; margin-top:0;">🏆 BAŞARI SERTİFİKASI</h1>
                <h2 style="margin:5px 0;">{ad_soyad}</h2>
                <p style="color:#888;">{surus_tarihi} | {bisiklet_markasi}</p>
                
                <hr style="border:0.5px solid #333; margin:20px 0;">
                
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:10px; margin-bottom:20px;">
                    <div style="background:#1F2937; padding:10px; border-radius:10px;">
                        <small style="color:#888;">Mesafe</small><br><b>{surus_km} KM</b>
                    </div>
                    <div style="background:#1F2937; padding:10px; border-radius:10px;">
                        <small style="color:#888;">Yükselti</small><br><b>{yukselti} M</b>
                    </div>
                    <div style="background:#1F2937; padding:10px; border-radius:10px;">
                        <small style="color:#888;">VKE</small><br><b style="color:#FFD700;">{vke_hesap}</b>
                    </div>
                </div>

                <div style="background:linear-gradient(145deg, #FF4B4B, #8B0000); padding:20px; border-radius:15px; box-shadow: 0 4px 15px rgba(255,75,75,0.3);">
                    <p style="margin:0; font-size:14px; opacity:0.8;">GENEL PERFORMANS SKORU</p>
                    <h1 style="font-size:65px; margin:0; font-weight:bold;">{final_puan}</h1>
                </div>
                
                <div style="margin-top:20px; font-size:15px; color:#32CD32; font-weight:bold;">
                    🔥 Yakılan Yağ: {yakilan_yag} gr | 🔋 Kalori: {kalori} kcal | 💨 Rüzgar: {ruzgar_hizi} km/h
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Veriler Excel'e işlendi ve VKE analiz edildi!")
        else:
            st.error(f"Hata: {response.status_code}")
    except Exception as e:
        st.error(f"Bağlantı hatası: {e}")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")
