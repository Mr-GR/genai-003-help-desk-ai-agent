import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from db.database import Base, get_db
from db import models  # noqa: F401  (registers tables on Base.metadata)

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)

VALID_PASSWORD = "Passw0rd!"


def test_successful_signup():
    response = client.post(
        "/signup",
        json={"username": "MannyTestPy", "password": VALID_PASSWORD},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "MannyTestPy"
    assert "password" not in data


def test_signup_duplicate_username_fails():
    client.post(
        "/signup",
        json={"username": "MannyTestPy", "password": VALID_PASSWORD},
    )
    response = client.post(
        "/signup",
        json={"username": "MannyTestPy", "password": VALID_PASSWORD},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_login_success():
    client.post(
        "/signup",
        json={"username": "MannyTestPy", "password": VALID_PASSWORD},
    )
    response = client.post(
        "/token",
        data={"username": "MannyTestPy", "password": VALID_PASSWORD},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password_fails():
    client.post(
        "/signup",
        json={"username": "MannyTestPy", "password": VALID_PASSWORD},
    )
    response = client.post(
        "/token",
        data={"username": "MannyTestPy", "password": "WrongPass1!"},
    )
    assert response.status_code == 401


def test_logout_requires_token():
    response = client.post("/logout")
    assert response.status_code == 401


def test_logout_with_valid_token():
    client.post(
        "/signup",
        json={"username": "MannyTestPy", "password": VALID_PASSWORD},
    )
    token_response = client.post(
        "/token",
        data={"username": "MannyTestPy", "password": VALID_PASSWORD},
    )
    token = token_response.json()["access_token"]
    response = client.post(
        "/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
