import streamlit as st
from PIL import Image
import base64
import requests
import io
import time

# Sayfa Ayarları (Geniş Ekran - Premium Görünüm)
st.set_page_config(page_title="SosyalZeka AI - PRO Studio", page_icon="🚀", layout="wide")

# Custom CSS ile arayüzü güzelleştirme
st.markdown("""
<style>
    .stApp { background-color: #f4f7f6; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    div[data-testid="stExpander"] { border-radius: 12px; background-color: white; padding: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 SosyalZeka: PRO Studio")
st.markdown("Toplu İçerik Motoru + Otomatik Stüdyo Çekimi (Zaman Nakittir Vizyonu)")
st.divider()

# Kolonları ayarlayalım (Kontrol Paneli, Görsel Önizleme, Çıktı Ekranı)
col_controls, col_previews, col_outputs = st.columns([1, 1.2, 1.8])

# GLOBAL DEĞİŞKENLER (Beyinleri takmak için)
HF_TOKEN = "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" # Koltuğu güzelleştiren beyin (Ücretsiz)
headers = {"Authorization": f"Bearer {HF_TOKEN.strip()}"}

with col_controls:
    st.subheader("1. Ayarlar ⚙️")
    uploaded_files = st.file_uploader("Görselleri seçin (Maks 5)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    st.write("---")
    
    # PREMIUM ÖZELLİK: Arka Plan Değiştirme
    studio_modu = st.toggle("✨ Amatör Çekimi Profesyonelleştir (Ücretsiz SDXL)", value=False, help="Atölye fotoğraflarını lüks ev arka planıyla değiştirir.")
    
    if studio_modu:
        ev_tarzi = st.selectbox("Ev Arka Plan Tarzı", ["Dubai Luxury Villa", "Modern Scandinavian Home", "Classic Italian Mansion", "Chic Boho Apartment"])
    else:
        st.caption("Not: Amatör fotoğrafın orijinal arka planı korunur.")

    st.write("---")
    
    st.write("Hedef Platform:")
    platform = st.radio("Platform", ["Instagram", "LinkedIn", "Twitter (X)", "TikTok"], horizontal=True, label_visibility="collapsed")
    
    ayar_col1, ayar_col2 = st.columns(2)
    with ayar_col1: dil = st.selectbox("Hedef Dil", ["Türkçe 🇹🇷", "İngilizce 🇬🇧", "Almanca 🇩🇪", "Arapça 🇸🇦"])
    with ayar_col2: ton = st.selectbox("İçerik Tonu", ["Eğlenceli & Samimi", "Kurumsal & Profesyonel", "Satış & İkna Odaklı"])

    st.write("")
    # PRO Buton
    uret_butonu = st.button("✨ Tüm Görselleri İşle ve Üret", use_container_width=True, type="primary")

with col_previews:
    st.subheader("2. Önizleme 👀")
    if uploaded_files:
        st.success(f"{len(uploaded_files)} görsel yüklendi.")
        # Fotoğrafları grid (ızgara) şeklinde gösterelim
        onizleme_grid = st.container(border=True)
        with onizleme_grid:
            cols = st.columns(3)
            for i, dosya in enumerate(uploaded_files[:5]):
                with cols[i % 3]:
                    st.image(dosya, caption=f"Görsel {i+1}", use_container_width=True)
    else:
        st.info("Lütfen sol taraftan görselleri yükleyin.")

with col_outputs:
    st.subheader("3. Yapay Zeka Çıktıları 🧠")
    output_container = st.container(border=True)
    
    if uret_butonu:
        if not uploaded_files:
            st.warning("⚠️ Önce fotoğraf yüklemeniz gerekir.")
        else:
            with output_container:
                if studio_modu: st.info(f"Yapay Zeka görselleri sırayla 'Studio Modu' ({ev_tarzi}) ile yeniliyor ve metinleri yazıyor...")
                else: st.info("Yapay Zeka görselleri inceliyor ve metinleri yazıyor...")
                
                for i, dosya in enumerate(uploaded_files):
                    with st.expander(f"📌 Görsel {i+1} İçin Hazırlanan İçerik", expanded=True):
                        col_img, col_txt = st.columns([1, 2.5])
                        
                        with col_img:
                            # EĞER STÜDYO MODU AÇIKSA: Buraya Hugging Face'den gelen profesyonel görseli basacağız
                            if studio_modu:
                                st.write("Amatör")
                                st.image(dosya, use_container_width=True)
                                st.write("Profesyonel")
                                st.write("*(Gerçek AI bağlandığında burada yenilenmiş görsel olacak)*")
                            else:
                                st.image(dosya, caption="Orijinal Görsel", use_container_width=True)
                                
                        with col_txt:
                            st.write(f"**Platform:** {platform} | **Dil:** {dil} | **Ton:** {ton}")
                            if studio_modu: st.caption(f"Arka plan: {ev_tarzi}")
                            
                            # Buraya Gemini'den gelen metni basacağız
                            st.write(f"*(Gerçek AI bağlandığında burada Gemini'nin Görsel {i+1} için yazdığı özel reklam metni, emojiler ve 5 adet #hashtag olacak)*")
                            st.button("📄 Metni Kopyala", key=f"copy_{i}")
    else:
        st.write("👈 Sol taraftan ayarları seçip 'İşle ve Üret' butonuna basın.")
