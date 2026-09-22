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
    "⚛️ Physics": ["Units & Dimensions", "Kinematics", "Laws of Motion", "Work Energy", "Rotational Motion", "Gravitation", "Thermodynamics", "Electrostatics", "Current Electricity", "Magnetism", "Optics", "Modern Physics"],
    "🧪 Chemistry": ["Basic Concepts", "Atomic Structure", "Periodic Table", "Chemical Bonding", "Thermodynamics", "Equilibrium", "s-p Block", "d-f Block", "Coordination", "Organic Basics", "Hydrocarbons", "Aldehydes Ketones"],
    "📐 Maths": ["Sets, Relations & Functions","Complex Numbers and Quadratic Equations","Trigonometry","Matrices and Determinants","Permutations and Combinations", "Binomial Theorem and Its Simple Applications", "Sequence and Series","Limit, Continuity and Differentiability","Integral Calculus", "Differential Equations","Coordinate Geometry","Three Dimensional Geometry","Vector Algebra", "Statistics and Probability", "Sets & Functions", "Complex Numbers", "Matrices", "Permutation", "Sequence & Series", "Limits", "Differentiation", "Integration", "Differential Equations", "Coordinate Geometry", "Vectors & 3D", "Probability"]
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

    if 'prac_q' not in st.session_state:
        st.session_state.prac_q = ""
        st.session_state.prac_ans = ""
        st.session_state.prac_exp = ""

    if st.button("Generate PYQ Practice"):
        with st.spinner("PYQ തയ്യാറാക്കുന്നു..."):
            p = f"""Generate {num} JEE Main PYQ for {subject} {chapter}, Level {level}, Type {qtype}.
            RULES:
            1. Pick from 2020-2025 PYQ only, shuffle.
            2. Output in 3 SEPARATE SECTIONS with headings:

            ---QUESTIONS---
            Q1. [2023 PYQ] question + options A B C D
            Q2. [2024 PYQ]...

            ---ANSWER KEY---
            1 - B, 2 - A, 3 - 25... (only answers, no explanation)

            ---EXPLANATIONS---
            Q1. Correct B because... (2 lines trick)
            Q2....
            """
            full = call_gemini(p)
            # Split into 3 parts
            try:
                q_part = full.split("---ANSWER KEY---")[0].replace("---QUESTIONS---","").strip()
                ans_part = full.split("---ANSWER KEY---")[1].split("---EXPLANATIONS---")[0].strip()
                exp_part = full.split("---EXPLANATIONS---")[1].strip()
            except:
                q_part = full
                ans_part = "Answer Key generating... press Explain button"
                exp_part = "Press button for explanation"

            st.session_state.prac_q = q_part
            st.session_state.prac_ans = ans_part
            st.session_state.prac_exp = exp_part
            st.rerun()

    if st.session_state.prac_q:
        st.divider()
        st.subheader("📝 Questions (PYQ 2020-2025)")
        st.markdown(st.session_state.prac_q)

        col1, col2 = st.columns(2)
        with col1:
            show_ans = st.checkbox("🔑 Answer Key കാണിക്കൂ")
            if show_ans:
                st.success(st.session_state.prac_ans)

        with col2:
            show_exp = st.checkbox("💡 Explanation കാണിക്കൂ")
            if show_exp:
                st.info(st.session_state.prac_exp)

        if st.button("Clear & New Set"):
            st.session_state.prac_q = ""
            st.session_state.prac_ans = ""
            st.session_state.prac_exp = ""
            st.rerun()

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