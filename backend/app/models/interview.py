import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .question import Question
    from .message import Message
    from .feedback import Feedback


class InterviewBase(SQLModel):
    title: str
    context: str
    interview_type: str


class Interview(InterviewBase, table=True):
    __tablename__ = "Interview"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to User
    user_id: uuid.UUID = Field(foreign_key="User.id", nullable=False)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="interviews")
    questions: List["Question"] = Relationship(back_populates="interview")
    messages: List["Message"] = Relationship(back_populates="interview")
    feedback: Optional["Feedback"] = Relationship(back_populates="interview")


# For API responses
class InterviewPublic(InterviewBase):
    id: uuid.UUID
    title: str
    created_at: datetime
    user_id: uuid.UUID
    interview_type: str


# For creating new interviews
class InterviewCreate(SQLModel):
    title: str
    context: str
    interview_type: str
