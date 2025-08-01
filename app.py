import streamlit as st
import os
from dotenv import load_dotenv
import json
import VideoToSummary
import google.generativeai as genai
import re
# Load Gemini API
load_dotenv()
key = os.getenv("GOOGLE_GENAI_API")
genai.configure(api_key=key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# ---------- Prompt Functions ----------

def generate_summary(transcript):
    summary_prompt = '''You are a YouTube video summarizer. You will take the transcript 
    text and summarize the entire video, including all the important points.
    Return the output in 250 words as a paragraph. Please provide the summary of the text given:\n'''
    response = model.generate_content(summary_prompt + transcript)
    return response.text

def generate_mcq(summary):
    prompt = f'''Create four multiple choice questions based on this: {summary} 
    Return only valid JSON in the following format:
    {{
    "title": "",
    "quiz": [
        {{
        "question": "",
        "options": ["", "", "", ""],
        "answer": ""
        }},
        ...
    ]
    }}'''
    response = model.generate_content(prompt)
    match=re.search(r"\{.*\}",response.text,re.DOTALL)
    json_str=match.group()
    return json.loads(json_str)

# ---------- Streamlit GUI ----------
st.title("GenTube AI 🤖")
st.caption("YouTube Video Summary & Quiz Generator")
st.markdown("Paste a YouTube video URL below and get a summary and quiz based on its transcript.")
import streamlit as st

import streamlit as st

# Inject custom CSS
st.markdown("""
    <style>
    /*Page background */
    .stApp {
        background-color: #1e2f33;
        color: #ffffff;
        padding: 1rem;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Input form styling */
    .block-container {
        padding: 2rem 2rem 1rem;
    }

    .element-container:has(input), .element-container:has(button) {
    width: 100% !important;
    max-width: 100% !important;
    padding-left: 0;
    padding-right: 0;
}

    /* Style text input */
    input[type="text"] {
        background-color: #2f3e46;
        color: #ffffff;
        border: 2px solid #607d8b;
        border-radius: 8px;
        padding: 10px;
    }

    /* Button style */
    button[kind="primary"] {
        background-color: #ff4b4b;
        color: white;
        border-radius: 6px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        margin-top: 10px;
    }

    /* Summary and quiz columns */
    .css-1kyxreq, .css-1n76uvr {
        background-color: #2a3b3f;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 2rem;
    }

    /* Subheaders */
    h3 {
        color: #ffd700;
    }

    /* Final score */
    .stMarkdown h3 {
        color: #80cbc4;
    }
    h1 {
    padding-topp:5px;
    line-height: 1.5;
    }
    
    </style>
    
""", unsafe_allow_html=True)

st.toast("the youtube-transcript-api library is being blocked by YouTube because developer using cloud server and this library do not work on cloud.Run this app locally on your personal device instead of a cloud platform")

# Top: Input + Button
with st.form("youtube_form"):
    youtube_url = st.text_input("Enter YouTube Video URL:")
    submitted = st.form_submit_button("Get Result")

# ---------- Generate or Load Data ----------
if submitted and youtube_url:
    transcript = VideoToSummary.extract_transcript_details(youtube_url)
    if transcript:
        summary = generate_summary(transcript)
        quiz_data = generate_mcq(summary)

        st.session_state.transcript = transcript
        st.session_state.summary = summary
        st.session_state.quiz_data = quiz_data
        st.session_state.score = 0
        st.session_state.answered = [False] * len(quiz_data["quiz"])
        st.session_state.user_answers = [None] * len(quiz_data["quiz"])
    else:
        st.error("Transcript not found. Check if the video has English captions.")

# ---------- Display if data is available ----------
if "summary" in st.session_state and "quiz_data" in st.session_state:
    summary = st.session_state.summary
    quiz_data = st.session_state.quiz_data

    col1, col2 = st.columns(2)

    # Left column: Summary
    with col1:
        st.subheader("📄 Video Summary")
        st.write(summary)

    # Right column: Quiz
    with col2:
        st.subheader("❓ Quiz Questions")

        for i, q in enumerate(quiz_data["quiz"]):
            st.markdown(f"**Q{i+1}: {q['question']}**")

            if not st.session_state.answered[i]:
                selected = st.radio(f"Choose your answer for Q{i+1}:", q["options"], key=f"q{i}")
                if st.button(f"Submit Q{i+1}", key=f"submit{i}"):
                    st.session_state.answered[i] = True
                    st.session_state.user_answers[i] = selected
                    correct = q["answer"]
                    if selected == correct:
                        st.success("✅ Correct!")
                        st.session_state.score += 1
                    else:
                        st.error(f"❌ Incorrect! Correct answer: **{correct}**")
            else:
                user_answer = st.session_state.user_answers[i]
                correct = q["answer"]
                if user_answer == correct:
                    st.success(f"✅ You chose **{user_answer}** — Correct!")
                else:
                    st.warning(f"❌ You chose **{user_answer}** — Correct answer: **{correct}**")

        st.markdown("---")
        st.markdown(f"### 🧮 Final Score: `{st.session_state.score} / {len(quiz_data['quiz'])}`")

st.markdown("""
    <hr>
    <div style="text-align: center; padding: 10px; font-size: 0.9rem; color: #ccc;">
        Made by <a href="https://www.linkedin.com/in/abhishek07122002" target="_blank" style="color: #00bcd4; text-decoration: none;">Abhishek Agrawal</a>
    </div>
""", unsafe_allow_html=True)
        
