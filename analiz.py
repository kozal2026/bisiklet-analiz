[18:28, 30.03.2026] Erdal: import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v28.4 - SERTİFİKA GÖRÜNTÜ HATASI GİDERİLDİ
st.set_page_config(page_title="Erkoz Analiz v28.4", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (TAM PROFİL & CANLI VKE) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

# VKE Hesaplama
vke_hesap = round(kilo / ((boy/100)**2), 1)
st.sidebar.metric("Vücut Kitle İndeksi (VKE)", vke_hesap)

st.sidebar.markdown("---")
st.sidebar.header("🚲 Ekipman & Alışkanlık")
bis_marka = st.sidebar.text_input("Bisiklet", value="Mosso Black Edition")
bis_kilo = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5)
haftalik_km = st.sidebar.number_input("Haftalık KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme", [1, 2, 3], index=2)

st.sidebar.markdown("---")
if st.sidebar.button("Yönetici Çıkışı"):
    st.session_state.is_admin = False

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Grup Terminali")

# Şifre Girişi (Sadece kapalıysa göster)
if not st.session_state.is_admin:
    sifre = st.sidebar.text_input("Yönetici Şifresi", type="password")
    if st.sidebar.button("Paneli Aç"):
        if sifre == "erkoz":
            st.session_state.is_admin = True
            st.rerun()

if st.session_state.is_admin:
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:45px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">📊 EXCEL LİSTESİNE GİT</button></a>', unsafe_allow_html=True)
    st.markdown("---")

# Giriş Alanları
col1, col2 = st.columns(2)
with col1:
    km = st.number_input("Sürüş Mesafesi (KM)", value=157.0)
    ruzgar = st.number_input("Rüzgar (km/h)", value=25.0)
with col2:
    yukselti = st.number_input("Tırmanış (m)", value=1049)
    kalori = st.number_input("Kalori", value=3150)

# --- KAYIT VE SERTİFİKA ---
if st.button("🚀 ANALİZİ TAMAMLA"):
    # Puan Motoru
    yas = date.today().year - dogum_tarihi.year
    std = ((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + (vke_hesap / 5)
    p_km = (std / km) * 100
    kademe = 1 if ruzgar <= 15 else (2 if ruzgar <= 31 else 3)
    p_ruzgar = (p_km / 10) * kademe
    p_yuk = (yukselti / 1000 * 0.3) + 1
    p_kal = (kalori / 1000) * 1.5
    
    final_puan = round(p_km + p_ruzgar + p_yuk + p_kal, 3)
    yag = round((kalori * 0.8) / 9, 1)

    payload = {"adSoyad": ad_soyad, "bisikleti": bis_marka, "bisKilosu": bis_kilo, "surusTarihi": str(date.today()), "surusKM": km, "ruzgarHizi": ruzgar, "yukselti": yukselti, "puan": final_puan}
    
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=15)
        
        # --- HATASIZ SERTİFİKA TASARIMI ---
        # Burada f-string hatasını önlemek için güvenli HTML kullandım
        st.markdown(f"""
        <div style="background-color:#111; border:4px solid #FF4B4B; padding:20px; border-radius:15px; color:white; text-align:center;">
            <h1 style="color:#FF4B4B; margin:0;">🏆 BAŞARI SERTİFİKASI</h1>
            <h2 style="margin:10px 0;">{ad_soyad}</h2>
            <p style="color:#888;">{date.today()} | {bis_marka}</p>
            <hr style="border:0.5px solid #333;">
            <table style="width:100%; color:white; margin:15px 0;">
                <tr>
                    <td><small>Mesafe</small><br><b>{km} KM</b></td>
                    <td><small>Yükselti</small><br><b>{yukselti} M</b></td>
                    <td><small>VKE</small><br><b style="color:#FFD700;">{vke_hesap}</b></td>
                </tr>
            </table>
            <div style="background:linear-gradient(to right, #FF4B4B, #8B0000); padding:15px; border-radius:10px;">
                <p style="margin:0; font-size:14px;">PERFORMANS SKORU</p>
                <h1 style="margin:0; font-size:55px;">{final_puan}</h1>
            </div>
            <p style="margin-top:15px; color:#32CD32;">🔥 {yag} gr Yağ Yakıldı | 🔋 {kalori} kcal</p>
        </div>
        """, unsafe_allow_html=True)
        st.success("Veri Excel'e uçtu!")
    except:
        st.error("Bağlantı hatası!")

st.caption("Erkoz Yazılım © 2026")
[18:39, 30.03.2026] Erdal: import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v28.6 - BİSİKLET KİLOSU PERFORMANSA DAHİL EDİLDİ
st.set_page_config(page_title="Erkoz Analiz v28.6", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycb6ZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (TAM PROFİL & BİSİKLET PARAMETRELERİ) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

# VKE ve Yaş
vke_hesap = round(kilo / ((boy/100)**2), 1)
yas = 2026 - dogum_tarihi.year

st.sidebar.markdown("---")
st.sidebar.header("🚲 Donanım Analizi")
bis_marka = st.sidebar.text_input("Bisiklet Modeli", value="Mosso Black Edition")
bis_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5, step=0.1)
haftalik_km = st.sidebar.number_input("Haftalık KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme", [1, 2, 3], index=2)

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Donanım Odaklı Performans")

if st.session_state.is_admin:
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:45px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">📊 EXCEL LİSTESİNİ AÇ</button></a>', unsafe_allow_html=True)

st.subheader("📅 Sürüş Bilgileri")
col1, col2 = st.columns(2)
with col1:
    km_input = st.number_input("Mesafe (KM)", value=157.0)
    ruzgar_hizi = st.number_input("Rüzgar (km/h)", value=25.0)
with col2:
    yukselti = st.number_input("Yükselti (m)", value=1049)
    surus_tarihi = st.date_input("Tarih", date.today())

# --- YENİ HESAPLAMA MOTORU ---
if st.button("🚀 ANALİZİ VE DONANIMI HESAPLA"):
    # 1. Bisiklet Kilo Bonus/Ceza Sistemi
    # 10 kiloyu baz alıyoruz. Her +1 kilo sürüşü %2 zorlaştırır.
    bisiklet_katsayisi = 1 + ((bis_kilosu - 10) * 0.02)
    
    # 2. Standart Puan (Excel tabandaki temelimiz)
    p1 = ((yas + 20) / 100) * 3
    p2 = (vke_hesap / 100) * 20
    p3 = (haftalik_km / 100) * 1.5
    p4 = (beslenme / 1) * 1.3
    standart_puan = (p1 + p2 + p3 + p4) * bisiklet_katsayisi # Donanım etkisi eklendi
    
    # 3. Sürüş Puanları
    km_puani = (standart_puan / km_input) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    ruzgar_puani = (km_puani * kademe) / 10
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    
    # FINAL SKOR
    genel_puan = round(km_puani + ruzgar_puani + yukselti_puani, 3)

    # --- SERTİFİKA (GELİŞMİŞ) ---
    st.markdown(f"""
    <div style="background-color:#0E1117; border:5px solid #FF4B4B; padding:25px; border-radius:20px; color:white; text-align:center;">
        <h1 style="color:#FF4B4B; margin:0;">🏆 BAŞARI SERTİFİKASI</h1>
        <h2 style="margin:5px 0;">{ad_soyad}</h2>
        <p style="color:#888;">{bis_marka} ({bis_kilosu} kg) | {surus_tarihi}</p>
        <hr style="border:0.5px solid #333; margin:20px 0;">
        <div style="display:grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap:10px; margin-bottom:20px;">
            <div style="background:#1F2937; padding:10px; border-radius:10px;"><small>KM</small><br><b>{km_input}</b></div>
            <div style="background:#1F2937; padding:10px; border-radius:10px;"><small>Yükselti</small><br><b>{yukselti}</b></div>
            <div style="background:#1F2937; padding:10px; border-radius:10px;"><small>VKE</small><br><b>{vke_hesap}</b></div>
            <div style="background:#1F2937; padding:10px; border-radius:10px;"><small>Bis.Kilo</small><br><b style="color:#FFD700;">{bis_kilosu}</b></div>
        </div>
        <div style="background:linear-gradient(145deg, #FF4B4B, #8B0000); padding:20px; border-radius:15px; box-shadow: 0 4px 15px rgba(255,75,75,0.4);">
            <p style="margin:0; font-size:14px; opacity:0.8;">BİSİKLET AĞIRLIĞI DAHİL PERFORMANS SKORU</p>
            <h1 style="font-size:65px; margin:0; font-weight:bold;">{genel_puan}</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sheets Gönderimi
    payload = {"adSoyad": ad_soyad, "bisikleti": bis_marka, "bisKilosu": bis_kilosu, "surusTarihi": str(surus_tarihi), "surusKM": km_input, "ruzgarHizi": ruzgar_hizi, "yukselti": yukselti, "puan": genel_puan}
    try:
        requests.post(SCRIPT_URL, json=payload, timeout=10)
        st.success(f"✅ Bisiklet kilosu ({bis_kilosu} kg) hesaplamaya katıldı!")
    except:
        st.error("Gönderim hatası!")

# Yönetici Paneli
if not st.session_state.is_admin:
    with st.sidebar.expander("🔑 Yönetici Girişi"):
        if st.text_input("Şifre", type="password") == "erkoz":
            st.session_state.is_admin = True
            st.rerun()
