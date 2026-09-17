import streamlit as st
import requests
import base64

st.set_page_config(page_title="JEE PCM Guru", page_icon="🎯", layout="centered")
st.title("🎯 JEE Main - PCM Guru")
st.caption("Physics | Chemistry | Maths - Fast Doubt Solver")

try:
    GOOGLE_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_KEY = st.sidebar.text_input("Enter Google API Key", type="password")
    st.sidebar.link_button("Get Free Key", "https://aistudio.google.com/app/apikey")

if not GOOGLE_KEY:
    st.warning("API Key ഇടൂ")
    st.stop()

def call_gemini(prompt, image_file=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-8b:generateContent?key={GOOGLE_KEY}"
    parts = [{"text": prompt + "\n\nKeep answer short, 300 words max, to the point."}]
    if image_file:
        b64 = base64.b64encode(image_file.getvalue()).decode('utf-8')
        parts.append({"inline_data": {"mime_type": image_file.type, "data": b64}})
    data = {"contents": [{"parts": parts}]}
    r = requests.post(url, json=data, timeout=30)
    if r.status_code == 200:
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {r.text[:500]}"

SYLLABUS = {
    "⚛️ Physics": ["Units & Dimensions", "Kinematics", "Laws of Motion", "Work Energy", "Rotational Motion", "Gravitation", "Thermodynamics", "Electrostatics", "Current Electricity", "Magnetism", "Optics", "Modern Physics"],
    "🧪 Chemistry": ["Basic Concepts", "Atomic Structure", "Periodic Table", "Chemical Bonding", "Thermodynamics", "Equilibrium", "s-p Block", "d-f Block", "Coordination", "Organic Basics", "Hydrocarbons", "Aldehydes Ketones"],
    "📐 Maths": ["Sets & Functions", "Complex Numbers", "Matrices", "Permutation", "Sequence & Series", "Limits", "Differentiation", "Integration", "Differential Equations", "Coordinate Geometry", "Vectors & 3D", "Probability"]
}

subject = st.selectbox("Subject", list(SYLLABUS.keys()))
chapter = st.selectbox("Chapter", SYLLABUS[subject])
level = st.select_slider("Level", ["Easy", "JEE Main", "JEE Advanced"], value="JEE Main")

tab1, tab2, tab3 = st.tabs(["📸 Doubt Solver", "📝 Practice", "📖 Formula"])

with tab1:
    q = st.text_area(f"{subject} doubt എഴുതൂ")
    img = st.file_uploader("Photo ഉണ്ടെങ്കിൽ", type=["jpg", "png", "jpeg"])
    if st.button("Solve Now ⚡", type="primary"):
        if not q and not img:
            st.error("Question ഇടൂ")
        else:
            with st.spinner("Guru ആലോചിക്കുന്നു..."):
                prompt = f"You are JEE {subject} expert. Chapter {chapter}, Level {level}. Solve step by step. Q: {q}"
                answer = call_gemini(prompt, img)
                st.markdown(answer)

with tab2:
    num = st.slider("എത്ര ചോദ്യം?", 1, 10, 5)
    qtype = st.radio("Type", ["MCQ", "Numerical"], horizontal=True)
    if st.button("Generate Practice"):
        with st.spinner("Questions തയ്യാറാക്കുന്നു..."):
            p = f"Generate {num} NEW {qtype} JEE Main level questions for {subject} {chapter} with answer key."
            st.markdown(call_gemini(p))

with tab3:
    if st.button("Show Formula Sheet"):
        with st.spinner("Loading..."):
            st.markdown(call_gemini(f"Give formula sheet for JEE {subject} {chapter}"))
        