import uuid
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


# Base model for shared fields
class UserBase(SQLModel):
    email: EmailStr = Field(index=True)
    username: str = Field(index=True, max_length=255)


# DB model
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Input for registration
class UserRegister(SQLModel):
    email: EmailStr
    username: str
    password: str


# Input for login
class UserLogin(SQLModel):
    email: EmailStr
    password: str


# Output for public data
class UserPublic(UserBase):
    id: uuid.UUID


# JWT token response
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
