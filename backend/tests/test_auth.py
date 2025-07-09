from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    """Test user registration"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
    }

    response = client.post("/api/v1/auth/register", json=user_data)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    # Password should not be in response
    assert "password" not in data


def test_login_user(client: TestClient):
    """Test user login"""
    # First register a user
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "loginpassword123",
    }
    client.post("/api/v1/auth/register", json=user_data)

    # Then login
    login_data = {"email": "login@example.com", "password": "loginpassword123"}

    response = client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_logout_user(client: TestClient):
    """Test user logout"""
    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Logged out"
