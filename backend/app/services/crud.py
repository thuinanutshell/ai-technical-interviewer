from sqlmodel import Session, select
from app.models.user import User, UserRegister
from app.core.security import get_password_hash


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()

def get_user_by_username(session: Session, username: str) -> User | None:
   return session.exec(select(User).where(User.username == username)).first() 

def create_user(session: Session, user_in: UserRegister) -> User:
    hashed = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email, username=user_in.username, hashed_password=hashed
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
