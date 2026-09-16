import streamlit as st
import requests
import base64
from PIL import Image

st.set_page_config(page_title="JEE Physics Guru", page_icon="⚛️", layout="centered")
st.title("⚛️ JEE Main Physics - AI Guru")
st.caption("Mechanics | Electrodynamics | Modern Physics")

try:
    GOOGLE_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_KEY = st.sidebar.text_input("Enter Google API Key (free)", type="password")
    st.sidebar.link_button("Get Free Key", "https://aistudio.google.com/app/apikey")

if not GOOGLE_KEY:
    st.warning("API Key idu, app work aakilla.")
    st.stop()

def call_gemini(prompt, image_file=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={GOOGLE_KEY}"
    parts = [{"text": prompt}]
    if image_file:
        img_bytes = image_file.getvalue()
        b64 = base64.b64encode(img_bytes).decode('utf-8')
        parts.append({"inline_data": {"mime_type": image_file.type, "data": b64}})

    data = {"contents": [{"parts": parts}]}
    r = requests.post(url, json=data)
    if r.status_code == 200:
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {r.text}"

CHAPTERS = [
    "Units & Dimensions", "Kinematics", "Laws of Motion", "Work Energy Power",
    "Rotational Motion", "Gravitation", "Properties of Solids & Fluids",
    "Thermodynamics & KTG", "Oscillations & Waves", "Electrostatics",
    "Current Electricity", "Magnetic Effects", "EMI & AC", "Ray & Wave Optics",
    "Modern Physics"
]

tab1, tab2, tab3 = st.tabs(["📸 Doubt Solver", "📝 Practice Generator", "📖 Formula Bank"])

with tab1:
    chapter_hint = st.selectbox("Chapter ethannu thonunnu?", CHAPTERS)
    level = st.select_slider("Level", ["Easy", "JEE Main", "JEE Advanced"])
    user_q = st.text_area("Question type cheyyu or paste cheyyu")
    img = st.file_uploader("Question photo upload cheyyam", type=["jpg","png","jpeg"])

    if st.button("Solve Now ⚡", type="primary"):
        if not user_q and not img:
            st.error("Question idu")
        else:
            with st.spinner("Physics Guru aalo chikku..."):
                prompt = f"You are expert JEE Main Physics teacher from Kota. Chapter: {chapter_hint}, Level: {level}. Solve step-by-step. Concept, Formula, Steps, Final Answer, Mistake to avoid. Question: {user_q} Answer in simple English + Malayalam."
                ans = call_gemini(prompt, img)
                st.markdown(ans)

with tab2:
    ch = st.selectbox("Chapter select cheyyu", CHAPTERS, key="gen_ch")
    num = st.slider("Ethra question venam?", 1, 10, 5)
    q_type = st.radio("Type", ["MCQ (4 options)", "Numerical Value Type"], horizontal=True)
    if st.button("Generate Questions"):
        with st.spinner("NTA style questions undakku..."):
            p = f"Generate {num} NEW {q_type} questions for JEE Main Physics chapter {ch} with answer and solution. JEE 2024 level."
            st.markdown(call_gemini(p))

with tab3:
    f_ch = st.selectbox("Chapter", CHAPTERS, key="form_ch")
    if st.button("Show Formulas & Tricks"):
        p = f"Give complete formula sheet + shortcuts + pitfalls for JEE Main Physics {f_ch}. Revision ready."
        st.markdown(call_gemini(p))