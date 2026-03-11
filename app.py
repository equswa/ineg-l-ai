import streamlit as st
from PIL import Image
import requests
import io
import base64
import time

# Sayfa Ayarları
st.set_page_config(page_title="Küresel Ticaret & İhracat Motoru", page_icon="🌍", layout="wide")

# ==========================================
# 🔒 GÜVENLİ KASA SİSTEMİ
# ==========================================
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    HF_TOKEN = st.secrets["HF_TOKEN"]
except KeyError:
    st.error("HATA: Güvenli kasa (Secrets) ayarlanmamış!")
    st.stop()

HF_API_URL = "https://router.huggingface.co/hf-inference/models/lllyasviel/sd-controlnet-canny"
hf_headers = {"Authorization": f"Bearer {HF_TOKEN.strip()}"}

st.title("🌍 Küresel Ticaret & İhracat Motoru")
st.markdown("Kayınçonun Atölyesinden Avrupa'ya: Ürünleri stüdyo kalitesine getirin ve toptan/perakende satış metinleri üretin.")
st.divider()

col_controls, col_outputs = st.columns([1, 2.5])

with col_controls:
    st.subheader("1. Ürün Görselleri 📸")
    uploaded_files = st.file_uploader("Görselleri seçin (Maks 5)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    st.write("---")
    studio_modu = st.toggle("✨ Stüdyo Modu (Arka Planı Lüks Yap)", value=False)
    if studio_modu:
        ev_tarzi = st.selectbox("Arka Plan Tarzı", ["Modern European Villa", "Dubai Luxury Home", "Scandinavian Minimalist Studio", "Classic Italian Mansion"])
    
    st.write("---")
    st.subheader("2. Satış ve İhracat Stratejisi 🎯")
    
    # İHRACATA ÖZEL SEÇENEKLER
    hedef = st.radio("Pazarlama Kanalı", [
        "🤝 B2B İhracat E-Postası (Yurtdışı Toptancılara)",
        "🛒 E-Ticaret (Etsy, Wayfair, Amazon Listing)", 
        "📱 Yurtdışı Sosyal Medya Reklamı"
    ])
    
    dil = st.selectbox("Hedef Ülke Dili", ["İngilizce (Global)", "Almanca (Avrupa)", "Arapça (Ortadoğu)", "Fransızca", "Rusça"])
    ton = st.selectbox("İletişim Tonu", ["Profesyonel & Kurumsal (Güven Verici)", "Lüks & Premium (Yüksek Fiyatlı)", "Agresif Satış (İkna Edici)"])

    st.write("")
    uret_butonu = st.button("🚀 İçerikleri Üret ve Piyasaya Sür", use_container_width=True, type="primary")

with col_outputs:
    st.subheader("3. Yapay Zeka Çıktıları 🧠")
    
    if uret_butonu:
        if not uploaded_files:
            st.warning("⚠️ Lütfen önce ürün fotoğrafı yükleyin.")
        else:
            # Stratejiye Göre Zekayı Yönlendirme (Prompt Engineering)
            if "B2B" in hedef:
                prompt = f"""Sen üst düzey bir İhracat Müdürüsün. Ekteki mobilya fotoğrafını incele. 
                Bu ürünün Türkiye'deki doğrudan üreticisi (fabrikası) olduğumuzu belirterek, hedef dildeki büyük bir mobilya distribütörüne toptan satış yapmak için resmi, ikna edici ve profesyonel bir B2B e-posta (Cold Email) yaz.
                E-postada 'doğrudan üreticiden aracısız alım', 'yüksek kalite', ve 'zamanında lojistik' vurgusu yap.
                Dil: {dil}. Ton: {ton}."""
            elif "E-Ticaret" in hedef:
                prompt = f"""Sen uzman bir Global E-ticaret SEO Uzmanısın. Ekteki mobilya fotoğrafını incele. 
                Bu ürünü Etsy, Wayfair veya Amazon'da satmak için muazzam bir ürün listelemesi hazırla. 
                Şunları içersin: Arama hacmi yüksek bir SEO başlığı, 5 maddelik vurucu özellikler (Bullet points) ve müşterinin satın alma arzusu yaratacak duygusal bir ürün açıklaması.
                En alta aranma hacmi yüksek 10 anahtar kelime (Tags) ekle.
                Dil: {dil}. Ton: {ton}."""
            else:
                prompt = f"""Sen uzman bir Global Dijital Pazarlamacısın. Ekteki mobilya fotoğrafını incele. 
                Yurtdışındaki son tüketiciye satışı hedefleyen, reklam olarak çıkılacak şık ve dikkat çekici bir sosyal medya metni yaz.
                Kısa, akılda kalıcı olsun, uygun emojiler kullan ve en alta o ülkede keşfete düşmeyi sağlayacak 7 adet hashtag ekle.
                Dil: {dil}. Ton: {ton}."""

            for i, dosya in enumerate(uploaded_files):
                with st.expander(f"📌 {hedef.split(' ')[1]} - Ürün {i+1}", expanded=True):
                    col_img, col_txt = st.columns([1, 2])
                    
                    image = Image.open(dosya).convert("RGB") 
                    islem_goren_resim = image
                    
                    with col_img:
                        if studio_modu:
                            with st.spinner('Lüks Stüdyo Çekimi Yapılıyor...'):
                                buffered = io.BytesIO()
                                image.save(buffered, format="JPEG")
                                img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                                payload = {
                                    "inputs": f"a luxury living room in a {ev_tarzi}, modern furniture, professional interior photography, 8k",
                                    "image": img_b64,
                                    "options": {"wait_for_model": True}
                                }
                                try:
                                    response = requests.post(HF_API_URL, headers=hf_headers, json=payload)
                                    if response.status_code == 200:
                                        islem_goren_resim = Image.open(io.BytesIO(response.content)).convert("RGB")
                                        st.image(islem_goren_resim, caption=f"Stüdyo: {ev_tarzi}", use_container_width=True)
                                    else:
                                        st.image(islem_goren_resim, caption="Orijinal Görsel", use_container_width=True)
                                except:
                                    st.image(islem_goren_resim, caption="Orijinal Görsel", use_container_width=True)
                        else:
                            st.image(islem_goren_resim, caption="Orijinal Görsel", use_container_width=True)
                            
                    with col_txt:
                        with st.spinner('Satış Metni Hazırlanıyor...'):
                            try:
                                # DOĞRUDAN GOOGLE REST API (Kesintisiz Bağlantı)
                                buffered = io.BytesIO()
                                islem_goren_resim.save(buffered, format="JPEG")
                                final_img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                                
                                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
                                gemini_payload = {
                                    "contents": [{
                                        "parts": [
                                            {"text": prompt},
                                            {"inline_data": {"mime_type": "image/jpeg", "data": final_img_b64}}
                                        ]
                                    }]
                                }
                                
                                res = requests.post(gemini_url, json=gemini_payload)
                                
                                if res.status_code == 200:
                                    sonuc_metni = res.json()['candidates'][0]['content']['parts'][0]['text']
                                    st.info(f"**Pazar:** {dil} | **Kanal:** {hedef.split(' ')[1]} | **Ton:** {ton}")
                                    st.markdown(sonuc_metni)
                                    
                                    # Profesyonel Kopyalama Butonu Hissi
                                    st.button("📋 Metni Kopyala", key=f"copy_{i}", help="Müşteriye veya platforma yapıştırmak için kopyalayın.")
                                else:
                                    st.error("Google API Bağlantı Hatası.")
                                
                                time.sleep(2) 
                            except Exception as e:
                                st.error(f"Sistem Hatası: {e}")
                                
            st.balloons()
