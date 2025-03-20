from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

app = Flask(__name__)
CORS(app) 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

PROMPT = """You are a YouTube video summarizer. You will take the transcript text 
and summarize the entire video into key points within 500 words and make it point wise and highlight the key points. Here is the transcript: """

def extract_transcript_details(youtube_video_url):
    """Fetch transcript of a YouTube video"""
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception:
        return None

def generate_gemini_content(transcript_text):
    """Summarize transcript using Google Gemini AI"""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(PROMPT + transcript_text)
        return response.text
    except Exception:
        return "Error generating summary."

@app.route("/summarize", methods=["POST"])
def summarize():
    """API Endpoint to process YouTube video URL and return summary"""
    data = request.json
    youtube_link = data.get("youtube_url", "")

    if not youtube_link:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    transcript_text = extract_transcript_details(youtube_link)

    if not transcript_text:
        return jsonify({"error": "Transcript not available for this video"}), 404

    summary = generate_gemini_content(transcript_text)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)

