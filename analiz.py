import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Erkoz Bisiklet Analiz", page_icon="🚴", layout="wide")

st.title("🚴 Erkoz Hakkaniyetli Bisiklet Analiz & Şampiyonlar Ligi")
st.subheader("Gerçek Sporcu Emeği Ölçüm Sistemi - İzmir 2026")

# 2. Giriş Alanları (Sidebar)
st.sidebar.header("📋 Sürücü ve Ekipman")
surucu_adi = st.sidebar.text_input("Sürücü Adı Soyadı", "Ahmet Tatar")
bisiklet_marka = st.sidebar.text_input("Bisiklet Marka / Model", "Salcano XRS001")

st.sidebar.markdown("---")
st.sidebar.subheader("⌚ Saat Verileri")
saat_kalori = st.sidebar.number_input("Cihaz Toplam Kalori (Yoksa 0)", min_value=0, value=0)

kalori_seviyesi = st.sidebar.selectbox("🔥 Sürüş Şiddeti", ["Az Kalori (Keyfi)", "Normal Kalori (Tempo)", "Çok Kalori (Performans)"], index=1)
ruzgar_sertligi = st.sidebar.select_slider("🌬️ İzmir Rüzgar Sertliği", options=["Sakin", "Tatlı Sert", "Yamanlar Esintisi", "Urla Fırtınası"], value="Tatlı Sert")

col1, col2 = st.columns(2)
with col1:
    yas = st.number_input("Yaşınız", min_value=10, max_value=100, value=60)
    kilo = st.number_input("Kilonuz (kg)", min_value=30.0, max_value=200.0, value=80.0)
    boy = st.number_input("Boyunuz (m)", min_value=1.0, max_value=2.5, value=1.75)
with col2:
    haftalik_km = st.number_input("Haftalık KM", min_value=0, value=255)
    haftalik_irtifa = st.number_input("Haftalık İrtifa (Metre)", min_value=0, value=1049)
    bisiklet_agirligi = st.slider("Bisiklet Ağırlığı (kg)", 6.0, 20.0, 9.42)

ruzgar_pozisyonu = st.selectbox("Grup İçi Pozisyon", ["Solo", "Kahraman (Önde)", "Takipçi"])

# 3. Hesaplama Fonksiyonu
def hesaplamalari_yap():
    agirlik_katsayisi = bisiklet_agirligi / 7.0 
    ruzgar_bonusu = 1.30 if "Kahraman" in ruzgar_pozisyonu else 1.0
    yas_bonusu = 1.0 + (yas / 100) 
    kalori_carpan = {"Az Kalori (Keyfi)": 1.0, "Normal Kalori (Tempo)": 1.15, "Çok Kalori (Performans)": 1.35}[kalori_seviyesi]
    ruzgar_carpan = {"Sakin": 1.0, "Tatlı Sert": 1.10, "Yamanlar Esintisi": 1.20, "Urla Fırtınası": 1.40}[ruzgar_sertligi]
    
    puan = int(((haftalik_km * 0.5) + (haftalik_irtifa * 0.1)) * agirlik_katsayisi * ruzgar_bonusu * yas_bonusu * kalori_carpan * ruzgar_carpan)
    hesaplanan_kalori = saat_kalori if saat_kalori > 0 else (haftalik_km * 35 + haftalik_irtifa * 0.5)
    yag_yuzdesi = {"Az Kalori (Keyfi)": 0.50, "Normal Kalori (Tempo)": 0.40, "Çok Kalori (Performans)": 0.30}[kalori_seviyesi]
    yag_gram = round((hesaplanan_kalori * yag_yuzdesi) / 9, 1)
    
    return puan, yag_gram, int(hesaplanan_kalori)

final_skor, yakilan_yag, toplam_kalori = hesaplamalari_yap()

# 4. Veritabanı ve Yönetim Fonksiyonları
dosya_adi = "erkoz_lig.csv"

def veriyi_kaydet(ad, puan, yag):
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M")
    yeni_veri = pd.DataFrame([[ad, puan, yag, tarih]], columns=["Sürücü", "Puan", "Yağ (g)", "Tarih"])
    if not os.path.isfile(dosya_adi):
        yeni_veri.to_csv(dosya_adi, index=False)
    else:
        yeni_veri.to_csv(dosya_adi, mode='a', header=False, index=False)

def son_kaydi_sil():
    if os.path.isfile(dosya_adi):
        df = pd.read_csv(dosya_adi)
        if not df.empty:
            df = df[:-1] # Son satırı at
            df.to_csv(dosya_adi, index=False)
            return True
    return False

# --- RAPOR OLUŞTURMA ---
if st.button("🚀 Hakkaniyetli Raporu Oluştur ve Lige Kaydol"):
    st.balloons()
    veriyi_kaydet(surucu_adi, final_skor, yakilan_yag)
    st.success("Rapor oluşturuldu ve Şampiyonlar Ligi'ne kaydedildi!")

# --- ŞAMPİYONLAR LİGİ VE YÖNETİM ---
st.markdown("---")
st.header("🏆 Erkoz Hakkaniyet Şampiyonlar Ligi")

if os.path.isfile(dosya_adi):
    df = pd.read_csv(dosya_adi)
    if not df.empty:
        # En yüksek puanlıları sırala
        sirali_df = df.sort_values(by="Puan", ascending=False)
        st.dataframe(sirali_df, use_container_width=True)
        
        # YÖNETİCİ PANELİ (Silme İşlemleri)
        st.sidebar.markdown("---")
        st.sidebar.subheader("🛠️ Yönetici Paneli")
        if st.sidebar.button("❌ Son Kaydı Sil"):
            if son_kaydi_sil():
                st.sidebar.warning("Son kayıt silindi. Sayfayı yenileyin.")
                st.rerun()
        
        if st.sidebar.button("🗑️ Tüm Listeyi Sıfırla"):
            os.remove(dosya_adi)
            st.sidebar.error("Tüm veriler temizlendi!")
            st.rerun()
    else:
        st.info("Henüz ligde kayıt yok.")
else:
    st.info("Lige ilk kaydı bekliyoruz!")