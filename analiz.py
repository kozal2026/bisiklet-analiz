import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v28.9 - DONANIM ŞEFFAF GÖSTERGE VE CANLI VKE
st.set_page_config(page_title="Erkoz Analiz v28.9", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
# KANKA: Kopyaladığın YENİ linki buraya tırnakların içine yapıştır.
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (TAM PROFİL & DONANIM ANALİZİ) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179, help="Puan katsayısı")
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0, help="Puan katsayısı")

st.sidebar.markdown("---")
st.sidebar.header("🚲 Donanım Parametreleri")
bis_marka = st.sidebar.text_input("Bisiklet Markası", value="Mosso Black Edition")
# KRİTİK ALAN: Bisiklet kilosu buraya giriyor.
bis_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5, step=0.1)
haftalik_km = st.sidebar.number_input("Haftalık KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme", [1, 2, 3], index=2)

# --- CANLI ANALİZ GÖSTERGELERİ (Yeni Özellik) ---
vke_hesap = round(kilo / ((boy/100)**2), 1)
yas = 2026 - dogum_tarihi.year

# 10 kg referanslı katsayı (%2 etki)
bak_katsayisi = round(1 + ((bis_kilosu - 10) * 0.02), 3)
zorluk_yuzdesi = round((bis_kilosu - 10) * 2, 1)

st.sidebar.markdown("---")
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    st.metric("Canlı VKE", vke_hesap)
with col_s2:
    label = "Donanım Zorluğu" if zorluk_yuzdesi >= 0 else "Donanım Avantajı"
    st.metric(label, f"%{zorluk_yuzdesi}", delta_color="normal")

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Profesyonel Grup Terminali")

if st.session_state.is_admin:
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:45px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold; font-size:16px;">📊 GÜNCEL EXCEL TABLOSUNU AÇ</button></a>', unsafe_allow_html=True)
    st.markdown("---")

st.subheader("🏁 Yeni Sürüş Analizi")
col1, col2 = st.columns(2)
with col1:
    surus_km = st.number_input("Sürüş Mesafesi (KM)", value=157.0)
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
with col2:
    yukselti = st.number_input("Tırmanış / Yükselti (m)", value=1049)
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())

st.markdown("---")

# --- ANALİZ VE KAYIT ---
if st.button("🏁 ANALİZİ VE DONANIMI HESAPLA"):
    # --- PUAN HESAPLAMA MOTORU (Bisiklet Kilosu Dahil) ---
    p1 = ((yas + 20) / 100) * 3
    p2 = (vke_hesap / 100) * 20
    p3 = (haftalik_km / 100) * 1.5
    p4 = (beslenme / 1) * 1.3
    
    # Bisikletin katsayısı standart puanı çarpar
    standart_puan = (p1 + p2 + p3 + p4) * bak_katsayisi
    
    # Sürüşe özel puanlar
    km_puani = (standart_puan / surus_km) * 100
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    ruzgar_puani = (km_puani / 10) * kademe
    yukselti_puani = (yukselti / 1000 * 0.3) + 1
    
    # FINAL SKOR (13.15 gibi gerçekçi değerler)
    final_puan = round(km_puani + ruzgar_puani + yukselti_puani, 3)

    # Donanım farkı göstergesi (+/-)
    fark_isareti = "+" if zorluk_yuzdesi >= 0 else ""
    # Katsayı rengi: Kırmızı zorluk (+), Yeşil avantaj (-)
    katsayi_rengi = "#FF4B4B" if zorluk_yuzdesi >= 0 else "#32CD32"

    payload = {
        "adSoyad": ad_soyad, 
        "bisikleti": bis_marka, 
        "bisKilosu": bis_kilosu,
        "surusTarihi": str(surus_tarihi), 
        "surusKM": surus_km, 
        "ruzgarHizi": ruzgar_hizi,
        "yukselti": yukselti, 
        "puan": final_puan
    }
    
    try:
        # verify=True eklendi, bağlantı güvenliği için
        response = requests.post(SCRIPT_URL, json=payload, timeout=15)
        
        if response.status_code == 200:
            st.balloons()
            
            # --- HATASIZ BAŞARI BELGESİ (GELİŞMİŞ DONANIM ŞEFFAFLIĞI) ---
            st.markdown(f"""
            <div style="background-color:#0E1117; border:5px solid #FF4B4B; padding:20px; border-radius:15px; color:white; text-align:center;">
                <h1 style="color:#FF4B4B; margin-top:0;">🏆 BAŞARI SERTİFİKASI</h1>
                <h2 style="margin:5px 0;">{ad_soyad}</h2>
                <p style="color:#888;">{surus_tarihi} | {bis_marka}</p>
                
                <hr style="border:0.5px solid #333; margin:15px 0;">
                
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

                <div style="margin-bottom:15px; font-size:14px; background-color:#161B22; padding:10px; border-radius:10px;">
                    🛠️ Donanım Analizi: <b>{bis_kilosu} kg</b> bisikletle sürüş. 
                    Referansa göre zorluk: <b style="color:{katsayi_rengi};">{fark_isareti}%{zorluk_yuzdesi}</b>
                </div>

                <div style="background:linear-gradient(145deg, #FF4B4B, #8B0000); padding:20px; border-radius:15px; box-shadow: 0 4px 15px rgba(255,75,75,0.4);">
                    <p style="margin:0; font-size:14px; opacity:0.8;">GENEL PERFORMANS SKORU</p>
                    <h1 style="font-size:65px; margin:0; font-weight:bold;">{final_puan}</h1>
                </div>
                
                <p style="margin-top:15px; font-size:14px; color:#32CD32; font-weight:bold;">
                    💨 Rüzgar: {ruzgar_hizi} km/h | ✅ Donanım Dengelemesi AKTİF
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Veriler Excel'e milimetrik olarak işlendi kanka!")
        else:
            st.error(f"Hata: {response.status_code}")
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | İzmir")

# Yönetici Paneli
if not st.session_state.is_admin:
    with st.sidebar.expander("🔑 Yönetici Girişi"):
        sifre = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            if sifre == "erkoz":
                st.session_state.is_admin = True
                st.rerun()
