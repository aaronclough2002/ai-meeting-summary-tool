import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# ---------- PAGE CONFIG (ONLY ONCE) ----------
st.set_page_config(
    page_title="AI Meeting Summary Tool",
    page_icon="📝",
    layout="wide",
)

# ---------- CLEAN THEME (MATCHES YOUR SITE) ----------
st.html("""
<style>
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #eef5ef 0%, #e8f1ea 100%);
}

h1, h2, h3 {
    color: #1e2f25;
}

.stButton > button {
    background: #4a765b;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.6rem 1rem;
}

.stButton > button:hover {
    background: #335340;
}

textarea {
    border-radius: 10px !important;
}

hr {
    border: none;
    border-top: 1px solid #d8e5db;
    margin: 2rem 0;
}

.answer-card {
    background: #f5faf6;
    border: 1px solid #d8e5db;
    border-radius: 16px;
    padding: 16px;
    white-space: pre-wrap;
    line-height: 1.6;
}

.empty-state {
    border: 1px dashed #d8e5db;
    padding: 16px;
    border-radius: 16px;
    color: #5f6f63;
}
</style>
""")

# ---------- SETUP ----------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- HEADER ----------
st.title("AI Meeting Summary Tool")
st.caption("Built by Aaron Clough")

st.write(
    "Paste a meeting transcript, project notes, or weekly update and generate a clean, structured summary."
)

# ---------- STATE ----------
if "meeting_summary_output" not in st.session_state:
    st.session_state["meeting_summary_output"] = ""

# ---------- LAYOUT ----------
col1, col2 = st.columns(2)

# ---------- INPUT ----------
with col1:
    st.subheader("Input")

    transcript = st.text_area(
        "Paste notes here",
        placeholder="Paste meeting notes, transcript, or project update...",
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

# ---------- OUTPUT ----------
with col2:
    st.subheader("Output")

    if st.session_state["meeting_summary_output"]:
        st.markdown(
            f'<div class="answer-card">{st.session_state["meeting_summary_output"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="empty-state">No output yet.</div>',
            unsafe_allow_html=True,
        )