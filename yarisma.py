import streamlit as st
import time
import random

# Sayfa ayarları
st.set_page_config(page_title="Milyoner Yarışması", layout="centered")

# --- GENİŞLETİLMİŞ TASARIM (CSS - Mobil Odaklı 2x2 Düzen) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #02021e; }
    
    /* Ödül Merdiveni (Sidebar) Tasarımı */
    [data-testid="stSidebar"] {
        background-color: #05052d;
        border-right: 2px solid #5d5dff;
    }
    .money-item {
        padding: 5px 10px;
        border-radius: 10px;
        margin-bottom: 2px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 18px;
    }
    .current-step {
        background-color: #ffd700;
        color: #02021e !important;
        border: 2px solid white;
    }
    .passed-step {
        color: #55557f !important;
    }
    .upcoming-step {
        color: #ffffff !important;
    }

    /* Soru Kutusu */
    .question-box {
        background: linear-gradient(145deg, #0d0d35, #161665);
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #5d5dff;
        color: white;
        text-align: center;
        font-size: 20px;
        margin-bottom: 20px;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }

    /* --- BUTON TASARIMI VE MOBİLDE 2x2 DÜZEN (BU KISIM KRİTİK!) --- */
    
    /* Mobil Uyumlu Buton Taşıyıcısı */
    .stHorizontalBlock {
        display: flex;
        flex-wrap: wrap; /* Mobilde sığmazsa alt satıra geçsin */
        justify-content: space-between; /* Aralarında boşluk olsun */
    }

    /* Butonların Kendisi */
    .stButton>button {
        width: 100%; /* Sütun genişliğini kaplasın */
        max-width: 48%; /* Mobilde yan yana iki tane sığsın (boşluklar dahil) */
        flex: 1 1 45%; /* Esnek genişlik */
        border-radius: 50px;
        height: 3.5em;
        background: linear-gradient(to right, #0d0d4b, #1e1e8e);
        color: #ffd700;
        border: 2px solid #5d5dff;
        font-weight: bold;
        font-size: 16px; /* Mobilde biraz daha küçük yazı */
        margin-bottom: 15px; /* Alt alta gelenler arasında boşluk */
        box-shadow: 0 3px 6px rgba(0,0,0,0.3);
    }
    
    /* Bilgisayarda Buton Genişliği (48% Mobilde Sadece Yan Yana Getirmek İçin) */
    @media (min-width: 768px) {
        .stButton>button {
            max-width: 100%; /* Bilgisayarda st.columns düzenine uysun */
        }
    }

    </style>
    """, unsafe_allow_html=True)

# --- SORU BANKASI (ÖNCEKİ SORULAR) ---
# (Lütfen koddaki get_soru_bankasi fonksiyonunu ve session state mantığını olduğu gibi koru)
# --- Sadece CSS ve Arayüz kısmını güncelliyoruz ---

# --- ARAYÜZ ---
st.title("💰 Kim Milyoner Olmak İster?")

if not st.session_state.elendi and st.session_state.index < len(oduller):
    soru = st.session_state.secili_sorular[st.session_state.index]
    
    # Gelişmiş Ödül Merdiveni (Sidebar - Olduğu Gibi)
    # ... (Lütfen Sidebar ve Joker kodunu koru)

    # Soru Kutusu
    st.markdown(f'<div class="question-box">{soru["s"]}</div>', unsafe_allow_html=True)

    # --- YENİ BUTON DÜZENİ (2x2) ---
    # st.columns(2) bilgisayarda yan yana getirir, 
    # CSS de mobilde yan yana gelmelerini zorlar.
    
    cols = st.columns(2)
    for i, opt in enumerate(soru["o"]):
        if opt in st.session_state.gizli_siklar:
            # Jokerle silinen şık
            with cols[i % 2]:
                st.button(f" ", disabled=True, key=f"btn_{i}")
        else:
            with cols[i % 2]:
                if st.button(opt, key=f"btn_{i}"):
                    # Doğru/Yanlış Cevap Kontrolü
                    if opt == soru["c"]:
                        st.success("DOĞRU!")
                        # ... (Lütfen devam eden session state ve rerun kodunu koru)
                    else:
                        st.error(f"YANLIŞ! Doğru cevap: {soru['c']}")
                        # ... (Lütfen devam eden elendi kodunu koru)

# --- (YENİDEN BAŞLA VE ELENDİ KODLARINI OLDUĞU GİBİ KORU) ---
