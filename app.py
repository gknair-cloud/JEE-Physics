import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="JEE Physics Guru", page_icon="⚛️", layout="centered")

# --- CONFIG ---
st.title("⚛️ JEE Main Physics - AI Guru")
st.caption("Mechanics | Electrodynamics | Modern Physics")

# Get API Key safely
try:
    GOOGLE_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    GOOGLE_KEY = st.sidebar.text_input("Enter Google API Key (free)", type="password")
    st.sidebar.link_button("Get Free Key", "https://aistudio.google.com/app/apikey")

if not GOOGLE_KEY:
    st.warning("API Key idu, app work aakilla. Free key kittum.")
    st.stop()

genai.configure(api_key=GOOGLE_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- PHYSICS CHAPTERS as per NTA ---
CHAPTERS = [
    "Units & Dimensions", "Kinematics", "Laws of Motion", "Work Energy Power",
    "Rotational Motion", "Gravitation", "Properties of Solids & Fluids",
    "Thermodynamics & KTG", "Oscillations & Waves", "Electrostatics",
    "Current Electricity", "Magnetic Effects", "EMI & AC", "Ray & Wave Optics",
    "Modern Physics - Dual Nature, Atoms, Nuclei, Semiconductors"
]

FORMULA_BANK = {
    "Kinematics": "v = u+at, s=ut+0.5at^2, v^2=u^2+2as, projectile: R = u^2 sin2θ/g",
    "Laws of Motion": "F=ma, Friction: f=μN, Circular: a_c = v^2/r",
    "Work Energy Power": "W=F.s, KE=0.5mv^2, PE=mgh, W=ΔKE",
    "Rotational Motion": "τ=Iα, L=Iω, KE_rot=0.5Iω^2, Moment of Inertia formulas",
    "Electrostatics": "F=kq1q2/r^2, E=kq/r^2, V=kq/r, U=0.5CV^2",
    "Current Electricity": "V=IR, P=VI, Series/Parallel, Kirchhoff laws",
    "Modern Physics": "E=hf, λ=h/p, Bohr model: r_n = n^2 h^2 / (4π^2 mke^2), Radioactive decay"
}

tab1, tab2, tab3 = st.tabs(["📸 Doubt Solver", "📝 Practice Generator", "📖 Formula Bank"])

with tab1:
    st.subheader("Doubt adikku")
    col1, col2 = st.columns(2)
    with col1:
        chapter_hint = st.selectbox("Chapter ethannu thonunnu?", CHAPTERS)
    with col2:
        level = st.select_slider("Level", ["Easy", "JEE Main", "JEE Advanced"])
    
    user_q = st.text_area("Question type cheyyu or paste cheyyu")
    img = st.file_uploader("Question photo upload cheyyam", type=["jpg","png","jpeg"])
    
    if st.button("Solve Now ⚡", type="primary"):
        if not user_q and not img:
            st.error("Question idu")
        else:
            with st.spinner("Physics Guru aalo chikku..."):
                prompt = f"""You are an expert JEE Main Physics teacher from Kota.
                Chapter: {chapter_hint}, Level: {level}
                Task: Solve this Physics doubt step-by-step like JEE teacher.
                Rules:
                1. Give Concept first (1 line)
                2. Then Formula used
                3. Step-by-step calculation
                4. Final Answer with option check if MCQ
                5. Common mistake to avoid
                Question: {user_q}
                Context Formulas: {FORMULA_BANK.get(chapter_hint, '')}
                Answer in simple English + some Malayalam explanation if possible.
                """
                if img:
                    import PIL.Image
                    image = PIL.Image.open(img)
                    response = model.generate_content([prompt, image])
                else:
                    response = model.generate_content(prompt)
                st.markdown(response.text)

with tab2:
    st.subheader("JEE Model Question Generator")
    ch = st.selectbox("Chapter select cheyyu", CHAPTERS, key="gen_ch")
    num = st.slider("Ethra question venam?", 1, 10, 5)
    q_type = st.radio("Type", ["MCQ (4 options)", "Numerical Value Type"], horizontal=True)
    
    if st.button("Generate Questions"):
        with st.spinner("NTA style questions undakku..."):
            p = f"Generate {num} NEW {q_type} questions for JEE Main Physics chapter {ch}. Each must have: Question, Options A-D if MCQ, Correct Answer, Detailed Solution. Difficulty: JEE Main 2024 level. Don't repeat PYQ exactly. Give as markdown table."
            res = model.generate_content(p)
            st.markdown(res.text)
            st.download_button("Download as PDF Text", res.text, file_name=f"{ch}_questions.txt")

with tab3:
    st.subheader("Formula Bank")
    f_ch = st.selectbox("Chapter", CHAPTERS, key="form_ch")
    if st.button("Show Formulas & Tricks"):
        p = f"Give complete formula sheet + shortcuts + dimensional tricks + common pitfalls for JEE Main Physics {f_ch}. Include all important formulas: {FORMULA_BANK.get(f_ch, 'all formulas')}. Make it revision-ready."
        res = model.generate_content(p)
        st.markdown(res.text)

st.sidebar.markdown("---")
st.sidebar.info("Tip: Photo eduthal clear aayittulla photo eduthu upload cheyyu. Answer copy adichu notes aakki vekkam.")