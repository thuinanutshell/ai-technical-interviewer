import uuid
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi import UploadFile, File, Form
from sqlmodel import Session, select

from app.models.interview import Interview, InterviewPublic, InterviewCreate
from app.models.user import User
from app.models.message import Message, MessageCreate, MessagePublic
from app.models.feedback import Feedback, FeedbackCreate, FeedbackPublic
from app.models.question import Question
from app.api.deps import get_current_user, SessionDep
from fastapi.logger import logger
from app.services.ai_service import transcribe_audio, generate_interview_feedback
from typing import List

router = APIRouter(prefix="/interviews", tags=["Interviews"])


# Create a new interview session
@router.post("/", response_model=InterviewPublic)
async def create_interview(
    interview_data: InterviewCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    logger.info(f"Received data: {interview_data}")
    body = await request.json()
    print("Raw body:", body)
    interview = Interview(
        title=interview_data.title,
        context=interview_data.context,
        user_id=current_user.id,
        interview_type=interview_data.interview_type,
    )
    session.add(interview)
    session.commit()
    session.refresh(interview)
    return interview


# Get all interviews for the current user
@router.get("/", response_model=list[Interview])
async def get_all_interviews(
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    interviews = session.exec(
        select(Interview).where(Interview.user_id == current_user.id)
    ).all()
    return interviews


# Get a specific interview by ID
@router.get("/{interview_id}", response_model=Interview)
async def get_interview_by_id(
    interview_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    interview = session.get(Interview, interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


@router.post("/{interview_id}/chat", response_model=List[MessagePublic])
async def handle_audio_chat(
    interview_id: uuid.UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    interview = session.get(Interview, interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")

    audio_bytes = await file.read()
    user_text = transcribe_audio(audio_bytes)

    # Save user's message
    user_msg = Message(role="user", content=user_text, interview_id=interview_id)
    session.add(user_msg)
    session.commit()
    session.refresh(user_msg)

    # Get questions for this interview (ordered by creation)
    questions = session.exec(
        select(Question)
        .where(Question.interview_id == interview_id)
        .order_by(Question.created_at)
    ).all()

    if not questions:
        raise HTTPException(
            status_code=404, detail="No questions found for this interview"
        )

    # Count how many AI messages already exist to determine current question
    assistant_messages = session.exec(
        select(Message)
        .where(Message.interview_id == interview_id, Message.role == "assistant")
        .order_by(Message.created_at)
    ).all()

    current_question_index = len(assistant_messages)

    # Determine AI response
    if current_question_index >= len(questions):
        ai_reply = "Thank you! You've completed the interview. Please wait while we generate your feedback."
    else:
        current_question = questions[current_question_index]
        ai_reply = f"Thank you for your response. Here's your next question: {current_question.description}"

    # Save AI message
    ai_msg = Message(role="assistant", content=ai_reply, interview_id=interview_id)
    session.add(ai_msg)
    session.commit()
    session.refresh(ai_msg)

    return [user_msg, ai_msg]


@router.post("/{interview_id}/chat/coding", response_model=List[MessagePublic])
async def handle_coding_audio_chat(
    interview_id: uuid.UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    interview = session.get(Interview, interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview.interview_type != "coding":
        raise HTTPException(
            status_code=400, detail="This route only supports coding interviews"
        )

    # Transcribe
    audio_bytes = await file.read()
    user_text = transcribe_audio(audio_bytes)

    # Save user message
    user_msg = Message(role="user", content=user_text, interview_id=interview_id)
    session.add(user_msg)
    session.commit()
    session.refresh(user_msg)

    # Determine current UMPIRE step based on how many assistant messages already exist
    assistant_messages = session.exec(
        select(Message)
        .where(Message.interview_id == interview_id, Message.role == "assistant")
        .order_by(Message.created_at)
    ).all()

    current_step_index = len(assistant_messages)

    if current_step_index >= len(UMPIRE_STEPS):
        ai_reply = (
            "✅ You've completed all 6 UMPIRE stages. Generating final feedback soon..."
        )
    else:
        current_step = UMPIRE_STEPS[current_step_index]
        ai_reply = generate_prompt_for_step(current_step)

    # Save assistant message
    ai_msg = Message(role="assistant", content=ai_reply, interview_id=interview_id)
    session.add(ai_msg)
    session.commit()
    session.refresh(ai_msg)

    return [user_msg, ai_msg]


@router.post("/{interview_id}/feedback", response_model=FeedbackPublic)
async def generate_feedback_for_interview(
    interview_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    interview = session.get(Interview, interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Avoid generating duplicate feedback
    if interview.feedback:
        return interview.feedback

    # Get user messages
    messages = session.exec(
        select(Message)
        .where(Message.interview_id == interview_id, Message.role == "user")
        .order_by(Message.created_at)
    ).all()

    user_texts = [m.content for m in messages]

    if not user_texts:
        raise HTTPException(status_code=400, detail="No user responses to analyze.")

    # Generate feedback
    feedback_data = generate_interview_feedback(user_texts)

    feedback = Feedback(
        interview_id=interview_id,
        tone_summary=feedback_data.get("tone_summary", ""),
        speech_rate=feedback_data.get("speech_rate", ""),
        overall_feedback=feedback_data.get("overall_feedback", ""),
    )

    session.add(feedback)
    session.commit()
    session.refresh(feedback)
    return feedback


from fastapi import Form
from enum import Enum

UMPIRE_STEPS = ["Understand", "Match", "Plan", "Implement", "Review", "Evaluate"]


@router.post("/{interview_id}/chat/coding", response_model=List[MessagePublic])
async def handle_coding_chat(
    interview_id: uuid.UUID,
    user_input: str = Form(...),
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    interview = session.get(Interview, interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")

    if interview.interview_type != "coding":
        raise HTTPException(
            status_code=400, detail="This route only supports coding interviews"
        )

    # Save user message
    user_msg = Message(role="user", content=user_input, interview_id=interview_id)
    session.add(user_msg)
    session.commit()
    session.refresh(user_msg)

    # Get previous assistant messages to determine current step
    assistant_messages = session.exec(
        select(Message)
        .where(Message.interview_id == interview_id, Message.role == "assistant")
        .order_by(Message.created_at)
    ).all()

    current_step_index = len(assistant_messages)

    if current_step_index >= len(UMPIRE_STEPS):
        # End of interview
        ai_reply = "✅ You've completed the UMPIRE interview! Please wait while we generate your final feedback."
    else:
        current_step = UMPIRE_STEPS[current_step_index]
        ai_reply = generate_prompt_for_step(current_step)

    # Save assistant message
    ai_msg = Message(role="assistant", content=ai_reply, interview_id=interview_id)
    session.add(ai_msg)
    session.commit()
    session.refresh(ai_msg)

    return [user_msg, ai_msg]


def generate_prompt_for_step(step: str) -> str:
    prompts = {
        "Understand": "🧠 Step 1: Understand the problem. Ask clarifying questions, test edge cases, or rephrase the prompt.",
        "Match": "🧩 Step 2: Match this to a known problem type. What category or pattern does this resemble (e.g., DFS, sliding window)?",
        "Plan": "📝 Step 3: Plan your solution using pseudocode or diagrams. Describe your approach before coding.",
        "Implement": "💻 Step 4: Implement your solution in code.",
        "Review": "🔍 Step 5: Review your code with specific examples. Walk through line by line and track variable values.",
        "Evaluate": "⚙️ Step 6: Evaluate the performance. What's the time and space complexity? Any edge cases or tradeoffs?",
    }
    return prompts.get(step, "Great job! You've completed all steps.")
