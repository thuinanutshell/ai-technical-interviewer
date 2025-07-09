import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# Set testing environment BEFORE any imports
os.environ["ENVIRONMENT"] = "testing"

from app.main import app
from app.api.deps import get_session


# Create test engine
test_engine = create_engine(
    "sqlite:///:memory:",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)


@pytest.fixture(name="session", scope="function")
def session_fixture():
    """Create a fresh test database session for each test"""
    # Create all tables
    SQLModel.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    # Clean up - drop all tables after each test
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client", scope="function")
def client_fixture(session: Session):
    """Create a test client with database session override"""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    # Clean up
    app.dependency_overrides.clear()
