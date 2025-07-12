import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .interview import Interview


class FeedbackBase(SQLModel):
    tone_summary: str
    speech_rate: Optional[str] = None
    overall_feedback: str


class Feedback(FeedbackBase, table=True):
    __tablename__ = "Feedback"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to Interview (one-to-one relationship)
    interview_id: uuid.UUID = Field(foreign_key="Interview.id", nullable=False, unique=True)

    # Relationship (one-to-one)
    interview: Optional["Interview"] = Relationship(back_populates="feedback")


# For API responses
class FeedbackPublic(FeedbackBase):
    id: uuid.UUID
    created_at: datetime
    interview_id: uuid.UUID


# For creating new feedback
class FeedbackCreate(SQLModel):
    tone_summary: str
    speech_rate: Optional[str] = None
    overall_feedback: str
    interview_id: uuid.UUID


# For updating feedback
class FeedbackUpdate(SQLModel):
    tone_summary: Optional[str] = None
    speech_rate: Optional[str] = None
    overall_feedback: Optional[str] = None
