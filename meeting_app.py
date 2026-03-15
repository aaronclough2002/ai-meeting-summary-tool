import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Create OpenAI client using API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# App title
st.title("AI Meeting Summary Tool")

# Text input for meeting transcript
transcript = st.text_area("Paste meeting transcript here")

# Button to generate summary
if st.button("Generate Summary"):

    prompt = f"""
Summarize the meeting and extract action items.

Meeting transcript:
{transcript}

Return:

Summary:
Action Items:
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    st.write(response.output_text)