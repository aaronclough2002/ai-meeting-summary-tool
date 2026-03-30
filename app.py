import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI Meeting Summary Tool",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
:root {
    --bg: linear-gradient(180deg, #eef5ef 0%, #e7f0e9 100%);
    --panel: rgba(255, 255, 255, 0.94);
    --panel-soft: #f5faf6;
    --hero: #dcebdd;
    --text: #1c2f25;
    --muted: #5f7165;
    --accent: #4a765b;
    --accent-dark: #335340;
    --line: rgba(60, 90, 69, 0.12);
    --shadow: 0 14px 34px rgba(0, 0, 0, 0.06);
    --radius: 22px;
}

/* Base */
html, body, [class*="css"] {
    font-family: "Segoe UI", Tahoma, sans-serif;
    color: var(--text);
}

.stApp,
[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit top spacing junk a bit */
[data-testid="stToolbar"] {
    right: 1rem;
}

/* Main typography */
h1, h2, h3, h4, p, label, div, span {
    color: var(--text) !important;
}

/* Outer hero card */
.hero-card {
    background: var(--panel);
    border-radius: var(--radius);
    padding: 32px 34px;
    box-shadow: var(--shadow);
    margin-bottom: 24px;
    border: 1px solid rgba(255,255,255,0.4);
}

.hero-title {
    margin: 0 0 10px 0;
    font-size: 46px;
    letter-spacing: -0.8px;
    line-height: 1.1;
    color: var(--text) !important;
}

.hero-subtitle {
    font-size: 19px;
    line-height: 1.85;
    color: #24362b !important;
    margin: 0;
}

/* Column cards */
.section-card {
    background: var(--panel);
    border-radius: var(--radius);
    padding: 24px;
    box-shadow: var(--shadow);
    border: 1px solid rgba(255,255,255,0.4);
    height: 100%;
}

.section-heading {
    margin: 0 0 14px 0;
    font-size: 30px;
    letter-spacing: -0.4px;
    color: var(--text) !important;
}

/* Expander */
div[data-testid="stExpander"] {
    background: var(--panel-soft) !important;
    border: 1px solid var(--line) !important;
    border-radius: 18px !important;
    overflow: hidden !important;
}

/* Text area */
div[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    color: var(--text) !important;
    border: 1px solid #d8e5db !important;
    border-radius: 16px !important;
    min-height: 320px !important;
    padding: 16px !important;
    font-size: 16px !important;
    line-height: 1.6 !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border: 1px solid #b7cfbd !important;
    box-shadow: 0 0 0 1px #b7cfbd !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 0.75rem 1.15rem !important;
    transition: 0.2s ease !important;
    box-shadow: none !important;
}

.stButton > button:hover {
    background: var(--accent-dark) !important;
    transform: translateY(-1px);
}

/* Output cards */
.answer-card {
    background: var(--panel-soft);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 22px;
    white-space: pre-wrap;
    line-height: 1.7;
    color: #24362b;
    font-size: 16px;
    min-height: 320px;
}

.empty-state {
    background: var(--panel-soft);
    border: 1px dashed #cfded2;
    padding: 22px;
    border-radius: 20px;
    color: var(--muted);
    line-height: 1.7;
    min-height: 320px;
}

/* Status messages */
[data-testid="stAlert"] {
    border-radius: 16px !important;
}

/* Caption */
div[data-testid="stCaptionContainer"] {
    margin-top: -2px;
    margin-bottom: 8px;
}

/* Horizontal rule */
hr {
    border: none;
    border-top: 1px solid #d8e5db;
    margin: 2rem 0;
}

/* Mobile */
@media (max-width: 900px) {
    .hero-title {
        font-size: 38px;
    }

    .hero-subtitle {
        font-size: 18px;
    }
}

@media (max-width: 600px) {
    .block-container {
        padding-top: 1rem;
    }

    .hero-card,
    .section-card {
        padding: 22px;
    }

    .hero-title {
        font-size: 32px;
    }

    .hero-subtitle {
        font-size: 17px;
    }
}
</style>
""", unsafe_allow_html=True)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.markdown("""
<div class="hero-card">
    <h1 class="hero-title">AI Meeting Summary Tool</h1>
    <p class="hero-subtitle">
        Paste a meeting transcript, project notes, or weekly update and generate a clean,
        structured summary with a polished look that matches the rest of your portfolio.
    </p>
</div>
""", unsafe_allow_html=True)

st.caption("Built by Aaron Clough")

if "meeting_summary_output" not in st.session_state:
    st.session_state["meeting_summary_output"] = ""

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-heading">Meeting input</h2>', unsafe_allow_html=True)

    with st.expander("ℹ️ What kind of input works best?"):
        st.markdown("""
- Meeting transcripts  
- Weekly project updates  
- Structured status notes  

Best results usually include:
- accomplishments
- current work in progress
- risks or blockers
- owners or next steps
""")

    transcript = st.text_area(
        "Paste meeting transcript or project notes",
        placeholder=(
            "Paste a transcript, meeting notes, or weekly update here...\n\n"
            "Example:\n"
            "- Completed this week:\n"
            "- In progress:\n"
            "- Risks/blockers:\n"
            "- Next steps:"
        ),
        label_visibility="collapsed",
    )

    if st.button("Generate Summary"):
        if not transcript.strip():
            st.error("Please paste content first.")
            st.stop()

        prompt = f"""
Summarize this into a professional project update.

Include:
- Summary
- Key Points
- Risks / Blockers
- Action Items

Input:
{transcript}
"""

        with st.spinner("Generating..."):
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
            )

        st.session_state["meeting_summary_output"] = response.output_text

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-heading">Generated summary</h2>', unsafe_allow_html=True)

    if st.session_state["meeting_summary_output"]:
        st.markdown(
            f'<div class="answer-card">{st.session_state["meeting_summary_output"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="empty-state">No summary yet. Paste a meeting transcript or project update on the left, then click <strong>Generate Summary</strong>.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)