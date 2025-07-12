import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User


class ResumeBase(SQLModel):
    parsed_data: str  # JSON string containing parsed resume data
    pdf_url: Optional[str] = None


class Resume(ResumeBase, table=True):
    __tablename__ = "Resume"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to User
    user_id: uuid.UUID = Field(foreign_key="User.id", nullable=False)

    # Relationship
    user: Optional["User"] = Relationship(back_populates="resumes")


# For API responses
class ResumePublic(ResumeBase):
    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID


# For creating new resumes
class ResumeCreate(SQLModel):
    parsed_data: str
    pdf_url: Optional[str] = None
