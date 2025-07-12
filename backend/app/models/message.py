import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .interview import Interview


class MessageBase(SQLModel):
    role: str
    content: str


class Message(MessageBase, table=True):
    __tablename__ = "Message"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key to Interview
    interview_id: uuid.UUID = Field(foreign_key="Interview.id", nullable=False)

    # Relationship
    interview: Optional["Interview"] = Relationship(back_populates="messages")


# For API responses
class MessagePublic(MessageBase):
    id: uuid.UUID
    created_at: datetime
    interview_id: uuid.UUID


# For creating new messages
class MessageCreate(SQLModel):
    role: str
    content: str
    interview_id: uuid.UUID
