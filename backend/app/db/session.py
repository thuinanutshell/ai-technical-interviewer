from sqlalchemy import create_engine
from app.core.config import settings
from sqlmodel import Session

engine = create_engine(str(settings.DATABASE_URL), echo=True)


def get_session():
    with Session(engine) as session:
        yield session
