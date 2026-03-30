import streamlit as st
from datetime import date
import requests

# ERKOZ ANALİZ v26.6 - SADE & PERFORMANS ODAKLI TABLO
st.set_page_config(page_title="Erkoz Analiz v26.6", layout="wide", page_icon="🚴‍♂️")

# --- AYARLAR ---
ADMIN_PASSWORD = "erkoz" 
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"
SHEETS_LINK = "https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M"

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- SOL PANEL (PROFİL & TEKNİK DETAYLAR) ---
st.sidebar.header("👤 Sürücü Profili")
ad_soyad = st.sidebar.text_input("Ad Soyad", value="Erdal Kozal")
dogum_tarihi = st.sidebar.date_input("Doğum Tarihi (Hesaplama İçin)", date(1967, 4, 3))
boy = st.sidebar.number_input("Boy (cm)", value=179)
kilo = st.sidebar.number_input("Kilo (kg)", value=69.0)

st.sidebar.markdown("---")
st.sidebar.header("🚲 Bisiklet Bilgileri")
bisiklet_modeli = st.sidebar.text_input("Bisiklet Markası", value="Mosso Black Edition")
bisiklet_kilosu = st.sidebar.number_input("Bisiklet Ağırlığı (kg)", value=10.5)
haftalik_km = st.sidebar.number_input("Haftalık Ortalama KM", value=200)
beslenme = st.sidebar.selectbox("Beslenme Düzeni (1-3)", [1, 2, 3], index=2)

st.sidebar.markdown("---")
st.sidebar.header("🔑 Yönetici Alanı")
sifre_denemesi = st.sidebar.text_input("Şifre", type="password")
if st.sidebar.button("Girişi Onayla"):
    if sifre_denemesi == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        st.sidebar.success("Yönetici Modu Aktif!")
    else:
        st.sidebar.error("Hatalı Şifre!")

# --- ANA EKRAN ---
st.title("🚴‍♂️ Erkoz Yazılım - Grup Performans Sistemi")
st.info("Kayıtlar doğrudan performans tablosuna işlenmektedir.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Sürüş Bilgileri")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=157.0)
    kalori = st.number_input("Yakılan Kalori (kcal)", value=3150)

with col2:
    st.subheader("🌤️ Koşullar")
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=25.0)
    kademe = 1 if ruzgar_hizi <= 15 else (2 if ruzgar_hizi <= 31 else 3)
    yukselti = st.number_input("Yükselti (m)", value=1049)

# --- ANALİZ VE KAYIT ---
if st.button("🚀 SÜRÜŞÜ KAYDET VE ANALİZ ET"):
    # Arka Plandaki Matematik (Kullanıcıya özel puan hesaplar)
    yas = date.today().year - dogum_tarihi.year
    vke = round(kilo / ((boy/100)**2), 1)
    vke_katkisi = round((vke / 100) * 20, 2)
    std_puan = round(((yas + 20) / 100) * 3 + (haftalik_km / 100) * 1.5 + (beslenme / 1) * 1.3 + vke_katkisi, 3)
    
    km_puani = round((std_puan / surus_km) * 100, 3)
    ruzgar_katkisi = round((km_puani / 10) * kademe, 3)
    yukselti_puani = round((yukselti / 1000 * 0.3) + 1, 3)
    kalori_bonusu = round((kalori / 1000) * 1.5, 3)
    yakilan_yag = round((kalori * 0.8) / 9, 1)
    
    final_puan = round(km_puani + ruzgar_katkisi + yukselti_puani + kalori_bonusu, 3)

    # --- SADELEŞTİRİLMİŞ PAYLOAD (SADECE İSTEDİĞİN SÜTUNLAR) ---
    payload = {
        "adSoyad": ad_soyad, 
        "bisikleti": bisiklet_modeli, 
        "bisKilosu": bisiklet_kilosu,
        "surusTarihi": str(surus_tarihi), 
        "surusKM": surus_km, 
        "ruzgarHizi": ruzgar_hizi,
        "yukselti": yukselti, 
        "puan": final_puan
    }
    
    try:
        requests.post(SCRIPT_URL, json=payload)
        st.balloons()
        
        # --- PRESTİJ BELGESİ (TAM GÖRSEL) ---
        cert_html = f"""
        <div style="background-color: #0E1117; border: 5px double #FF4B4B; padding: 20px; border-radius: 15px; font-family: sans-serif; color: white;">
            <h2 style="color: #FF4B4B; text-align: center; margin-top: 0;">🏆 ERKOZ PERFORMANS ANALİZİ</h2>
            <p style="text-align: center; color: #888;">Tarih: {surus_tarihi}</p>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span>Sürücü: <b>{ad_soyad}</b></span>
                <span>Bisiklet: <b>{bisiklet_modeli}</b></span>
            </div>
            <hr style="border: 0.5px solid #333; margin: 15px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="background:#161B22; padding:12px; border-radius:8px;">
                    <small style="color:#888">KM Puanı ({surus_km} KM):</small><br><b style="color:#00D4FF">{km_puani}</b>
                </div>
                <div style="background:#161B22; padding:12px; border-radius:8px;">
                    <small style="color:#888">Rüzgar ({ruzgar_hizi} km/h):</small><br><b style="color:#00D4FF">+{ruzgar_katkisi}</b>
                </div>
                <div style="background:#161B22; padding:12px; border-radius:8px;">
                    <small style="color:#888">Yükselti ({yukselti} M):</small><br><b style="color:#00D4FF">+{yukselti_puani}</b>
                </div>
                <div style="background:#161B22; padding:12px; border-radius:8px;">
                    <small style="color:#888">Yakılan Yağ:</small><br><b style="color:#32CD32">{yakilan_yag} Gram</b>
                </div>
            </div>
            <div style="margin-top: 20px; background: #1F2937; padding: 15px; border-radius: 10px; border: 2px solid #FF4B4B; text-align: center;">
                <small style="color:#888;">GENEL SÜRÜŞ SKORU</small>
                <h1 style="color: #FF4B4B; font-size: 55px; margin: 0;">{final_puan}</h1>
            </div>
            <div style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #333; display: flex; justify-content: space-between; align-items: center;">
                <b style="color: #FF4B4B;">Erkoz Yazılım Ar-Ge</b>
                <span style="color: #EEE;"><i>Erdal Kozal</i></span>
            </div>
        </div>
        """
        st.components.v1.html(cert_html, height=520)
        st.success("Veriler başarıyla performans tablosuna eklendi!")
    except:
        st.error("Excel bağlantı hatası!")

# --- YÖNETİCİ PANELİ ---
if st.session_state.is_admin:
    st.markdown("---")
    st.header("🏁 Erkoz Yönetici Paneli")
    st.markdown(f'<a href="{SHEETS_LINK}" target="_blank"><button style="width:100%; height:60px; background-color:#FF4B4B; color:white; border:none; border-radius:10px; font-size:18px; font-weight:bold; cursor:pointer;">📊 GRUP LİSTESİNİ AÇ</button></a>', unsafe_allow_html=True)

st.markdown("---")
st.caption("Erkoz Yazılım © 2026")
