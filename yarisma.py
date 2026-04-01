import streamlit as st
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="Milyoner Yarışması", layout="centered")

# --- CSS: MOBİLDE 2x2 BUTON DÜZENİ ---
st.markdown("""
    <style>
    .stApp { background-color: #02021e; }
    
    /* Butonları yan yana zorlayan sihirli dokunuş */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
    }
    
    div[data-testid="column"] {
        width: calc(50% - 10px) !important;
        flex: 1 1 calc(50% - 10px) !important;
        min-width: calc(50% - 10px) !important;
    }

    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.8em;
        background: linear-gradient(to right, #0d0d4b, #1e1e8e);
        color: #ffd700;
        border: 2px solid #5d5dff;
        font-weight: bold;
        font-size: 15px;
    }

    .question-box {
        background: linear-gradient(145deg, #0d0d35, #161665);
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #5d5dff;
        color: white;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- OYUN VERİLERİ VE BAŞLATMA ---
def get_soru_bankasi():
    return [
        {"s": "Futbolda kalecinin topu elle tutabildiği alan hangisidir?", "o": ["Ceza Sahası", "Orta Saha", "Taç Çizgisi", "Korner Köşesi"], "c": "Ceza Sahası", "z": 1},
        {"s": "Hangisi bir yaylı çalgıdır?", "o": ["Gitar", "Keman", "Piyano", "Flüt"], "c": "Keman", "z": 1},
        {"s": "İstiklal Marşı'mızın şairi kimdir?", "o": ["Ziya Gökalp", "Namık Kemal", "Mehmet Akif Ersoy", "Reşat Nuri"], "c": "Mehmet Akif Ersoy", "z": 1},
        {"s": "Türkiye'nin yüzölçümü en büyük ili hangisidir?", "o": ["İstanbul", "Ankara", "Konya", "Erzurum"], "c": "Konya", "z": 1},
        {"s": "Osmanlı Devleti'nin kurucusu kimdir?", "o": ["Orhan Bey", "Osman Bey", "I. Murat", "Fatih Sultan Mehmet"], "c": "Osman Bey", "z": 3},
        {"s": "Aspirin'in ham maddesi olan ağaç hangisidir?", "o": ["Çam", "Söğüt", "Meşe", "Gürgen"], "c": "Söğüt", "z": 5}
    ]

oduller = ["500 TL", "1.000 TL", "2.000 TL", "3.000 TL", "5.000 TL", "7.500 TL", "15.000 TL", "30.000 TL", "60.000 TL", "125.000 TL", "250.000 TL", "1.000.000 TL"]

# Hata almamak için tüm değişkenleri tek seferde tanımlıyoruz
if 'index' not in st.session_state or 'elendi' not in st.session_state:
    st.session_state.index = 0
    st.session_state.elendi = False
    st.session_state.joker_50 = True
    st.session_state.gizli_siklar = []
    st.session_state.havuz = get_soru_bankasi()
    st.session_state.secili_sorular = random.sample(st.session_state.havuz, min(len(st.session_state.havuz), 12))

# --- OYUN EKRANI ---
st.title("💰 Kim Milyoner Olmak İster?")

if not st.session_state.elendi and st.session_state.index < len(st.session_state.secili_sorular):
    soru = st.session_state.secili_sorular[st.session_state.index]
    
    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    # Butonları yan yana dizecek yapı
    col1, col2 = st.columns(2)
    for i, opt in enumerate(soru["o"]):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            if opt in st.session_state.gizli_siklar:
                st.button(" ", disabled=True, key=f"btn_{i}_{st.session_state.index}")
            else:
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
    
    # Joker Butonu (Sadece mobilde denge için alta koydum)
    if st.session_state.joker_50:
        if st.button("🃏 %50 Jokerini Kullan"):
            yanlislar = [opt for opt in soru['o'] if opt != soru['c']]
            st.session_state.gizli_siklar = random.sample(yanlislar, 2)
            st.session_state.joker_50 = False
            st.rerun()

elif st.session_state.elendi:
    st.error("YANLIŞ CEVAP! Yarışma Bitti.")
    if st.button("Yeniden Başla"):
        st.session_state.clear()
        st.rerun()
