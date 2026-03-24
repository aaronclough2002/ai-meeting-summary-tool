import os

from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Create OpenAI client using API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="AI Meeting Summary Tool",
    page_icon="📝",
    layout="wide",
)

# ---------- STYLING ----------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0b1220 0%, #0f172a 100%);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 1.1rem;
        padding-bottom: 1rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    .top-note {
        color: #94a3b8;
        margin-bottom: 1rem;
        max-width: 920px;
        line-height: 1.5;
        font-size: 0.98rem;
    }

    .answer-card {
        border: 1px solid #ffffff;
        padding: 14px;
        border-radius: 8px;
        background: #0f172a;
        line-height: 1.55;
        white-space: pre-wrap;
    }

    .empty-state {
        border: 1px dashed #ffffff;
        padding: 14px;
        border-radius: 8px;
        color: #94a3b8;
    }

    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {
        border-radius: 8px;
    }

    div[data-testid="stTextArea"] textarea {
        min-height: 320px;
    }

    div[data-testid="stVerticalBlock"] > div:empty {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
st.title("AI Meeting Summary Tool")
st.caption("AI Demo | Built by Aaron Clough")

st.markdown(
    """
    <div class="top-note">
    Paste a meeting transcript, project notes, or weekly update text and generate a structured summary with key decisions, risks, and action items.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- SESSION STATE ----------
if "meeting_summary_output" not in st.session_state:
    st.session_state["meeting_summary_output"] = ""

# ---------- TOP ----------
col1, col2 = st.columns(2, gap="large")

# ---------- INPUT ----------
with col1:
    st.subheader("Meeting input")

    with st.expander("ℹ️ What kind of input works best?"):
        st.markdown("""
        This tool works best with:

        - **Meeting transcripts**
          - Full meeting notes or pasted transcripts
        - **Freeform weekly project updates**
          - A few paragraphs describing what happened this week
        - **Structured status notes**
          - Completed work, in progress items, risks, blockers, and next steps

        **Best results usually come from input that includes:**
        - key accomplishments
        - current work in progress
        - risks or blockers
        - owners or next steps

        **Examples of useful inputs:**
        - meeting transcript from a project sync
        - PM weekly status notes
        - raw notes from Jira, Slack, or email summaries
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

    generate_clicked = st.button("Generate Summary")

    if generate_clicked:
        if not transcript or not transcript.strip():
            st.error("Please paste a meeting transcript or project update first.")
            st.stop()

        prompt = f"""
You are helping generate a polished project or meeting summary for business stakeholders.

Summarize the content below into a clean, structured update.

Rules:
- Ignore filler, repetition, and side conversation.
- Focus on meaningful project, meeting, or business updates.
- Write clearly and professionally.
- If action items are present or implied, list them separately.
- If risks or blockers are present, include them.
- If decisions were made, include them.
- Do not invent facts that are not supported by the input.

Return the output in this format:

Summary:
[concise summary paragraph]

Key Points:
- ...
- ...
- ...

Risks / Blockers:
- ...
- ...

Action Items:
- Owner (if known): action item
- Owner (if known): action item

Input:
{transcript}
"""

        with st.spinner("Generating summary..."):
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
            )

        st.session_state["meeting_summary_output"] = response.output_text

# ---------- OUTPUT ----------
with col2:
    st.subheader("Generated summary")

    if st.session_state["meeting_summary_output"]:
        st.markdown(
            f'<div class="answer-card">{st.session_state["meeting_summary_output"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="empty-state">
            No summary yet. Paste a meeting transcript or project update on the left, then click <strong>Generate Summary</strong>.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------- BOTTOM SPACE ----------
st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)