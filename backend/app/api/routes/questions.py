import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.question import (
    Question,
    QuestionCreate,
    QuestionPublic,
    QuestionGenerateRequest,
)
from app.models.user import User
from app.models.interview import Interview
from app.models.resume import Resume
from app.api.deps import get_current_user, SessionDep
from app.services.ai_service import generate_behavioral_questions

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/", response_model=QuestionPublic)
async def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    """Manually create a question."""
    interview = session.get(Interview, question_data.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")

    question = Question(
        description=question_data.description,
        type=question_data.type,
        interview_id=question_data.interview_id,
    )
    session.add(question)
    session.commit()
    session.refresh(question)
    return question


@router.get("/", response_model=List[QuestionPublic])
async def get_all_questions(
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
    interview_id: Optional[uuid.UUID] = None,
):
    """Get all questions, optionally filtered by interview."""
    if interview_id:
        interview = session.get(Interview, interview_id)
        if not interview or interview.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Interview not found")

        questions = session.exec(
            select(Question).where(Question.interview_id == interview_id)
        ).all()
    else:
        questions = session.exec(
            select(Question).join(Interview).where(Interview.user_id == current_user.id)
        ).all()

    return questions


@router.post("/generate", response_model=List[QuestionPublic])
async def generate_questions_from_resume(
    data: QuestionGenerateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    """Generate behavioral questions from resume using AI."""
    resume = session.get(Resume, data.resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")

    interview = session.get(Interview, data.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Generate questions using your AI service
    generated_questions = generate_behavioral_questions(
        parsed_resume=resume.parsed_data,
        num_questions=data.num_questions,
    )

    created_questions = []
    for q in generated_questions:
        question = Question(
            description=q,
            type="behavioral",
            interview_id=interview.id,
        )
        session.add(question)
        created_questions.append(question)

    session.commit()
    return created_questions
