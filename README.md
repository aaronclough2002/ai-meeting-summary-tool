# AI Meeting Summary Tool

A simple AI web app built with Python and Streamlit.

Users can paste meeting notes or a transcript and generate:

• a summary  
• action items  

The AI processing is powered by the OpenAI API.

## Tech Stack

Python  
Streamlit  
OpenAI API  

## Run Locally

Install dependencies:

pip install -r requirements.txt

Create a `.env` file with your API key:

OPENAI_API_KEY=your_key_here

Run the app:

streamlit run meeting_app.py