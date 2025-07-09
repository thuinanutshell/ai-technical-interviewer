from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode
from sqlmodel import Session
from app.core.db import engine
from app.core.config import settings
from app.models.user import Token, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Depends(get_session)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = SessionDep,
) -> User:
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid token")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
