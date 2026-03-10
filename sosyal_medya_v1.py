import streamlit as st
from PIL import Image
import requests
import io
import base64
import time

# Sayfa Ayarları
st.set_page_config(page_title="SosyalZeka AI - PRO Studio", page_icon="🚀", layout="wide")

# ==========================================
# 🔒 GÜVENLİ KASA SİSTEMİ
# ==========================================
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    HF_TOKEN = st.secrets["HF_TOKEN"]
except KeyError:
    st.error("HATA: Güvenli kasa (Secrets) ayarlanmamış!")
    st.stop()

# Hugging Face Ayarları
HF_API_URL = "https://router.huggingface.co/hf-inference/models/lllyasviel/sd-controlnet-canny"
hf_headers = {"Authorization": f"Bearer {HF_TOKEN.strip()}"}

st.title("🚀 SosyalZeka: PRO Studio")
st.markdown("Toplu İçerik Motoru + Otomatik Stüdyo Çekimi")
st.divider()

col_controls, col_outputs = st.columns([1, 2.5])

with col_controls:
    st.subheader("1. Ayarlar ⚙️")
    uploaded_files = st.file_uploader("Görselleri seçin (Maks 5)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    
    st.write("---")
    studio_modu = st.toggle("✨ Amatör Çekimi Profesyonelleştir", value=False)
    if studio_modu:
        ev_tarzi = st.selectbox("Ev Arka Plan Tarzı", ["Dubai Luxury Villa", "Modern Scandinavian Home", "Classic Italian Mansion"])
    
    st.write("---")
    platform = st.radio("Platform", ["Instagram", "LinkedIn", "Twitter (X)", "TikTok"], horizontal=True)
    dil = st.selectbox("Hedef Dil", ["Türkçe", "İngilizce", "Almanca", "Arapça"])
    ton = st.selectbox("İçerik Tonu", ["Eğlenceli & Samimi", "Kurumsal & Profesyonel", "Satış & İkna Odaklı"])

    uret_butonu = st.button("✨ İçerikleri Üret", use_container_width=True, type="primary")

with col_outputs:
    st.subheader("2. Yapay Zeka Çıktıları 🧠")
    
    if uret_butonu:
        if not uploaded_files:
            st.warning("⚠️ Lütfen önce fotoğraf yükleyin.")
        else:
            prompt = f"""
            Sen uzman bir Sosyal Medya Yöneticisi ve Dijital Pazarlama Uzmanısın. 
            Ekteki mobilya/mekan fotoğrafını incele. 
            Şu ayarlara göre viral olacak, etkileşimi yüksek bir gönderi metni yaz:
            - Platform: {platform}
            - Dil: {dil}
            - Ton: {ton}
            
            Lütfen metni doğrudan paylaşmaya hazır şekilde yaz. Uygun emojiler kullan.
            En sona bu platformda keşfete düşmeyi sağlayacak 5-7 adet hashtag ekle.
            """

            for i, dosya in enumerate(uploaded_files):
                with st.expander(f"📌 Görsel {i+1} İçin Hazırlanan İçerik", expanded=True):
                    col_img, col_txt = st.columns([1, 2])
                    
                    image = Image.open(dosya).convert("RGB") 
                    islem_goren_resim = image
                    
                    with col_img:
                        if studio_modu:
                            with st.spinner('Stüdyo motoru çalışıyor...'):
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
                                        st.image(islem_goren_resim, caption="Orijinal", use_container_width=True)
                                except:
                                    st.image(islem_goren_resim, caption="Orijinal", use_container_width=True)
                        else:
                            st.image(islem_goren_resim, caption="Orijinal Görsel", use_container_width=True)
                            
                    with col_txt:
                        with st.spinner('Google sistemine zorla giriliyor...'):
                            try:
                                # 1. GOOGLE'IN LİSTESİNİ ÇEKİYORUZ
                                list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
                                list_res = requests.get(list_url)
                                
                                if list_res.status_code != 200:
                                    st.error("API Anahtarı geçersiz veya kısıtlanmış.")
                                    st.stop()
                                    
                                modeller = list_res.json().get('models', [])
                                
                                # Görsel okuyabilen modelleri filtrele
                                uygun_modeller = [m['name'] for m in modeller if 'generateContent' in m.get('supportedGenerationMethods', []) and ('1.5' in m['name'] or '2.0' in m['name'] or 'vision' in m['name'])]
                                
                                # Görseli Google formatına çevir
                                buffered = io.BytesIO()
                                islem_goren_resim.save(buffered, format="JPEG")
                                final_img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                                
                                basarili_sonuc = None
                                hata_raporu = []
                                calisan_motor = ""
                                
                                # 2. BULUNAN MODELLERİ TEK TEK DENE
                                for model_adi in uygun_modeller:
                                    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/{model_adi}:generateContent?key={GEMINI_API_KEY}"
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
                                        basarili_sonuc = res.json()['candidates'][0]['content']['parts'][0]['text']
                                        calisan_motor = model_adi.replace("models/", "")
                                        break # Başarılı olduysa döngüden çık!
                                    elif res.status_code == 429:
                                        hata_raporu.append(f"{model_adi.replace('models/', '')}: Ücretsiz Kota Yok (Limit: 0)")
                                    else:
                                        hata_raporu.append(f"{model_adi.replace('models/', '')}: {res.status_code} Hatası")
                                
                                # 3. SONUCU EKRANA BAS
                                if basarili_sonuc:
                                    st.success(f"**Platform:** {platform} | **Dil:** {dil} | **Motor:** {calisan_motor}")
                                    st.write(basarili_sonuc)
                                    st.balloons()
                                else:
                                    st.error("🚨 Google Tüm Kapıları Kapattı!")
                                    for hata in hata_raporu:
                                        st.write(f"- {hata}")
                                    st.info("💡 ÇÖZÜM: Google sizin API anahtarınızda ücretsiz kullanımı (Free Tier) tamamen durdurmuş. Lütfen FARKLI BİR GMAIL HESABI ile Google AI Studio'ya girip yeni bir API anahtarı alın.")
                                
                                time.sleep(2) 
                            except Exception as e:
                                st.error(f"Sistem Hatası: {e}")
