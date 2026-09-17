import streamlit as st
import requests
import base64

st.set_page_config(page_title="JEE PCM Guru", page_icon="🎯", layout="centered")
st.title("🎯 JEE Main - PCM Guru")
st.caption("Physics | Chemistry | Maths - NTA Pattern")

try:
    GOOGLE_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_KEY = st.sidebar.text_input("Enter Google API Key", type="password")
    st.sidebar.link_button("Get Free Key", "https://aistudio.google.com/app/apikey")

if not GOOGLE_KEY:
    st.warning("API Key ഇടൂ, എന്നിട്ട് തുടങ്ങാം")
    st.stop()

def call_gemini(prompt, image_file=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={GOOGLE_KEY}"
    parts = [{"text": prompt}]
    if image_file:
        b64 = base64.b64encode(image_file.getvalue()).decode('utf-8')
        parts.append({"inline_data": {"mime_type": image_file.type, "data": b64}})
    data = {"contents": [{"parts": parts}]}
    r = requests.post(url, json=data)
    return r.json()['candidates'][0]['content']['parts'][0]['text'] if r.status_code==200 else f"Error: {r.text}"

SYLLABUS = {
    "⚛️ Physics": ["Units & Dimensions", "Kinematics", "Laws of Motion", "Work Energy Power", "Rotational Motion", "Gravitation", "Properties of Matter", "Thermodynamics", "Oscillations & Waves", "Electrostatics", "Current Electricity", "Magnetism", "EMI & AC", "Optics", "Modern Physics"],
    "🧪 Chemistry": ["Some Basic Concepts", "Atomic Structure", "Periodic Table", "Chemical Bonding", "States of Matter", "Thermodynamics Chem", "Equilibrium", "Redox", "Hydrogen", "s-Block", "p-Block", "d & f Block", "Coordination Compounds", "Organic - Basic", "Hydrocarbons", "Haloalkanes", "Alcohols Phenols Ethers", "Aldehydes Ketones", "Amines", "Biomolecules"],
    "📐 Maths": ["Sets Relations Functions", "Complex Numbers", "Matrices Determinants", "Quadratic Equations", "Permutation Combination", "Binomial Theorem", "Sequence & Series", "Limits Continuity", "Differentiability", "Differentiation", "Indefinite Integration", "Definite Integration", "Differential Equations", "Coordinate Geometry", "Straight Lines", "Circles", "Parabola Ellipse Hyperbola", "Vectors", "3D Geometry", "Probability", "Statistics"]
}

subject = st.selectbox("Subject തിരഞ്ഞെടുക്കുക", list(SYLLABUS.keys()))
chapter = st.selectbox("Chapter", SYLLABUS[subject])
level = st.select_slider("Level", ["Easy", "JEE Main", "JEE Advanced"], value="JEE Main")

tab1, tab2, tab3 = st.tabs(["📸 Doubt Solver", "📝 Practice", "📖 Formula Sheet"])

with tab1:
    q = st.text_area(f"{subject} doubt എഴുതൂ")
    img = st.file_uploader("Photo ഉണ്ടെങ്കിൽ upload ചെയ്യൂ", type=["jpg","png","jpeg"])
    if st.button("Solve Now ⚡", type="primary"):
        if not q and not img: st.error("Question ഇടൂ")
        else:
            with st.spinner("Guru ആലോചിക്കുന്നു..."):
                prompt = f"You are JEE {subject} expert. Chapter {chapter}, Level {level}. Solve step-by-step with Concept, Formula, Trick, Final Answer in Malayalam + English mix. Question: {q}"
                st.markdown(call_gemini(prompt, img))

with tab2:
    num = st.slider("എത്ര ചോദ്യം?", 1, 20, 10, 5)
    qtype = st.radio("Type", ["MCQ", "Numerical Value"], horizontal=True)
    if st.button("Generate Practice Set"):
        with st.spinner("NTA style questions..."):
            p = f"Generate {num} NEW {qtype} JEE Main 2025 level questions for {subject} - {chapter} with answer key and detailed solution."
            st.markdown(call_gemini(p))

with tab3:
    if st.button("Show Full Formula Sheet"):
        st.markdown(call_gemini(f"Give complete revision formula sheet, shortcuts, PYQ tricks for JEE {subject} chapter {chapter}"))