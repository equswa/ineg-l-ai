import streamlit as st
import requests
import io
from PIL import Image
import base64

st.set_page_config(page_title="İnegöl AI - Profesyonel", page_icon="🪑")

# Token'ını buraya tekrar yapıştır
HF_TOKEN = "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"
headers = {"Authorization": f"Bearer {HF_TOKEN.strip()}"}

# Senin koltuğunun şeklini koruyan özel model
API_URL = "https://router.huggingface.co/hf-inference/models/lllyasviel/sd-controlnet-canny"

st.title("🪑 İnegöl AI: Akıllı Tasarım")
st.write("Yüklediğin koltuğun şekli korunarak lüks bir odaya yerleştirilir.")

uploaded_file = st.file_uploader("Koltuk fotoğrafı yükle (Atölye çekimi)...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Orijinal Mobilya", use_container_width=True)

    if st.button("Kataloğa Yerleştir ✨"):
        with st.spinner('Mobilya iskeleti analiz ediliyor ve oda döşeniyor...'):
            # Görseli API'nin anlayacağı formata (base64) çeviriyoruz
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            payload = {
                "inputs": "a modern luxury living room with high-end furniture, professional interior photography, 8k, realistic lighting",
                "image": img_base64,
                "options": {"wait_for_model": True}
            }

            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                result_img = Image.open(io.BytesIO(response.content))
                st.success("İşte Mobilyanın Yeni Hali!")
                st.image(result_img, use_container_width=True)
                st.balloons()
            else:
                st.error(f"Hata: {response.status_code}. Lütfen model uyanana kadar 20 sn bekleyip tekrar basın.")

st.divider()
st.caption("Aşama 1: Tasarım Kalitesi Artırıldı ✅")