# GenTube-AI: Powered YouTube Video Summarizer & Quiz Generator

GenTube is a GenAI-powered web application that transforms educational YouTube videos into concise summaries and interactive quizzes using Google's Gemini Pro API. The application automatically fetches the transcript of any public YouTube video, summarizes the content in under 250 words, and generates multiple-choice questions to help users actively learn and retain information.

Built with Streamlit for an intuitive UI, GenTube offers an efficient, AI-enhanced learning experience by combining transcript processing, large language model prompting, and dynamic quiz interaction in one platform.

---

## 🚀 Features

- 🔗 **YouTube Integration** – Paste any YouTube URL to extract video transcript (if captions are available).
- 🧠 **Gemini-Powered Summarizer** – AI-generated summaries under 250 words using Gemini Pro API.
- ❓ **MCQ Generator** – Generates multiple-choice questions with answers in JSON format.
- ✅ **Interactive Quiz** – Users select answers, get instant feedback, and see their score.
- 🎨 **Custom UI Styling** – Dark-themed, responsive Streamlit UI with enhanced styling using custom CSS.

---

## 🧠 How It Works

**Transcript Retrieval :** The application extracts the transcript of a YouTube video using the [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/). It supports both manually created and auto-generated English captions from public videos.

**Summary & Quiz Generation :** The extracted transcript is passed to Google's Gemini Pro large language model (LLM) using predefined prompt templates. The model first generates a concise summary of the video content, then creates an interactive multiple-choice quiz highlighting the key concepts discussed in the video.

## 🛠️ Tech Stack

| Component                | Technology                          |
|--------------------------|--------------------------------------|
| Frontend/UI              | Streamlit (Python)                   |
| AI Model                 | Google Gemini 1.5 Flash              |
| Transcript API           | youtube-transcript-api               |
| Language                 | Python 3.x                           |
| Styling                  | Custom CSS in Streamlit              |
| Environment Variables    | python-dotenv                        |

---
## 🙋‍♂️ Author
- Abhishek Agarwal
- 💼 Beginner in Generative AI & Prompt Engineering
- 🌐 LinkedIn https://www.linkedin.com/in/abhishek07122002/
  


