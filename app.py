import streamlit as st
import requests
import base64

st.set_page_config(page_title="JEE PCM Guru", page_icon="🎯", layout="centered")
st.title("🎯 JEE Main - PCM Guru")
st.caption("PYQ | Practice | Mock Test - 2020-2025")

try:
    GOOGLE_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_KEY = st.sidebar.text_input("Enter Google API Key", type="password")
    st.sidebar.link_button("Get Free Key", "https://aistudio.google.com/app/apikey")

if not GOOGLE_KEY:
    st.warning("API Key ഇടൂ")
    st.stop()

def call_gemini(prompt, image_file=None):
    # 100% CORRECT MODEL NAME - ഇത് മാറ്റരുത്
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

subject = st.selectbox("Subject", list(SYLLABUS.keys()))
chapter = st.selectbox("Chapter", SYLLABUS[subject])
level = st.select_slider("Level", ["Easy", "JEE Main", "JEE Advanced"], value="JEE Main")

tab1, tab2, tab3, tab4 = st.tabs(["📸 Doubt Solver", "📝 Practice PYQ", "📖 Formula", "🎯 Mock Test (30Q PYQ)"])

with tab1:
    q = st.text_area(f"{subject} doubt എഴുതൂ")
    img = st.file_uploader("Photo ഉണ്ടെങ്കിൽ", type=["jpg", "png", "jpeg"])
    if st.button("Solve Now ⚡", type="primary"):
        if not q and not img:
            st.error("Question ഇടൂ")
        else:
            with st.spinner("Solving..."):
                st.markdown(call_gemini(f"You are JEE {subject} expert. Chapter {chapter}, Level {level}. Solve step by step short. Q: {q}", img))

with tab2:
    num = st.slider("എത്ര ചോദ്യം?", 5, 20, 10)
    qtype = st.radio("Type", ["MCQ", "Numerical", "Mixed PYQ"], horizontal=True)
    if st.button("Generate Practice with Explanation"):
        with st.spinner("PYQ തയ്യാറാക്കുന്നു..."):
            p = f"""Generate {num} JEE Main Previous Year Questions (PYQ) for {subject} {chapter}, Level {level}, Type {qtype}.
            RULES:
            1. MUST pick from last 5 years PYQ (2020-2025).
            2. For each question, MANDATORY format:
               Q1. [2023 PYQ] question...
               A)...
               Correct Answer: B
               Explanation: short 2-3 line trick
            3. Shuffle years.
            4. Give FULL answer + explanation for every question."""
            st.markdown(call_gemini(p))

with tab3:
    if st.button("Show Formula Sheet"):
        st.markdown(call_gemini(f"Give JEE formula sheet for {subject} {chapter} short"))

with tab4:
    st.subheader("🎯 30Q Mock - Last 5 Years PYQ Shuffled")
    st.caption("10 Physics + 10 Chemistry + 10 Maths | Real JEE PYQ 2020-2025")

    if 'mock_q' not in st.session_state:
        st.session_state.mock_q = ""
        st.session_state.mock_started = False

    if not st.session_state.mock_started:
        if st.button("Start 30Q PYQ Mock Test 🚀", type="primary", use_container_width=True):
            st.session_state.mock_started = True
            with st.spinner("30 PYQ Paper തയ്യാറാക്കുന്നു... 15 sec"):
                prompt = f"""Create JEE Main 30Q Mock Test - ONLY from PYQ Last 5 Years (2020-2025).
                Pattern: Q1-10 Physics, Q11-20 Chemistry, Q21-30 Maths.
                MUST shuffle years, add tag like [2022], [2024] for each Q.
                Level {level}. Give ONLY questions with options, NO answers now."""
                st.session_state.mock_q = call_gemini(prompt)
                st.rerun()
    else:
        st.info("⏰ 30 Questions - Real PYQ - 90 Min")
        st.markdown(st.session_state.mock_q)
        st.divider()
        user_ans = st.text_area("Answers എഴുതൂ (1-A, 2-C...)")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Check Score + Explain"):
                if user_ans:
                    with st.spinner("Checking..."):
                        check = f"Q: {st.session_state.mock_q}\nStudent: {user_ans}\nCheck score out of 30, give correct answers with 2-line explanation for each wrong one."
                        st.markdown(call_gemini(check))
        with c2:
            if st.button("🔄 New Paper"):
                st.session_state.mock_started = False
                st.session_state.mock_q = ""
                st.rerun()