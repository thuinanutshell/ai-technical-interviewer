import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
from sqlmodel import Session, SQLModel
from app.core.db import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables() -> None:
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def main() -> None:
    logger.info("Initializing service")

    # Create tables
    logger.info("Creating database tables")
    create_tables()

    # Initialize database with default data
    logger.info("Initializing database")
    with Session(engine) as session:
        init_db(session)

    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
