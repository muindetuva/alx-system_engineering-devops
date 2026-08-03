"""Test the copied data service without requiring the auth service."""

import os

os.environ.setdefault("JWT_SECRET_KEY", "ci-test-secret")

from fastapi.testclient import TestClient  # noqa: E402

from main import app  # noqa: E402


client = TestClient(app)


def test_health():
    """The data service must expose a successful health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_items_requires_bearer_token():
    """The protected item route must reject an unauthenticated request."""
    response = client.get("/items")
    assert response.status_code == 401
