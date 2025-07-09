from sqlmodel import Session, create_engine, select
from app.core.config import settings
from app.models.user import User, UserRegister
from app.services import crud

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    """
    Initialize the database with tables and default users.
    """
    # Uncomment the next lines if you're not using Alembic migrations
    # from sqlmodel import SQLModel
    # SQLModel.metadata.create_all(engine)

    # Create first superuser if it doesn't exist
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserRegister(
            email=settings.FIRST_SUPERUSER,
            username="admin",  # You'll need to add this
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = crud.create_user(session=session, user_in=user_in)
        print(f"Created superuser: {user.email}")
