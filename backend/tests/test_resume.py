import io
import uuid
from fastapi.testclient import TestClient
from app.models.user import User
from app.api.deps import get_current_user


def override_get_current_user():
    return User(
        id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
        email="test@example.com",
        username="test",
        hashed_password="fake")


def test_upload_resume(client: TestClient):
    from app.main import app

    app.dependency_overrides[get_current_user] = override_get_current_user

    # Load a real PDF from disk
    with open("tests/files/sample_resume.pdf", "rb") as f:
        file_bytes = f.read()

    file = io.BytesIO(file_bytes)
    file.name = "sample_resume.pdf"

    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("sample_resume.pdf", file, "application/pdf")},
    )

    assert response.status_code == 200
    data = response.json()

    print("✅ Parsed Resume Markdown:\n", data["parsed_data"])

    assert data["parsed_data"] != ""
    assert "user_id" in data
    assert data["user_id"] == str(uuid.UUID("00000000-0000-0000-0000-000000000000"))

    app.dependency_overrides.clear()
