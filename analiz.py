import streamlit as st
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Erkoz Bisiklet Analiz", page_icon="🚴")

st.title("🚴 Erkoz Hakkaniyetli Bisiklet Analiz")
st.subheader("Gerçek Sporcu Emeği Ölçüm Sistemi")

# 2. Giriş Alanları (Sol Menü - Sidebar)
st.sidebar.header("📋 Sürücü ve Ekipman")
surucu_adi = st.sidebar.text_input("Sürücü Adı Soyadı", "Ahmet Tatar")
bisiklet_marka = st.sidebar.text_input("Bisiklet Marka / Model", "Salcano XRS001")

# YENİ: Akıllı Saat Kalori Girişi
st.sidebar.markdown("---")
st.sidebar.subheader("⌚ Saat Verileri")
saat_kalori = st.sidebar.number_input("Cihazda Görün Toplam Kalori (Yoksa 0)", min_value=0, value=0, help="Huawei Fit 3, Garmin veya Apple Watch verisi.")

kalori_seviyesi = st.sidebar.selectbox(
    "🔥 Sürüş Şiddeti (Efor)", 
    ["Az Kalori (Keyfi)", "Normal Kalori (Tempo)", "Çok Kalori (Performans)"],
    index=1
)

ruzgar_sertligi = st.sidebar.select_slider(
    "🌬️ İzmir Rüzgar Sertliği",
    options=["Sakin", "Tatlı Sert", "Yamanlar Esintisi", "Urla Fırtınası"],
    value="Tatlı Sert"
)

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

# 3. Hesaplama Mantığı (Erkoz 2026 + Yağ Yakım Algoritması)
def hesaplamalari_yap():
    # Temel Puanlama
    agirlik_katsayisi = bisiklet_agirligi / 7.0 
    ruzgar_bonusu = 1.30 if "Kahraman" in ruzgar_pozisyonu else 1.0
    yas_bonusu = 1.0 + (yas / 100) 
    
    # Efor ve Rüzgar Çarpanları
    kalori_carpan = {"Az Kalori (Keyfi)": 1.0, "Normal Kalori (Tempo)": 1.15, "Çok Kalori (Performans)": 1.35}[kalori_seviyesi]
    ruzgar_carpan = {"Sakin": 1.0, "Tatlı Sert": 1.10, "Yamanlar Esintisi": 1.20, "Urla Fırtınası": 1.40}[ruzgar_sertligi]
    
    # Puan Hesaplama
    puan = int(((haftalik_km * 0.5) + (haftalik_irtifa * 0.1)) * agirlik_katsayisi * ruzgar_bonusu * yas_bonusu * kalori_carpan * ruzgar_carpan)
    
    # YAĞ YAKIM HESABI (Bilimsel Formül: 1g Yağ = 9 Kalori)
    # Eğer saatten kalori girilmediyse, tahmini bir kalori hesapla
    hesaplanan_kalori = saat_kalori if saat_kalori > 0 else (haftalik_km * 35 + haftalik_irtifa * 0.5)
    
    # Efor seviyesine göre yağdan giden yüzde (Yüksek eforda karbonhidrat artar, yağ yüzdesi düşer)
    yag_yuzdesi = {"Az Kalori (Keyfi)": 0.50, "Normal Kalori (Tempo)": 0.40, "Çok Kalori (Performans)": 0.30}[kalori_seviyesi]
    yag_gram = (hesaplanan_kalori * yag_yuzdesi) / 9
    
    return puan, round(yag_gram, 1), int(hesaplanan_kalori)

final_skor, yakilan_yag, toplam_kalori = hesaplamalari_yap()

st.success(f"📊 Mevcut Hesaplanan Hakkaniyet Puanı: *{final_skor}*")

# 4. ŞIK RAPOR
if st.button("Hakkaniyetli Raporu Oluştur"):
    st.balloons()
    su_an = datetime.now().strftime("%d/%m/%Y")
    
    st.markdown(f"""
    <div style="border: 4px solid #ff4b4b; padding: 20px; border-radius: 15px; background-color: #ffffff; text-align: center;">
        <h1 style="color: #ff4b4b; margin-bottom: 0;">🏆 ERKOZ PERFORMANS SERTİFİKASI</h1>
        <p style="color: gray;">Lisans No: {yas}{int(bisiklet_agirligi)}EXTREM | Tarih: {su_an}</p>
        <hr style="border: 1px solid #eee;">
        <div style="text-align: left; font-size: 18px;">
            <p><b>Sürücü:</b> {surucu_adi}</p>
            <p><b>Ekipman:</b> {bisiklet_marka} ({bisiklet_agirligi} kg)</p>
            <p><b>Zorluk Şartları:</b> {ruzgar_sertligi} / {kalori_seviyesi}</p>
            <p><b>Toplam Enerji:</b> {toplam_kalori} kcal</p>
            <p style="color: #2e7d32; font-weight: bold;">🔥 Yakılan Saf Yağ: {yakilan_yag} gram</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background-color: #2e7d32; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-top: 10px;">
        <p style="font-size: 20px; margin-bottom: 0;">HAKKANİYETLİ BAŞARI PUANI</p>
        <h1 style="font-size: 60px; margin-top: 0;">{final_skor}</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align: right; margin-top: 15px; font-style: italic;">
        <p>"Ağır bisikletle rüzgarı yaranın, kalorisini saatten bakanın hakkı yenmez."</p>
        <p><b>- Erkoz Yazılım İzmir 2026</b></p>
    </div>
    """, unsafe_allow_html=True)