import streamlit as st
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="Milyoner Yarışması", layout="centered")

# --- NİHAİ AYDINLIK TASARIM (CSS) ---
st.markdown("""
    <style>
    /* 1. Ana Arka Plan (BEYAZ YAPTIK) */
    .stApp { background-color: #FFFFFF; }
    
    /* 2. Soru Kutusu Tasarımı (Koyu Lacivert / Mavi Zemin) */
    .question-box {
        background: linear-gradient(to right, #11114e, #2d2d9b);
        padding: 25px;
        border-radius: 10px; /* Daha köşeli, profesyonel */
        border: 4px solid #FDFDFD;
        color: white;
        text-align: center;
        font-size: 21px;
        font-weight: bold;
        box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        margin-bottom: 25px;
        width: 100%;
    }

    /* 3. Buton Düzeni (MOBİLDE 2x2 ZORUNLU YAPTIK) */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: space-between !important;
        gap: 10px !important;
    }
    
    div[data-testid="column"] {
        width: calc(50% - 10px) !important;
        flex: 1 1 calc(50% - 10px) !important;
        min-width: calc(50% - 10px) !important;
    }

    /* 4. Butonların Kendisi (CEVAPLAR) */
    .stButton>button {
        width: 100%;
        border-radius: 50px; /* Gerçek yarışmadaki gibi yuvarlak */
        height: 3.8em;
        /* Koyu Gri/Mavi Buton - Beyaz Yazı */
        background: linear-gradient(to right, #44446e, #2a2a61);
        color: white; /* Yazı Rengi */
        border: 2px solid #333333; /* Hafif belirgin çerçeve */
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* 5. Buton Hover ve Aktif Hali (Sarı/Altın Efekti) */
    .stButton>button:hover {
        background: linear-gradient(to right, #ffd700, #ffb800) !important;
        color: black !important;
        border-color: #ffffff !important;
    }
    
    /* 6. Joker Butonu Özel Stili (Sarı Zemin - Siyah Yazı) */
    .joker-btn>div>div>div>button {
        background: linear-gradient(to right, #ffd700, #ffb800) !important;
        color: black !important;
        border: 2px solid #5d5dff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- OYUN VERİLERİ VE BAŞLATMA ---
def get_soru_bankasi():
    return [
        {"s": "Futbolda kalecinin topu elle tutabildiği alan hangisidir?", "o": ["Ceza Sahası", "Orta Saha", "Taç Çizgisi", "Korner Köşesi"], "c": "Ceza Sahası", "z": 1},
        {"s": "Hangisi bir yaylı çalgıdır?", "o": ["Gitar", "Keman", "Piyano", "Flüt"], "c": "Keman", "z": 1},
        {"s": "Türkiye'nin yüzölçümü en büyük ili hangisidir?", "o": ["İstanbul", "Ankara", "Konya", "Erzurum"], "c": "Konya", "z": 1},
        {"s": "Osmanlı Devleti'nin kurucusu kimdir?", "o": ["Orhan Bey", "Osman Bey", "I. Murat", "Fatih Sultan Mehmet"], "c": "Osman Bey", "z": 3},
        {"s": "Elementlerin periyodik tablosunu bulan bilim insanı kimdir?", "o": ["Einstein", "Newton", "Mendeleyev", "Pasteur"], "c": "Mendeleyev", "z": 9}
    ]

# Değişkenleri tanımlıyoruz
if 'index' not in st.session_state or 'elendi' not in st.session_state:
    st.session_state.index = 0
    st.session_state.elendi = False
    st.session_state.joker_50 = True
    st.session_state.gizli_siklar = []
    st.session_state.havuz = get_soru_bankasi()
    st.session_state.secili_sorular = random.sample(st.session_state.havuz, len(st.session_state.havuz))

# --- OYUN EKRANI ---
# Başlığı da siyah yapalım beyaz zeminde
st.markdown('<h1 style="color: black; text-align: center;">💰 Milyoner Yarışması</h1>', unsafe_allow_html=True)

if not st.session_state.elendi and st.session_state.index < len(st.session_state.secili_sorular):
    soru = st.session_state.secili_sorular[st.session_state.index]
    
    # Soru Kutusu (Koyu Renk Beyaz Yazılı)
    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    # --- YENİ BUTON DÜZENİ VE RENKLERİ ---
    col1, col2 = st.columns(2)
    for i, opt in enumerate(soru["o"]):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            if opt in st.session_state.gizli_siklar:
                # Silinen şık (Açık gri, basılamaz)
                st.button(" ", disabled=True, key=f"btn_{i}_{st.session_state.index}")
            else:
                # Normal Şık
                if st.button(opt, key=f"btn_{i}_{st.session_state.index}"):
                    if opt == soru["c"]:
                        st.success("DOĞRU!")
                        time.sleep(1)
                        st.session_state.index += 1
                        st.session_state.gizli_siklar = []
                        st.rerun()
                    else:
                        st.session_state.elendi = True
                        st.rerun()
    
    # Joker Butonu (Alta, Sarı Renkli)
    if st.session_state.joker_50:
        st.markdown("---")
        if st.button("🃏 %50 Jokerini Kullan", key="joker_main"):
            yanlislar = [opt for opt in soru['o'] if opt != soru['c']]
            st.session_state.gizli_siklar = random.sample(yanlislar, 2)
            st.session_state.joker_50 = False
            st.rerun()

elif st.session_state.elendi:
    st.markdown('<div style="background-color: #f8d7da; color: #721c24; padding: 20px; border-radius: 10px; text-align: center;"><h1>YANLIŞ CEVAP! Yarışma Bitti.</h1></div>', unsafe_allow_html=True)
    if st.button("Yeniden Başla"):
        st.session_state.clear()
        st.rerun()
else:
    st.balloons()
    st.success("TEBRİKLER! TÜM SORULARI BİLDİNİZ!")
    if st.button("Yeniden Başla"):
        st.session_state.clear()
        st.rerun()
