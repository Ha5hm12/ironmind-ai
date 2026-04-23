import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ── 1. Setup ──────────────────────────────────────────────────────────────────
load_dotenv()

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception as e:
    api_key = os.getenv("GROQ_API_KEY")

st.write("Key found:", bool(api_key))  # debug line - remove later

if not api_key:
    st.error("❌ GROQ_API_KEY not found!")
    st.stop()

client = Groq(api_key=api_key)

client = Groq(api_key=api_key)

# ── 2. System Prompt (the "personality" of your bot) ─────────────────────────
SYSTEM_PROMPT = """You are IronMind AI, an elite personal fitness coach with 15+ years 
of experience in strength training, nutrition, and sports science.

Personality: Motivating, direct, science-backed, and no-nonsense. You push people 
to be their best but always prioritize safety and proper form.

Your expertise covers:
- Custom workout plans (strength, cardio, HIIT, flexibility)
- Nutrition and meal timing advice
- Recovery strategies and injury prevention
- Goal setting (fat loss, muscle gain, endurance)
- Exercise form and technique breakdowns

Rules:
- ONLY answer questions related to fitness, exercise, nutrition, recovery, or health.
- If someone asks something off-topic (politics, coding, etc.), firmly but politely 
  redirect them back to fitness.
- Always ask for relevant info (age, goal, fitness level) if not provided.
- Use bullet points and clear structure for workout plans.
- Add motivational sign-offs to your responses (short, punchy).
- Never recommend anything that could cause injury — always emphasize proper form."""

# ── 3. Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IronMind AI – Your Personal Coach",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 4. Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;500;600&display=swap');

/* ─ global ─ */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0d;
    color: #f0ece4;
}

/* ─ background texture ─ */
.stApp {
    background:
        radial-gradient(ellipse at 20% 10%, rgba(255, 80, 0, 0.08) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 90%, rgba(255, 200, 0, 0.06) 0%, transparent 60%),
        #0d0d0d;
}

/* ─ sidebar ─ */
section[data-testid="stSidebar"] {
    background: #111111;
    border-right: 1px solid #222;
}

/* ─ header ─ */
.ironmind-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    letter-spacing: 0.08em;
    background: linear-gradient(90deg, #ff5000, #ffb300);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.ironmind-sub {
    text-align: center;
    color: #888;
    font-size: 0.95rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* ─ stat badges ─ */
.badge-row {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
    flex-wrap: wrap;
}
.badge {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 30px;
    padding: 0.35rem 1rem;
    font-size: 0.8rem;
    color: #aaa;
    letter-spacing: 0.05em;
}
.badge span { color: #ff5000; font-weight: 600; }

/* ─ chat messages ─ */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.8rem 0;
}
.msg-user .bubble {
    background: linear-gradient(135deg, #ff5000, #cc3a00);
    color: #fff;
    padding: 0.9rem 1.2rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 72%;
    font-size: 0.95rem;
    line-height: 1.55;
    box-shadow: 0 4px 20px rgba(255,80,0,0.25);
}
.msg-coach {
    display: flex;
    justify-content: flex-start;
    margin: 0.8rem 0;
}
.msg-coach .bubble {
    background: #1c1c1c;
    border: 1px solid #2e2e2e;
    color: #eee;
    padding: 0.9rem 1.2rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 72%;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.coach-label {
    font-size: 0.7rem;
    color: #ff5000;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

/* ─ input box ─ */
.stChatInput textarea {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    color: #f0ece4 !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stChatInput textarea:focus {
    border-color: #ff5000 !important;
    box-shadow: 0 0 0 2px rgba(255,80,0,0.2) !important;
}

/* ─ sidebar elements ─ */
.sidebar-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #ff5000;
    letter-spacing: 0.06em;
    margin-bottom: 1rem;
}
.stSlider > div { color: #bbb; }

/* ─ divider ─ */
hr { border-color: #222 !important; }

/* ─ buttons ─ */
.stButton > button {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    color: #f0ece4 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: #ff5000 !important;
    color: #ff5000 !important;
    background: #1f1410 !important;
}
</style>
""", unsafe_allow_html=True)

# ── 5. Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Coach Settings</div>', unsafe_allow_html=True)

    temperature = st.slider("Response Intensity", 0.0, 1.0, 0.75, 0.05,
        help="Higher = more creative/varied responses")
    max_tokens = st.slider("Response Length", 150, 2048, 1024, 64,
        help="Max words in each reply")

    st.markdown("---")

    st.markdown("**🎯 Quick Prompts**")
    quick_prompts = [
        "Give me a 4-day split for muscle gain",
        "What should I eat before a workout?",
        "How do I fix my squat form?",
        "Create a beginner HIIT routine",
        "How much protein do I need daily?",
    ]
    for qp in quick_prompts:
        if st.button(qp, key=qp):
            st.session_state.quick_prompt = qp

    st.markdown("---")

    if st.button("🗑️ Reset Session"):
        st.session_state.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.pop("quick_prompt", None)
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small style='color:#555'>Powered by Groq · Llama 3.1<br>Built with Streamlit</small>",
        unsafe_allow_html=True
    )

# ── 6. Header ─────────────────────────────────────────────────────────────────
st.markdown('<div class="ironmind-title">IRONMIND AI</div>', unsafe_allow_html=True)
st.markdown('<div class="ironmind-sub">Elite Personal Fitness Coach · Powered by AI</div>', unsafe_allow_html=True)

st.markdown("""
<div class="badge-row">
  <div class="badge">🏋️ <span>Strength Training</span></div>
  <div class="badge">🥗 <span>Nutrition Plans</span></div>
  <div class="badge">🔥 <span>HIIT & Cardio</span></div>
  <div class="badge">😴 <span>Recovery Science</span></div>
</div>
""", unsafe_allow_html=True)

# ── 7. Session State ──────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# ── 8. Display Chat History ───────────────────────────────────────────────────
for message in st.session_state.chat_history[1:]:  # skip system message
    if message["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="bubble">{message["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-coach">
            <div class="bubble">
                <div class="coach-label">🏋️ IronMind Coach</div>
                {message["content"]}
            </div>
        </div>""", unsafe_allow_html=True)

# ── 9. Handle Quick Prompt from Sidebar ──────────────────────────────────────
if "quick_prompt" in st.session_state:
    user_input = st.session_state.pop("quick_prompt")
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.markdown(f"""
    <div class="msg-user">
        <div class="bubble">{user_input}</div>
    </div>""", unsafe_allow_html=True)

    with st.spinner("🔥 Your coach is analyzing..."):
        try:
            response = client.chat.completions.create(
                messages=st.session_state.chat_history,
                model="llama-3.1-8b-instant",
                temperature=temperature,
                max_tokens=max_tokens
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.markdown(f"""
            <div class="msg-coach">
                <div class="bubble">
                    <div class="coach-label">🏋️ IronMind Coach</div>
                    {reply}
                </div>
            </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ {str(e)}")
    st.rerun()

# ── 10. Chat Input ────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask your coach — workouts, nutrition, recovery..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    st.markdown(f"""
    <div class="msg-user">
        <div class="bubble">{prompt}</div>
    </div>""", unsafe_allow_html=True)

    with st.spinner("🔥 Your coach is analyzing..."):
        try:
            response = client.chat.completions.create(
                messages=st.session_state.chat_history,
                model="llama-3.1-8b-instant",
                temperature=temperature,
                max_tokens=max_tokens
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.markdown(f"""
            <div class="msg-coach">
                <div class="bubble">
                    <div class="coach-label">🏋️ IronMind Coach</div>
                    {reply}
                </div>
            </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ── 11. Footer ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#444; font-size:0.8rem; letter-spacing:0.05em;'>
    NO SHORTCUTS. NO EXCUSES. JUST RESULTS. 💪
</div>
""", unsafe_allow_html=True)
