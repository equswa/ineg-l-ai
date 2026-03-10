import streamlit as st
from PIL import Image

# Sayfa Ayarları (Geniş Ekran)
st.set_page_config(page_title="SosyalZeka AI - PRO", page_icon="🚀", layout="wide")

st.title("🚀 SosyalZeka: Toplu İçerik Motoru")
st.markdown("Zaman nakittir! Birden fazla görsel yükle, hepsinin içeriğini tek tıkla hazırla.")
st.divider()

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("1. Görselleri Yükle 📸 (Çoklu Seçim)")
    
    # İŞTE SİHİRLİ KOD: accept_multiple_files=True (Aynı anda birden fazla fotoğraf seçmeni sağlar)
    uploaded_files = st.file_uploader("Görselleri sürükle veya seç (Maks 5 önerilir)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    if uploaded_files:
        st.success(f"Harika! {len(uploaded_files)} adet görsel yüklendi.")
        # Yüklenen fotoğrafların küçük önizlemelerini yan yana gösterelim
        onizleme_kolonlari = st.columns(len(uploaded_files) if len(uploaded_files) <= 5 else 5)
        for i, dosya in enumerate(uploaded_files[:5]): 
            with onizleme_kolonlari[i % 5]:
                st.image(dosya, use_container_width=True)

    st.divider()
    
    st.subheader("2. Tüm Görseller İçin Ayarlar ⚙️")
    st.write("Hedef Platform:")
    platform = st.radio("Platform", ["Instagram", "LinkedIn", "Twitter (X)", "TikTok"], horizontal=True, label_visibility="collapsed")
    
    ayar_col1, ayar_col2 = st.columns(2)
    with ayar_col1:
        dil = st.selectbox("Hedef Dil", ["Türkçe 🇹🇷", "İngilizce 🇬🇧", "Almanca 🇩🇪", "İspanyolca 🇪🇸", "Arapça 🇸🇦"])
    with ayar_col2:
        ton = st.selectbox("İçerik Tonu", ["Eğlenceli & Samimi", "Kurumsal & Profesyonel", "Satış & İkna Odaklı", "Bilgi Verici"])

    st.write("")
    # PRO Buton
    uret_butonu = st.button("✨ Tüm Görseller İçin Üret", use_container_width=True, type="primary")

with col2:
    st.subheader("3. Yapay Zeka Çıktıları 🧠")
    
    with st.container(border=True):
        if uret_butonu:
            if not uploaded_files:
                st.warning("⚠️ Lütfen önce analiz edilecek fotoğrafları yükle!")
            else:
                st.info("Yapay Zeka tüm görselleri sırayla inceliyor... (Motor bağlantısı bekleniyor)")
                
                # Her bir fotoğraf için açılır kapanır (Expander) bir kutu oluşturuyoruz
                for i, dosya in enumerate(uploaded_files):
                    with st.expander(f"📌 Görsel {i+1} İçin Hazırlanan İçerik", expanded=True):
                        # Kutunun içini de ikiye bölelim: Solda resim, sağda metin
                        resim_kolonu, metin_kolonu = st.columns([1, 2])
                        with resim_kolonu:
                            st.image(dosya, use_container_width=True)
                        with metin_kolonu:
                            st.success(f"**Platform:** {platform} | **Dil:** {dil} | **Ton:** {ton}")
                            st.write(f"*(Gerçek AI bağlandığında burada Görsel {i+1} için Gemini'nin yazdığı özel reklam metni, emojiler ve 5 adet #hashtag olacak)*")
        else:
            st.write("👈 Sol taraftan birden fazla görsel seçip 'Üret' butonuna basın.")
