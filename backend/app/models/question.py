import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from uuid import UUID

if TYPE_CHECKING:
    from .interview import Interview


# Base schema shared by all variants
class QuestionBase(SQLModel):
    description: str
    type: str  # e.g., "behavioral", "trees", "dynamic programming"


# SQLModel Table
class Question(QuestionBase, table=True):
    __tablename__ = "Question"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    deleted_at: Optional[datetime] = Field(default=None)

    # Foreign key
    interview_id: uuid.UUID = Field(foreign_key="Interview.id", nullable=False)

    # Relationship
    interview: Optional["Interview"] = Relationship(back_populates="questions")


# Public response model
class QuestionPublic(QuestionBase):
    id: uuid.UUID
    created_at: datetime
    interview_id: uuid.UUID


# Used for manually creating a question
class QuestionCreate(SQLModel):
    description: str
    type: str
    interview_id: uuid.UUID


# Used for AI generation input
class QuestionGenerateRequest(BaseModel):
    resume_id: UUID
    interview_id: UUID
    num_questions: int
