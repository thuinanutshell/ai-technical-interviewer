import uuid
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .resume import Resume
    from .interview import Interview


# Base model for shared fields
class UserBase(SQLModel):
    email: EmailStr = Field(index=True)
    username: str = Field(index=True, max_length=255)


# DB model that inherits from the base model
class User(UserBase, table=True):
    __tablename__ = "User"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    deleted_at: Optional[datetime] = Field(default=None)

    # One-to-many relationships
    resumes: List["Resume"] = Relationship(back_populates="user")
    interviews: List["Interview"] = Relationship(back_populates="user")


# Input that the server expects to receive for registration
class UserRegister(SQLModel):
    email: EmailStr
    username: str
    password: str


# Input that the server expects to receive for login
class UserLogin(SQLModel):
    email: EmailStr
    password: str


# Output from the server sent to the client (public data)
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime


# JWT token response
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
