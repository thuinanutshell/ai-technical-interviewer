"""
AI Services:
1. Generate behavioral questions from parsed resume using Google Gemini API
2. Transcribe audio using open-source Whisper
3. Generate multi-turn follow-up question (Gemini)
4. (TODO) Provide AI feedback
"""

import os
import tempfile
from typing import List
import json
import re

from dotenv import load_dotenv
import google.generativeai as genai
import whisper

from app.models.message import Message

# -----------------------------
# 0. Load environment and setup
# -----------------------------

load_dotenv(dotenv_path=".env.development")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------
# 1. Behavioral Question Generation (Gemini)
# -----------------------------

BEHAVIORAL_QUESTION_PROMPT = """
You're a technical interviewer. Given a candidate's resume, generate {num_questions} high-quality behavioral interview questions. These should focus on soft skills, leadership, teamwork, communication, conflict resolution, and self-improvement.

Resume:
---------
{resume}
---------
Return only a numbered list of questions, without explanations.
"""


def generate_behavioral_questions(
    parsed_resume: str, num_questions: int = 5
) -> List[str]:
    prompt = BEHAVIORAL_QUESTION_PROMPT.format(
        resume=parsed_resume,
        num_questions=num_questions,
    )

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    if not response.text:
        raise RuntimeError("Gemini did not return any output.")

    # Basic parsing of numbered list
    questions = [
        line.strip().lstrip("1234567890. ").strip()
        for line in response.text.splitlines()
        if line.strip()
    ]
    return [q for q in questions if q]


# -----------------------------
# 2. Audio Transcription (Whisper Open Source)
# -----------------------------


def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribe a user's audio response using open-source Whisper.
    """
    model = whisper.load_model("base")
    with tempfile.NamedTemporaryFile(suffix=".webm") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio.flush()
        result = model.transcribe(temp_audio.name)
        return result["text"]


def extract_json_from_text(text: str) -> dict:
    try:
        # Try direct JSON load first
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: extract JSON inside triple backticks or braces
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in model response.")
        json_str = json_match.group()
        return json.loads(json_str)


def generate_interview_feedback(user_responses: List[str]) -> dict:
    joined_responses = "\n\n".join(user_responses)

    prompt = f"""
    You are an AI mock interviewer. Based on the following responses from a candidate's behavioral interview, generate:

    1. A brief summary of their tone (e.g., polite, confident, nervous).
    2. A comment on their speech rate (e.g., fast, slow, moderate) – assume these were audio answers.
    3. An overall performance feedback focusing on clarity, communication, and behavioral impact.

    Responses:
    ----------------
    {joined_responses}
    ----------------

    Respond ONLY with a JSON object using the following keys:
    "tone_summary", "speech_rate", "overall_feedback"
        """

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    print("🔍 Gemini Raw Output:", repr(response.text))

    return extract_json_from_text(response.text)
