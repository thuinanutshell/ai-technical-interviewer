from .user import User, UserBase, UserRegister, UserLogin, UserPublic, Token
from .resume import Resume, ResumeBase, ResumePublic, ResumeCreate
from .interview import (
    Interview,
    InterviewBase,
    InterviewPublic,
    InterviewCreate,
)
from .question import (
    Question,
    QuestionBase,
    QuestionPublic,
    QuestionCreate,
)
from .message import Message, MessageBase, MessagePublic, MessageCreate
from .feedback import (
    Feedback,
    FeedbackBase,
    FeedbackPublic,
    FeedbackCreate,
    FeedbackUpdate,
)

__all__ = [
    # User models
    "User",
    "UserBase",
    "UserRegister",
    "UserLogin",
    "UserPublic",
    "Token",
    # Resume models
    "Resume",
    "ResumeBase",
    "ResumePublic",
    "ResumeCreate",
    # Interview models
    "Interview",
    "InterviewBase",
    "InterviewPublic",
    "InterviewCreate",
    "InterviewUpdate",
    # Question models
    "Question",
    "QuestionBase",
    "QuestionPublic",
    "QuestionCreate",
    "QuestionUpdate",
    # Message models
    "Message",
    "MessageBase",
    "MessagePublic",
    "MessageCreate",
    # Feedback models
    "Feedback",
    "FeedbackBase",
    "FeedbackPublic",
    "FeedbackCreate",
    "FeedbackUpdate",
]

from sqlmodel import SQLModel

# This will be used by Alembic to get the metadata of all models
Base = SQLModel
