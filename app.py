import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv
import pathlib
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(youtube_url):
    try:
        query = urlparse(youtube_url)
        if query.hostname == "youtu.be":
            return query.path[1:]
        if query.hostname in ("www.youtube.com", "youtube.com"):
            return parse_qs(query.query)["v"][0]
        return None
    except Exception as e:
        st.error(f"Could not extract video ID: {e}")
        return None

def extract_transcript_details(youtube_url):
    try:
        video_id = get_video_id(youtube_url)
        print(video_id)
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        clear_text=""
            # is iterable
        for snippet in fetched_transcript:
                clear_text+=" "+snippet.text
        return clear_text
    except Exception as e:
        st.error(f"Transcript could not be fetched: {e}")
        return None

load_dotenv()

key=os.getenv("GOOGLE_GENAI_API")

genai.configure(api_key=key)

model=genai.GenerativeModel(model_name="gemini-1.5-flash")

prompt='''you are Youtube video summarizer. you will be taking the transcript 
text and summarizing the entire video and include all the importent point in summary.
Return the output with in 250 words in a paragraph formate. Please provide the summary of the text given :'''


def generate_gemini_content(transcript_text,prompt):
   
    response= model.generate_content(prompt+transcript_text)
    return response.text
  
st.title("youTube Transcript to Detailed")
youTube_link=st.text_input("Enter the YouTube video Link ")  
if youTube_link:
    video_id=youTube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
    
if st.button("Get Detailed Note"):
    transcript_text=extract_transcript_details(youTube_link)
    
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes: ")
        st.write(summary)
    



