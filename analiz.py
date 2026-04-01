import streamlit as st
import requests
import json
from datetime import date

# --- ERKOZ ANALİZ v48.3 | PRECISION AGE & DATA SYNC ---
st.set_page_config(page_title="Erkoz Analiz v48.3", layout="wide", page_icon="🚴‍♂️")

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxZBLq5CwQosxqAG7LpuNYoIf9nMKloputy7EOVEZx5XcUmhI0wJAh3jExb6gPIrANrJg/exec"

# 1. OTURUM YÖNETİMİ
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {
        "ad_soyad": "Erdal Kozal", 
        "dogum_tarihi": "1967-04-03", 
        "boy": 179, 
        "kilo": 69.0, 
        "bis_marka": "Mosso Black Edition", 
        "bis_kilosu": 10.5
    }

if 'last_km' not in st.session_state:
    st.session_state['last_km'] = 0.0

# 2. YAN PANEL
with st.sidebar:
    st.header("🛡️ Erkoz Kontrol Merkezi")
    ad_soyad = st.text_input("Sürücü Adı", value=st.session_state['user_data']["ad_soyad"])
    d_tarihi = st.date_input("Doğum Tarihi", date.fromisoformat(st.session_state['user_data']["dogum_tarihi"]))
    boy = st.number_input("Boy (cm)", value=int(st.session_state['user_data']["boy"]))
    kilo = st.number_input("Kilo (kg)", value=float(st.session_state['user_data']["kilo"]))
    
    st.markdown("---")
    bis_marka = st.text_input("Bisiklet Modeli", value=st.session_state['user_data']["bis_marka"])
    bis_kilo = st.number_input("Bisiklet Ağırlığı (kg)", value=float(st.session_state['user_data']["bis_kilosu"]))

    # Hassas Yaş Hesaplama
    today = date.today()
    yas = today.year - d_tarihi.year - ((today.month, today.day) < (d_tarihi.month, d_tarihi.day))
    
    vke = round(kilo / ((boy/100)**2), 1)
    zorluk = round((bis_kilo - 10) * 2, 1)
    
    st.sidebar.info(f"Sürücü Yaşı: {yas}")
    st.sidebar.metric("Vücut Kitle Endeksi", vke)
    st.sidebar.metric("Donanım Zorluk", f"%{zorluk}")

# 3. ANA PANEL
st.title("🚀 Erkoz Yazılım | Pro Analiz")

c1, c2 = st.columns(2)
with c1:
    km_in = st.number_input("Tur Mesafesi (KM)", value=113.0, step=0.1)
    ruz_in = st.number_input("Ort. Rüzgar (km/h)", value=15.0)
with c2:
    yuk_in = st.number_input("Kazanılan İrtifa (m)", value=1049)
    kal_in = st.number_input("Yakılan Enerji (kcal)", value=2500)

# 4. İŞLEMLER
if st.button("📊 ANALİZ ET VE BULUTA GÖNDER"):
    if km_in == st.session_state['last_km']:
        st.warning(f"⚠️ Bu tur ({km_in} KM) zaten kaydedildi kanka!")
    else:
        # Algoritma v48.3
        bak = 1 + (zorluk / 100)
        # Puanlama mantığını biraz daha optimize ettik
        final_puan = round((((((yas+20)/100)*3) + ((vke/100)*20) + 6.9) * bak / (km_in if km_in > 0 else 1)) * 115, 2)
        yag_gr = round((kal_in * 0.77) / 9, 1) # Yağ yakım katsayısı revize

        payload = {
            "adSoyad": ad_soyad, "yas": yas, "vke": vke,
            "bisikleti": bis_marka, "surusKM": km_in, 
            "yukselti": yuk_in, "puan": final_puan
        }
        
        try:
            # Google Apps Script bazen JSON header bekler
            headers = {'Content-Type': 'application/json'}
            response = requests.post(SCRIPT_URL, data=json.dumps(payload), headers=headers, timeout=10)
            
            if response.status_code == 200:
                st.success(f"✅ Veri Excel'e uçuruldu! Skor: {final_puan}")
                st.session_state['last_km'] = km_in
            else:
                st.error("❌ Sunucu hatası! Veri gitmedi.")
        except:
            st.error("🌐 Bağlantı hatası! İnterneti kontrol et kanka.")

        # BAŞARI EKRANI
        st.balloons()
        with st.expander("📝 TUR ÖZETİ VE SERTİFİKA", expanded=True):
            st.subheader(f"Tebrikler, {ad_soyad}!")
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Performans Skoru", final_puan)
            sc2.metric("Yakılan Saf Yağ", f"{yag_gr} gr")
            sc3.metric("Zorluk Katsayısı", f"x{bak}")
            st.info("Bu skor; yaşın, kilon ve kullandığın bisikletin ağırlığına göre hesaplanmış 'Adaletli Performans Puanı'dır.")

st.caption("Erkoz Yazılım © 2026 | v48.3 Premium")
