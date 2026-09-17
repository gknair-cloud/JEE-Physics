import streamlit as st
import requests
import base64

st.set_page_config(page_title="JEE PCM Guru", page_icon="🎯", layout="centered")
st.title("🎯 JEE Main - PCM Guru")
st.caption("30 Q Mock Test | Doubt Solver | Formula")

try:
    GOOGLE_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_KEY = st.sidebar.text_input("Enter Google API Key", type="password")
    st.sidebar.link_button("Get Free Key", "https://aistudio.google.com/app/apikey")

if not GOOGLE_KEY:
    st.warning("API Key ഇടൂ")
    st.stop()

def call_gemini(prompt, image_file=None):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={GOOGLE_KEY}"
    parts = [{"text": prompt}]
    if image_file:
        b64 = base64.b64encode(image_file.getvalue()).decode('utf-8')
        parts.append({"inline_data": {"mime_type": image_file.type, "data": b64}})
    data = {"contents": [{"parts": parts}]}
    r = requests.post(url, json=data, timeout=60)
    if r.status_code == 200:
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {r.text[:500]}"

SYLLABUS = {
    "⚛️ Physics": ["Mechanics", "Thermodynamics", "Electrostatics", "Optics", "Modern Physics"],
    "🧪 Chemistry": ["Physical", "Inorganic", "Organic"],
    "📐 Maths": ["Algebra", "Calculus", "Coordinate", "Vectors"]
}

tab1, tab2, tab3, tab4 = st.tabs(["📸 Doubt Solver", "📝 Practice", "📖 Formula", "🎯 Mock Test (30Q)"])

with tab1:
    q = st.text_area("Doubt എഴുതൂ")
    img = st.file_uploader("Photo", type=["jpg", "png", "jpeg"])
    if st.button("Solve Now ⚡", type="primary"):
        if not q and not img:
            st.error("Question ഇടൂ")
        else:
            with st.spinner("Solving..."):
                st.markdown(call_gemini(f"You are JEE expert. Solve short: {q}", img))

with tab2:
    subject = st.selectbox("Subject", list(SYLLABUS.keys()))
    if st.button("5 Questions Generate"):
        st.markdown(call_gemini(f"Generate 5 JEE Main MCQ for {subject} with answers"))

with tab3:
    if st.button("Formula Sheet"):
        st.markdown(call_gemini("Give JEE PCM important formulas short"))

with tab4:
    st.subheader("🎯 30 Question Mini Mock - Real JEE Pattern")
    st.caption("10 Physics + 10 Chemistry + 10 Maths | 90 Minutes")

    if 'mock_q' not in st.session_state:
        st.session_state.mock_q = ""
        st.session_state.mock_started = False

    if not st.session_state.mock_started:
        level = st.select_slider("Level", ["Easy", "Medium", "Hard"], value="Medium")
        if st.button("Start 30Q Mock Test 🚀", type="primary", use_container_width=True):
            st.session_state.mock_started = True
            with st.spinner("30 Question Paper തയ്യാറാക്കുന്നു... 15 sec എടുക്കും"):
                prompt = f"""Create JEE Main Mock Test - EXACTLY 30 Questions.
                Pattern: Q1-10 Physics, Q11-20 Chemistry, Q21-30 Maths.
                Level: {level}. Mix of MCQ (4 options) and Numerical type.
                Format:
                Q1. question...
                A)...
                B)...
                Q2...
                IMPORTANT: Give ONLY questions, NO answers. Keep questions short."""
                st.session_state.mock_q = call_gemini(prompt)
                st.rerun()
    else:
        st.info("⏰ 30 Questions - 90 Min - Best of luck!")
        st.markdown(st.session_state.mock_q)
        st.divider()
        st.subheader("Answer Sheet")
        ans_input = st.text_area("നിങ്ങളുടെ ഉത്തരങ്ങൾ (Ex: 1-A 2-B 3-25... 30-C)", height=150)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Submit & Get Score", type="primary"):
                if len(ans_input) < 10:
                    st.warning("Answers എഴുതൂ")
                else:
                    with st.spinner("Paper Checking..."):
                        check_p = f"Questions: {st.session_state.mock_q}\n\nStudent answers: {ans_input}\n\nYou are JEE evaluator. Check answers, give Score out of 30, give correct answers, and give short explanation for wrong ones. Give motivation in Malayalam."
                        st.markdown(call_gemini(check_p))
        with c2:
            if st.button("🔄 New Mock Test"):
                st.session_state.mock_started = False
                st.session_state.mock_q = ""
                st.rerun()