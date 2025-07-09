from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from datetime import timedelta

from app.models.user import UserLogin, UserRegister, UserPublic, Token
from app.core.security import verify_password, create_access_token
from app.services import crud
from app.core.config import settings
from app.core.db import engine


# Session dependency function
def get_session():
    with Session(engine) as session:
        yield session


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
def register(user_in: UserRegister, session: Session = Depends(get_session)):
    existing_email = crud.get_user_by_email(session, user_in.email)
    existing_username = crud.get_user_by_username(session, user_in.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(session, user_in)


@router.post("/login", response_model=Token)
def login(user_in: UserLogin, session: Session = Depends(get_session)):
    user = crud.get_user_by_email(session, user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token, token_type="bearer")


@router.post("/logout")
def logout():
    return {"msg": "Logged out"}
