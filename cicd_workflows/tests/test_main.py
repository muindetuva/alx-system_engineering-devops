"""Test token issuing and verification in the copied auth service."""

import os

os.environ.setdefault("JWT_SECRET_KEY", "ci-test-secret")

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402


client = TestClient(app)


def test_token_and_verify_round_trip():
    """A valid login token must verify with the expected subject."""
    token_response = client.post(
        "/token",
        json={"username": "learner", "password": "container-ready"},
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]

    verify_response = client.get("/verify", params={"token": token})
    assert verify_response.status_code == 200
    assert verify_response.json() == {"valid": True, "subject": "learner"}


def test_invalid_credentials_are_rejected():
    """An invalid password must not produce an access token."""
    response = client.post(
        "/token",
        json={"username": "learner", "password": "wrong-password"},
    )
    assert response.status_code == 401
