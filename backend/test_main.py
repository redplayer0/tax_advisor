import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.db import get_session, hash_password
from app.main import app, create_access_token
from app.models import User

TEST_DATABASE_URL = "sqlite:///test_database.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(name="client")
def client_fixture():
    SQLModel.metadata.create_all(engine)
    with TestClient(app) as client:
        yield client
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="test_user")
def test_user_fixture():
    user = User(
        username="testuser",
        hashed_password=hash_password("testpassword"),
    )
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


@pytest.fixture(name="access_token")
def access_token_fixture(test_user):
    return create_access_token(data={"sub": test_user.username})


def test_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_signup(client):
    response = client.post(
        "/signup",
        json={
            "username": "newuser",
            "password": "newpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"


def test_duplicate_signup(client, test_user):
    response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "anotherpassword",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "User already exists"}


def test_password_length(client):
    response = client.post(
        "/signup",
        json={
            "username": "shortpassword",
            "password": "short",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Password must be at least 8 characters long"}


def test_login(client, test_user):
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword",
            "grant_type": "password",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):
    response = client.post(
        "/token",
        data={
            "username": "invaliduser",
            "password": "wrongpassword",
            "grant_type": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_users_me(client, access_token):
    response = client.get(
        "/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_protected_route_without_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_advice_generation(client, access_token):
    response = client.post(
        "/advice",
        json={
            "monthly_income": 3000,
            "monthly_expenses": 2000,
            "is_married": True,
            "children_count": 2,
            "prompt": "How can I save taxes?",
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["model_response"]) > 0
