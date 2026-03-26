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
html, body, [class*="css"] {
    font-family: "Segoe UI", Tahoma, sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #eef5ef 0%, #e8f1ea 100%) !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #eef5ef 0%, #e8f1ea 100%) !important;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0) !important;
}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3, p, label, div, span {
    color: #1e2f25 !important;
}

div[data-testid="stExpander"] {
    background: #f5faf6 !important;
    border: 1px solid #d8e5db !important;
    border-radius: 14px !important;
}

div[data-testid="stTextArea"] textarea {
    background: #ffffff !important;
    color: #1e2f25 !important;
    border: 1px solid #d8e5db !important;
    border-radius: 12px !important;
    min-height: 320px !important;
}

.stButton > button {
    background: #4a765b !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 0.65rem 1rem !important;
}

.stButton > button:hover {
    background: #335340 !important;
}

.answer-card {
    background: #f5faf6;
    border: 1px solid #d8e5db;
    border-radius: 16px;
    padding: 16px;
    white-space: pre-wrap;
    line-height: 1.6;
    color: #1e2f25;
}

.empty-state {
    background: #f5faf6;
    border: 1px dashed #d8e5db;
    padding: 16px;
    border-radius: 16px;
    color: #5f6f63;
}

hr {
    border: none;
    border-top: 1px solid #d8e5db;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("AI Meeting Summary Tool")
st.caption("Built by Aaron Clough")

st.write(
    "Paste a meeting transcript, project notes, or weekly update and generate a clean, structured summary."
)

if "meeting_summary_output" not in st.session_state:
    st.session_state["meeting_summary_output"] = ""

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Meeting input")

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

with col2:
    st.subheader("Generated summary")

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