import streamlit as st
from datetime import date
import requests
import pandas as pd

# ERKOZ ANALİZ v26.0 - YÖNETİCİ & GRUP KAYIT VERSİYONU
st.set_page_config(page_title="Erkoz Analiz v26.0", layout="wide", page_icon="🚴‍♂️")

# --- GİZLİ ŞİFRE ---
ADMIN_PASSWORD = "erkoz" # Burayı istediğin şifre yap kanka

st.title("🚴‍♂️ Erkoz Yazılım - Grup Performans Sistemi")
st.markdown("---")

# Google Apps Script URL (Senin tablonun linki)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx6UlQDdgybmd9UyNwyIE7Nx2JFXHn5pGMyXA8I_3Zg1zQA9SEYZPp_XFwLh_i63zhU4w/exec"

# --- MOTOR ---
def ruzgar_kademesi_bul(hiz):
    if hiz <= 15: return 1
    elif hiz <= 31: return 2
    else: return 3

# --- SOL PANEL (PROFİL VE YÖNETİM) ---
st.sidebar.header("👤 Sürücü Kayıt Paneli")
ad_soyad = st.sidebar.text_input("Ad Soyad", placeholder="Arkadaşın adını yazsın...")
boy = st.sidebar.number_input("Boy (cm)", value=175)
kilo = st.sidebar.number_input("Kilo (kg)", value=75.0)
bisiklet = st.sidebar.text_input("Bisiklet Modeli", value="Yol/Dağ Bisikleti")

st.sidebar.markdown("---")
st.sidebar.header("🔑 Yönetici Alanı")
admin_key = st.sidebar.text_input("Yönetici Şifresi", type="password")

# --- ANA EKRAN ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("📅 Sürüş Bilgileri")
    surus_tarihi = st.date_input("Sürüş Tarihi", date.today())
    surus_km = st.number_input("Yapılan KM", value=50.0)
    kalori = st.number_input("Yakılan Kalori", value=1500)

with col2:
    st.subheader("🌤️ Koşullar")
    ruzgar_hizi = st.number_input("Rüzgar Hızı (km/h)", value=15.0)
    kademe = ruzgar_kademesi_bul(ruzgar_hizi)
    if ruzgar_hizi > 0:
        st.info(f"Rüzgar Kademesi: {kademe}")
    yukselti = st.number_input("Yükselti (m)", value=500)

# --- VERİ KAYIT ---
if st.button("🚀 SÜRÜŞÜ ERKOZ SİSTEMİNE KAYDET"):
    if not ad_soyad:
        st.error("Lütfen Ad Soyad giriniz!")
    else:
        # Puanlama Mantığı (Genel Standart Üzerinden)
        vke = round(kilo / ((boy/100)**2), 1)
        vke_katkisi = round((vke / 100) * 20, 2)
        km_puani = round((10.0 / surus_km) * 100, 3) # Standart baz puan
        ruzgar_katkisi = round((km_puani / 10) * kademe, 3)
        yukselti_puani = round((yukselti / 1000 * 0.3) + 1, 3)
        kalori_bonusu = round((kalori / 1000) * 1.5, 3)
        yakilan_yag = round((kalori * 0.8) / 9, 1)
        
        final_puan = round(km_puani + ruzgar_katkisi + yukselti_puani + kalori_bonusu + vke_katkisi, 3)

        payload = {
            "adSoyad": ad_soyad, "boy": boy, "kilo": kilo, "bisiklet": bisiklet,
            "s_tarih": str(surus_tarihi), "s_km": surus_km, "ruzgar": ruzgar_hizi,
            "yukselti": yukselti, "puan": final_puan, "kalori": kalori, "yag": yakilan_yag
        }
        
        try:
            requests.post(SCRIPT_URL, json=payload)
            st.balloons()
            st.success(f"Tebrikler {ad_soyad}! Verilerin Erdal Kozal'ın ana tablosuna başarıyla işlendi.")
            
            # Arkadaşına özel mini sertifika (Senin imzanla)
            cert = f"""
            <div style="border: 4px solid #FF4B4B; padding: 15px; border-radius: 10px; background: #0E1117; color: white; text-align: center;">
                <h3>🏆 SÜRÜŞ ONAYLANDI</h3>
                <p>{ad_soyad} - {surus_km} KM - {final_puan} Puan</p>
                <small>Bu sürüş Erdal Kozal tarafından kayıt altına alınmıştır.</small>
            </div>
            """
            st.markdown(cert, unsafe_allow_html=True)
        except:
            st.error("Bağlantı hatası.")

# --- SADECE SANA ÖZEL: AYLIK LİSTE ÇEKME ---
if admin_key == ADMIN_PASSWORD:
    st.markdown("---")
    st.header("🏁 Erkoz Yönetici Paneli")
    if st.button("📊 TÜM LİSTEYİ GETİR (AY SONU RAPORU)"):
        try:
            # Google Sheets'ten verileri çekiyoruz (Bu kısım için Sheets linkini JSON formatında açman gerekebilir)
            # Şimdilik sana Excel'e gitmen için bir kısayol ve mesaj verelim
            st.info("Kanka, şifreyi doğru girdin. Tüm grup verileri şu an Google Sheets tablanda birikiyor.")
            st.write("👉 [Erkoz Bisiklet Analiz Tablosuna Git](https://docs.google.com/spreadsheets/d/1X_O9U0f2K6pD8uS-GjKq69L1A9Z0oWpXfRzG6oXjL8M)") # Senin tablo linkin
            # Buraya istersen veriyi direkt ekrana tablo olarak döken kodu da ekleyebiliriz kanka.
        except:
            st.write("Veri çekme işleminde bir hata oluştu.")

st.markdown("---")
st.caption("Erkoz Yazılım © 2026 | Sadece Yetkili Sürücüler İçindir.")
