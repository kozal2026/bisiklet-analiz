import streamlit as st
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="Milyoner Yarışması", layout="centered")

# --- Gelişmiş Tasarım (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #02021e; }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3.5em;
        background: linear-gradient(to right, #0d0d4b, #1e1e8e);
        color: #ffd700;
        border: 2px solid #5d5dff;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }
    .stButton>button:hover {
        border-color: #ffd700;
        color: white;
    }
    .question-box {
        background: linear-gradient(145deg, #0d0d35, #161665);
        padding: 30px;
        border-radius: 20px;
        border: 3px solid #5d5dff;
        color: white;
        text-align: center;
        font-size: 24px;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .money-list {
        color: #ffd700;
        text-align: right;
        font-family: monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Soru Bankası ---
if 'sorular' not in st.session_state:
    st.session_state.sorular = [
        {"s": "Türkiye'nin başkenti neresidir?", "o": ["İstanbul", "Ankara", "İzmir", "Bursa"], "c": "Ankara", "p": "500 TL"},
        {"s": "Hangi gezegen 'Kızıl Gezegen' olarak bilinir?", "o": ["Venüs", "Jüpiter", "Mars", "Satürn"], "c": "Mars", "p": "1.000 TL"},
        {"s": "Python dilinde ekrana yazı yazdırmak için hangisi kullanılır?", "o": ["echo", "print", "display", "write"], "c": "print", "p": "2.000 TL"},
    ]

# --- Oyun Durumu ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.elendi = False

# --- Yarışma Ekranı ---
st.title("💰 Milyoner Olmak İster Misin?")

if not st.session_state.elendi and st.session_state.index < len(st.session_state.sorular):
    soru = st.session_state.sorular[st.session_state.index]
    
    # Mevcut ödül ve Soru
    st.sidebar.title("Ödül Tablosu")
    for q in reversed(st.session_state.sorular):
        prefix = "👉 " if q['p'] == soru['p'] else "   "
        st.sidebar.write(f"{prefix} {q['p']}")

    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    # Seçenekler
    cols = st.columns(2)
    for i, opt in enumerate(soru["o"]):
        with cols[i % 2]:
            if st.button(opt):
                if opt == soru["c"]:
                    st.balloons()
                    st.success("DOĞRU!")
                    time.sleep(1.5)
                    st.session_state.index += 1
                    st.rerun()
                else:
                    st.error("YANLIŞ CEVAP!")
                    st.session_state.elendi = True
                    time.sleep(1)
                    st.rerun()

elif st.session_state.elendi:
    st.error(f"Maalesef elendiniz. Kazandığınız ödül: {st.session_state.sorular[st.session_state.index-1]['p'] if st.session_state.index > 0 else '0 TL'}")
    if st.button("Tekrar Dene"):
        st.session_state.index = 0
        st.session_state.elendi = False
        st.rerun()
else:
    st.balloons()
    st.success("TEBRİKLER! TÜM SORULARI BİLDİNİZ!")
    if st.button("Başa Dön"):
        st.session_state.index = 0
        st.rerun()
